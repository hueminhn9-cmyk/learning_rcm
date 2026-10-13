import React, { useState, useEffect } from 'react';
import { 
  BookOpen, CheckCircle2, Lock, PlayCircle, Star, Target, 
  Clock, Award, Layers, Sparkles, ChevronRight, Search, Bell, 
  User, LayoutDashboard, Compass, BookMarked, BarChart3, Settings
} from 'lucide-react';

const API_BASE_URL = "http://localhost:8000/api/v1";

export default function StudentDashboard() {
  // State Management
  const [loading, setLoading] = useState(true);
  const [learningPathData, setLearningPathData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedTopicId, setSelectedTopicId] = useState(102); // Topic "Giải tích 1" (UNLOCKED)
  const [activeTab, setActiveTab] = useState('path');

  // Fetch Data from FastAPI Backend
  useEffect(() => {
    fetchDashboardData();
  }, [selectedTopicId]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // 1. Fetch Learning Path API
      const pathPayload = {
        user_id: 1,
        target_topic_id: 104, // Target: Học máy cơ bản
        mastered_topic_ids: [101], // Mastered: Đại số Đại cương
        all_topics: [
          { id: 101, code: "T101", title: "Đại số Đại cương", description: "Nền tảng ma trận và không gian vector" },
          { id: 102, code: "T102", title: "Giải tích 1", description: "Đạo hàm, tích phân và chuỗi số" },
          { id: 103, code: "T103", title: "Giải tích 2", description: "Đạo hàm riêng và Tích phân bội" },
          { id: 104, code: "T104", title: "Học máy cơ bản", description: "Mô hình Regression, Classification và Clustering" }
        ],
        prerequisites: [
          { topic_id: 102, prerequisite_topic_id: 101, dependency_type: "STRICT" },
          { topic_id: 103, prerequisite_topic_id: 102, dependency_type: "STRICT" },
          { topic_id: 104, prerequisite_topic_id: 103, dependency_type: "STRICT" }
        ]
      };

      const pathRes = await fetch(`${API_BASE_URL}/learning-path/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(pathPayload)
      });

      if (pathRes.ok) {
        const pathJson = await pathRes.json();
        setLearningPathData(pathJson);
      } else {
        throw new Error("Failed to fetch API");
      }

      // 2. Fetch Content Recommendations API
      const recPayload = {
        topic_id: selectedTopicId,
        student_profile: {
          user_id: 1,
          learning_style: "VISUAL",
          preferred_material_type: "VIDEO",
          estimated_ability_score: 3.5,
          recent_quiz_avg_score: 85.0
        },
        candidate_materials: [
          { id: 1, title: "Video: Đạo hàm & Ứng dụng trong Gradient Descent", material_type: "VIDEO", content_url: "#", difficulty_level: 3.5, version: 1, is_latest: true },
          { id: 2, title: "Bài đọc: Tóm tắt Tích phân & Ma trận Gradient", material_type: "READING", content_url: "#", difficulty_level: 3.0, version: 1, is_latest: true },
          { id: 3, title: "Slide: Tổng quan Kỹ thuật Tối ưu hóa Toán học", material_type: "SLIDE", content_url: "#", difficulty_level: 4.0, version: 1, is_latest: true },
          { id: 4, title: "Bài tập: 15 Bài toán Đạo hàm riêng ứng dụng ML", material_type: "EXERCISE", content_url: "#", difficulty_level: 3.8, version: 1, is_latest: true }
        ],
        top_k: 3
      };

      const recRes = await fetch(`${API_BASE_URL}/recommendations/materials`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(recPayload)
      });

      if (recRes.ok) {
        const recJson = await recRes.json();
        setRecommendations(recJson.recommendations || []);
      }

    } catch (error) {
      console.warn("Backend API not reachable, falling back to simulated data", error);
      // Fallback Mock Data for standalone UX
      setLearningPathData({
        total_steps: 4,
        completed_steps_count: 1,
        unlocked_steps_count: 1,
        locked_steps_count: 2,
        estimated_hours: 7.5,
        learning_path: [
          { step_number: 1, topic_id: 101, code: "T101", title: "Đại số Đại cương", status: "COMPLETED", reasoning: "Bạn đã làm chủ kiến thức này." },
          { step_number: 2, topic_id: 102, code: "T102", title: "Giải tích 1", status: "UNLOCKED", reasoning: "Tiên quyết đã sẵn sàng. Hãy bắt đầu ngay!" },
          { step_number: 3, topic_id: 103, code: "T103", title: "Giải tích 2", status: "LOCKED", reasoning: "Yêu cầu hoàn thành: Giải tích 1" },
          { step_number: 4, topic_id: 104, code: "T104", title: "Học máy cơ bản", status: "LOCKED", reasoning: "Yêu cầu hoàn thành: Giải tích 2" }
        ]
      });

      setRecommendations([
        {
          material: { id: 1, title: "Video bài giảng: Gradient Descent & Đạo hàm", material_type: "VIDEO", difficulty_level: 3.5 },
          similarity_score: 0.9996,
          match_percentage: 99.96,
          recommendation_reason: "Phù hợp phong cách VISUAL (VIDEO) | Độ khó tối ưu 3.5/5.0"
        },
        {
          material: { id: 2, title: "Bài đọc tổng hợp: Ứng dụng Giải tích trong AI", material_type: "READING", difficulty_level: 3.0 },
          similarity_score: 0.7850,
          match_percentage: 78.50,
          recommendation_reason: "Củng cố lý thuyết nền tảng"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const progressPercent = learningPathData 
    ? Math.round((learningPathData.completed_steps_count / learningPathData.total_steps) * 100) 
    : 25;

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans antialiased overflow-hidden">
      
      {/* 1. SIDEBAR NAVIGATION */}
      <aside className="w-64 bg-slate-900/90 border-r border-slate-800 flex flex-col justify-between p-4 backdrop-blur-md">
        <div>
          {/* Logo Brand */}
          <div className="flex items-center gap-3 px-3 py-4 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg text-white leading-tight">Aegis Learn</h1>
              <span className="text-xs text-indigo-400 font-medium tracking-wide">AI Learning Agent</span>
            </div>
          </div>

          {/* Nav Items */}
          <nav className="space-y-1.5">
            <NavItem icon={<LayoutDashboard size={18} />} label="Tổng quan" active={false} />
            <NavItem icon={<Compass size={18} />} label="Lộ trình học tập" active={true} badge="AI Path" />
            <NavItem icon={<BookMarked size={18} />} label="Kho học liệu" active={false} />
            <NavItem icon={<BarChart3 size={18} />} label="Đánh giá & Kết quả" active={false} />
            <NavItem icon={<Target size={18} />} label="Mục tiêu của tôi" active={false} />
          </nav>
        </div>

        {/* User Profile Summary Bottom Sidebar */}
        <div className="pt-4 border-t border-slate-800">
          <div className="flex items-center gap-3 p-2 rounded-xl bg-slate-800/50 hover:bg-slate-800 transition">
            <div className="w-9 h-9 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-semibold border border-indigo-500/30">
              NV
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-200 truncate">Nguyễn Văn A</p>
              <p className="text-xs text-slate-400 truncate">Sinh viên tự chủ</p>
            </div>
            <Settings size={16} className="text-slate-400 hover:text-slate-200 cursor-pointer" />
          </div>
        </div>
      </aside>

      {/* 2. MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col overflow-y-auto bg-slate-950">
        
        {/* TOPBAR */}
        <header className="h-16 border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center gap-4 w-96">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input 
                type="text" 
                placeholder="Tìm kiếm môn học, chủ đề, học liệu..." 
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-1.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button className="relative p-2 text-slate-400 hover:text-slate-200 rounded-xl bg-slate-900 border border-slate-800 transition">
              <Bell size={18} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-indigo-500 rounded-full"></span>
            </button>
            <div className="h-8 w-[1px] bg-slate-800"></div>
            <div className="flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 px-3 py-1 rounded-full text-xs font-semibold">
              <Award size={14} /> Level: Advanced AI Learner
            </div>
          </div>
        </header>

        {/* DASHBOARD CONTENT BODY */}
        <div className="p-8 space-y-8 max-w-7xl mx-auto w-full">
          
          {/* HEADER GREETING */}
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">Lộ trình học tập cá nhân hóa 🚀</h2>
            <p className="text-slate-400 text-sm mt-1">Đồ thị kiến thức được cập nhật theo thời gian thực dựa trên tiên quyết và tiến độ của bạn.</p>
          </div>

          {/* CARD 1: MỤC TIÊU HIỆN TẠI & TIẾN ĐỘ */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Goal Details & Progress Bar Card */}
            <div className="lg:col-span-2 bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950/40 border border-slate-800 rounded-2xl p-6 relative overflow-hidden shadow-xl">
              <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl pointer-events-none"></div>
              
              <div className="flex items-start justify-between">
                <div>
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-medium border border-indigo-500/20 mb-3">
                    <Target size={12} /> Mục tiêu hiện tại
                  </span>
                  <h3 className="text-xl font-bold text-white">Chinh phục: Học máy cơ bản (AI Fundamentals)</h3>
                  <p className="text-slate-400 text-sm mt-1">Hoàn thành lộ trình 4 bước từ toán nền tảng đến mô hình AI.</p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Thời gian ước tính</span>
                  <span className="text-lg font-bold text-indigo-400 flex items-center gap-1 justify-end">
                    <Clock size={16} /> {learningPathData?.estimated_hours || 7.5} giờ
                  </span>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-6 space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-300 font-medium">Tiến độ hoàn thành</span>
                  <span className="text-indigo-400 font-bold">{progressPercent}%</span>
                </div>
                <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
                  <div 
                    className="bg-gradient-to-r from-indigo-500 to-violet-500 h-full rounded-full transition-all duration-700 ease-out shadow-lg shadow-indigo-500/50"
                    style={{ width: `${progressPercent}%` }}
                  ></div>
                </div>
              </div>

              {/* Mini Stats Bar */}
              <div className="grid grid-cols-3 gap-4 mt-6 pt-4 border-t border-slate-800/80">
                <div className="text-center">
                  <span className="text-xs text-slate-400 block">Đã xong</span>
                  <span className="text-base font-bold text-emerald-400">{learningPathData?.completed_steps_count || 1} bước</span>
                </div>
                <div className="text-center border-x border-slate-800">
                  <span className="text-xs text-slate-400 block">Sẵn sàng học</span>
                  <span className="text-base font-bold text-indigo-400">{learningPathData?.unlocked_steps_count || 1} bước</span>
                </div>
                <div className="text-center">
                  <span className="text-xs text-slate-400 block">Bị khóa (Tiên quyết)</span>
                  <span className="text-base font-bold text-slate-500">{learningPathData?.locked_steps_count || 2} bước</span>
                </div>
              </div>
            </div>

            {/* AI Advisor Badge Card */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between shadow-xl">
              <div>
                <div className="flex items-center gap-2 text-violet-400 font-semibold text-sm mb-2">
                  <Sparkles size={16} /> Gợi ý từ AI Agent
                </div>
                <p className="text-slate-300 text-sm leading-relaxed">
                  "Hệ thống nhận thấy bạn đã hoàn thành xuất sắc <strong className="text-emerald-400">Đại số Đại cương</strong>. Chủ đề tiếp theo <strong className="text-indigo-400">Giải tích 1</strong> đã được mở khóa hoàn toàn!"
                </p>
              </div>
              <button 
                onClick={() => setSelectedTopicId(102)}
                className="w-full mt-4 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 px-4 rounded-xl text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-indigo-600/30"
              >
                Học bước mở khóa ngay <ChevronRight size={16} />
              </button>
            </div>
          </div>

          {/* CARD 2: TIMELINE COMPONENT - LỘ TRÌNH CÁ NHÂN (GRAPH TIMELINE) */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Layers className="text-indigo-400" size={20} /> Lộ trình bài học dựa trên Đồ thị Tiên quyết
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">Thứ tự các bước được thuật toán Topological Sort tự động sắp xếp.</p>
              </div>
              <span className="text-xs text-slate-400 bg-slate-800 px-3 py-1 rounded-lg">DAG Topological Order</span>
            </div>

            {/* Timeline Steps Container */}
            <div className="relative pl-6 space-y-8 before:absolute before:left-3 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-800">
              {learningPathData?.learning_path.map((step) => {
                const isCompleted = step.status === 'COMPLETED';
                const isUnlocked = step.status === 'UNLOCKED';
                const isLocked = step.status === 'LOCKED';
                const isSelected = selectedTopicId === step.topic_id;

                return (
                  <div 
                    key={step.step_number}
                    onClick={() => !isLocked && setSelectedTopicId(step.topic_id)}
                    className={`relative flex items-start gap-4 p-4 rounded-xl transition border cursor-pointer ${
                      isSelected 
                        ? 'bg-indigo-950/40 border-indigo-500/50 shadow-lg shadow-indigo-500/10' 
                        : isLocked 
                          ? 'bg-slate-900/40 border-slate-800/50 opacity-60 cursor-not-allowed' 
                          : 'bg-slate-900 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {/* Node Icon Circle */}
                    <div className={`absolute -left-9 top-4 w-6 h-6 rounded-full flex items-center justify-center ring-4 ring-slate-950 text-xs font-bold transition-all ${
                      isCompleted 
                        ? 'bg-emerald-500 text-slate-950 ring-emerald-500/20' 
                        : isUnlocked 
                          ? 'bg-indigo-500 text-white ring-indigo-500/30 animate-pulse' 
                          : 'bg-slate-800 text-slate-500 ring-slate-800'
                    }`}>
                      {isCompleted ? <CheckCircle2 size={14} /> : isLocked ? <Lock size={12} /> : step.step_number}
                    </div>

                    {/* Step Main Info */}
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">{step.code}</span>
                        <h4 className="font-semibold text-white text-base">{step.title}</h4>
                        
                        {/* Status Badges */}
                        {isCompleted && (
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            Đã hoàn thành
                          </span>
                        )}
                        {isUnlocked && (
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center gap-1">
                            <Sparkles size={12} /> Bước tiếp theo (Mở khóa)
                          </span>
                        )}
                        {isLocked && (
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-400 border border-slate-700 flex items-center gap-1">
                            <Lock size={11} /> Đang khóa
                          </span>
                        )}
                      </div>

                      <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{step.reasoning}</p>
                    </div>

                    {/* Action Button */}
                    {isUnlocked && (
                      <button className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium px-3 py-2 rounded-lg flex items-center gap-1 transition shadow-md shadow-indigo-600/30">
                        <PlayCircle size={14} /> Vào bài học
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* CARD 3: THẺ HỌC LIỆU KHUYẾN NGHỊ (CONTENT RECOMMENDATION CARDS) */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Sparkles className="text-violet-400" size={20} /> Học liệu khuyến nghị dành riêng cho bạn
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">Dựa trên thuật toán Cosine Similarity tương thích với năng lực và định dạng ưa thích.</p>
              </div>
              <span className="text-xs text-slate-400 bg-slate-900 border border-slate-800 px-3 py-1 rounded-lg">
                Topic ID: {selectedTopicId}
              </span>
            </div>

            {/* Recommendation Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {recommendations.map((rec, index) => (
                <MaterialCard key={rec.material.id || index} recommendation={rec} />
              ))}
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}

// Sub-component: Recommended Material Card
function MaterialCard({ recommendation }) {
  const { material, match_percentage, recommendation_reason } = recommendation;
  
  const isVideo = material.material_type === 'VIDEO';
  const isReading = material.material_type === 'READING';
  const isExercise = material.material_type === 'EXERCISE';

  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 shadow-xl hover:shadow-indigo-500/10 group">
      <div>
        {/* Top Badges */}
        <div className="flex items-center justify-between mb-3">
          <span className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 ${
            isVideo 
              ? 'bg-red-500/10 text-red-400 border border-red-500/20' 
              : isReading 
                ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' 
                : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
          }`}>
            {isVideo ? <PlayCircle size={13} /> : <BookOpen size={13} />}
            {material.material_type}
          </span>

          {/* Match Score Percentage Badge */}
          <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-indigo-500/20 to-violet-500/20 text-indigo-300 border border-indigo-500/30">
            {match_percentage}% Match
          </span>
        </div>

        {/* Title */}
        <h4 className="font-semibold text-white text-base leading-snug group-hover:text-indigo-300 transition-colors line-clamp-2">
          {material.title}
        </h4>

        {/* Dynamic AI Reasoning Tag */}
        <p className="text-xs text-slate-400 mt-2 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/80 leading-relaxed">
          💡 <strong className="text-slate-300">Lý do gợi ý:</strong> {recommendation_reason}
        </p>
      </div>

      {/* Footer Info & Action Button */}
      <div className="mt-5 pt-4 border-t border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span className="flex items-center gap-1">
            <Star size={13} className="text-amber-400 fill-amber-400" /> Độ khó: {material.difficulty_level}/5.0
          </span>
          <span className="flex items-center gap-1">
            <Clock size={13} /> ~35 phút
          </span>
        </div>

        <button className="bg-slate-800 hover:bg-indigo-600 text-slate-200 hover:text-white px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1">
          Học ngay <ChevronRight size={13} />
        </button>
      </div>
    </div>
  );
}

// Sub-component: Navigation Item
function NavItem({ icon, label, active, badge }) {
  return (
    <a 
      href="#" 
      className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition ${
        active 
          ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20 shadow-sm' 
          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
      }`}
    >
      <div className="flex items-center gap-3">
        {icon}
        <span>{label}</span>
      </div>
      {badge && (
        <span className="bg-indigo-500/20 text-indigo-400 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase border border-indigo-500/30">
          {badge}
        </span>
      )}
    </a>
  );
}
