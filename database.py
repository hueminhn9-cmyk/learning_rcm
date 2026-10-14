# -*- coding: utf-8 -*-
"""
Database Connection & Session Factory for Aegis Learn (SQLAlchemy 2.0 Singleton)
================================================================================
Manages shared DB engine, SessionLocal factory, and FastAPI get_db dependency.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learning_app.db")

# Singleton Engine
# check_same_thread=False is required for SQLite when accessed across multiple threads in FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI Dependency for Database Session lifecycle management.
    Yields an active SQLAlchemy session and ensures it is properly closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
