import React from 'react';

/**
 * QuizHistoryTab Component
 * Trang/Tab Lịch sử làm bài thi trắc nghiệm dành cho sinh viên.
 * Quản lý tiến trình:
 * - Bảng danh sách các lần thi đã thực hiện.
 * - Phân màu badge điểm số: Xanh (>=80%), Vàng (60-79%), Đỏ (<60%).
 * - Nút "Xem lại bài làm" tải lại chính xác trạng thái bài cũ kèm lời giải thích.
 * - Nút "Làm lại" để làm lại đề thi đó.
 */
export default function QuizHistoryTab({ historyList = [], onReviewAttempt, onRetakeQuiz, loading, onRefresh }) {

  // Định dạng thời gian hoàn thành (giây -> phút giây)
  const formatDuration = (seconds) => {
    if (!seconds) return "0 phút 0s";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m} phút ${s}s`;
  };

  // Trả về badge màu sắc chuẩn theo điểm số
  const getScoreBadge = (score) => {
    const s = parseFloat(score) || 0;
    if (s >= 80.0) {
      return (
        <span className="bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 px-3 py-1 rounded-xl text-xs font-black inline-flex items-center gap-1">
          <span>{s}%</span>
          <span className="text-[10px] bg-emerald-500/20 px-1.5 py-0.5 rounded font-bold">Giỏi</span>
        </span>
      );
    } else if (s >= 60.0) {
      return (
        <span className="bg-amber-500/15 text-amber-300 border border-amber-500/30 px-3 py-1 rounded-xl text-xs font-black inline-flex items-center gap-1">
          <span>{s}%</span>
          <span className="text-[10px] bg-amber-500/20 px-1.5 py-0.5 rounded font-bold">Khá / Đạt</span>
        </span>
      );
    } else {
      return (
        <span className="bg-rose-500/15 text-rose-300 border border-rose-500/30 px-3 py-1 rounded-xl text-xs font-black inline-flex items-center gap-1">
          <span>{s}%</span>
          <span className="text-[10px] bg-rose-500/20 px-1.5 py-0.5 rounded font-bold">Chưa đạt</span>
        </span>
      );
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl space-y-6">
      
      {/* HEADER STRIP */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="text-indigo-400 font-semibold text-xs tracking-wider uppercase flex items-center gap-1.5">
            <span>📜 Lịch sử Thi & Đánh giá Năng lực</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-white mt-1">
            Quản lý Lịch sử Bài Kiểm Tra Trắc Nghiệm 📊
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Theo dõi tiến trình điểm số, thời gian làm bài và bấm nút để mở lại đáp án & lời giải chi tiết của bất kỳ lần thi nào.
          </p>
        </div>

        {onRefresh && (
          <button
            onClick={onRefresh}
            className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-4 py-2.5 rounded-xl transition border border-slate-700 flex items-center gap-1.5 shrink-0"
          >
            <span>🔄 Cập nhật lịch sử</span>
          </button>
        )}
      </div>

      {/* LOADING STATE */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 space-y-3">
          <div className="animate-spin text-2xl">🌀</div>
          <p className="text-xs">Đang tải lịch sử thi của bạn...</p>
        </div>
      ) : historyList.length === 0 ? (
        /* EMPTY STATE */
        <div className="bg-slate-950 p-10 rounded-2xl border border-slate-800 text-center space-y-3">
          <span className="text-3xl">📝</span>
          <h3 className="text-base font-bold text-white">Chưa có lịch sử làm bài</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Bạn chưa thực hiện bài kiểm tra trắc nghiệm nào. Hãy truy cập Trung tâm Kiểm tra để bắt đầu làm bài đầu tiên!
          </p>
        </div>
      ) : (
        /* HISTORY TABLE CONTAINER */
        <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-950">
          <table className="w-full text-left border-collapse text-xs text-slate-300">
            <thead>
              <tr className="bg-slate-900/80 text-slate-400 font-bold border-b border-slate-800 uppercase text-[11px] tracking-wider">
                <th className="py-4 px-4 sm:px-6">Tên Bài kiểm tra / Chủ đề</th>
                <th className="py-4 px-4">Ngày giờ nộp bài</th>
                <th className="py-4 px-4 text-center">Điểm số</th>
                <th className="py-4 px-4 text-center">Số câu đúng</th>
                <th className="py-4 px-4">Thời gian</th>
                <th className="py-4 px-4 sm:px-6 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {historyList.map((item) => (
                <tr key={item.attempt_id} className="hover:bg-slate-900/60 transition group">
                  
                  {/* Cột 1: Tên bài thi */}
                  <td className="py-4 px-4 sm:px-6 font-bold text-white">
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                      <span>{item.quiz_title || `Bài kiểm tra #${item.quiz_id}`}</span>
                    </div>
                  </td>

                  {/* Cột 2: Ngày giờ nộp bài */}
                  <td className="py-4 px-4 text-slate-400 font-mono text-[11px]">
                    {item.created_at || "Vừa xong"}
                  </td>

                  {/* Cột 3: Điểm số với Badge màu */}
                  <td className="py-4 px-4 text-center">
                    {getScoreBadge(item.score)}
                  </td>

                  {/* Cột 4: Số câu đúng */}
                  <td className="py-4 px-4 text-center font-semibold text-slate-200">
                    <span className="text-indigo-400 font-bold">{item.correct_count}</span> / {item.total_questions} câu
                  </td>

                  {/* Cột 5: Thời gian hoàn thành */}
                  <td className="py-4 px-4 text-slate-300 font-medium">
                    ⏱️ {formatDuration(item.duration_seconds)}
                  </td>

                  {/* Cột 6: Thao tác (Xem lại bài làm & Làm lại) */}
                  <td className="py-4 px-4 sm:px-6 text-right">
                    <div className="flex justify-end items-center gap-2">
                      <button
                        onClick={() => onReviewAttempt && onReviewAttempt(item.attempt_id)}
                        className="bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/30 font-bold px-3.5 py-1.5 rounded-xl transition text-xs flex items-center gap-1 shadow-sm"
                        title="Xem lại toàn bộ đáp án và lời giải chi tiết"
                      >
                        <span>🔍 Xem lại bài làm</span>
                      </button>

                      <button
                        onClick={() => onRetakeQuiz && onRetakeQuiz(item.quiz_id)}
                        className="bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-medium px-3 py-1.5 rounded-xl transition text-xs border border-slate-700"
                        title="Làm lại bài thi này"
                      >
                        <span>🔄 Làm lại</span>
                      </button>
                    </div>
                  </td>

                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

    </div>
  );
}
