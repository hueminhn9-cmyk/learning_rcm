import React from 'react';

/**
 * QuizReviewScreen Component
 * Chế độ Xem lại Chi tiết Đáp án & Lời giải (Detailed Review Mode).
 * Tô màu trực quan:
 * - Chọn ĐÚNG: Viền xanh lá, Icon ✓
 * - Chọn SAI: Viền đỏ + Icon ✗ tại đáp án chọn sai; đồng thời viền xanh lá + Icon ✓ tại đáp án đúng thực sự.
 * - Hộp thoại "💡 Giải thích chi tiết" trình bày cặn kẽ bản chất kiến thức.
 */
export default function QuizReviewScreen({ attemptDetail, onClose, onRetake }) {
  if (!attemptDetail) return null;

  const {
    quiz_title,
    score,
    passed,
    correct_count,
    total_questions,
    duration_seconds,
    created_at,
    review_questions = []
  } = attemptDetail;

  const formatDuration = (seconds) => {
    if (!seconds) return "0 phút 0 giây";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}m ${s}s`;
  };

  return (
    <div className="fixed inset-0 bg-slate-950/90 backdrop-blur-md z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-4xl w-full shadow-2xl space-y-6 my-auto max-h-[92vh] flex flex-col overflow-hidden">
        
        {/* TOP BAR HEADER */}
        <div className="bg-slate-950/90 px-6 py-4 border-b border-slate-800 flex justify-between items-center shrink-0">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold font-mono text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded border border-indigo-500/20">
                LẦN THI CHUẨN ĐOÁN
              </span>
              <span className="text-xs text-slate-400">{created_at}</span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-white mt-1">
              🔍 Lời Giải Chi Tiết: {quiz_title || "Bài kiểm tra Đánh giá"}
            </h2>
          </div>

          <button
            onClick={onClose}
            className="w-9 h-9 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition font-bold"
          >
            ✕
          </button>
        </div>

        {/* SUMMARY METRIC STRIP */}
        <div className="px-6 shrink-0">
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 flex flex-wrap justify-between items-center gap-4 text-xs">
            <div className="flex items-center gap-3">
              <span className={`text-2xl font-black ${passed ? 'text-emerald-400' : 'text-rose-400'}`}>
                {score}%
              </span>
              <span className={`px-3 py-1 rounded-xl text-[11px] font-bold ${passed ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-300 border border-rose-500/20'}`}>
                {passed ? "✓ ĐẠT" : "✗ CẦN CẢI THIỆN"}
              </span>
            </div>

            <div className="flex items-center gap-6 text-slate-300">
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">Kết quả</span>
                <span className="font-bold text-white">{correct_count} / {total_questions} câu đúng</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px] uppercase font-semibold">Thời gian</span>
                <span className="font-bold text-white">{formatDuration(duration_seconds)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* QUESTIONS & DETAILED EXPLANATIONS LIST (SCROLLABLE AREA) */}
        <div className="px-6 overflow-y-auto space-y-6 flex-1 pr-3">
          {review_questions.map((q, idx) => {
            const isUserCorrect = q.is_correct;
            const optionsObj = q.options || {};
            const optionKeys = Object.keys(optionsObj);

            return (
              <div
                key={q.question_id || idx}
                className={`p-5 rounded-2xl border transition ${
                  isUserCorrect
                    ? 'bg-slate-950/70 border-emerald-500/30'
                    : 'bg-slate-950/70 border-rose-500/30'
                } space-y-4`}
              >
                {/* Question Header & Status Badge */}
                <div className="flex justify-between items-start gap-3 border-b border-slate-800/80 pb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-7 h-7 rounded-xl bg-slate-800 text-indigo-400 font-bold font-mono text-xs flex items-center justify-center border border-slate-700">
                      {idx + 1}
                    </span>
                    <span className="text-xs font-semibold text-slate-400">Câu hỏi {idx + 1} / {total_questions}</span>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-xl text-xs font-bold flex items-center gap-1.5 ${
                      isUserCorrect
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    }`}
                  >
                    {isUserCorrect ? "✓ Đúng (+10 điểm)" : "✗ Sai"}
                  </span>
                </div>

                {/* Question Text */}
                <p className="text-sm sm:text-base font-bold text-white leading-relaxed">
                  {q.question_text || q.content}
                </p>

                {/* Options Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 pt-1">
                  {optionKeys.map((key) => {
                    const optionVal = optionsObj[key];
                    const isSelected = (q.selected_answer === key);
                    const isCorrectOption = (q.correct_answer === key);

                    let cardStyle = "bg-slate-900 border-slate-800 text-slate-300";
                    let badgeStyle = "bg-slate-800 text-slate-400";
                    let iconSymbol = null;

                    if (isCorrectOption) {
                      // Đáp án đúng thực sự -> Luôn tô viền xanh lá
                      cardStyle = "bg-emerald-950/40 border-emerald-500 text-emerald-200 font-bold ring-1 ring-emerald-500/50 shadow-md shadow-emerald-500/10";
                      badgeStyle = "bg-emerald-500 text-slate-950 font-black";
                      iconSymbol = <span className="text-emerald-400 font-bold text-base">✓ (Đáp án đúng)</span>;
                    } else if (isSelected && !isUserCorrect) {
                      // Người dùng chọn phương án SAI -> Tô viền đỏ
                      cardStyle = "bg-rose-950/40 border-rose-500 text-rose-200 font-semibold ring-1 ring-rose-500/40";
                      badgeStyle = "bg-rose-500 text-white font-black";
                      iconSymbol = <span className="text-rose-400 font-bold text-base">✗ (Bạn đã chọn)</span>;
                    }

                    return (
                      <div
                        key={key}
                        className={`p-3 rounded-xl border flex items-center justify-between gap-3 text-xs transition ${cardStyle}`}
                      >
                        <div className="flex items-center gap-2.5">
                          <span className={`w-6 h-6 rounded-lg text-xs font-mono font-bold flex items-center justify-center shrink-0 ${badgeStyle}`}>
                            {key}
                          </span>
                          <span className="leading-snug">{optionVal}</span>
                        </div>

                        {iconSymbol && <div className="shrink-0">{iconSymbol}</div>}
                      </div>
                    );
                  })}
                </div>

                {/* DETAILED EXPLANATION BOX (HỘP THOẠI GIẢI THÍCH CHI TIẾT) */}
                <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1.5 text-xs text-slate-300 leading-relaxed shadow-inner">
                  <div className="flex items-center gap-1.5 text-amber-400 font-bold">
                    <span>💡 解 答 - Lời giải & Giải thích chi tiết (Pedagogical Explanation):</span>
                  </div>
                  <p className="text-slate-200 pl-1 border-l-2 border-amber-500/60 font-medium">
                    {q.explanation || "Đáp án đúng được xác định dựa trên nguyên lý sư phạm & chuẩn dữ liệu Python AI."}
                  </p>
                </div>

              </div>
            );
          })}
        </div>

        {/* BOTTOM FOOTER BUTTONS */}
        <div className="bg-slate-950/90 px-6 py-4 border-t border-slate-800 flex justify-between items-center gap-4 shrink-0">
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold px-5 py-2.5 rounded-xl transition text-xs border border-slate-700"
          >
            ← Quay lại
          </button>

          {onRetake && (
            <button
              onClick={onRetake}
              className="bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-bold px-6 py-2.5 rounded-xl transition shadow-lg text-xs"
            >
              🔄 Thử lại bài thi này
            </button>
          )}
        </div>

      </div>
    </div>
  );
}
