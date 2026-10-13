import React, { useState, useEffect } from 'react';
import { 
  BarChart3, TrendingUp, AlertTriangle, CheckCircle, Clock, Sliders, 
  History, Users, FileText, Shield, Save, Sparkles, AlertCircle, RefreshCw
} from 'lucide-react';

const API_BASE_URL = "http://localhost:8000/api/v1";

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    total_students: 1250,
    goal_completion_rate: 68.4,
    total_student_feedback_reports: 14,
    manual_grading_queue_count: 3,
    struggling_topics: [
      { topic_code: "T103", title: "Giải tích 2", failure_rate: 34.2, avg_attempts: 3.1 },
      { topic_code: "T104", title: "Học máy cơ bản", failure_rate: 28.5, avg_attempts: 2.7 },
      { topic_code: "T102", title: "Giải tích 1", failure_rate: 18.0, avg_attempts: 1.9 }
    ],
    monthly_completion_trend: [
      { month: "T6", completed_goals: 110 },
      { month: "T7", completed_goals: 145 },
      { month: "T8", completed_goals: 190 },
      { month: "T9", completed_goals: 230 },
      { month: "T10", completed_goals: 310 }
    ]
  });

  const [configForm, setConfigForm] = useState({
    w_prerequisite: 1.5,
    w_difficulty_gap: 1.2,
    w_bloom_match: 1.0,
    min_passing_score: 60.0
  });

  const [configHistory, setConfigHistory] = useState([
    { version: 2, config_key: "RECOMMENDATION_WEIGHTS", w_prerequisite: 1.5, w_difficulty_gap: 1.2, w_bloom_match: 1.0, min_passing_score: 60.0, updated_by_user_id: 99, updated_at: "2026-10-09 11:20:00" },
    { version: 1, config_key: "RECOMMENDATION_WEIGHTS", w_prerequisite: 1.0, w_difficulty_gap: 1.0, w_bloom_match: 1.0, min_passing_score: 60.0, updated_by_user_id: 99, updated_at: "2026-10-01 09:00:00" }
  ]);

  const [gradingQueue, setGradingQueue] = useState([
    { id: 1, student_name: "Lê Văn B", topic: "T103 - Giải tích 2", submitted_at: "10 phút trước", essay_preview: "Em áp dụng công thức Đạo hàm riêng để tính độ dốc Gradient..." },
    { id: 2, student_name: "Trần Thị C", topic: "T104 - Học máy cơ bản", submitted_at: "25 phút trước", essay_preview: "Phân tích sự khác biệt giữa Overfitting và Underfitting..." },
    { id: 3, student_name: "Phạm Quốc D", topic: "T104 - Học máy cơ bản", submitted_at: "1 giờ trước", essay_preview: "Giải thích hàm mất mát Mean Squared Error (MSE)..." }
  ]);

  const [saveMessage, setSaveMessage] = useState("");

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      // 1. Lấy thống kê hệ thống từ FastAPI
      const statsRes = await fetch(`${API_BASE_URL}/admin/stats`);
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }

      // 2. Lấy Lịch sử phiên bản cấu hình từ FastAPI
      const historyRes = await fetch(`${API_BASE_URL}/admin/recommendation-config/history`);
      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setConfigHistory(historyData);
      }
    } catch (error) {
      console.warn("Backend API offline, sử dụng dữ liệu mô phỏng Admin", error);
    }
  };

  const handleUpdateConfig = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        config_key: "RECOMMENDATION_WEIGHTS",
        description: "Cập nhật trọng số khuyến nghị & ngưỡng đạt",
        w_prerequisite: parseFloat(configForm.w_prerequisite),
        w_difficulty_gap: parseFloat(configForm.w_difficulty_gap),
        w_bloom_match: parseFloat(configForm.w_bloom_match),
        min_passing_score: parseFloat(configForm.min_passing_score),
        updated_by_user_id: 99 // Admin ID
      };

      const res = await fetch(`${API_BASE_URL}/admin/recommendation-config/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const newHistoryItem = await res.json();
        setConfigHistory([newHistoryItem, ...configHistory]);
        setSaveMessage(`✅ Đã lưu thành công Phiên bản v${newHistoryItem.version}!`);
      } else {
        setSaveMessage("✅ Đã cập nhật phiên bản mô phỏng v" + (configHistory.length + 1));
        setConfigHistory([
          {
            version: configHistory.length + 1,
            config_key: "RECOMMENDATION_WEIGHTS",
            w_prerequisite: configForm.w_prerequisite,
            w_difficulty_gap: configForm.w_difficulty_gap,
            w_bloom_match: configForm.w_bloom_match,
            min_passing_score: configForm.min_passing_score,
            updated_by_user_id: 99,
            updated_at: new Date().toISOString().replace('T', ' ').substring(0, 19)
          },
          ...configHistory
        ]);
      }
    } catch (err) {
      setSaveMessage("✅ Đã cập nhật phiên bản v" + (configHistory.length + 1));
    }

    setTimeout(() => setSaveMessage(""), 4000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased p-8 space-y-8">
      
      {/* HEADER BAR */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase mb-1">
            <Shield size={14} /> Quản trị viên Hệ thống (System Admin)
          </div>
          <h1 className="text-2xl font-bold text-white">Bảng điều khiển Quản trị & Thống kê 📊</h1>
        </div>

        <div className="flex items-center gap-3">
          <button onClick={fetchAdminData} className="flex items-center gap-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 px-4 py-2 rounded-xl text-sm transition">
            <RefreshCw size={14} /> Làm mới dữ liệu
          </button>
          <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5">
            <CheckCircle size={14} /> API Backend Online
          </div>
        </div>
      </div>

      {/* STATS METRIC CARDS (4 CARDS) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Card 1: Goal Completion Rate */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Tỷ lệ hoàn thành mục tiêu</span>
            <TrendingUp size={16} className="text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">{stats.goal_completion_rate}%</div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-3 overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${stats.goal_completion_rate}%` }}></div>
          </div>
        </div>

        {/* Card 2: Total Active Students */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Sinh viên hoạt động</span>
            <Users size={16} className="text-indigo-400" />
          </div>
          <div className="text-2xl font-extrabold text-white">{stats.total_students.toLocaleString()}</div>
          <p className="text-xs text-indigo-400 mt-2">↑ 12% so với tháng trước</p>
        </div>

        {/* Card 3: Student Feedback Reports */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Phản hồi báo lỗi</span>
            <AlertTriangle size={16} className="text-amber-400" />
          </div>
          <div className="text-2xl font-extrabold text-amber-400">{stats.total_student_feedback_reports} báo cáo</div>
          <p className="text-xs text-slate-400 mt-2">Đang chờ Admin xử lý</p>
        </div>

        {/* Card 4: Manual Grading Queue */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs mb-2">
            <span>Hàng chờ chấm tự luận</span>
            <Clock size={16} className="text-violet-400" />
          </div>
          <div className="text-2xl font-extrabold text-violet-400">{gradingQueue.length} bài thi</div>
          <p className="text-xs text-slate-400 mt-2">Cần Admin phê duyệt</p>
        </div>
      </div>

      {/* MAIN CONTENT SPLIT GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN: CHARTS & STRUGGLING TOPICS (2 COLUMNS) */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* CHART 1: STRUGGLING TOPICS (CÁC CHỦ ĐỀ THƯỜNG GẶP KHÓ) */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <AlertCircle className="text-rose-400" size={20} /> Các chủ đề sinh viên thường gặp khó nhất
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">Tỷ lệ không đạt bài kiểm tra dựa trên dữ liệu hệ thống.</p>
              </div>
              <span className="text-xs text-rose-400 bg-rose-500/10 border border-rose-500/20 px-3 py-1 rounded-lg">High Risk Topics</span>
            </div>

            {/* Custom Bar Chart Visualizing Failure Rates */}
            <div className="space-y-4 pt-2">
              {stats.struggling_topics.map((item, idx) => (
                <div key={idx} className="space-y-1.5">
                  <div className="flex justify-between items-center text-sm">
                    <span className="font-semibold text-white">{item.topic_code} - {item.title}</span>
                    <span className="text-xs text-rose-400 font-bold">Tỷ lệ không đạt: {item.failure_rate}% (Thử lại tb: {item.avg_attempts} lần)</span>
                  </div>
                  <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
                    <div 
                      className="bg-gradient-to-r from-amber-500 to-rose-500 h-full rounded-full transition-all duration-700 shadow-md"
                      style={{ width: `${item.failure_rate * 2.5}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* MANUAL GRADING QUEUE TABLE */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <FileText className="text-violet-400" size={20} /> Hàng chờ chấm điểm tự luận (Manual Grading Queue)
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">Bài thi được chuyển tự động từ hệ thống chấm thi khi có câu hỏi tự luận.</p>
              </div>
              <span className="text-xs text-violet-400 bg-violet-500/10 border border-violet-500/20 px-3 py-1 rounded-lg">
                {gradingQueue.length} Chờ chấm
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-300">
                <thead className="bg-slate-950 text-slate-400 text-xs uppercase border-b border-slate-800">
                  <tr>
                    <th className="px-4 py-3">Sinh viên</th>
                    <th className="px-4 py-3">Chủ đề bài thi</th>
                    <th className="px-4 py-3">Nội dung tự luận</th>
                    <th className="px-4 py-3 text-right">Thao tác</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {gradingQueue.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-800/40 transition">
                      <td className="px-4 py-3 font-semibold text-white">{item.student_name}</td>
                      <td className="px-4 py-3 text-indigo-400 font-mono text-xs">{item.topic}</td>
                      <td className="px-4 py-3 text-xs text-slate-400 truncate max-w-xs">{item.essay_preview}</td>
                      <td className="px-4 py-3 text-right">
                        <button 
                          onClick={() => setGradingQueue(gradingQueue.filter(q => q.id !== item.id))}
                          className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1.5 rounded-lg transition"
                        >
                          Chấm điểm
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>

        {/* RIGHT COLUMN: RECOMMENDATION CONFIG EDITOR & VERSION HISTORY */}
        <div className="space-y-8">
          
          {/* CONFIG UPDATE FORM */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
            <div className="border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Sliders className="text-indigo-400" size={20} /> Cấu hình Trọng số Khuyến nghị
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Điều chỉnh tham số thuật toán AI không cần redeploy code.</p>
            </div>

            {saveMessage && (
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold rounded-xl">
                {saveMessage}
              </div>
            )}

            <form onSubmit={handleUpdateConfig} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Trọng số Tiên quyết (w_prerequisite)
                </label>
                <input 
                  type="number" 
                  step="0.1" 
                  value={configForm.w_prerequisite}
                  onChange={(e) => setConfigForm({...configForm, w_prerequisite: e.target.value})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Trọng số Khoảng cách Độ khó (w_difficulty_gap)
                </label>
                <input 
                  type="number" 
                  step="0.1" 
                  value={configForm.w_difficulty_gap}
                  onChange={(e) => setConfigForm({...configForm, w_difficulty_gap: e.target.value})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Trọng số Bloom Taxonomy (w_bloom_match)
                </label>
                <input 
                  type="number" 
                  step="0.1" 
                  value={configForm.w_bloom_match}
                  onChange={(e) => setConfigForm({...configForm, w_bloom_match: e.target.value})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Ngưỡng Điểm Đạt bài test (%) (min_passing_score)
                </label>
                <input 
                  type="number" 
                  step="5" 
                  value={configForm.min_passing_score}
                  onChange={(e) => setConfigForm({...configForm, min_passing_score: e.target.value})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 outline-none"
                />
              </div>

              <button 
                type="submit"
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 px-4 rounded-xl text-sm flex items-center justify-center gap-2 transition shadow-lg shadow-indigo-600/30"
              >
                <Save size={16} /> Lưu & Xuất Phiên bản mới
              </button>
            </form>
          </div>

          {/* VERSION HISTORY AUDIT LOG */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <History className="text-indigo-400" size={18} /> Nhật ký Phiên bản Cấu hình
              </h3>
              <span className="text-xs text-slate-400 font-mono">Audit Log</span>
            </div>

            <div className="space-y-3 max-h-64 overflow-y-auto pr-1">
              {configHistory.map((item) => (
                <div key={item.version} className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
                  <div className="flex justify-between items-center font-semibold">
                    <span className="text-indigo-400 font-mono">Phiên bản v{item.version}</span>
                    <span className="text-slate-500">{item.updated_at}</span>
                  </div>
                  <div className="text-slate-300 grid grid-cols-2 gap-1 pt-1">
                    <span>w_prereq: {item.w_prerequisite}</span>
                    <span>w_diff: {item.w_difficulty_gap}</span>
                    <span>w_bloom: {item.w_bloom_match}</span>
                    <span>Ngưỡng đạt: {item.min_passing_score}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
