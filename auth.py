# -*- coding: utf-8 -*-
"""
Authentication & Authorization Security Layer for Aegis Learn
=============================================================
1. JWT Token Generator & Verifier (python-jose / PyJWT)
2. Secure Password Hashing & Verification (Bcrypt + Seed Compatibility)
3. FastAPI Dependencies: get_current_user, get_current_admin, get_optional_current_user
"""

import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db
from models import User, UserRole

logger = logging.getLogger("aegis.auth")

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "aegis_learn_super_secret_jwt_key_2026_secured")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

# Try to import python-jose first, fallback to PyJWT
try:
    from jose import JWTError, jwt
    USE_JOSE = True
except ImportError:
    import jwt
    from jwt import PyJWTError as JWTError
    USE_JOSE = False

http_bearer_scheme = HTTPBearer(auto_error=False)


# ==========================================
# 1. PASSWORD SECURITY (BCRYPT)
# ==========================================
def get_password_hash(password: str) -> str:
    """Hash password using bcrypt with automatic salt generation."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hashed password.
    Supports backward compatibility for legacy plain/mock seed hashes,
    allowing existing mock accounts (admin/student) to authenticate and migrate.
    """
    if not hashed_password or not plain_password:
        return False

    # 1. Legacy mock hashes from initial database seed
    if hashed_password == "hashed_admin_pass" and plain_password in ["admin123", "admin", "hashed_admin_pass"]:
        return True
    if hashed_password == "hashed_student_pass" and plain_password in ["student123", "student", "hashed_student_pass"]:
        return True
    if plain_password == hashed_password:
        return True

    # 2. Modern Bcrypt verification
    try:
        pwd_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
    except Exception as e:
        logger.warning(f"Bcrypt verification failed: {e}")
        return False


# ==========================================
# 2. JWT TOKEN CREATION & DECODING
# ==========================================
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generate a signed JWT token containing user identity and role claims."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Ensure sub is string per JWT standards
    if "sub" not in to_encode and "user_id" in to_encode:
        to_encode["sub"] = str(to_encode["user_id"])

    if USE_JOSE:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    else:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a signed JWT access token."""
    try:
        if USE_JOSE:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        else:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn (Invalid or expired token)",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ==========================================
# 3. FASTAPI DEPENDENCIES FOR AUTH & RBAC
# ==========================================
def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI Dependency: Extract and validate user identity from Authorization Bearer token.
    Raises 401 Unauthorized if token is missing, invalid, or user does not exist.
    """
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yêu cầu đăng nhập. Vui lòng cung cấp JWT Bearer token qua header Authorization.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(auth.credentials)
    user_id_str = payload.get("sub") or payload.get("user_id")

    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không chứa định danh người dùng (sub claim missing).",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Định danh người dùng trong Token không hợp lệ.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Modern SQLAlchemy 2.0 query
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Người dùng không tồn tại trong hệ thống.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này hiện đang bị khóa.",
        )

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    FastAPI Dependency: Protect Admin endpoints.
    Enforces role == 'ADMIN'. Rejects students and unauthorized users with 403 Forbidden.
    """
    role_str = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if role_str.upper() != "ADMIN":
        logger.warning(f"Forbidden access attempt to admin endpoint by user_id={current_user.id}, role={role_str}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Từ chối truy cập: Endpoint này yêu cầu quyền Quản trị viên (Admin privileges required).",
        )
    return current_user


def get_optional_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    FastAPI Dependency: Extract user if token is provided, return None otherwise without throwing 401.
    Useful for endpoints supporting both authenticated personalized experience and guest access.
    """
    if not auth or not auth.credentials:
        return None

    try:
        payload = decode_access_token(auth.credentials)
        user_id_str = payload.get("sub") or payload.get("user_id")
        if not user_id_str:
            return None
        user = db.get(User, int(user_id_str))
        if user and user.is_active:
            return user
        return None
    except Exception:
        return None
