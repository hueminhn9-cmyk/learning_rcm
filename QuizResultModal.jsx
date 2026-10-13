import React from 'react';

/**
 * QuizResultModal Component
 * Màn hình kết quả tổng quan tức thì ngay sau khi sinh viên nộp bài kiểm tra.
 * Hiển thị điểm số, số câu đúng, trạng thái Đạt/Cần cải thiện và các nút thao tác.
 */
export default function QuizResultModal({ result, onReviewDetails, onRetake, onClose }) {
  if (!result) return null;

  const scorePercentage = result.score || 0;
  const passed = result.passed ?? (scorePercentage >= 60);

  const formatDuration = (seconds) => {
    if (!seconds) return "0 phút 0 giây";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m} phút ${s} giây`;
  };

  return (
    <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-2xl space-y-6 text-center animate-in fade-in zoom-in duration-200">
        
        {/* Header Icon & Title */}
        <div className="space-y-2">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-violet-500/20 border border-indigo-500/30 text-3xl shadow-inner">
            {passed ? "🎉" : "💪"}
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
            {passed ? "Chúc mừng! Bạn đã hoàn thành bài thi" : "Kết quả Bài kiểm tra"}
          </h2>
          <p className="text-xs text-slate-400 font-medium">
            {result.quiz_title || "Bài kiểm tra Đánh giá Kiến thức"}
          </p>
        </div>

        {/* Score & Pass/Fail Badge Banner */}
        <div className={`p-6 rounded-2xl border ${passed ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-400' : 'bg-rose-950/30 border-rose-500/30 text-rose-400'} space-y-2`}>
          <div className="text-4xl sm:text-5xl font-black tracking-tight">
            {scorePercentage}%
          </div>
          <div className="flex items-center justify-center gap-2">
            <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${passed ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'}`}>
              {passed ? "✓ ĐẠT (PASSED)" : "✗ CẦN CẢI THIỆN (FAILED)"}
            </span>
          </div>
        </div>

        {/* Metric Cards Grid */}
        <div className="grid grid-cols-2 gap-3 text-left">
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-1">
            <span className="text-[11px] text-slate-400 font-semibold block">Số câu trả lời đúng</span>
            <div className="text-lg font-bold text-white flex items-center gap-1.5">
              <span className="text-indigo-400 font-extrabold">{result.correct_count}</span>
              <span className="text-slate-500 text-xs">/ {result.total_questions} câu</span>
            </div>
          </div>

          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-1">
            <span className="text-[11px] text-slate-400 font-semibold block">Thời gian làm bài</span>
            <div className="text-sm font-bold text-slate-200">
              {formatDuration(result.duration_seconds)}
            </div>
          </div>
        </div>

        {/* Primary & Secondary Action Buttons */}
        <div className="space-y-3 pt-2">
          <button
            onClick={onReviewDetails}
            className="w-full bg-gradient-to-r from-indigo-600 via-violet-600 to-purple-600 hover:from-indigo-500 hover:to-violet-500 text-white font-bold py-3.5 px-5 rounded-2xl transition shadow-xl shadow-indigo-600/30 text-xs sm:text-sm flex items-center justify-center gap-2 transform active:scale-95"
          >
            <span>🔍 Xem chi tiết đáp án & Lời giải</span>
            <span>→</span>
          </button>

          <div className="flex gap-3">
            <button
              onClick={onRetake}
              className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-3 px-4 rounded-2xl transition text-xs border border-slate-700 active:scale-95"
            >
              🔄 Làm lại bài thi
            </button>
            <button
              onClick={onClose}
              className="bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 font-semibold px-5 py-3 rounded-2xl transition text-xs border border-slate-700"
            >
              Đóng
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
