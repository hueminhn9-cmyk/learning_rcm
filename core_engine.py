"""
Enterprise Core Engine for Intelligent Tutoring System (ITS) & LMS
===================================================================
Author: Lead Solutions & AI Architect
Architecture: Autonomous Student + Governance Admin (2-Actor Domain)
Modules:
  1. KnowledgeGapAnalyzer & PrerequisiteDAGResolver (DAG & Topological Sort)
  2. SmartMaterialRecommender (Content-Based Cosine Similarity & Multi-Objective Ranking)
  3. DynamicRoadmapVersionManager (Immutable Event-Sourced Versioning & Audit Trail)
"""

from __future__ import annotations
import math
from enum import Enum
from typing import List, Dict, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


# ============================================================================
# DOMAIN MODELS & SHARED DATA CONTRACTS
# ============================================================================

class UserRole(str, Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"


class MasteryStatus(str, Enum):
    MASTERED = "MASTERED"          # Đạt (Đã nắm vững)
    NOT_MASTERED = "NOT_MASTERED"  # Chưa đạt (Cần học/học lại)
    NO_DATA = "NO_DATA"            # Chưa có dữ liệu đánh giá


class StepStatus(str, Enum):
    COMPLETED = "COMPLETED"        # Đã hoàn thành
    UNLOCKED = "UNLOCKED"          # Đủ tiên quyết, sẵn sàng học
    LOCKED = "LOCKED"              # Chưa đủ tiên quyết, đang khóa


class MaterialFormat(str, Enum):
    VIDEO = "VIDEO"
    READING = "READING"
    SLIDE = "SLIDE"
    EXERCISE = "EXERCISE"


class PublicationStatus(str, Enum):
    PUBLISHED = "PUBLISHED"        # Công bố công khai
    UNPUBLISHED = "UNPUBLISHED"    # Ngừng công bố / Nháp
    ARCHIVED = "ARCHIVED"          # Lưu trữ


class TriggerEventType(str, Enum):
    INITIAL_GENERATION = "INITIAL_GENERATION"
    ASSESSMENT_PASSED = "ASSESSMENT_PASSED"
    ASSESSMENT_FAILED = "ASSESSMENT_FAILED"
    GOAL_CHANGED = "GOAL_CHANGED"
    SCHEDULE_UPDATED = "SCHEDULE_UPDATED"


# --- Exceptions ---
class CyclicDependencyException(Exception):
    """Ngoại lệ phát hiện vòng lặp chu trình trong đồ thị tiên quyết."""
    pass


class TargetNotFoundException(Exception):
    """Ngoại lệ mục tiêu học tập không tồn tại trong đồ thị tri thức."""
    pass


# --- Data Structures ---
@dataclass(frozen=True)
class Topic:
    topic_id: str
    code: str
    title: str
    description: str
    estimated_hours: float = 2.0


@dataclass
class KnowledgeProfileItem:
    topic_id: str
    status: MasteryStatus
    mastery_score: float = 0.0     # Thang điểm 0 - 100
    last_assessed_at: Optional[datetime] = None


@dataclass
class LearningStep:
    step_number: int
    topic_id: str
    code: str
    title: str
    status: StepStatus
    direct_prerequisites: List[str]
    explainable_reason: str


@dataclass
class StudentNeedVector:
    """Vector nhu cầu học tập của sinh viên"""
    target_topic_id: str
    desired_difficulty: float      # Thang 1.0 - 5.0
    preferred_format: MaterialFormat
    preferred_duration_minutes: float  # Phút


@dataclass
class LearningMaterial:
    material_id: str
    topic_id: str
    title: str
    format: MaterialFormat
    difficulty_level: float        # Thang 1.0 - 5.0
    duration_minutes: float
    coverage_weight: float         # 0.0 - 1.0 (Độ bao phủ chủ đề)
    quality_score: float           # 0.0 - 5.0 (Đánh giá học thuật / rating)
    status: PublicationStatus = PublicationStatus.PUBLISHED
    author_id: str = "ADMIN_DEFAULT"


@dataclass
class RecommendationItem:
    rank: int
    role: str                      # "PRIMARY" | "ALTERNATIVE"
    material: LearningMaterial
    cosine_similarity: float
    composite_score: float
    explainable_reason: str


@dataclass
class RoadmapSnapshot:
    version: str                   # SemVer: v1.0, v1.1, v2.0
    created_at: datetime
    trigger_event: TriggerEventType
    event_payload: Dict[str, Any]
    target_topic_id: str
    steps: List[LearningStep]
    knowledge_state_snapshot: Dict[str, MasteryStatus]
    parent_version: Optional[str] = None


# ============================================================================
# MODULE 1: GAP ANALYSIS & PREREQUISITE DAG RESOLVER
# ============================================================================

class PrerequisiteDAG:
    """
    Quản lý cấu trúc Đồ thị Hướng không chu kỳ (DAG) của các Chủ đề học tập.
    Admin là Actor duy nhất có quyền quản trị đồ thị này.
    """
    def __init__(self):
        self._topics: Dict[str, Topic] = {}
        self._adj_list: Dict[str, Set[str]] = {}      # u -> {v} (u là tiên quyết của v)
        self._rev_adj_list: Dict[str, Set[str]] = {}  # v -> {u} (u là tiên quyết trực tiếp của v)

    def add_topic(self, topic: Topic) -> None:
        self._topics[topic.topic_id] = topic
        if topic.topic_id not in self._adj_list:
            self._adj_list[topic.topic_id] = set()
        if topic.topic_id not in self._rev_adj_list:
            self._rev_adj_list[topic.topic_id] = set()

    def add_prerequisite(self, prereq_id: str, target_id: str) -> None:
        if prereq_id not in self._topics or target_id not in self._topics:
            raise KeyError(f"Chủ đề '{prereq_id}' hoặc '{target_id}' không tồn tại trong DAG.")
        self._adj_list[prereq_id].add(target_id)
        self._rev_adj_list[target_id].add(prereq_id)

    def get_topic(self, topic_id: str) -> Topic:
        return self._topics[topic_id]

    def has_topic(self, topic_id: str) -> bool:
        return topic_id in self._topics

    def get_direct_prerequisites(self, topic_id: str) -> Set[str]:
        return self._rev_adj_list.get(topic_id, set())

    def get_all_ancestors(self, topic_id: str) -> Set[str]:
        """Truy vết ngược toàn bộ các tiền đề gián tiếp và trực tiếp (Transitive Closure)"""
        visited: Set[str] = set()
        queue = list(self._rev_adj_list.get(topic_id, set()))
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.add(curr)
                queue.extend(self._rev_adj_list.get(curr, set()))
        return visited

    def detect_cycles(self) -> None:
        """Kiểm tra chu trình sử dụng thuật toán Kahn. Ném ngoại lệ nếu có cycle."""
        in_degree = {u: len(self._rev_adj_list[u]) for u in self._topics}
        queue = [u for u, deg in in_degree.items() if deg == 0]
        visited_count = 0

        while queue:
            node = queue.pop(0)
            visited_count += 1
            for neighbor in self._adj_list.get(node, set()):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count != len(self._topics):
            raise CyclicDependencyException(
                "Phát hiện chu trình phụ thuộc (Cycle Detected) trong Đồ thị Tiên quyết! "
                "Đồ thị vi phạm tính chất Directed Acyclic Graph (DAG)."
            )


class KnowledgeGapAnalyzer:
    """
    Module 1: Phân tích khoảng thiếu hụt kiến thức và sắp xếp Tô-pô (Topological Sort).
    Sinh lộ trình học tập cá nhân hóa có khả năng giải thích (Explainable AI - XAI).
    """
    def __init__(self, dag: PrerequisiteDAG):
        self.dag = dag

    def generate_personalized_roadmap(
        self,
        student_id: str,
        target_topic_id: str,
        student_profile: Dict[str, KnowledgeProfileItem]
    ) -> List[LearningStep]:
        # 1. Kiểm tra tính toàn vẹn của Đồ thị
        self.dag.detect_cycles()

        if not self.dag.has_topic(target_topic_id):
            raise TargetNotFoundException(f"Mục tiêu '{target_topic_id}' không tồn tại trong hệ thống tri thức.")

        # 2. Truy vết tập hợp tri thức cần thiết (Ancestors + Target)
        needed_ancestors = self.dag.get_all_ancestors(target_topic_id)
        all_required_ids = needed_ancestors.union({target_topic_id})

        # 3. Xây dựng đồ thị con (Subgraph) và tính In-degree để Topological Sort
        subgraph_in_degree: Dict[str, int] = {}
        for node in all_required_ids:
            direct_pre = self.dag.get_direct_prerequisites(node)
            subgraph_in_degree[node] = len([p for p in direct_pre if p in all_required_ids])

        # Sắp xếp Tô-pô (Kahn's Algorithm trên Subgraph)
        queue = [node for node, deg in subgraph_in_degree.items() if deg == 0]
        sorted_topic_ids: List[str] = []

        while queue:
            curr = queue.pop(0)
            sorted_topic_ids.append(curr)
            for neighbor in self.dag._adj_list.get(curr, set()):
                if neighbor in subgraph_in_degree:
                    subgraph_in_degree[neighbor] -= 1
                    if subgraph_in_degree[neighbor] == 0:
                        queue.append(neighbor)

        # 4. Đánh giá trạng thái và tạo Explainability Context cho từng bước học
        steps: List[LearningStep] = []
        mastered_set = {
            tid for tid, item in student_profile.items() 
            if item.status == MasteryStatus.MASTERED
        }

        for idx, tid in enumerate(sorted_topic_ids, start=1):
            topic = self.dag.get_topic(tid)
            direct_prereqs = list(self.dag.get_direct_prerequisites(tid))
            all_prereqs_met = all(p in mastered_set for p in direct_prereqs)

            # Phân loại trạng thái bước học
            if tid in mastered_set:
                status = StepStatus.COMPLETED
                reason = "Sinh viên đã đạt chuẩn thành thạo chủ đề này trong bài đánh giá trước."
            elif all_prereqs_met:
                status = StepStatus.UNLOCKED
                if len(direct_prereqs) == 0:
                    reason = "Chủ đề nền tảng nhập môn, không có tiên quyết, sẵn sàng học ngay."
                else:
                    prereq_names = [self.dag.get_topic(p).title for p in direct_prereqs]
                    reason = f"Đã thỏa mãn tất cả điều kiện tiên quyết ({', '.join(prereq_names)}). Mở khóa học ngay!"
            else:
                status = StepStatus.LOCKED
                missing = [self.dag.get_topic(p).title for p in direct_prereqs if p not in mastered_set]
                reason = f"Đang khóa do chưa hoàn thành các kiến thức nền bắt buộc: {', '.join(missing)}."

            steps.append(
                LearningStep(
                    step_number=idx,
                    topic_id=tid,
                    code=topic.code,
                    title=topic.title,
                    status=status,
                    direct_prerequisites=direct_prereqs,
                    explainable_reason=reason
                )
            )

        return steps


# ============================================================================
# MODULE 2: SMART MATERIAL RECOMMENDER (CONTENT-BASED COSINE SIMILARITY)
# ============================================================================

class SmartMaterialRecommender:
    """
    Module 2: Đề xuất học liệu thông minh dựa trên Content-Based Filtering, 
    Cosine Similarity đa chiều và Hàm tính điểm tổng hợp (Composite Multi-Objective Score).
    """
    FORMAT_ORDER = [MaterialFormat.VIDEO, MaterialFormat.READING, MaterialFormat.SLIDE, MaterialFormat.EXERCISE]

    def __init__(
        self,
        weight_similarity: float = 0.50,
        weight_quality: float = 0.30,
        weight_coverage: float = 0.20
    ):
        """Trọng số do Admin cấu hình (Tổng các trọng số chuẩn hóa = 1.0)"""
        self.w_sim = weight_similarity
        self.w_qual = weight_quality
        self.w_cov = weight_coverage

    def _vectorize_student_need(self, need: StudentNeedVector) -> List[float]:
        """
        Chuẩn hóa vector nhu cầu:
        [độ_khó/5.0, thời_lượng_chuẩn_hóa/60.0, format_one_hot...]
        """
        norm_diff = need.desired_difficulty / 5.0
        norm_dur = min(need.preferred_duration_minutes / 60.0, 1.0)
        format_vec = [1.0 if f == need.preferred_format else 0.0 for f in self.FORMAT_ORDER]
        return [norm_diff, norm_dur] + format_vec

    def _vectorize_material(self, mat: LearningMaterial) -> List[float]:
        """Chuẩn hóa vector đặc trưng của học liệu"""
        norm_diff = mat.difficulty_level / 5.0
        norm_dur = min(mat.duration_minutes / 60.0, 1.0)
        format_vec = [1.0 if f == mat.format else 0.0 for f in self.FORMAT_ORDER]
        return [norm_diff, norm_dur] + format_vec

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Tính Cosine Similarity giữa 2 vectors bất kỳ"""
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return max(0.0, min(1.0, dot_product / (norm_a * norm_b)))

    def recommend_top_materials(
        self,
        need: StudentNeedVector,
        candidates: List[LearningMaterial],
        is_topic_unlocked_or_mastered: bool
    ) -> List[RecommendationItem]:
        # 1. BỘ LỌC NGHIÊM NGẶT (Strict Boundary Rules)
        # Nếu chủ đề chưa thỏa điều kiện tiên quyết -> Không đề xuất học liệu
        if not is_topic_unlocked_or_mastered:
            return []

        # Chỉ xét học liệu đã công bố (PUBLISHED), loại bỏ hoàn toàn UNPUBLISHED & ARCHIVED
        valid_candidates = [
            m for m in candidates 
            if m.topic_id == need.target_topic_id and m.status == PublicationStatus.PUBLISHED
        ]

        if not valid_candidates:
            return []

        student_vec = self._vectorize_student_need(need)
        scored_items: List[Tuple[LearningMaterial, float, float]] = []

        # 2. TÍNH TOÁN COSINE SIMILARITY & COMPOSITE SCORE
        for mat in valid_candidates:
            mat_vec = self._vectorize_material(mat)
            cos_sim = self._cosine_similarity(student_vec, mat_vec)

            norm_quality = mat.quality_score / 5.0
            norm_coverage = mat.coverage_weight

            # Công thức điểm tổng hợp (Composite Multi-Objective Score)
            composite_score = (
                self.w_sim * cos_sim +
                self.w_qual * norm_quality +
                self.w_cov * norm_coverage
            )
            scored_items.append((mat, cos_sim, composite_score))

        # 3. SẮP XẾP VÀ TRÍCH XUẤT TOP 3 HỌC LIỆU
        scored_items.sort(key=lambda x: x[2], reverse=True)
        top_items = scored_items[:3]

        results: List[RecommendationItem] = []
        for idx, (mat, cos_sim, comp_score) in enumerate(top_items, start=1):
            is_primary = (idx == 1)
            role = "PRIMARY" if is_primary else "ALTERNATIVE"

            # 4. EXPLAINABILITY ENGINE (Tạo lý do giải thích minh bạch)
            format_match = "Trùng khớp định dạng ưa thích" if mat.format == need.preferred_format else "Định dạng thay thế phong phú"
            sim_percent = round(cos_sim * 100, 1)

            if is_primary:
                reason = (
                    f"HỌC LIỆU CHÍNH TỐI ƯU NHẤT (Điểm tổng hợp: {comp_score:.2f}): "
                    f"Độ tương đồng nhu cầu {sim_percent}%, {format_match}, "
                    f"chất lượng học thuật {mat.quality_score}/5.0 và độ bao phủ {mat.coverage_weight * 100:.0f}%."
                )
            else:
                reason = (
                    f"LỰA CHỌN THAY THẾ #{idx - 1} (Điểm tổng hợp: {comp_score:.2f}): "
                    f"Độ tương thích {sim_percent}%, phù hợp nếu bạn muốn góc nhìn khác hoặc định dạng {mat.format.value}."
                )

            results.append(
                RecommendationItem(
                    rank=idx,
                    role=role,
                    material=mat,
                    cosine_similarity=round(cos_sim, 4),
                    composite_score=round(comp_score, 4),
                    explainable_reason=reason
                )
            )

        return results


# ============================================================================
# MODULE 3: DYNAMIC ROADMAP & IMMUTABLE VERSION CONTROL
# ============================================================================

class DynamicRoadmapVersionManager:
    """
    Module 3: Quản lý phiên bản lộ trình động, kiểm soát lịch sử bất biến (Append-Only Event Sourcing)
    đảm bảo truy vết bằng chứng học tập (Auditability) khi sinh viên hoàn thành đánh giá hoặc cập nhật mục tiêu.
    """
    def __init__(self, gap_analyzer: KnowledgeGapAnalyzer):
        self.gap_analyzer = gap_analyzer
        # Phân vùng dữ liệu: student_id -> List[RoadmapSnapshot] (Lịch sử phiên bản không bao giờ bị xóa đè)
        self._version_registry: Dict[str, List[RoadmapSnapshot]] = {}

    def get_version_history(self, student_id: str) -> List[RoadmapSnapshot]:
        return self._version_registry.get(student_id, [])

    def get_latest_roadmap(self, student_id: str) -> Optional[RoadmapSnapshot]:
        history = self.get_version_history(student_id)
        return history[-1] if history else None

    def initialize_roadmap(
        self,
        student_id: str,
        target_topic_id: str,
        student_profile: Dict[str, KnowledgeProfileItem]
    ) -> RoadmapSnapshot:
        """Khởi tạo phiên bản lộ trình đầu tiên v1.0"""
        steps = self.gap_analyzer.generate_personalized_roadmap(student_id, target_topic_id, student_profile)
        state_snapshot = {tid: item.status for tid, item in student_profile.items()}

        snapshot = RoadmapSnapshot(
            version="v1.0",
            created_at=datetime.utcnow(),
            trigger_event=TriggerEventType.INITIAL_GENERATION,
            event_payload={"description": "Khởi tạo lộ trình học tập ban đầu theo mục tiêu chuyên ngành."},
            target_topic_id=target_topic_id,
            steps=steps,
            knowledge_state_snapshot=state_snapshot,
            parent_version=None
        )

        self._version_registry[student_id] = [snapshot]
        return snapshot

    def handle_assessment_completion(
        self,
        student_id: str,
        assessed_topic_id: str,
        score: float,
        student_profile: Dict[str, KnowledgeProfileItem],
        pass_threshold: float = 80.0
    ) -> RoadmapSnapshot:
        """
        Xử lý khi sinh viên nộp bài kiểm tra/quiz:
        - Cập nhật hồ sơ kiến thức.
        - Giữ nguyên lộ trình cũ trong lịch sử.
        - Tính toán và phát hành phiên bản mới (v1.1, v1.2...).
        """
        history = self._version_registry.get(student_id, [])
        if not history:
            raise ValueError(f"Sinh viên '{student_id}' chưa có lộ trình ban đầu.")

        current_latest = history[-1]
        passed = (score >= pass_threshold)

        # 1. Cập nhật hồ sơ kiến thức của sinh viên
        new_status = MasteryStatus.MASTERED if passed else MasteryStatus.NOT_MASTERED
        student_profile[assessed_topic_id] = KnowledgeProfileItem(
            topic_id=assessed_topic_id,
            status=new_status,
            mastery_score=score,
            last_assessed_at=datetime.utcnow()
        )

        # 2. Tính toán lộ trình mới theo đồ thị DAG
        new_steps = self.gap_analyzer.generate_personalized_roadmap(
            student_id=student_id,
            target_topic_id=current_latest.target_topic_id,
            student_profile=student_profile
        )

        # 3. Tạo định danh phiên bản tăng dần (SemVer minor revision)
        old_ver_num = float(current_latest.version.replace("v", ""))
        new_ver_str = f"v{old_ver_num + 0.1:.1f}"

        trigger = TriggerEventType.ASSESSMENT_PASSED if passed else TriggerEventType.ASSESSMENT_FAILED
        payload = {
            "topic_id": assessed_topic_id,
            "score": score,
            "passed": passed,
            "threshold": pass_threshold,
            "action": "Mở khóa các chủ đề tiếp theo" if passed else "Đề xuất bài ôn tập cứu điểm"
        }

        # 4. Ghi nhận snapshot mới vào lịch sử (Append-only, tuyệt đối không sửa snapshot cũ)
        new_snapshot = RoadmapSnapshot(
            version=new_ver_str,
            created_at=datetime.utcnow(),
            trigger_event=trigger,
            event_payload=payload,
            target_topic_id=current_latest.target_topic_id,
            steps=new_steps,
            knowledge_state_snapshot={tid: item.status for tid, item in student_profile.items()},
            parent_version=current_latest.version
        )

        self._version_registry[student_id].append(new_snapshot)
        return new_snapshot

    def handle_goal_change(
        self,
        student_id: str,
        new_target_topic_id: str,
        student_profile: Dict[str, KnowledgeProfileItem]
    ) -> RoadmapSnapshot:
        """
        Xử lý khi sinh viên thay đổi mục tiêu đầu ra:
        - Tăng major version (ví dụ: v1.1 -> v2.0).
        - Lưu trữ lộ trình cũ, sinh lộ trình mới.
        """
        history = self._version_registry.get(student_id, [])
        if not history:
            raise ValueError(f"Sinh viên '{student_id}' chưa có lộ trình ban đầu.")

        current_latest = history[-1]
        new_steps = self.gap_analyzer.generate_personalized_roadmap(
            student_id=student_id,
            target_topic_id=new_target_topic_id,
            student_profile=student_profile
        )

        old_major = int(float(current_latest.version.replace("v", "")))
        new_ver_str = f"v{old_major + 1}.0"

        new_snapshot = RoadmapSnapshot(
            version=new_ver_str,
            created_at=datetime.utcnow(),
            trigger_event=TriggerEventType.GOAL_CHANGED,
            event_payload={"old_target": current_latest.target_topic_id, "new_target": new_target_topic_id},
            target_topic_id=new_target_topic_id,
            steps=new_steps,
            knowledge_state_snapshot={tid: item.status for tid, item in student_profile.items()},
            parent_version=current_latest.version
        )

        self._version_registry[student_id].append(new_snapshot)
        return new_snapshot
