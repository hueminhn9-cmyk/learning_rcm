"""
Database Models for Personalized Learning System (FastAPI + SQLAlchemy 2.0)
Architecture: Autonomous Student + Admin (No teacher role)
Includes Knowledge Profile, Personal Notes, Content Feedback, Scheduled Assessments & Gamification
"""

from enum import Enum as PyEnum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    String, Text, Integer, Float, Boolean, DateTime, ForeignKey, 
    Enum, UniqueConstraint, Index, JSON, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# ==========================================
# ENUM DEFINITIONS
# ==========================================
class UserRole(str, PyEnum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"

class DependencyType(str, PyEnum):
    STRICT = "STRICT"          # Bắt buộc học xong chủ đề trước
    RECOMMENDED = "RECOMMENDED" # Khuyến nghị nên học trước

class MaterialType(str, PyEnum):
    VIDEO = "VIDEO"
    READING = "READING"
    SLIDE = "SLIDE"
    EXERCISE = "EXERCISE"

class BloomLevel(str, PyEnum):
    REMEMBER = "REMEMBER"
    UNDERSTAND = "UNDERSTAND"
    APPLY = "APPLY"
    ANALYZE = "ANALYZE"
    EVALUATE = "EVALUATE"
    CREATE = "CREATE"

class QuestionType(str, PyEnum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TRUE_FALSE = "TRUE_FALSE"
    SHORT_ANSWER = "SHORT_ANSWER"
    ESSAY = "ESSAY"

class ProgressStatus(str, PyEnum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class AssessmentType(str, PyEnum):
    DIAGNOSTIC = "DIAGNOSTIC"                  # SV01 - Đánh giá năng lực đầu vào
    QUIZ = "QUIZ"                              # SV02 - Kiểm tra chủ đề
    WEEKLY_CHECKPOINT = "WEEKLY_CHECKPOINT"    # SV06 - Kiểm tra định kỳ hàng tuần
    MONTHLY_PROJECT = "MONTHLY_PROJECT"        # SV07 - Bài kiểm tra dự án tổng hợp hàng tháng
    PRACTICE = "PRACTICE"                      # SV09 - Tự luyện tập từ kho đề
    FINAL = "FINAL"                            # Bài kiểm tra kết thúc môn học

class FeedbackType(str, PyEnum):
    TOO_DIFFICULT = "TOO_DIFFICULT"
    TOO_EASY = "TOO_EASY"
    CONTENT_ERROR = "CONTENT_ERROR"
    BROKEN_LINK = "BROKEN_LINK"

class FeedbackStatus(str, PyEnum):
    NEW = "NEW"
    IN_REVIEW = "IN_REVIEW"
    RESOLVED = "RESOLVED"

class MasteryStatus(str, PyEnum):
    MASTERED = "MASTERED"             # Đã đạt thành thạo
    WEAK = "WEAK"                     # Yếu / Chưa đạt (Cần học bổ trợ)
    NEEDS_ASSESSMENT = "NEEDS_ASSESSMENT" # Chưa đủ dữ liệu đánh giá


# ==========================================
# MODULE 1: QUẢN LÝ USER & HỒ SƠ
# ==========================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    profile: Mapped[Optional["UserProfile"]] = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    goals: Mapped[List["UserGoal"]] = relationship("UserGoal", back_populates="user", cascade="all, delete-orphan")
    progresses: Mapped[List["UserProgress"]] = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    assessment_results: Mapped[List["AssessmentResult"]] = relationship("AssessmentResult", back_populates="user", cascade="all, delete-orphan")
    knowledge_profiles: Mapped[List["KnowledgeProfile"]] = relationship("KnowledgeProfile", back_populates="user", cascade="all, delete-orphan")
    notes: Mapped[List["PersonalNote"]] = relationship("PersonalNote", back_populates="user", cascade="all, delete-orphan")
    feedbacks: Mapped[List["ContentFeedback"]] = relationship("ContentFeedback", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    learning_style: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    study_streak_days: Mapped[int] = mapped_column(Integer, default=1)
    total_study_minutes: Mapped[int] = mapped_column(Integer, default=0)
    exp_points: Mapped[int] = mapped_column(Integer, default=100)

    user: Mapped["User"] = relationship("User", back_populates="profile")


class UserGoal(Base):
    __tablename__ = "user_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    target_subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    target_topic_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    target_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    available_hours_per_week: Mapped[float] = mapped_column(Float, default=10.0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="goals")
    target_subject: Mapped[Optional["Subject"]] = relationship("Subject")
    target_topic: Mapped[Optional["Topic"]] = relationship("Topic")


class KnowledgeProfile(Base):
    __tablename__ = "knowledge_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[MasteryStatus] = mapped_column(Enum(MasteryStatus), default=MasteryStatus.NEEDS_ASSESSMENT)
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)
    last_assessed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_user_topic_knowledge_profile"),
    )

    user: Mapped["User"] = relationship("User", back_populates="knowledge_profiles")
    topic: Mapped["Topic"] = relationship("Topic")


class PersonalNote(Base):
    __tablename__ = "personal_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    material_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("learning_materials.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="notes")
    topic: Mapped["Topic"] = relationship("Topic")
    material: Mapped[Optional["LearningMaterial"]] = relationship("LearningMaterial")


class ContentFeedback(Base):
    __tablename__ = "content_feedbacks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    material_id: Mapped[int] = mapped_column(Integer, ForeignKey("learning_materials.id", ondelete="CASCADE"), nullable=False, index=True)
    feedback_type: Mapped[FeedbackType] = mapped_column(Enum(FeedbackType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[FeedbackStatus] = mapped_column(Enum(FeedbackStatus), default=FeedbackStatus.NEW)
    admin_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="feedbacks")
    material: Mapped["LearningMaterial"] = relationship("LearningMaterial")


# ==========================================
# MODULE 2: ĐỒ THỊ KIẾN THỨC (KNOWLEDGE GRAPH)
# ==========================================
class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    subject: Mapped["Subject"] = relationship("Subject", back_populates="topics")
    learning_outcomes: Mapped[List["LearningOutcome"]] = relationship("LearningOutcome", back_populates="topic", cascade="all, delete-orphan")
    materials: Mapped[List["LearningMaterial"]] = relationship("LearningMaterial", back_populates="topic", cascade="all, delete-orphan")
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    
    prerequisites: Mapped[List["TopicPrerequisite"]] = relationship(
        "TopicPrerequisite", foreign_keys="[TopicPrerequisite.topic_id]", back_populates="topic", cascade="all, delete-orphan"
    )
    is_prerequisite_for: Mapped[List["TopicPrerequisite"]] = relationship(
        "TopicPrerequisite", foreign_keys="[TopicPrerequisite.prerequisite_topic_id]", back_populates="prerequisite_topic", cascade="all, delete-orphan"
    )


class LearningOutcome(Base):
    __tablename__ = "learning_outcomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    bloom_level: Mapped[BloomLevel] = mapped_column(Enum(BloomLevel), default=BloomLevel.REMEMBER)

    topic: Mapped["Topic"] = relationship("Topic", back_populates="learning_outcomes")
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="outcome")


class TopicPrerequisite(Base):
    __tablename__ = "topic_prerequisites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    dependency_type: Mapped[DependencyType] = mapped_column(Enum(DependencyType), default=DependencyType.STRICT)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("topic_id", "prerequisite_topic_id", name="uq_topic_prerequisite"),
    )

    topic: Mapped["Topic"] = relationship("Topic", foreign_keys=[topic_id], back_populates="prerequisites")
    prerequisite_topic: Mapped["Topic"] = relationship("Topic", foreign_keys=[prerequisite_topic_id], back_populates="is_prerequisite_for")


