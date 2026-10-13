"""
FastAPI Backend API Controller & Static UI Server Entrypoint
Comprehensive EdTech Features Suite (Student + Admin + AI Engine)
"""

import os
from typing import List, Dict, Any
from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    UserRegisterDTO, UserLoginDTO, TokenResponseDTO,
    UserGoalCreateDTO, GoalFeasibilityResponseDTO,
    LearningPathRequest, LearningPathResponse,
    RecommendationRequest, RecommendationResponse,
    AssessmentSubmitRequest, AssessmentSubmitResponse,
    ConfigWeightUpdateDTO, ConfigHistoryItemDTO, AdminStatsResponse,
    SpacedRepetitionResponse, QuizDetailResponseDTO, KnowledgeProfileItemDTO,
    LearningProgressReportDTO, ManualGradingSubmitDTO,
    CreateNoteDTO, NoteResponseDTO, CreateFeedbackDTO, FeedbackItemDTO, FeedbackAdminUpdateDTO,
    FeynmanReflectionSubmitDTO, FeynmanReflectionResponseDTO,
    AvailableAssessmentsResponse, ProjectSubmissionRequest, SingleAnswerDTO,
    AvailableAssessmentItemDTO, QuestionReviewItemDTO, MaterialItemDTO,
    AIChatRequestDTO, AIChatResponseDTO,
    AISuggestGradingRequestDTO, AISuggestGradingResponseDTO,
    AIFeedbackAnalysisRequestDTO, AIFeedbackAnalysisResponseDTO,
    AIAutoTuneWeightsResponseDTO, AIRemedialQuizRequestDTO, AIRemedialQuizResponseDTO,
    QuizSubmitRequestDTO, QuizSubmitResponseDTO, QuizHistoryItemDTO, QuizAttemptDetailDTO
)
from services import (
    LearningPathService, ContentRecommendationService,
    SpacedRepetitionService, AssessmentProcessingService, AdminConfigService,
    QuestionBankService, ScheduledAssessmentService, KnowledgeProfileService,
    ProgressAnalyticsService, AdminOperationService, InteractiveLearningService,
    AITutorService, AdminAIService, QuizAttemptService
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="Aegis Learn - Personalized Learning Support Engine",
    description="Hệ thống hỗ trợ học tập cá nhân hóa toàn diện dựa trên Đồ thị tiên quyết, AI Recommendation, Spaced Repetition, Scheduled Quizzes & Gamification",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")


# ==========================================
# 1. UI STATIC PAGES SERVING
# ==========================================
@app.get("/", response_class=FileResponse, summary="Student Dashboard UI")
async def serve_student_dashboard():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/admin", response_class=FileResponse, summary="Admin Dashboard UI")
async def serve_admin_dashboard():
    admin_path = os.path.join(BASE_DIR, "admin.html")
    if os.path.exists(admin_path):
        return FileResponse(admin_path)
    raise HTTPException(status_code=404, detail="admin.html not found")


# ==========================================
# 2. AUTHENTICATION API
# ==========================================
@router.post("/auth/register", response_model=TokenResponseDTO, summary="Đăng ký tài khoản")
async def register(dto: UserRegisterDTO):
    return TokenResponseDTO(
        access_token="mock_jwt_access_token_12345",
        token_type="bearer",
        user_id=1,
        email=dto.email,
        role=dto.role,
        full_name=dto.full_name
    )


@router.post("/auth/login", response_model=TokenResponseDTO, summary="Đăng nhập tài khoản")
async def login(dto: UserLoginDTO):
    role = "ADMIN" if "admin" in dto.email.lower() else "STUDENT"
    name = "Quản trị viên" if role == "ADMIN" else "Nguyễn Văn A"
    return TokenResponseDTO(
        access_token="mock_jwt_access_token_12345",
        token_type="bearer",
        user_id=1,
        email=dto.email,
        role=role,
        full_name=name
    )


# ==========================================
# 3. GOAL & FEASIBILITY API (SV03)
# ==========================================
@router.post("/goals/feasibility", response_model=GoalFeasibilityResponseDTO, summary="Tính toán khả thi hạn chót mục tiêu (SV03)")
async def calculate_goal_feasibility(dto: UserGoalCreateDTO):
    return ProgressAnalyticsService.calculate_goal_feasibility(dto)


# ==========================================
# 4. KNOWLEDGE GRAPH & LEARNING PATH API
# ==========================================
@router.post("/learning-path/generate", response_model=LearningPathResponse, summary="Sinh Lộ trình học tập cá nhân hóa (Graph DAG)")
async def generate_learning_path(request: LearningPathRequest):
    try:
        return LearningPathService.generate_path(request)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.post("/recommendations/materials", response_model=RecommendationResponse, summary="Khuyến nghị Học liệu (Cosine Similarity)")
async def recommend_learning_materials(request: RecommendationRequest):
    return ContentRecommendationService.recommend(request)


@router.get("/materials/search", response_model=List[MaterialItemDTO], summary="Tìm kiếm tất cả học liệu kho CSDL (Search View)")
async def search_materials(q: str = "", topic_id: int = 0):
    return ContentRecommendationService.search_all_materials(q, topic_id)


@router.get("/learning-path/spaced-repetition/{user_id}", response_model=SpacedRepetitionResponse, summary="Thuật toán Ôn tập Ngắt quãng (Ebbinghaus)")
async def get_spaced_repetition_recommendations(user_id: int):
    return SpacedRepetitionService.calculate_memory_retention(user_id)


# ==========================================
# 5. KNOWLEDGE PROFILE & ANALYTICS API (SV05, SV12)
# ==========================================
@router.get("/knowledge-profile/{user_id}", response_model=List[KnowledgeProfileItemDTO], summary="Hồ sơ Năng lực Kiến thức theo Chủ đề (SV05)")
async def get_knowledge_profile(user_id: int):
    return KnowledgeProfileService.get_knowledge_profile(user_id)


@router.get("/analytics/progress/{user_id}", response_model=LearningProgressReportDTO, summary="Báo cáo Tiến độ & Streak Học tập (SV12)")
async def get_full_progress_dashboard(user_id: int):
    return ProgressAnalyticsService.get_full_progress_report(user_id)


# ==========================================
# 6. QUESTION BANK & ASSESSMENTS API (EXAM CENTER)
# ==========================================
@router.get("/assessments/available", response_model=AvailableAssessmentsResponse, summary="Lấy danh mục Kho đề thi & Dự án (Exam Center)")
async def get_available_assessments():
    return QuestionBankService.get_available_assessments()


@router.get("/question-bank/practice", response_model=QuizDetailResponseDTO, summary="Lấy đề tự luyện tập theo Chủ đề (SV09)")
async def get_practice_quiz(topic_id: int = 102, count: int = 5, difficulty_level: float = 2.0):
    return QuestionBankService.get_practice_quiz(topic_id, count, difficulty_level)


@router.post("/assessments/random-generate", response_model=QuizDetailResponseDTO, summary="Sinh đề ngẫu nhiên mới 10 câu không trùng lặp 🎲")
async def generate_random_quiz(dto: Dict[str, Any]):
    user_id = dto.get("user_id", 1)
    count = dto.get("count", 10)
    return QuestionBankService.generate_random_quiz(user_id, count)


@router.post("/assessments/weekly/generate", response_model=QuizDetailResponseDTO, summary="Sinh đề Kiểm tra Định kỳ Tuần (SV06)")
async def generate_weekly_checkpoint(dto: Dict[str, Any]):
    user_id = dto.get("user_id", 1)
    return ScheduledAssessmentService.generate_weekly_checkpoint(user_id)


@router.post("/assessments/monthly/generate", response_model=QuizDetailResponseDTO, summary="Sinh đề Kiểm tra Dự án Tháng (SV07)")
async def generate_monthly_project_assessment(dto: Dict[str, Any]):
    user_id = dto.get("user_id", 1)
    return ScheduledAssessmentService.generate_monthly_project_assessment(user_id)


@router.post("/assessments/project/submit", response_model=AssessmentSubmitResponse, summary="Nộp bài Dự án Hàng tháng (Monthly Project Submission)")
async def submit_project_milestone(request: ProjectSubmissionRequest):
    submit_req = AssessmentSubmitRequest(
        user_id=request.user_id,
        assessment_id=request.assessment_id,
        topic_id=104,
        answers=[
            SingleAnswerDTO(question_id=999, user_answer=f"Link: {request.submission_url} | Nộp bài: {request.report_text}", question_type="ESSAY")
        ],
        time_taken_seconds=1800
    )
    return AssessmentProcessingService.submit_assessment(submit_req)


@router.post("/assessments/submit", response_model=AssessmentSubmitResponse, summary="Nộp bài đánh giá (Submit Quiz)")
async def submit_assessment(request: AssessmentSubmitRequest):
    return AssessmentProcessingService.submit_assessment(request)


# ==========================================
# 6.1. INSTANT RESULT & QUIZ HISTORY API
# ==========================================
@router.post("/quiz/submit", response_model=QuizSubmitResponseDTO, summary="Nộp bài kiểm tra & Chấm điểm tức thì (Instant Grading & Detailed Review)")
async def submit_quiz(dto: QuizSubmitRequestDTO):
    return QuizAttemptService.submit_quiz(dto)


@router.get("/quiz/history", response_model=List[QuizHistoryItemDTO], summary="Lấy danh sách Lịch sử thi trắc nghiệm của sinh viên")
async def get_quiz_history(user_id: int = 1):
    return QuizAttemptService.get_user_history(user_id)


@router.get("/quiz/history/{attempt_id}", response_model=QuizAttemptDetailDTO, summary="Lấy chi tiết đáp án & lời giải một lần thi cụ thể")
async def get_quiz_attempt_detail(attempt_id: int):
    return QuizAttemptService.get_attempt_detail(attempt_id)



# ==========================================
# 7. PERSONAL NOTES & CONTENT FEEDBACK API (SV08, SV13)
# ==========================================
@router.post("/notes", response_model=NoteResponseDTO, summary="Lưu Ghi chú Bài học (SV08)")
async def create_note(dto: CreateNoteDTO):
    return InteractiveLearningService.create_note(dto)


@router.get("/notes/{user_id}", response_model=List[NoteResponseDTO], summary="Lấy danh sách Ghi chú của Sinh viên")
async def get_user_notes(user_id: int):
    return InteractiveLearningService.MOCK_NOTES


@router.post("/feedback", response_model=FeedbackItemDTO, summary="Báo lỗi & Phản hồi Học liệu (SV13)")
async def create_feedback(dto: CreateFeedbackDTO):
    fb = FeedbackItemDTO(
        id=len(AdminOperationService.FEEDBACK_LIST) + 1,
        user_id=dto.user_id,
        material_id=dto.material_id,
        material_title=f"Học liệu #{dto.material_id}",
        feedback_type=dto.feedback_type,
        description=dto.description,
        status="NEW",
        admin_response=None,
        created_at="Vừa xong"
    )
    AdminOperationService.FEEDBACK_LIST.append(fb)
    return fb


# ==========================================
# 8. INTERACTIVE LEARNING & FEYNMAN API
# ==========================================
@router.post("/learning/feynman/reflect", response_model=FeynmanReflectionResponseDTO, summary="Chấm điểm Kỹ thuật Tự diễn đạt Feynman")
async def submit_feynman_reflection(dto: FeynmanReflectionSubmitDTO):
    return InteractiveLearningService.submit_feynman_reflection(dto)


# ==========================================
# 9. ADMIN OPERATIONS API (QT10, QT11)
# ==========================================
@router.get("/admin/stats", response_model=AdminStatsResponse, summary="Thống kê Tổng quan Admin")
async def get_admin_stats():
    return AdminConfigService.get_dashboard_stats()


@router.get("/admin/feedbacks", response_model=List[FeedbackItemDTO], summary="Admin - Danh sách Phản hồi Học liệu (QT11)")
async def get_admin_feedbacks():
    return AdminOperationService.FEEDBACK_LIST


@router.post("/admin/feedbacks/resolve", response_model=FeedbackItemDTO, summary="Admin - Xử lý Phản hồi Báo lỗi")
async def resolve_feedback(dto: FeedbackAdminUpdateDTO):
    return AdminOperationService.process_feedback(dto)


@router.post("/admin/grading/submit", summary="Admin - Chấm điểm Bài tự luận / Dự án (QT10)")
async def grade_essay_submission(dto: ManualGradingSubmitDTO):
    return AdminOperationService.grade_essay_submission(dto)


@router.post("/admin/recommendation-config/update", response_model=ConfigHistoryItemDTO, summary="Cập nhật Cấu hình Khuyến nghị & Audit Log")
async def update_recommendation_config(dto: ConfigWeightUpdateDTO):
    return AdminConfigService.update_config(dto)


@router.get("/admin/recommendation-config/history", response_model=List[ConfigHistoryItemDTO], summary="Lịch sử Phiên bản Cấu hình Audit Log")
async def get_recommendation_config_history():
    return AdminConfigService.get_history()


# ==========================================
# 9.1 ADMIN AI ASSISTANT API (QT10, QT11, AUTO-TUNE, REMEDIAL)
# ==========================================
@router.post("/admin/ai/suggest-grading", response_model=AISuggestGradingResponseDTO, summary="Admin AI - Chấm điểm gợi ý bài tự luận (QT10)")
async def ai_suggest_grading(dto: AISuggestGradingRequestDTO):
    return AdminAIService.suggest_essay_grading(dto)


@router.post("/admin/ai/analyze-feedback", response_model=AIFeedbackAnalysisResponseDTO, summary="Admin AI - Phân tích & Đề xuất giải pháp báo lỗi (QT11)")
async def ai_analyze_feedback(dto: AIFeedbackAnalysisRequestDTO):
    return AdminAIService.analyze_feedback(dto)


@router.post("/admin/ai/auto-tune-weights", response_model=AIAutoTuneWeightsResponseDTO, summary="Admin AI - Tự động cân chỉnh trọng số khuyến nghị (Auto-Tune)")
async def ai_auto_tune_weights():
    return AdminAIService.auto_tune_weights()


@router.post("/admin/ai/generate-remedial-quiz", response_model=AIRemedialQuizResponseDTO, summary="Admin AI - Sinh đề cứu điểm cho môn học gặp khó")
async def ai_generate_remedial_quiz(dto: AIRemedialQuizRequestDTO):
    return AdminAIService.generate_remedial_quiz(dto)



# ==========================================
# 10. AI TUTOR CHATBOT API (SV_CHAT)
# ==========================================
@router.post("/ai/chat", response_model=AIChatResponseDTO, summary="Gia sư AI Trợ lý Học tập & Giải đáp (AI Tutor Chat)")
async def chat_with_ai_tutor(dto: AIChatRequestDTO):
    return AITutorService.get_tutor_response(dto)


@router.post("/learning-path/mark-mastered", summary="Cập nhật mốc thành thạo sau kiểm tra")
async def mark_topic_mastered(dto: Dict[str, Any]):
    user_id = dto.get("user_id", 1)
    topic_id = dto.get("topic_id", 101)
    score = dto.get("score", 85.0)
    return KnowledgeProfileService.mark_topic_mastered(user_id, topic_id, score)


@router.get("/health", summary="Health Check API")
async def health_check():
    return {
        "status": "online",
        "service": "Aegis Learn Personalized Engine v2.0",
        "version": "2.0.0"
    }


app.include_router(router)
