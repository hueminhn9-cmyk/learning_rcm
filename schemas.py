"""
Comprehensive Pydantic Schemas for API Requests & Responses (FastAPI)
Includes Student, Admin, AI Recommendation, Assessments, Analytics & Gamification DTOs
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ==========================================
# 1. AUTHENTICATION & PROFILE SCHEMAS
# ==========================================
class UserRegisterDTO(BaseModel):
    email: str = Field(..., example="student.a@aegislearn.edu.vn")
    password: str = Field(..., min_length=6, example="password123")
    full_name: str = Field(..., example="Nguyễn Văn A")
    role: str = Field("STUDENT", example="STUDENT") # STUDENT | ADMIN


class UserLoginDTO(BaseModel):
    email: str = Field(..., example="student.a@aegislearn.edu.vn")
    password: str = Field(..., example="password123")


class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    role: str
    full_name: str


class UserProfileUpdateDTO(BaseModel):
    full_name: Optional[str] = None
    learning_style: Optional[str] = None # VISUAL | AUDITORY | READ_WRITE | KINESTHETIC
    preferred_material_type: Optional[str] = None # VIDEO | READING | SLIDE | EXERCISE


# ==========================================
# 2. GOAL & FEASIBILITY SCHEMAS (SV03)
# ==========================================
class UserGoalCreateDTO(BaseModel):
    user_id: int
    title: str = Field(..., example="Hoàn thành môn Học máy trước kỳ thi")
    target_subject_id: Optional[int] = None
    target_topic_id: Optional[int] = None
    target_date: str = Field(..., example="2026-12-01")
    available_hours_per_week: float = Field(10.0, ge=1.0, le=50.0)


class GoalFeasibilityResponseDTO(BaseModel):
    goal_id: int
    user_id: int
    target_title: str
    target_date: str
    total_required_hours: float
    available_hours_per_week: float
    weeks_remaining: float
    max_possible_hours: float
    is_feasible: bool = Field(..., description="Tính khả thi (Đạt nếu max_possible_hours >= total_required_hours)")
    feasibility_status: str = Field(..., description="HIGHLY_FEASIBLE | TIGHT_SCHEDULE | UNFEASIBLE")
    recommendation_note: str


# ==========================================
# 3. KNOWLEDGE GRAPH & LEARNING PATH SCHEMAS
# ==========================================
class TopicNodeDTO(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None


class PrerequisiteRelationDTO(BaseModel):
    topic_id: int
    prerequisite_topic_id: int
    dependency_type: str = "STRICT"


class LearningPathRequest(BaseModel):
    user_id: int
    target_topic_id: int
    mastered_topic_ids: List[int] = Field(default=[])
    all_topics: List[TopicNodeDTO]
    prerequisites: List[PrerequisiteRelationDTO]


class LearningStepDTO(BaseModel):
    step_number: int
    topic_id: int
    code: str
    title: str
    status: str # COMPLETED | UNLOCKED | LOCKED
    direct_prerequisite_ids: List[int] = Field(default=[])
    reasoning: str


class LearningPathResponse(BaseModel):
    success: bool = True
    user_id: int
    target_topic_id: int
    total_steps: int
    completed_steps_count: int
    unlocked_steps_count: int
    locked_steps_count: int
    learning_path: List[LearningStepDTO]
    estimated_hours: float


# ==========================================
# 4. MATERIAL RECOMMENDATION SCHEMAS
# ==========================================
class StudentProfileDTO(BaseModel):
    user_id: int
    learning_style: str = "VISUAL"
    preferred_material_type: str = "VIDEO"
    estimated_ability_score: float = Field(3.5, ge=1.0, le=5.0)
    recent_quiz_avg_score: float = Field(85.0, ge=0.0, le=100.0)


class MaterialItemDTO(BaseModel):
    id: int
    title: str
    university: Optional[str] = "edX"
    material_type: str
    content_url: Optional[str] = None
    description: Optional[str] = None
    text_content: Optional[str] = None
    difficulty_level: float
    version: int = 1
    is_latest: bool = True


class RecommendationRequest(BaseModel):
    topic_id: int
    student_profile: StudentProfileDTO
    candidate_materials: List[MaterialItemDTO]
    top_k: int = 5


class RecommendedMaterialDTO(BaseModel):
    material: MaterialItemDTO
    similarity_score: float
    match_percentage: float
    recommendation_reason: str


class RecommendationResponse(BaseModel):
    success: bool = True
    topic_id: int
    student_id: int
    recommended_count: int
    recommendations: List[RecommendedMaterialDTO]


# ==========================================
# 5. QUESTION BANK & QUIZ SCHEMAS (EXAM CENTER)
# ==========================================
class QuizQuestionDetailDTO(BaseModel):
    id: int
    topic_id: int
    content: str
    question_type: str # MULTIPLE_CHOICE | TRUE_FALSE | ESSAY
    options: Optional[Dict[str, str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty_level: float = 1.0


class QuizDetailResponseDTO(BaseModel):
    assessment_id: int
    title: str
    assessment_type: str # DIAGNOSTIC | QUIZ | WEEKLY_CHECKPOINT | MONTHLY_PROJECT | PRACTICE
    time_limit_minutes: int
    total_questions: int
    questions: List[QuizQuestionDetailDTO]


class AvailableAssessmentItemDTO(BaseModel):
    id: int
    title: str
    assessment_type: str # WEEKLY_CHECKPOINT | MONTHLY_PROJECT | PRACTICE
    time_limit_minutes: int
    topic_id: Optional[int] = None
    topic_title: Optional[str] = None
    description: Optional[str] = None
    deadline_str: Optional[str] = None
    weight_percentage: Optional[int] = None


class AvailableAssessmentsResponse(BaseModel):
    weekly_quizzes: List[AvailableAssessmentItemDTO]
    monthly_projects: List[AvailableAssessmentItemDTO]
    practice_topics: List[Dict[str, Any]]


class ProjectSubmissionRequest(BaseModel):
    user_id: int
    assessment_id: int
    project_title: str
    submission_url: str # GitHub / Google Drive link
    report_text: str


class PracticeQuizRequestDTO(BaseModel):
    user_id: int
    topic_id: int
    question_count: int = Field(5, ge=1, le=20)
    difficulty_level: Optional[float] = None


class GenerateWeeklyQuizRequest(BaseModel):
    user_id: int


class GenerateMonthlyProjectRequest(BaseModel):
    user_id: int


# ==========================================
# 6. QUIZ SUBMISSION & GRADING SCHEMAS
# ==========================================
class SingleAnswerDTO(BaseModel):
    question_id: int
    user_answer: str
    question_type: str = "MULTIPLE_CHOICE"


class AssessmentSubmitRequest(BaseModel):
    user_id: int
    assessment_id: int
    topic_id: int
    answers: List[SingleAnswerDTO]
    time_taken_seconds: int


class QuestionReviewItemDTO(BaseModel):
    question_id: int
    content: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str


class AssessmentSubmitResponse(BaseModel):
    success: bool = True
    assessment_id: int
    user_id: int
    score: float
    passed: bool
    status: str # GRADED | PENDING_MANUAL_GRADING
    topic_mastery_updated: bool
    question_reviews: List[QuestionReviewItemDTO] = Field(default=[])
    remedial_materials: List[RecommendedMaterialDTO] = Field(default=[])
    message: str


class ManualGradingSubmitDTO(BaseModel):
    queue_id: int
    admin_id: int
    score: float = Field(..., ge=0.0, le=100.0)
    rubric_feedback: str
    passed: bool


# ==========================================
# 7. KNOWLEDGE PROFILE & ANALYTICS SCHEMAS (SV05, SV12)
# ==========================================
class KnowledgeProfileItemDTO(BaseModel):
    topic_id: int
    topic_code: str
    topic_title: str
    status: str # MASTERED | WEAK | NEEDS_ASSESSMENT
    mastery_score: float
    last_assessed_at: str


class LearningProgressReportDTO(BaseModel):
    user_id: int
    full_name: str
    overall_progress_percentage: float
    completed_topics_count: int
    total_topics_count: int
    study_streak_days: int
    total_study_minutes: int
    exp_points: int
    knowledge_profiles: List[KnowledgeProfileItemDTO]
    recent_assessments: List[Dict[str, Any]]


# ==========================================
# 8. SPACED REPETITION SCHEMAS
# ==========================================
class TopicMemoryRetentionDTO(BaseModel):
    topic_id: int
    topic_code: str
    topic_title: str
    last_studied_days_ago: int
    memory_retention_percentage: float
    needs_review: bool
    recommended_review_type: str


class SpacedRepetitionResponse(BaseModel):
    user_id: int
    total_mastered_topics: int
    topics_needing_review_count: int
    review_recommendations: List[TopicMemoryRetentionDTO]


# ==========================================
# 9. PERSONAL NOTE & CONTENT FEEDBACK SCHEMAS (SV08, SV13)
# ==========================================
class CreateNoteDTO(BaseModel):
    user_id: int
    topic_id: int
    material_id: Optional[int] = None
    title: str
    content: str


class NoteResponseDTO(BaseModel):
    id: int
    user_id: int
    topic_id: int
    material_id: Optional[int] = None
    title: str
    content: str
    created_at: str


class CreateFeedbackDTO(BaseModel):
    user_id: int
    material_id: int
    feedback_type: str # TOO_DIFFICULT | TOO_EASY | CONTENT_ERROR | BROKEN_LINK
    description: str


class FeedbackItemDTO(BaseModel):
    id: int
    user_id: int
    material_id: int
    material_title: str
    feedback_type: str
    description: str
    status: str # NEW | IN_REVIEW | RESOLVED
    admin_response: Optional[str] = None
    created_at: str


class FeedbackAdminUpdateDTO(BaseModel):
    feedback_id: int
    admin_id: int
    status: str = "RESOLVED"
    admin_response: str


# ==========================================
# 10. INTERACTIVE FEYNMAN METHOD SCHEMAS
# ==========================================
class FeynmanReflectionSubmitDTO(BaseModel):
    user_id: int
    topic_id: int
    explanation_text: str = Field(..., description="Bài tự giải thích lại khái niệm bằng ngôn ngữ cá nhân của sinh viên")


class FeynmanReflectionResponseDTO(BaseModel):
    topic_id: int
    keyword_coverage_score: float = Field(..., description="Điểm bao phủ từ khóa khái niệm cốt lõi (0 - 100)")
    conceptual_clarity_level: str # EXCELLENT | GOOD | NEEDS_IMPROVEMENT
    ai_feedback: str
    earned_exp_points: int


# ==========================================
# 11. ADMIN CONFIG & STATS SCHEMAS
# ==========================================
class ConfigWeightUpdateDTO(BaseModel):
    config_key: str = "RECOMMENDATION_WEIGHTS"
    description: Optional[str] = "Cập nhật trọng số khuyến nghị và ngưỡng đạt"
    w_prerequisite: float = Field(1.5, ge=0.0, le=5.0)
    w_difficulty_gap: float = Field(1.2, ge=0.0, le=5.0)
    w_bloom_match: float = Field(1.0, ge=0.0, le=5.0)
    min_passing_score: float = Field(60.0, ge=0.0, le=100.0)
    updated_by_user_id: int = 99


class ConfigHistoryItemDTO(BaseModel):
    version: int
    config_key: str
    w_prerequisite: float
    w_difficulty_gap: float
    w_bloom_match: float
    min_passing_score: float
    updated_by_user_id: int
    updated_at: str


class AdminStatsResponse(BaseModel):
    total_students: int
    goal_completion_rate: float
    total_student_feedback_reports: int
    manual_grading_queue_count: int
    struggling_topics: List[Dict[str, Any]]
    monthly_completion_trend: List[Dict[str, Any]]


# ==========================================
# 14. AI TUTOR CHAT SCHEMAS
# ==========================================
class AIChatRequestDTO(BaseModel):
    user_id: int = 1
    topic_id: Optional[int] = None
    message: str = Field(..., min_length=1, example="Làm thế nào để xử lý giá trị NaN trong Pandas?")
    history: Optional[List[Dict[str, str]]] = Field(default=[], description="Lịch sử chat [{role: 'user'|'assistant', content: '...'}]")


class AIChatResponseDTO(BaseModel):
    reply: str
    suggested_followups: List[str] = Field(default=[])
    topic_id: Optional[int] = None
    model_used: str = "Aegis AI EdTech Assistant v2.0"
    sources: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Nguồn trích dẫn Google / Web Docs có kiểm chứng [title, url, snippet]")


# ==========================================
# 15. ADMIN AI ASSISTANT SCHEMAS (QT10, QT11, AUTO-TUNE, REMEDIAL)
# ==========================================
class AISuggestGradingRequestDTO(BaseModel):
    queue_id: int
    essay_text: str = Field(..., example="Hàm Sigmoid sigma(z) = 1 / (1 + e^-z) biến đổi giá trị z về khoảng (0, 1)...")
    student_name: Optional[str] = "Nguyễn Văn A"
    topic_title: Optional[str] = "Dự án AI: Phân loại dữ liệu học tập OULAD"


class AISuggestGradingResponseDTO(BaseModel):
    queue_id: int
    suggested_score: float = Field(85.0, ge=0.0, le=100.0)
    suggested_passed: bool = True
    pros: List[str] = Field(default=[])
    cons: List[str] = Field(default=[])
    pedagogical_feedback: str
    model_used: str = "Aegis Admin AI Grader v2.0"


class AIFeedbackAnalysisRequestDTO(BaseModel):
    feedback_id: int
    material_title: str = Field(..., example="Video: Gradient Descent")
    feedback_type: str = Field(..., example="TOO_DIFFICULT")
    description: str = Field(..., example="Phần toán giải tích ở phút 05:20 quá nhanh, em chưa hiểu rõ.")


class AIFeedbackAnalysisResponseDTO(BaseModel):
    feedback_id: int
    category: str = Field("Sư phạm", description="Kỹ thuật | Sư phạm")
    urgency_level: str = Field("Trung bình", description="Cao | Trung bình | Thấp")
    root_cause_analysis: str
    action_plan: List[str] = Field(default=[])
    draft_student_reply: str
    model_used: str = "Aegis Admin AI Analyzer v2.0"


class AIAutoTuneWeightsResponseDTO(BaseModel):
    w_prerequisite: float = Field(1.8, ge=0.0, le=5.0)
    w_difficulty_gap: float = Field(1.4, ge=0.0, le=5.0)
    w_bloom_match: float = Field(1.2, ge=0.0, le=5.0)
    min_passing_score: float = Field(70.0, ge=0.0, le=100.0)
    rationale: str
    improvements_expected: List[str] = Field(default=[])
    model_used: str = "Aegis Admin AI Auto-Tuner v2.0"


class AIRemedialQuizRequestDTO(BaseModel):
    topic_code: str = Field("T104", example="T104")
    topic_title: str = Field("Học máy cơ bản", example="Học máy cơ bản")
    count: int = Field(3, ge=1, le=10)


class AIRemedialQuestionItemDTO(BaseModel):
    id: int
    content: str
    options: Dict[str, str]
    correct_answer: str
    explanation: str
    focus_concept: str


class AIRemedialQuizResponseDTO(BaseModel):
    topic_code: str
    topic_title: str
    remedial_questions: List[AIRemedialQuestionItemDTO]
    model_used: str = "Aegis Admin AI Remedial Generator v2.0"


# ==========================================
# 11. INSTANT RESULT & REVIEW & HISTORY SCHEMAS
# ==========================================
class QuizAnswerSubmitDTO(BaseModel):
    question_id: int
    selected_answer: str = Field(..., example="A")


class QuizSubmitRequestDTO(BaseModel):
    user_id: int = Field(1, example=1)
    quiz_id: int = Field(201, example=201)
    quiz_title: str = Field("Bài kiểm tra Cú pháp Python", example="Bài kiểm tra Cú pháp Python")
    answers: List[QuizAnswerSubmitDTO]
    duration_seconds: int = Field(180, example=180)


class QuestionReviewDetailedDTO(BaseModel):
    question_id: int
    question_text: str
    options: Dict[str, str] = Field(default_factory=dict)
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str


class QuizSubmitResponseDTO(BaseModel):
    attempt_id: int
    quiz_id: int
    quiz_title: str
    score: float = Field(..., description="Điểm số phần trăm, vd: 85.0")
    total_questions: int
    correct_count: int
    passed: bool
    duration_seconds: int
    created_at: str
    review_questions: List[QuestionReviewDetailedDTO]


class QuizHistoryItemDTO(BaseModel):
    attempt_id: int
    quiz_id: int
    quiz_title: str
    score: float
    total_questions: int
    correct_count: int
    passed: bool
    duration_seconds: int
    created_at: str


class QuizAttemptDetailDTO(BaseModel):
    attempt_id: int
    quiz_id: int
    quiz_title: str
    score: float
    total_questions: int
    correct_count: int
    passed: bool
    duration_seconds: int
    created_at: str
    review_questions: List[QuestionReviewDetailedDTO]


# ==========================================
# 16. HIGH-SCORE ENGINE SCHEMAS (SCORE COCKPIT, ERROR VAULT, CRAMMING, FLASHCARDS)
# ==========================================
class ScorePredictionTopicItemDTO(BaseModel):
    topic_id: int
    code: str
    title: str
    mastery_percentage: float
    impact_points: float
    status: str = Field("NEEDS_IMPROVEMENT", description="STRONG | NEEDS_IMPROVEMENT | CRITICAL_GAP")


class ScorePredictionResponseDTO(BaseModel):
    current_predicted_score: float = Field(7.4, description="Điểm số dự báo thi hiện tại (thang 10)")
    target_score: float = Field(9.0, description="Mục tiêu điểm số (thang 10)")
    grade_letter: str = Field("B+", description="Xếp loại học lực hiện tại")
    target_grade: str = Field("A", description="Mục tiêu xếp loại")
    points_gap: float = Field(1.6, description="Số điểm cần bù đắp để đạt mục tiêu")
    days_remaining: int = Field(14, description="Số ngày đếm ngược đến kỳ thi")
    total_quizzes_taken: int = Field(0)
    topics_radar: List[ScorePredictionTopicItemDTO] = Field(default_factory=list)
    quick_wins: List[str] = Field(default_factory=list)
    exam_readiness_percentage: float = Field(74.0)


class ErrorVaultItemDTO(BaseModel):
    question_id: int
    topic_id: int
    topic_code: str
    topic_title: str
    content: str
    options: Dict[str, str]
    correct_answer: str
    user_answer: str
    explanation: str
    trap_warning: str
    trap_type: str = Field("TRAP_LOGIC", description="TRAP_LOGIC | TRAP_SYNTAX | TRAP_FORMULA | CARELESS")
    times_incorrect: int = 1


class FlashcardItemDTO(BaseModel):
    id: int
    topic_id: int
    topic_code: str
    topic_title: str
    front: str
    back: str
    key_insight: str
    difficulty: str = "MEDIUM"
    retention_rate: float = 75.0


class CrammingCheatSheetDTO(BaseModel):
    topic_id: int
    topic_code: str
    topic_title: str
    one_page_summary: str
    must_remember_formulas: List[str] = Field(default_factory=list)
    top_exam_traps: List[str] = Field(default_factory=list)
    high_yield_questions: List[AIRemedialQuestionItemDTO] = Field(default_factory=list)


# ==========================================
# 19. MULTI-SUBJECT DISCOVERY & 3-TIER RECOMMENDATION SCHEMAS
# ==========================================
class SubjectTopicBriefDTO(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    order_index: int = 1
    difficulty_level: float = 3.0


class SubjectListItemDTO(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    topics_count: int = 0
    materials_count: int = 0
    questions_count: int = 0
    topics: List[SubjectTopicBriefDTO] = Field(default_factory=list)


class Tier1WebResourceDTO(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    institution: Optional[str] = "Chính thống"
    material_type: str = "READING"
    difficulty_level: float = 3.0
    is_free: bool = True


class Tier2YouTubeVideoDTO(BaseModel):
    title: str
    url: str
    channel: Optional[str] = "YouTube"
    duration_minutes: Optional[int] = 30
    level: float = 3.0
    description: Optional[str] = None


class Tier3ScoreStrategyDTO(BaseModel):
    target_score: float
    grade_letter: str
    target_bracket: str
    feasibility_status: str
    estimated_study_hours: float
    daily_commitment_minutes: int
    exam_prep_milestones: List[str] = Field(default_factory=list)
    key_focus_topics: List[str] = Field(default_factory=list)
    action_plan: List[str] = Field(default_factory=list)


class RelatedSubjectSuggestionDTO(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    topics_count: int = 0
    relevance_reason: str = "Môn học phù hợp với từ khóa"


class SubjectSearchRecommendationResponseDTO(BaseModel):
    query: str
    target_score: float
    matched_subject: SubjectListItemDTO
    related_subjects: List[RelatedSubjectSuggestionDTO] = Field(default_factory=list)
    tier1_web_resources: List[Tier1WebResourceDTO] = Field(default_factory=list)
    tier2_youtube_videos: List[Tier2YouTubeVideoDTO] = Field(default_factory=list)
    tier3_score_strategy: Tier3ScoreStrategyDTO
    recommended_path: List[Dict[str, Any]] = Field(default_factory=list)


class ActiveLearningSessionDTO(BaseModel):
    user_id: int
    subject_id: int
    topic_id: Optional[int] = None
    subject_code: Optional[str] = None
    subject_title: Optional[str] = None
    message: Optional[str] = "Đã lưu trạng thái học tập thành công"


# ==========================================
# 20. PORTFOLIO & CAPSTONE PROJECTS SCHEMAS
# ==========================================
class PortfolioProjectStepDTO(BaseModel):
    step_number: int
    title: str
    description: str
    code_snippet: Optional[str] = None
    key_deliverable: str


class PortfolioProjectDTO(BaseModel):
    id: str
    title: str
    subject_code: str
    subject_title: str
    industry: str
    difficulty: str
    estimated_hours: str
    summary: str
    business_impact: str
    tech_stack: List[str]
    dataset_name: str
    dataset_url: str
    dataset_description: str
    github_starter_url: str
    colab_starter_url: str
    cv_bullet_point: str
    steps: List[PortfolioProjectStepDTO]