# ==========================================
# MODULE 3: HỌC LIỆU & ĐÁNH GIÁ (MATERIALS & ASSESSMENTS)
# ==========================================
class LearningMaterial(Base):
    __tablename__ = "learning_materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    university: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default="edX")
    material_type: Mapped[MaterialType] = mapped_column(Enum(MaterialType), nullable=False)
    content_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty_level: Mapped[float] = mapped_column(Float, default=1.0)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    parent_material_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("learning_materials.id", ondelete="SET NULL"), nullable=True)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    topic: Mapped["Topic"] = relationship("Topic", back_populates="materials")
    created_by: Mapped["User"] = relationship("User")
    parent_material: Mapped[Optional["LearningMaterial"]] = relationship("LearningMaterial", remote_side=[id], backref="version_history")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    outcome_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("learning_outcomes.id", ondelete="SET NULL"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    options: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty_level: Mapped[float] = mapped_column(Float, default=1.0)

    topic: Mapped["Topic"] = relationship("Topic", back_populates="questions")
    outcome: Mapped[Optional["LearningOutcome"]] = relationship("LearningOutcome", back_populates="questions")


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=True)
    topic_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    assessment_type: Mapped[AssessmentType] = mapped_column(Enum(AssessmentType), nullable=False)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, default=30)
    passing_score: Mapped[float] = mapped_column(Float, default=60.0)

    assessment_questions: Mapped[List["AssessmentQuestion"]] = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    assessment_id: Mapped[int] = mapped_column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    order_index: Mapped[int] = mapped_column(Integer, default=1)

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="assessment_questions")
    question: Mapped["Question"] = relationship("Question")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    material_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("learning_materials.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[ProgressStatus] = mapped_column(Enum(ProgressStatus), default=ProgressStatus.NOT_STARTED)
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", "material_id", name="uq_user_material_progress"),
    )

    user: Mapped["User"] = relationship("User", back_populates="progresses")
    topic: Mapped["Topic"] = relationship("Topic")
    material: Mapped[Optional["LearningMaterial"]] = relationship("LearningMaterial")


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id: Mapped[int] = mapped_column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    rubric_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="assessment_results")
    assessment: Mapped["Assessment"] = relationship("Assessment")


# ==========================================
# MODULE 4: CẤU HÌNH KHUYẾN NGHỊ (RECOMMENDATION CONFIG)
# ==========================================
class RecommendationConfig(Base):
    __tablename__ = "recommendation_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    config_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    weight_value: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    parameters: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


# ==========================================
# MODULE 5: LỊCH SỬ THI TRẮC NGHIỆM (QUIZ ATTEMPTS & REVIEWS)
# ==========================================
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    quiz_title: Mapped[str] = mapped_column(String(255), nullable=False, default="Bài kiểm tra Trắc nghiệm")
    score: Mapped[float] = mapped_column(Float, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    passed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User")
    answers: Mapped[List["QuizAttemptAnswer"]] = relationship("QuizAttemptAnswer", back_populates="attempt", cascade="all, delete-orphan")


class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(Integer, ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    selected_answer: Mapped[str] = mapped_column(String(255), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    attempt: Mapped["QuizAttempt"] = relationship("QuizAttempt", back_populates="answers")

