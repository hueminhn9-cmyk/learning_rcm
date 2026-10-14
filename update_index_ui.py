# -*- coding: utf-8 -*-
"""
Script to rebuild index.html with the 5 Dedicated Workspaces and 3-Tier Search Recommendation Modal
"""

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Locate where StudentDashboardApp starts
start_marker = "    function StudentDashboardApp() {"
end_marker = "    ReactDOM.createRoot(document.getElementById('root')).render(<StudentDashboardApp />);"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("[ERROR] Could not find markers in index.html")
    sys.exit(1)

new_student_app = r'''    function StudentDashboardApp() {
      // 1. THEME & EYE-CARE MODE (Default: Light Dịu Mắt)
      const [theme, setTheme] = useState(() => localStorage.getItem('aegis_theme') || 'light');

      useEffect(() => {
        if (theme === 'dark') {
          document.documentElement.classList.remove('theme-light');
          document.documentElement.classList.add('dark');
          document.body.classList.remove('theme-light');
          document.body.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
          document.documentElement.classList.add('theme-light');
          document.body.classList.remove('dark');
          document.body.classList.add('theme-light');
        }
        localStorage.setItem('aegis_theme', theme);
      }, [theme]);

      const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
      };

      // 2. CORE WORKSPACE NAVIGATION
      // Workspaces: "COCKPIT" | "LEARNING_PATH" | "EXAM_ARENA" | "ERROR_VAULT" | "AI_STUDY_ROOM"
      const [activeWorkspace, setActiveWorkspace] = useState("COCKPIT");

      // 3. DYNAMIC MULTI-SUBJECT CATALOG
      const [subjectsList, setSubjectsList] = useState([]);
      const [activeSubject, setActiveSubject] = useState(null);
      const [targetScore, setTargetScore] = useState(9.0);
      const [searchQuery, setSearchQuery] = useState("");
      const [isSearchLoading, setIsSearchLoading] = useState(false);

      // 4. 3-TIER RECOMMENDATION MODAL
      const [isSearchModalOpen, setIsSearchModalOpen] = useState(false);
      const [searchModalData, setSearchModalData] = useState(null);

      // 5. HIGH-SCORE COCKPIT DATA
      const [scorePrediction, setScorePrediction] = useState(null);
      const [isPredictionLoading, setIsPredictionLoading] = useState(false);

      // Pomodoro Timer (25 mins)
      const [pomodoroSeconds, setPomodoroSeconds] = useState(1500);
      const [isPomodoroRunning, setIsPomodoroRunning] = useState(false);

      useEffect(() => {
        let interval = null;
        if (isPomodoroRunning && pomodoroSeconds > 0) {
          interval = setInterval(() => setPomodoroSeconds(p => p - 1), 1000);
        } else if (pomodoroSeconds === 0 && isPomodoroRunning) {
          setIsPomodoroRunning(false);
          alert("⏰ Hết 25 phút tập trung! Hãy nghỉ giải lao 5 phút nhé.");
          setPomodoroSeconds(1500);
        }
        return () => clearInterval(interval);
      }, [isPomodoroRunning, pomodoroSeconds]);

      const formatPomodoro = (secs) => {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
      };

      // 6. LEARNING PATH (DAG) DATA
      const [learningPathData, setLearningPathData] = useState(null);
      const [selectedTopicId, setSelectedTopicId] = useState(null);
      const [topicMaterials, setTopicMaterials] = useState([]);
      const [topicTab, setTopicTab] = useState("WEB_DOCS"); // WEB_DOCS | VIDEOS | EXERCISE
      const [masteredTopicIds, setMasteredTopicIds] = useState([101, 102]);

      // 7. EXAM ARENA DATA
      const [examArenaTab, setExamArenaTab] = useState("TOPIC_DRILL"); // TOPIC_DRILL | MOCK_EXAM | HISTORY
      const [selectedDrillTopic, setSelectedDrillTopic] = useState(null);
      const [drillDifficulty, setDrillDifficulty] = useState(3.0);
      const [activeQuiz, setActiveQuiz] = useState(null);
      const [quizAnswers, setQuizAnswers] = useState({});
      const [quizTimer, setQuizTimer] = useState(900);
      const [quizResult, setQuizResult] = useState(null);
      const [instantResultModal, setInstantResultModal] = useState(null);
      const [activeReviewDetailModal, setActiveReviewDetailModal] = useState(null);
      const [quizHistoryList, setQuizHistoryList] = useState([]);
      const [isHistoryLoading, setIsHistoryLoading] = useState(false);

      // Quiz Timer Countdown
      useEffect(() => {
        let timer = null;
        if (activeQuiz && quizTimer > 0) {
          timer = setInterval(() => {
            setQuizTimer(prev => {
              if (prev <= 1) {
                clearInterval(timer);
                handleSubmitQuiz();
                return 0;
              }
              return prev - 1;
            });
          }, 1000);
        }
        return () => clearInterval(timer);
      }, [activeQuiz, quizTimer]);

      // 8. ERROR VAULT (SỔ TAY BẪY SAI)
      const [errorVaultList, setErrorVaultList] = useState([]);
      const [isVaultLoading, setIsVaultLoading] = useState(false);

      // 9. AI STUDY ROOM DATA
      const [studyRoomTab, setStudyRoomTab] = useState("AI_TUTOR"); // AI_TUTOR | FEYNMAN | CRAMMING | FLASHCARDS
      const [chatMessages, setChatMessages] = useState([
        {
          id: 1,
          role: "assistant",
          content: "### 👋 Chào bạn! Mình là Gia sư AI (Aegis AI Master Tutor)\nĐược kết nối trực tiếp với **Google Search Grounding & Tài liệu Học thuật Chuẩn**.\n\nBạn có thể hỏi bất kỳ môn học nào trong ngành Trí tuệ Nhân tạo: **Toán AI, Deep Learning, SQL, Lập trình Python, Cấu trúc Dữ liệu & Giải thuật**!\n\nMình sẽ phân tích cặn kẽ bản chất toán học, code mẫu, các bẫy đề thi và trích dẫn trực tiếp nguồn chính thống cho bạn.",
          suggested_followups: [
            "Cách phân biệt loc và iloc trong Pandas?",
            "Bản chất hình học của Ma trận & Vector riêng (Eigenvalue)?",
            "Thuật toán tìm kiếm A* và hàm Heuristic trong AI?",
            "Cơ chế Self-Attention trong mô hình Transformer hoạt động thế nào?",
            "Cách tối ưu hóa chỉ mục B-Tree trong truy vấn SQL?"
          ],
          sources: [
            { title: "Google Developers & Research AI", url: "https://developers.google.com/", snippet: "Tài liệu kỹ thuật AI chính thức từ Google Research." },
            { title: "Python 3 Official Docs", url: "https://docs.python.org/3/tutorial/", snippet: "Tài liệu ngôn ngữ lập trình Python chuẩn mực." }
          ]
        }
      ]);
      const [chatInput, setChatInput] = useState("");
      const [isAiThinking, setIsAiThinking] = useState(false);
      const [copiedCodeId, setCopiedCodeId] = useState(null);

      // Feynman Room States
      const [feynmanConcept, setFeynmanConcept] = useState("Gradient Descent");
      const [feynmanText, setFeynmanText] = useState("");
      const [feynmanEvaluation, setFeynmanEvaluation] = useState(null);
      const [isEvaluatingFeynman, setIsEvaluatingFeynman] = useState(false);

      // 48h Cramming Cheat Sheet
      const [cheatSheetData, setCheatSheetData] = useState(null);
      const [cheatSheetTopicId, setCheatSheetTopicId] = useState(103);

      // Flashcards SM-2
      const [flashcardsList, setFlashcardsList] = useState([]);
      const [cardIdx, setCardIdx] = useState(0);
      const [isCardFlipped, setIsCardFlipped] = useState(false);

      // User Stats
      const [userProfile, setUserProfile] = useState({
        full_name: "Nguyễn Văn A",
        streak_days: 5,
        exp_points: 350
      });

      // ============================================================
      // INITIAL DATA FETCHING ON MOUNT
      // ============================================================
      useEffect(() => {
        fetchSubjectsCatalog();
        fetchScorePrediction();
        fetchErrorVault();
        fetchFlashcards();
        fetchCrammingCheatSheet(103);
      }, []);

      const fetchSubjectsCatalog = async () => {
        try {
          const res = await fetch(`${API_BASE_URL}/subjects`);
          if (res.ok) {
            const data = await res.json();
            setSubjectsList(data);
            if (data.length > 0) {
              const defaultSub = data.find(s => s.code === "AI_PYTHON") || data[0];
              setActiveSubject(defaultSub);
              if (defaultSub.topics && defaultSub.topics.length > 0) {
                const firstTopic = defaultSub.topics[0];
                setSelectedTopicId(firstTopic.id);
                setSelectedDrillTopic(firstTopic.id);
                fetchLearningPath(defaultSub, firstTopic.id);
                fetchTopicMaterials(firstTopic.id);
              }
            }
          }
        } catch (e) {
          console.warn("Lỗi tải danh mục môn học:", e);
        }
      };

      const fetchLearningPath = async (subject = activeSubject, targetTid = selectedTopicId) => {
        if (!subject || !subject.topics || subject.topics.length === 0) return;
        const allTopics = subject.topics.map(t => ({
          id: t.id,
          code: t.code,
          title: t.title,
          description: t.description
        }));
        const targetId = targetTid || subject.topics[subject.topics.length - 1].id;

        // Xây dựng DAG tuần tự
        const prereqs = [];
        for (let i = 1; i < subject.topics.length; i++) {
          prereqs.push({
            topic_id: subject.topics[i].id,
            prerequisite_topic_id: subject.topics[i - 1].id,
            dependency_type: "STRICT"
          });
        }

        try {
          const res = await fetch(`${API_BASE_URL}/learning-path/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: 1,
              target_topic_id: targetId,
              mastered_topic_ids: masteredTopicIds,
              all_topics: allTopics,
              prerequisites: prereqs
            })
          });
          if (res.ok) {
            const data = await res.json();
            setLearningPathData(data);
          }
        } catch (e) {
          console.warn("Lỗi sinh lộ trình DAG:", e);
        }
      };

      const fetchTopicMaterials = async (topicId) => {
        if (!topicId) return;
        try {
          const res = await fetch(`${API_BASE_URL}/materials/search?topic_id=${topicId}`);
          if (res.ok) {
            const data = await res.json();
            setTopicMaterials(data);
          }
        } catch (e) {
          console.warn("Lỗi tải tài liệu topic:", e);
        }
      };

      const fetchScorePrediction = async () => {
        setIsPredictionLoading(true);
        try {
          const res = await fetch(`${API_BASE_URL}/analytics/score-prediction/1`);
          if (res.ok) {
            const data = await res.json();
            setScorePrediction(data);
          }
        } catch (e) {
          console.warn("Lỗi tải dự báo điểm:", e);
        } finally {
          setIsPredictionLoading(false);
        }
      };

      const fetchErrorVault = async () => {
        setIsVaultLoading(true);
        try {
          const res = await fetch(`${API_BASE_URL}/quiz/errors/1`);
          if (res.ok) {
            const data = await res.json();
            setErrorVaultList(data);
          }
        } catch (e) {
          console.warn("Lỗi tải sổ tay bẫy sai:", e);
        } finally {
          setIsVaultLoading(false);
        }
      };

      const fetchFlashcards = async (topicId = 0) => {
        try {
          const res = await fetch(`${API_BASE_URL}/flashcards/deck?topic_id=${topicId}`);
          if (res.ok) {
            const data = await res.json();
            setFlashcardsList(data);
            setCardIdx(0);
            setIsCardFlipped(false);
          }
        } catch (e) {
          console.warn("Lỗi tải flashcards:", e);
        }
      };

      const fetchCrammingCheatSheet = async (topicId = 103) => {
        try {
          const res = await fetch(`${API_BASE_URL}/cramming/cheat-sheet/${topicId}`);
          if (res.ok) {
            const data = await res.json();
            setCheatSheetData(data);
            setCheatSheetTopicId(topicId);
          }
        } catch (e) {
          console.warn("Lỗi tải cheat sheet:", e);
        }
      };

      const fetchQuizHistory = async () => {
        setIsHistoryLoading(true);
        try {
          const res = await fetch(`${API_BASE_URL}/quiz/history/user/1`);
          if (res.ok) {
            const data = await res.json();
            setQuizHistoryList(data);
          }
        } catch (e) {
          console.warn("Lỗi tải lịch sử thi:", e);
        } finally {
          setIsHistoryLoading(false);
        }
      };

      // ============================================================
      // HANDLERS: SUBJECT SWITCHING & 3-TIER SEARCH
      // ============================================================
      const handleSwitchSubject = (subjectId) => {
        const found = subjectsList.find(s => s.id === parseInt(subjectId));
        if (found) {
          setActiveSubject(found);
          const firstTid = (found.topics && found.topics.length > 0) ? found.topics[0].id : 101;
          setSelectedTopicId(firstTid);
          setSelectedDrillTopic(firstTid);
          fetchLearningPath(found, firstTid);
          fetchTopicMaterials(firstTid);
          fetchFlashcards(firstTid);
          fetchCrammingCheatSheet(firstTid);
        }
      };

      const handleExecute3TierSearch = async (queryText = searchQuery, score = targetScore) => {
        setIsSearchLoading(true);
        try {
          const res = await fetch(`${API_BASE_URL}/subjects/search?q=${encodeURIComponent(queryText || "")}&target_score=${score}`);
          if (res.ok) {
            const data = await res.json();
            setSearchModalData(data);
            setIsSearchModalOpen(true);
          }
        } catch (e) {
          alert("Lỗi tìm kiếm môn học!");
        } finally {
          setIsSearchLoading(false);
        }
      };

      const handleApplySubjectFromSearch = (matchedSubject) => {
        if (!matchedSubject) return;
        setIsSearchModalOpen(false);
        handleSwitchSubject(matchedSubject.id);
        setActiveWorkspace("LEARNING_PATH");
      };

      // ============================================================
      // HANDLERS: QUIZZES & EXAMS
      // ============================================================
      const handleStartTopicDrill = async (topicId, diff = 3.0) => {
        const tid = topicId || selectedTopicId || 101;
        try {
          const res = await fetch(`${API_BASE_URL}/question-bank/practice?topic_id=${tid}&count=15&difficulty_level=${diff}`);
          if (res.ok) {
            const data = await res.json();
            startQuizSession({
              ...data,
              title: `Topic Drill: ${activeSubject?.title || 'Luyện tập'} (15 câu)`,
              time_limit_minutes: 20
            });
          }
        } catch (e) {
          alert("Lỗi tải đề Topic Drill!");
        }
      };

      const handleStartMockExam = async () => {
        try {
          const res = await fetch(`${API_BASE_URL}/question-bank/random?count=25`);
          if (res.ok) {
            const data = await res.json();
            startQuizSession({
              ...data,
              title: `Đề Thi Thử Chuẩn Hóa Phòng Thi Thật (Mock Exam Simulator) - Môn ${activeSubject?.title || 'AI'}`,
              time_limit_minutes: 50,
              is_mock_exam: true
            });
          }
        } catch (e) {
          alert("Lỗi tải Đề thi thử mô phỏng!");
        }
      };

      const handleStartErrorClearance = async () => {
        try {
          const res = await fetch(`${API_BASE_URL}/quiz/error-clearance/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: 1 })
          });
          if (res.ok) {
            const data = await res.json();
            startQuizSession(data);
          }
        } catch (e) {
          alert("Lỗi sinh đề phục thù xoá lỗi sai!");
        }
      };

      const startQuizSession = (quizData) => {
        setActiveQuiz(quizData);
        setQuizAnswers({});
        setQuizTimer((quizData.time_limit_minutes || 20) * 60);
        setQuizResult(null);
      };

      const handleSubmitQuiz = async () => {
        if (!activeQuiz) return;
        const answersList = Object.keys(quizAnswers).map(qid => ({
          question_id: parseInt(qid),
          selected_answer: quizAnswers[qid]
        }));
        const durationSecs = ((activeQuiz.time_limit_minutes || 20) * 60) - quizTimer;

        try {
          const res = await fetch(`${API_BASE_URL}/quiz/submit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: 1,
              quiz_id: activeQuiz.id || 201,
              quiz_title: activeQuiz.title || "Bài kiểm tra Đánh giá Năng lực",
              answers: answersList,
              duration_seconds: durationSecs > 0 ? durationSecs : 180
            })
          });

          let resultData = null;
          if (res.ok) {
            resultData = await res.json();
          } else {
            // Fallback scoring
            let correct = 0;
            const reviewQs = (activeQuiz.questions || []).map(q => {
              const sel = quizAnswers[q.id] || "Chưa chọn";
              const isCorr = (sel.toUpperCase() === (q.correct_answer || "A").toUpperCase());
              if (isCorr) correct++;
              return {
                question_id: q.id,
                question_text: q.content,
                options: q.options || {},
                selected_answer: sel,
                correct_answer: q.correct_answer || "A",
                is_correct: isCorr,
                explanation: q.explanation || "Giải thích đáp án chi tiết."
              };
            });
            const sc = Math.round((correct / (activeQuiz.questions?.length || 1)) * 100);
            resultData = {
              attempt_id: Date.now(),
              quiz_id: activeQuiz.id || 201,
              quiz_title: activeQuiz.title || "Bài kiểm tra",
              score: sc,
              total_questions: activeQuiz.questions?.length || 1,
              correct_count: correct,
              passed: sc >= 60,
              duration_seconds: durationSecs,
              created_at: "Vừa xong",
              review_questions: reviewQs
            };
          }

          setActiveQuiz(null);
          setInstantResultModal(resultData);
          fetchScorePrediction();
          fetchErrorVault();
          fetchQuizHistory();

          if (resultData && resultData.score >= 70 && selectedTopicId) {
            setMasteredTopicIds(prev => Array.from(new Set([...prev, selectedTopicId])));
            fetchLearningPath(activeSubject, selectedTopicId);
          }
        } catch (e) {
          alert("Lỗi nộp bài thi!");
        }
      };

      // ============================================================
      // HANDLERS: AI TUTOR WITH GOOGLE GROUNDING
      // ============================================================
      const handleSendAiChatMessage = async (customMsg = null) => {
        const text = (customMsg || chatInput).trim();
        if (!text || isAiThinking) return;

        const userMsg = { id: Date.now(), role: "user", content: text };
        setChatMessages(prev => [...prev, userMsg]);
        setChatInput("");
        setIsAiThinking(true);

        try {
          const res = await fetch(`${API_BASE_URL}/ai/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: 1,
              topic_id: selectedTopicId || 101,
              message: text,
              history: chatMessages.slice(-6).map(m => ({ role: m.role, content: m.content }))
            })
          });

          if (res.ok) {
            const data = await res.json();
            const aiMsg = {
              id: Date.now() + 1,
              role: "assistant",
              content: data.reply,
              suggested_followups: data.suggested_followups || [],
              model_used: data.model_used,
              sources: data.sources || []
            };
            setChatMessages(prev => [...prev, aiMsg]);
          }
        } catch (e) {
          console.warn("AI Chat error:", e);
        } finally {
          setIsAiThinking(false);
        }
      };

      // Evaluate Feynman Explanation
      const handleEvaluateFeynman = async () => {
        if (!feynmanText.trim()) {
          alert("Vui lòng nhập lời giải thích của bạn để AI đánh giá!");
          return;
        }
        setIsEvaluatingFeynman(true);
        try {
          const res = await fetch(`${API_BASE_URL}/learning/feynman/reflect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: 1,
              topic_id: selectedTopicId || 101,
              concept_explained: feynmanConcept,
              student_explanation: feynmanText
            })
          });
          if (res.ok) {
            const data = await res.json();
            setFeynmanEvaluation(data);
          }
        } catch (e) {
          alert("Lỗi chấm điểm phòng Feynman!");
        } finally {
          setIsEvaluatingFeynman(false);
        }
      };

      // Format Markdown Helper
      const renderFormattedAiContent = (text) => {
        if (!text) return null;
        const parts = text.split(/(```[\s\S]*?```)/g);
        return parts.map((part, index) => {
          if (part.startsWith('```') && part.endsWith('```')) {
            const lines = part.slice(3, -3).trim().split('\n');
            const lang = lines[0].trim();
            const code = (lang && !lang.includes(' ') && lines.length > 1) ? lines.slice(1).join('\n') : lines.join('\n');
            return (
              <div key={index} className="my-3 rounded-xl overflow-hidden border border-slate-800 bg-slate-950 shadow-md">
                <div className="bg-slate-900/90 px-3.5 py-1.5 flex justify-between items-center text-[11px] text-slate-400 border-b border-slate-800">
                  <span className="font-mono text-indigo-400 font-semibold">{lang || 'python'}</span>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(code);
                      setCopiedCodeId(index);
                      setTimeout(() => setCopiedCodeId(null), 2000);
                    }}
                    className="hover:text-white transition flex items-center gap-1 font-medium text-[11px]"
                  >
                    {copiedCodeId === index ? "✓ Đã chép" : "📋 Sao chép code"}
                  </button>
                </div>
                <pre className="p-3.5 text-xs text-emerald-300 font-mono overflow-x-auto leading-relaxed">
                  <code>{code}</code>
                </pre>
              </div>
            );
          }

          const lines = part.split('\n');
          return (
            <div key={index} className="space-y-1.5">
              {lines.map((line, lIdx) => {
                if (line.startsWith('### ')) {
                  return <h4 key={lIdx} className="text-base font-bold text-white mt-3 mb-1.5 flex items-center gap-1.5">{line.replace('### ', '')}</h4>;
                }
                if (line.startsWith('#### ')) {
                  return <h5 key={lIdx} className="text-sm font-bold text-indigo-300 mt-2 mb-1">{line.replace('#### ', '')}</h5>;
                }
                if (line.startsWith('- ') || line.startsWith('* ')) {
                  return (
                    <div key={lIdx} className="flex items-start gap-2 ml-2 text-xs text-slate-300 leading-relaxed">
                      <span className="text-indigo-400 mt-0.5">•</span>
                      <span>{line.substring(2)}</span>
                    </div>
                  );
                }
                if (!line.trim()) return <div key={lIdx} className="h-1" />;
                return <p key={lIdx} className="text-xs text-slate-300 leading-relaxed">{line}</p>;
              })}
            </div>
          );
        });
      };

      // ============================================================
      // RENDER MAIN APPLICATION
      // ============================================================
      return (
        <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">

          {/* ======================================================= */}
          {/* SIDEBAR NAVIGATION (5 DEDICATED WORKSPACES) */}
          {/* ======================================================= */}
          <aside className="w-64 bg-slate-900/90 border-r border-slate-800 flex flex-col justify-between p-4 backdrop-blur-lg shrink-0 z-20">
            <div>
              {/* BRAND LOGO */}
              <div className="flex items-center gap-3 px-3 py-3 mb-6 bg-slate-950/40 rounded-2xl border border-slate-800/80">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white font-black text-xl">
                  🛡️
                </div>
                <div>
                  <h1 className="font-extrabold text-base text-white tracking-tight leading-tight">Aegis Learn</h1>
                  <span className="text-[11px] text-indigo-400 font-semibold flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    High-Score Engine
                  </span>
                </div>
              </div>

              {/* 5 WORKSPACE NAVIGATION BUTTONS */}
              <div className="space-y-1">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-1 block">Không gian học tập</span>

                {/* 1. COCKPIT */}
                <button
                  onClick={() => setActiveWorkspace("COCKPIT")}
                  className={`w-full flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-bold transition ${activeWorkspace === 'COCKPIT' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-base">🎯</span>
                    <span>Bảng Điều Khiển Điểm Số</span>
                  </div>
                  {scorePrediction && (
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-black ${activeWorkspace === 'COCKPIT' ? 'bg-white/20 text-white' : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'}`}>
                      {scorePrediction.current_predicted_score}đ
                    </span>
                  )}
                </button>

                {/* 2. LEARNING PATH DAG */}
                <button
                  onClick={() => setActiveWorkspace("LEARNING_PATH")}
                  className={`w-full flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-bold transition ${activeWorkspace === 'LEARNING_PATH' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-base">🗺️</span>
                    <span>Lộ Trình Kiến Thức DAG</span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono">
                    {learningPathData?.completed_steps_count || 0}/{learningPathData?.total_steps || 0}
                  </span>
                </button>

                {/* 3. EXAM ARENA */}
                <button
                  onClick={() => setActiveWorkspace("EXAM_ARENA")}
                  className={`w-full flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-bold transition ${activeWorkspace === 'EXAM_ARENA' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-base">📝</span>
                    <span>Đấu Trường Luyện Thi</span>
                  </div>
                  <span className="bg-amber-500/20 text-amber-300 text-[10px] font-bold px-2 py-0.5 rounded-full border border-amber-500/30">
                    50 Phút
                  </span>
                </button>

                {/* 4. ERROR VAULT */}
                <button
                  onClick={() => { setActiveWorkspace("ERROR_VAULT"); fetchErrorVault(); }}
                  className={`w-full flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-bold transition ${activeWorkspace === 'ERROR_VAULT' ? 'bg-gradient-to-r from-rose-600 to-pink-600 text-white shadow-lg shadow-rose-600/30' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-base">📕</span>
                    <span>Sổ Tay Bẫy Sai & Phục Thù</span>
                  </div>
                  <span className="bg-rose-500/20 text-rose-300 text-[10px] font-bold px-2 py-0.5 rounded-full border border-rose-500/30">
                    {errorVaultList.length} Lỗi
                  </span>
                </button>

                {/* 5. AI STUDY ROOM */}
                <button
                  onClick={() => setActiveWorkspace("AI_STUDY_ROOM")}
                  className={`w-full flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-bold transition ${activeWorkspace === 'AI_STUDY_ROOM' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-base">🤖</span>
                    <span>Phòng Học AI & Gia Sư</span>
                  </div>
                  <span className="bg-emerald-500/20 text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-500/30">
                    Google
                  </span>
                </button>
              </div>

              {/* EXTERNAL SHORTCUTS */}
              <div className="mt-6 pt-4 border-t border-slate-800 space-y-1">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-3 mb-1 block">Hệ thống</span>
                <a href="/admin" className="flex items-center gap-3 px-3.5 py-2 rounded-xl text-xs font-medium text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 transition">
                  <span>🛡️</span> Quản trị viên (Admin)
                </a>
                <a href="/docs" target="_blank" className="flex items-center gap-3 px-3.5 py-2 rounded-xl text-xs font-medium text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 transition">
                  <span>⚡</span> Swagger API Docs
                </a>
              </div>
            </div>

            {/* GAMIFICATION & USER PROFILE */}
            <div className="pt-4 border-t border-slate-800 space-y-3">
              <div className="bg-slate-950/80 p-3 rounded-2xl border border-slate-800 text-xs flex justify-between items-center shadow-inner">
                <span className="flex items-center gap-1.5 text-amber-400 font-bold">
                  🔥 Streak: {userProfile.streak_days} Ngày
                </span>
                <span className="text-indigo-400 font-extrabold">⭐ {userProfile.exp_points} XP</span>
              </div>

              <div className="flex items-center gap-3 p-2.5 rounded-2xl bg-slate-800/40 border border-slate-800">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-violet-600 text-white flex items-center justify-center font-black text-xs shadow-md">
                  AI
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-bold text-white truncate">{userProfile.full_name}</p>
                  <p className="text-[10px] text-slate-400 truncate">Chuyên ngành Trí tuệ Nhân tạo</p>
                </div>
              </div>
            </div>
          </aside>

          {/* ======================================================= */}
          {/* MAIN WORKSPACE CONTAINER */}
          {/* ======================================================= */}
          <main className="flex-1 flex flex-col overflow-y-auto min-w-0">

            {/* GLOBAL TOPBAR: MULTI-SUBJECT SELECTOR & 3-TIER SEARCH */}
            <header className="h-16 border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-xl px-6 flex items-center justify-between sticky top-0 z-30 shrink-0">
              {/* SEARCH BAR & TARGET SCORE */}
              <div className="flex items-center gap-3 flex-1 max-w-2xl">
                <div className="relative flex-1 flex items-center">
                  <span className="absolute left-3.5 text-slate-400 text-sm">🔍</span>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleExecute3TierSearch(e.target.value, targetScore); }}
                    placeholder="Tìm kiếm môn học AI (Toán AI, Deep Learning, SQL, Python, Giải thuật...)"
                    className="w-full bg-slate-950/80 border border-slate-800 rounded-2xl pl-10 pr-28 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 shadow-inner"
                  />
                  <button
                    onClick={() => handleExecute3TierSearch(searchQuery, targetScore)}
                    disabled={isSearchLoading}
                    className="absolute right-1.5 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-[11px] font-bold px-3 py-1.5 rounded-xl transition shadow shadow-indigo-600/30 flex items-center gap-1"
                  >
                    {isSearchLoading ? "⏳ Đang tìm..." : "Lên Lộ Trình 🚀"}
                  </button>
                </div>

                {/* TARGET SCORE SELECTOR */}
                <div className="hidden sm:flex items-center gap-1.5 bg-slate-950/80 border border-slate-800 rounded-2xl px-3 py-1.5 shrink-0">
                  <span className="text-[11px] font-bold text-amber-400">🎯 Mục tiêu:</span>
                  <select
                    value={targetScore}
                    onChange={(e) => setTargetScore(parseFloat(e.target.value))}
                    className="bg-transparent text-xs font-bold text-white outline-none cursor-pointer"
                  >
                    <option value={10.0} className="bg-slate-900">10.0 (Tuyệt đối)</option>
                    <option value={9.5} className="bg-slate-900">9.5 (A+ Thủ khoa)</option>
                    <option value={9.0} className="bg-slate-900">9.0 (A Xuất sắc)</option>
                    <option value={8.5} className="bg-slate-900">8.5 (A Giỏi)</option>
                    <option value={7.5} className="bg-slate-900">7.5 (B+ Khá)</option>
                  </select>
                </div>
              </div>

              {/* ACTIVE SUBJECT SWITCHER & THEME TOGGLE */}
              <div className="flex items-center gap-3">
                {/* ACTIVE SUBJECT DROPDOWN */}
                <div className="hidden md:flex items-center gap-2 bg-indigo-950/40 border border-indigo-500/30 rounded-2xl px-3 py-1.5">
                  <span className="text-xs">📚</span>
                  <select
                    value={activeSubject?.id || ""}
                    onChange={(e) => handleSwitchSubject(e.target.value)}
                    className="bg-transparent text-xs font-bold text-indigo-300 outline-none cursor-pointer max-w-[200px] truncate"
                  >
                    {subjectsList.map(s => (
                      <option key={s.id} value={s.id} className="bg-slate-900 text-white">
                        {s.code}: {s.title}
                      </option>
                    ))}
                  </select>
                </div>

                {/* THEME TOGGLE */}
                <button
                  onClick={toggleTheme}
                  title="Chuyển đổi Chế độ Sáng dịu mắt / Tối"
                  className="bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-3 py-1.5 rounded-2xl text-xs font-semibold transition flex items-center gap-1.5 shadow-sm"
                >
                  <span>{theme === 'light' ? '🌙' : '☀️'}</span>
                  <span className="hidden sm:inline">{theme === 'light' ? 'Tối' : 'Sáng'}</span>
                </button>
              </div>
            </header>

            {/* ======================================================= */}
            {/* WORKSPACE 1: 🎯 COCKPIT (BẢNG ĐIỀU KHIỂN ĐIỂM SỐ) */}
            {/* ======================================================= */}
            {activeWorkspace === "COCKPIT" && (
              <div className="p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">

                {/* HERO SCORE PREDICTOR CARD */}
                <div className="bg-gradient-to-br from-indigo-950/80 via-slate-900 to-slate-900 border border-indigo-500/40 rounded-3xl p-6 lg:p-8 shadow-2xl relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>

                  <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 relative z-10">
                    <div>
                      <div className="flex items-center gap-2 mb-2 flex-wrap">
                        <span className="px-3 py-1 rounded-full text-xs font-black bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                          🎯 BỘ CHUẨN ĐOÁN NĂNG LỰC ĐIỂM SỐ
                        </span>
                        <span className="text-xs text-slate-400 font-mono">
                          Môn: {activeSubject?.title || 'Trí tuệ Nhân tạo'}
                        </span>
                      </div>
                      <h2 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
                        Chinh Phục Điểm {targetScore.toFixed(1)}: {scorePrediction?.target_grade || 'Điểm A+ Thủ khoa'} 🏆
                      </h2>
                      <p className="text-xs text-slate-400 mt-1 max-w-2xl">
                        Thuật toán tổng hợp từ kết quả làm bài trắc nghiệm, lịch sử sai bẫy đề thi và mức độ hoàn thành đồ thị DAG để dự báo chính xác điểm số cuối kỳ của bạn.
                      </p>
                    </div>

                    {/* SCORE COMPARISON BOX */}
                    <div className="flex items-center gap-4 bg-slate-950/90 border border-indigo-500/30 rounded-2xl p-4 shadow-xl">
                      <div className="text-center px-3">
                        <span className="text-[11px] text-slate-400 font-semibold block">Dự báo Hiện tại</span>
                        <div className="text-3xl font-black text-indigo-400">
                          {scorePrediction?.current_predicted_score || 4.5}
                          <span className="text-xs text-slate-500">/10</span>
                        </div>
                        <span className="text-[10px] text-indigo-300 font-bold block mt-0.5">
                          {scorePrediction?.grade_letter || 'Grade C'}
                        </span>
                      </div>

                      <div className="text-xl text-slate-600 font-light">➔</div>

                      <div className="text-center px-3 border-l border-slate-800">
                        <span className="text-[11px] text-amber-400 font-semibold block">Mục tiêu Đạt</span>
                        <div className="text-3xl font-black text-emerald-400">
                          {targetScore.toFixed(1)}
                          <span className="text-xs text-slate-500">/10</span>
                        </div>
                        <span className="text-[10px] text-emerald-300 font-bold block mt-0.5">
                          {targetScore >= 9.0 ? 'Grade A (Xuất sắc)' : 'Grade B+ (Giỏi)'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* PROGRESS BAR & STATS */}
                  <div className="mt-8 pt-6 border-t border-slate-800 grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
                      <span className="text-xs text-slate-400 block">Khoảng cách cần bù</span>
                      <span className="text-xl font-bold text-rose-400">
                        +{Math.max(0, (targetScore - (scorePrediction?.current_predicted_score || 4.5))).toFixed(1)} điểm
                      </span>
                    </div>

                    <div className="bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
                      <span className="text-xs text-slate-400 block">Thời gian đếm ngược thi</span>
                      <span className="text-xl font-bold text-amber-400">⏱️ {scorePrediction?.days_remaining || 14} ngày</span>
                    </div>

                    <div className="bg-slate-950/60 p-4 rounded-2xl border border-slate-800">
                      <span className="text-xs text-slate-400 block">Độ sẵn sàng phòng thi</span>
                      <span className="text-xl font-bold text-indigo-400">
                        {scorePrediction?.exam_readiness_percentage || 74}%
                      </span>
                    </div>

                    <div className="bg-slate-950/60 p-4 rounded-2xl border border-slate-800 flex items-center justify-between">
                      <div>
                        <span className="text-xs text-slate-400 block">Đã thi thử</span>
                        <span className="text-xl font-bold text-white">
                          {scorePrediction?.total_quizzes_taken || 0} bài
                        </span>
                      </div>
                      <button
                        onClick={handleStartMockExam}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs px-3.5 py-2 rounded-xl transition shadow"
                      >
                        Thi thử 50' →
                      </button>
                    </div>
                  </div>
                </div>

                {/* GRID: WEAKNESS RADAR & POMODORO TIMER */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                  {/* WEAKNESS RADAR GAP (LỖ HỔNG KIẾN THỨC) */}
                  <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-6">
                    <div className="flex justify-between items-center border-b border-slate-800 pb-4">
                      <div>
                        <h3 className="text-lg font-bold text-white flex items-center gap-2">
                          <span>📡</span> Radar Lỗ Hổng Điểm Số (Topic Weakness Matrix)
                        </h3>
                        <p className="text-xs text-slate-400 mt-0.5">
                          Đo lường mức độ thành thạo và tính toán chính xác điểm số bạn đang bị trừ oan ở từng chủ đề.
                        </p>
                      </div>
                      <button
                        onClick={fetchScorePrediction}
                        className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
                      >
                        🔄 Làm mới
                      </button>
                    </div>

                    <div className="space-y-3">
                      {(scorePrediction?.topics_radar || []).map((topicItem) => {
                        const isCritical = topicItem.status === 'CRITICAL_GAP';
                        const isImproving = topicItem.status === 'NEEDS_IMPROVEMENT';
                        return (
                          <div
                            key={topicItem.topic_id}
                            className={`p-4 rounded-2xl border transition flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 ${isCritical ? 'bg-rose-950/20 border-rose-500/30' : isImproving ? 'bg-amber-950/20 border-amber-500/30' : 'bg-slate-950 border-slate-800'}`}
                          >
                            <div className="space-y-1">
                              <div className="flex items-center gap-2">
                                <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                                  {topicItem.code}
                                </span>
                                <h4 className="font-bold text-white text-xs sm:text-sm">{topicItem.title}</h4>
                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${isCritical ? 'bg-rose-500/20 text-rose-300' : isImproving ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'}`}>
                                  {isCritical ? '⚠️ Lỗ hổng nguy hiểm' : isImproving ? '⚡ Cần củng cố' : '✓ Vững vàng'}
                                </span>
                              </div>
                              <div className="flex items-center gap-4 text-xs text-slate-400">
                                <span>Độ làm chủ: <strong className="text-white">{topicItem.mastery_percentage}%</strong></span>
                                <span className="text-rose-400">Làm mất: <strong>-{topicItem.impact_points} điểm</strong> vào điểm thi cuối kỳ</span>
                              </div>
                            </div>

                            <button
                              onClick={() => {
                                setSelectedDrillTopic(topicItem.topic_id);
                                handleStartTopicDrill(topicItem.topic_id, 3.0);
                              }}
                              className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs px-4 py-2 rounded-xl transition shadow flex items-center gap-1 shrink-0"
                            >
                              <span>Gỡ điểm ngay</span>
                              <span>→</span>
                            </button>
                          </div>
                        );
                      })}
                    </div>

                    {/* 3 QUICK WINS (VIỆC CẦN LÀM HÔM NAY) */}
                    <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3">
                      <h4 className="text-xs font-extrabold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                        <span>⚡</span> 3 Nhiệm Vụ Trọng Tâm Hôm Nay (Quick Wins)
                      </h4>
                      <div className="space-y-2">
                        {(scorePrediction?.quick_wins || [
                          "🎯 Luyện 15 câu bẫy Pandas (loc/iloc, axis=1) ➔ Bù đắp ngay +1.2 điểm",
                          "💡 Ôn 6 thẻ Flashcard Gradient Descent ➔ Củng cố ngay +0.4 điểm phần tự luận",
                          "⚡ Thi thử Đề Chuẩn Hóa Phòng Thi Thật 50 phút ➔ Rèn luyện phản xạ thời gian"
                        ]).map((win, wIdx) => (
                          <div key={wIdx} className="flex items-start gap-2.5 text-xs text-slate-300 bg-slate-900/60 p-3 rounded-xl border border-slate-800/80">
                            <span className="text-emerald-400 font-bold">✓</span>
                            <span>{win}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* POMODORO FOCUS TIMER WIDGET */}
                  <div className="space-y-6">
                    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl text-center space-y-6">
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
                          🍅 Pomodoro 25 Phút Tập Trung
                        </span>
                        <h3 className="text-lg font-bold text-white mt-2">Đồng Hồ Chuyên Sâu</h3>
                        <p className="text-xs text-slate-400 mt-1">25 phút tập trung cao độ, không xao nhãng để ghi nhớ kiến thức sâu.</p>
                      </div>

                      <div className="w-48 h-48 mx-auto rounded-full bg-slate-950 border-4 border-indigo-500/40 flex flex-col items-center justify-center shadow-inner relative">
                        <span className="text-4xl font-black text-white font-mono tracking-wider">
                          {formatPomodoro(pomodoroSeconds)}
                        </span>
                        <span className="text-[11px] text-slate-400 mt-1 font-medium">
                          {isPomodoroRunning ? "Đang đếm ngược..." : "Sẵn sàng"}
                        </span>
                      </div>

                      <div className="flex gap-3 justify-center">
                        <button
                          onClick={() => setIsPomodoroRunning(!isPomodoroRunning)}
                          className={`flex-1 font-bold text-xs py-3 rounded-xl transition shadow-lg ${isPomodoroRunning ? 'bg-amber-600 hover:bg-amber-500 text-white' : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30'}`}
                        >
                          {isPomodoroRunning ? "⏸️ Tạm Dừng" : "▶️ Bắt Đầu 25 Phút"}
                        </button>
                        <button
                          onClick={() => { setIsPomodoroRunning(false); setPomodoroSeconds(1500); }}
                          className="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs px-4 py-3 rounded-xl border border-slate-700 transition"
                        >
                          🔄 Đặt lại
                        </button>
                      </div>
                    </div>

                    {/* SHORTCUT CARD TO ERROR VAULT */}
                    <div className="bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-900 border border-rose-500/30 rounded-3xl p-6 shadow-xl space-y-3">
                      <span className="text-2xl">🎯</span>
                      <h4 className="font-bold text-white text-base">Sổ Tay Bẫy Đề Thi ({errorVaultList.length} câu)</h4>
                      <p className="text-xs text-slate-400 leading-relaxed">
                        Bạn có {errorVaultList.length} câu hỏi từng làm sai hoặc bẫy kinh điển chưa được tẩy trắng. Hãy làm bài phục thù ngay!
                      </p>
                      <button
                        onClick={handleStartErrorClearance}
                        className="w-full bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs py-3 rounded-xl transition shadow-lg shadow-rose-600/30"
                      >
                        🎯 Thi Phục Thù Xóa Lỗ Hổng →
                      </button>
                    </div>
                  </div>

                </div>
              </div>
            )}

            {/* ======================================================= */}
            {/* WORKSPACE 2: 🗺️ LEARNING PATH (ĐỒ THỊ DAG KIẾN THỨC) */}
            {/* ======================================================= */}
            {activeWorkspace === "LEARNING_PATH" && (
              <div className="p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">

                {/* SUBJECT BANNER */}
                <div className="bg-gradient-to-r from-indigo-950/80 via-slate-900 to-slate-900 border border-indigo-500/40 rounded-3xl p-6 lg:p-8 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-mono text-xs font-bold px-2.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        {activeSubject?.code || 'AI_PYTHON'}
                      </span>
                      <span className="text-xs text-emerald-400 font-bold">
                        ● {activeSubject?.topics_count || 5} Bài học tiên quyết
                      </span>
                    </div>
                    <h2 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
                      {activeSubject?.title || 'Lộ trình Lập trình Python & Trí tuệ Nhân tạo'}
                    </h2>
                    <p className="text-xs text-slate-400 mt-1 max-w-2xl">
                      {activeSubject?.description || 'Đồ thị tiên quyết DAG tự động mở khóa bài học tiếp theo sau khi bạn hoàn thành bài kiểm tra trắc nghiệm.'}
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => handleExecute3TierSearch(activeSubject?.title, targetScore)}
                      className="bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-slate-700 font-bold text-xs px-4 py-2.5 rounded-2xl transition flex items-center gap-1.5 shadow"
                    >
                      <span>🔍 Xem Tài liệu Web & YouTube Chọn Lọc</span>
                    </button>
                  </div>
                </div>

                {/* DAG GRAPH TIMELINE */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-xl space-y-6">
                  <div className="flex justify-between items-center border-b border-slate-800 pb-4">
                    <div>
                      <h3 className="text-lg font-bold text-white flex items-center gap-2">
                        <span>📌</span> Đồ Thị Tuần Tự Kiến Thức DAG (Topological Sort)
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Bấm vào từng bài học để đọc tài liệu chính thức, xem video giảng và làm bài test mở khóa.
                      </p>
                    </div>
                  </div>

                  <div className="relative pl-6 space-y-6 before:absolute before:left-3 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-800">
                    {(learningPathData?.learning_path || []).map((step) => {
                      const isCompleted = step.status === 'COMPLETED';
                      const isUnlocked = step.status === 'UNLOCKED';
                      const isLocked = step.status === 'LOCKED';
                      const isSelected = selectedTopicId === step.topic_id;

                      return (
                        <div
                          key={step.step_number}
                          onClick={() => {
                            setSelectedTopicId(step.topic_id);
                            fetchTopicMaterials(step.topic_id);
                          }}
                          className={`relative p-5 rounded-2xl transition border cursor-pointer hover:-translate-y-0.5 shadow-md ${isSelected ? 'bg-indigo-950/40 border-indigo-500/70 shadow-indigo-500/10' : 'bg-slate-950/80 border-slate-800 hover:border-slate-700'}`}
                        >
                          {/* CIRCLE ICON */}
                          <div className={`absolute -left-9 top-5 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ring-4 ring-slate-950 ${isCompleted ? 'bg-emerald-500 text-slate-950' : isUnlocked ? 'bg-indigo-500 text-white animate-pulse' : 'bg-slate-800 text-slate-400'}`}>
                            {isCompleted ? '✓' : isLocked ? '🔒' : step.step_number}
                          </div>

                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                            <div className="space-y-1">
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-bold">
                                  {step.code}
                                </span>
                                <h4 className="font-bold text-white text-base">{step.title}</h4>
                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${isCompleted ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : isUnlocked ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-slate-800 text-slate-500'}`}>
                                  {isCompleted ? 'Đã thành thạo' : isUnlocked ? 'Sẵn sàng học' : 'Đang khóa'}
                                </span>
                              </div>
                              <p className="text-xs text-slate-400">{step.reasoning}</p>
                            </div>

                            <div className="flex items-center gap-2 shrink-0">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  if (isLocked) {
                                    alert("Bài học này bị khóa bởi các chủ đề tiên quyết. Vui lòng hoàn thành bài học trước!");
                                    return;
                                  }
                                  handleStartTopicDrill(step.topic_id, 3.0);
                                }}
                                className={`font-bold text-xs px-4 py-2 rounded-xl transition shadow flex items-center gap-1.5 ${isCompleted ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-600 hover:text-white' : isUnlocked ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30' : 'bg-slate-800 text-slate-500 cursor-not-allowed'}`}
                              >
                                <span>{isCompleted ? '✓ Thi Cải Thiện' : '✍️ Test Mở Khóa →'}</span>
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* SELECTED TOPIC MATERIALS DRAWER */}
                {selectedTopicId && (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-xl space-y-6">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-800 pb-4">
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400">Tài liệu học tập chi tiết</span>
                        <h3 className="text-lg font-bold text-white mt-1">
                          Kho Học Liệu: {activeSubject?.topics?.find(t => t.id === selectedTopicId)?.title || 'Bài học'}
                        </h3>
                      </div>

                      {/* TABS */}
                      <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800">
                        <button
                          onClick={() => setTopicTab("WEB_DOCS")}
                          className={`text-xs font-bold px-3 py-1.5 rounded-lg transition ${topicTab === 'WEB_DOCS' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
                        >
                          🌐 Web & Docs ({topicMaterials.filter(m => m.material_type !== 'VIDEO').length})
                        </button>
                        <button
                          onClick={() => setTopicTab("VIDEOS")}
                          className={`text-xs font-bold px-3 py-1.5 rounded-lg transition ${topicTab === 'VIDEOS' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
                        >
                          📺 Video YouTube ({topicMaterials.filter(m => m.material_type === 'VIDEO').length})
                        </button>
                      </div>
                    </div>

                    {/* MATERIALS GRID */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {topicMaterials
                        .filter(m => topicTab === "VIDEOS" ? m.material_type === "VIDEO" : m.material_type !== "VIDEO")
                        .map((mat) => (
                          <div key={mat.id} className="bg-slate-950 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 flex flex-col justify-between transition shadow-md hover:-translate-y-1">
                            <div className="space-y-2">
                              <div className="flex justify-between items-center">
                                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                                  {mat.university || 'Chính thống'}
                                </span>
                                <span className="text-[10px] text-slate-400">⭐ Độ khó: {mat.difficulty_level}/5</span>
                              </div>
                              <h4 className="font-bold text-white text-sm line-clamp-2">{mat.title}</h4>
                              <p className="text-xs text-slate-400 line-clamp-3 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/80">
                                {mat.text_content || 'Tài liệu hướng dẫn chuyên sâu cho bài học.'}
                              </p>
                            </div>

                            <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                              <a
                                href={mat.content_url || "https://docs.python.org/3/"}
                                target="_blank"
                                rel="noreferrer"
                                className="bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/30 text-xs font-bold px-3 py-1.5 rounded-xl transition flex items-center gap-1 shadow-sm"
                              >
                                <span>{topicTab === 'VIDEOS' ? 'Xem bài giảng ↗' : 'Mở tài liệu đọc ↗'}</span>
                              </a>
                              <button
                                onClick={() => handleStartTopicDrill(selectedTopicId, 3.0)}
                                className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3 py-1.5 rounded-xl transition border border-slate-700"
                              >
                                Test trắc nghiệm
                              </button>
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>
                )}

              </div>
            )}

            {/* ======================================================= */}
            {/* WORKSPACE 3: 📝 EXAM ARENA (ĐẤU TRƯỜNG LUYỆN THI) */}
            {/* ======================================================= */}
            {activeWorkspace === "EXAM_ARENA" && (
              <div className="p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">

                {/* EXAM ARENA SUB-TABS */}
                <div className="flex bg-slate-900 p-1.5 rounded-2xl border border-slate-800 max-w-md">
                  <button
                    onClick={() => setExamArenaTab("TOPIC_DRILL")}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${examArenaTab === 'TOPIC_DRILL' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    🎯 Topic Drill (15 Câu)
                  </button>
                  <button
                    onClick={() => setExamArenaTab("MOCK_EXAM")}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${examArenaTab === 'MOCK_EXAM' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    ⏱️ Thi Thử Mô Phỏng (50')
                  </button>
                  <button
                    onClick={() => { setExamArenaTab("HISTORY"); fetchQuizHistory(); }}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${examArenaTab === 'HISTORY' ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    📜 Lịch Sử Bài Làm
                  </button>
                </div>

                {/* TAB 1: TOPIC DRILL */}
                {examArenaTab === "TOPIC_DRILL" && (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-xl space-y-6">
                    <div>
                      <h3 className="text-xl font-bold text-white flex items-center gap-2">
                        <span>🎯</span> Luyện Tập Chuyên Đề Nhanh (Topic Drill - 15 Câu)
                      </h3>
                      <p className="text-xs text-slate-400 mt-1">
                        Tập trung rèn luyện phản xạ và củng cố kiến thức từng bài học để quét sạch mọi bẫy đề thi.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-300">Chọn chủ đề luyện tập:</label>
                        <select
                          value={selectedDrillTopic || ""}
                          onChange={(e) => setSelectedDrillTopic(parseInt(e.target.value))}
                          className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-3 text-xs text-white outline-none"
                        >
                          {(activeSubject?.topics || []).map(t => (
                            <option key={t.id} value={t.id}>
                              {t.code}: {t.title}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-300">Chọn độ khó bài test:</label>
                        <select
                          value={drillDifficulty}
                          onChange={(e) => setDrillDifficulty(parseFloat(e.target.value))}
                          className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-3 text-xs text-white outline-none"
                        >
                          <option value={1.5}>Dễ (1.5/5.0) - Nhớ lại khái niệm cơ bản</option>
                          <option value={3.0}>Trung bình (3.0/5.0) - Hiểu sâu & Áp dụng</option>
                          <option value={4.5}>Khó & Bẫy (4.5/5.0) - Bẫy tư duy phòng thi</option>
                        </select>
                      </div>
                    </div>

                    <button
                      onClick={() => handleStartTopicDrill(selectedDrillTopic, drillDifficulty)}
                      className="w-full bg-gradient-to-r from-indigo-600 via-violet-600 to-purple-600 hover:from-indigo-500 hover:to-violet-500 text-white font-extrabold text-sm py-4 rounded-2xl transition shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2"
                    >
                      <span>🚀 Bắt Đầu Làm Bài Topic Drill (15 Câu)</span>
                      <span>→</span>
                    </button>
                  </div>
                )}

                {/* TAB 2: MOCK EXAM SIMULATOR */}
                {examArenaTab === "MOCK_EXAM" && (
                  <div className="bg-gradient-to-br from-indigo-950/80 via-slate-900 to-slate-900 border border-indigo-500/40 rounded-3xl p-6 lg:p-8 shadow-2xl space-y-6">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                      <div>
                        <span className="px-3 py-1 rounded-full text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/30">
                          ⏱️ MÔ PHỎNG PHÒNG THI CHUẨN ĐẦU RA (50 PHÚT)
                        </span>
                        <h3 className="text-2xl font-black text-white mt-2">
                          Đề Thi Thử Chuẩn Hóa Môn: {activeSubject?.title || 'AI'}
                        </h3>
                        <p className="text-xs text-slate-400 mt-1 max-w-2xl">
                          Đề thi bao quát 100% các chủ đề trong môn học với 25 câu hỏi tổng hợp, đồng hồ đếm ngược 50 phút và tính điểm chữ GPA 4.0 chuẩn đại học.
                        </p>
                      </div>

                      <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 text-center shrink-0">
                        <span className="text-[11px] text-slate-400 font-semibold block">Thời gian làm bài</span>
                        <span className="text-2xl font-black text-amber-400">50:00</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-300">
                      <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-1">
                        <span className="text-slate-400">Số lượng câu hỏi</span>
                        <p className="text-base font-bold text-white">25 câu trắc nghiệm</p>
                      </div>
                      <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-1">
                        <span className="text-slate-400">Mức điểm đạt chuẩn</span>
                        <p className="text-base font-bold text-emerald-400">70% (Điểm C/B trở lên)</p>
                      </div>
                      <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 space-y-1">
                        <span className="text-slate-400">Mục tiêu của bạn</span>
                        <p className="text-base font-bold text-indigo-400">{targetScore.toFixed(1)} / 10.0 (Điểm A)</p>
                      </div>
                    </div>

                    <button
                      onClick={handleStartMockExam}
                      className="w-full bg-gradient-to-r from-amber-500 via-orange-600 to-rose-600 hover:from-amber-400 hover:to-orange-500 text-slate-950 font-black text-sm py-4 rounded-2xl transition shadow-xl shadow-amber-500/20 flex items-center justify-center gap-2"
                    >
                      <span>⚡ BƯỚC VÀO PHÒNG THI THỬ 50 PHÚT NGAY</span>
                      <span>→</span>
                    </button>
                  </div>
                )}

                {/* TAB 3: QUIZ HISTORY */}
                {examArenaTab === "HISTORY" && (
                  <QuizHistoryTab
                    historyList={quizHistoryList}
                    onReviewAttempt={async (attemptId) => {
                      try {
                        const res = await fetch(`${API_BASE_URL}/quiz/history/${attemptId}`);
                        if (res.ok) {
                          const data = await res.json();
                          setActiveReviewDetailModal(data);
                        }
                      } catch (e) {
                        alert("Không thể tải chi tiết bài làm!");
                      }
                    }}
                    onRetakeQuiz={() => handleStartTopicDrill(selectedTopicId, 3.0)}
                    loading={isHistoryLoading}
                    onRefresh={fetchQuizHistory}
                  />
                )}

              </div>
            )}

            {/* ======================================================= */}
            {/* WORKSPACE 4: 📕 ERROR VAULT (SỔ TAY BẪY SAI & PHỤC THÙ) */}
            {/* ======================================================= */}
            {activeWorkspace === "ERROR_VAULT" && (
              <div className="p-6 lg:p-8 space-y-8 max-w-7xl mx-auto w-full">

                {/* ERROR VAULT HERO */}
                <div className="bg-gradient-to-br from-rose-950/80 via-slate-900 to-slate-900 border border-rose-500/40 rounded-3xl p-6 lg:p-8 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="px-3 py-1 rounded-full text-xs font-black bg-rose-500/20 text-rose-300 border border-rose-500/30">
                        📕 SMART ERROR VAULT
                      </span>
                      <span className="text-xs text-slate-400 font-mono">
                        {errorVaultList.length} câu hỏi bẫy thi & lỗi sai
                      </span>
                    </div>
                    <h2 className="text-2xl lg:text-3xl font-black text-white tracking-tight">
                      Sổ Tay Bẫy Đề Thi & Xóa Điểm Liệt 🎯
                    </h2>
                    <p className="text-xs text-slate-400 mt-1 max-w-2xl">
                      Mọi câu hỏi bạn từng chọn sai trong các bài kiểm tra được tự động gom vào đây kèm phân tích tâm lý vì sao bạn mắc bẫy. Làm đúng lại để xóa bỏ hoàn toàn lỗ hổng điểm số!
                    </p>
                  </div>

                  <button
                    onClick={handleStartErrorClearance}
                    className="bg-gradient-to-r from-rose-600 via-pink-600 to-purple-600 hover:from-rose-500 hover:to-pink-500 text-white font-black text-xs px-6 py-3.5 rounded-2xl transition shadow-xl shadow-rose-600/30 flex items-center gap-2 shrink-0"
                  >
                    <span>🎯 Thi Phục Thù Tẩy Trắng Lỗi</span>
                    <span>→</span>
                  </button>
                </div>

                {/* ERROR VAULT CARDS */}
                {isVaultLoading ? (
                  <div className="p-12 text-center text-slate-400 space-y-3">
                    <div className="animate-spin text-3xl">🌀</div>
                    <p className="text-xs">Đang tải danh sách câu hỏi bẫy sai...</p>
                  </div>
                ) : errorVaultList.length === 0 ? (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-12 text-center space-y-4">
                    <span className="text-4xl">🎉</span>
                    <h3 className="text-lg font-bold text-white">Tuyệt vời! Sổ tay đang trống</h3>
                    <p className="text-xs text-slate-400 max-w-md mx-auto">
                      Bạn chưa có câu hỏi sai nào tồn đọng. Hãy tiếp tục duy trì phong độ làm bài thi tuyệt đối nhé!
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {errorVaultList.map((err, errIdx) => (
                      <div key={errIdx} className="bg-slate-900 border border-slate-800 hover:border-rose-500/50 rounded-2xl p-6 shadow-xl space-y-4 transition">
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-xs font-bold px-2.5 py-0.5 rounded bg-slate-800 text-slate-300">
                              {err.topic_code || 'BẪY THI'}
                            </span>
                            <span className="text-xs text-indigo-400 font-semibold">{err.topic_title}</span>
                          </div>
                          <span className="text-[11px] font-bold text-rose-400 bg-rose-500/10 px-2.5 py-0.5 rounded-full border border-rose-500/20">
                            {err.trap_warning || '⚠️ Bẫy đề thi kinh điển'}
                          </span>
                        </div>

                        {/* QUESTION CONTENT */}
                        <h4 className="font-bold text-white text-sm leading-relaxed">{err.content}</h4>

                        {/* OPTIONS */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          {Object.keys(err.options || {}).map(optKey => {
                            const isUserAns = err.user_answer === optKey;
                            const isCorrAns = err.correct_answer === optKey;
                            return (
                              <div
                                key={optKey}
                                className={`p-3 rounded-xl border flex items-center justify-between ${isCorrAns ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300 font-bold' : isUserAns ? 'bg-rose-950/40 border-rose-500/50 text-rose-300' : 'bg-slate-950 border-slate-800/80 text-slate-400'}`}
                              >
                                <span><strong>{optKey}.</strong> {err.options[optKey]}</span>
                                {isCorrAns && <span className="text-emerald-400 font-black text-xs">✓ Đáp án đúng</span>}
                                {isUserAns && !isCorrAns && <span className="text-rose-400 font-bold text-xs">✗ Bạn chọn</span>}
                              </div>
                            );
                          })}
                        </div>

                        {/* PEDAGOGICAL EXPLANATION */}
                        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1 text-xs">
                          <span className="font-bold text-indigo-400">💡 Giải thích chi tiết & Cách né bẫy:</span>
                          <p className="text-slate-300 leading-relaxed">{err.explanation}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

              </div>
            )}

            {/* ======================================================= */}
            {/* WORKSPACE 5: 🤖 AI STUDY ROOM (GIA SƯ AI GOOGLE GROUNDING) */}
            {/* ======================================================= */}
            {activeWorkspace === "AI_STUDY_ROOM" && (
              <div className="p-6 lg:p-8 space-y-6 max-w-6xl mx-auto w-full flex-1 flex flex-col h-[calc(100vh-4rem)]">

                {/* STUDY ROOM SUB-TABS */}
                <div className="flex bg-slate-900 p-1.5 rounded-2xl border border-slate-800 shrink-0 max-w-xl">
                  <button
                    onClick={() => setStudyRoomTab("AI_TUTOR")}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${studyRoomTab === 'AI_TUTOR' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    🤖 Gia Sư AI (Google)
                  </button>
                  <button
                    onClick={() => setStudyRoomTab("FEYNMAN")}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${studyRoomTab === 'FEYNMAN' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    🧠 Phòng Feynman
                  </button>
                  <button
                    onClick={() => { setStudyRoomTab("CRAMMING"); fetchCrammingCheatSheet(selectedTopicId || 103); }}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${studyRoomTab === 'CRAMMING' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    ⚡ Nước Rút 48h
                  </button>
                  <button
                    onClick={() => { setStudyRoomTab("FLASHCARDS"); fetchFlashcards(selectedTopicId || 0); }}
                    className={`flex-1 text-xs font-bold py-2.5 rounded-xl transition ${studyRoomTab === 'FLASHCARDS' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
                  >
                    🗂️ Flashcard SM-2
                  </button>
                </div>

                {/* SUB-TAB 1: AI TUTOR CHAT WITH GOOGLE GROUNDING */}
                {studyRoomTab === "AI_TUTOR" && (
                  <div className="flex-1 bg-slate-900 border border-slate-800 rounded-3xl flex flex-col overflow-hidden shadow-2xl">
                    {/* CHAT HEADER */}
                    <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex justify-between items-center shrink-0">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white text-lg shadow">
                          🤖
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="font-bold text-white text-sm">Gia sư AI Master Tutor</h3>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                              ● Google Search Grounding Active
                            </span>
                          </div>
                          <p className="text-[11px] text-slate-400">Trả lời chính xác kèm trích dẫn tài liệu chính thức từ Google, Cambridge, PyTorch, Scikit-Learn.</p>
                        </div>
                      </div>
                      <button
                        onClick={() => setChatMessages([chatMessages[0]])}
                        className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-xl border border-slate-700 transition"
                      >
                        🗑️ Xóa chat
                      </button>
                    </div>

                    {/* QUICK PROMPT CHIPS */}
                    <div className="flex items-center gap-2 p-2.5 bg-slate-950/40 border-b border-slate-800/80 overflow-x-auto shrink-0">
                      <span className="text-[11px] font-bold text-slate-400 shrink-0">💡 Gợi ý nhanh:</span>
                      {[
                        "Phân biệt loc và iloc trong Pandas?",
                        "Bản chất hình học của Ma trận & Vector riêng?",
                        "Giải thích thuật toán tìm kiếm A* trong AI?",
                        "Cách tối ưu hóa Gradient Descent và học máy?",
                        "Kiến trúc Transformer và Attention hoạt động thế nào?"
                      ].map((prompt, pIdx) => (
                        <button
                          key={pIdx}
                          onClick={() => handleSendAiChatMessage(prompt)}
                          className="bg-slate-900 hover:bg-indigo-950/60 border border-slate-800 hover:border-indigo-500/40 text-slate-300 hover:text-indigo-200 text-xs px-3 py-1 rounded-xl transition shrink-0 whitespace-nowrap shadow-sm"
                        >
                          {prompt}
                        </button>
                      ))}
                    </div>

                    {/* MESSAGES LIST */}
                    <div className="flex-1 p-5 overflow-y-auto space-y-4">
                      {chatMessages.map((msg) => {
                        const isUser = msg.role === "user";
                        return (
                          <div key={msg.id} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
                            {!isUser && (
                              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center text-white text-base shrink-0 shadow">
                                🤖
                              </div>
                            )}

                            <div className={`p-4 rounded-2xl max-w-[85%] space-y-2 ${isUser ? 'bg-indigo-600 text-white font-medium' : 'bg-slate-950 border border-slate-800 text-slate-200 shadow-xl'}`}>
                              {isUser ? (
                                <p className="text-xs whitespace-pre-wrap">{msg.content}</p>
                              ) : (
                                <div className="text-xs leading-relaxed space-y-2">
                                  {renderFormattedAiContent(msg.content)}

                                  {/* CLICKABLE GOOGLE / WEB GROUNDED CITATIONS */}
                                  {(msg.sources || []).length > 0 && (
                                    <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
                                      <span className="text-[11px] font-bold text-indigo-400 flex items-center gap-1.5">
                                        <span>🌐</span> Nguồn trích dẫn kiểm chứng từ Google & Tài liệu chuẩn:
                                      </span>
                                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                        {msg.sources.map((src, sIdx) => (
                                          <a
                                            key={sIdx}
                                            href={src.url}
                                            target="_blank"
                                            rel="noreferrer"
                                            className="bg-slate-900 hover:bg-indigo-950/50 border border-slate-800 hover:border-indigo-500/40 p-2.5 rounded-xl transition block group"
                                          >
                                            <span className="font-bold text-indigo-300 group-hover:text-white text-xs block truncate">
                                              🔗 {src.title}
                                            </span>
                                            <span className="text-[10px] text-slate-400 line-clamp-1 mt-0.5">
                                              {src.snippet}
                                            </span>
                                          </a>
                                        ))}
                                      </div>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          </div>
                        );
                      })}

                      {isAiThinking && (
                        <div className="flex items-center gap-3 text-indigo-400 text-xs font-semibold p-4 animate-pulse">
                          <span>🤖</span>
                          <span>Gia sư AI đang tra cứu Google & soạn bài giảng chi tiết cho bạn...</span>
                        </div>
                      )}
                    </div>

                    {/* INPUT BOX */}
                    <div className="p-3 bg-slate-950 border-t border-slate-800 flex gap-2">
                      <input
                        type="text"
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                        onKeyDown={(e) => { if (e.key === 'Enter') handleSendAiChatMessage(); }}
                        placeholder="Hỏi bất kỳ kiến thức nào: lý thuyết, công thức toán, code Python, debug..."
                        className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl px-4 py-2.5 text-xs text-white outline-none focus:border-indigo-500 shadow-inner"
                      />
                      <button
                        onClick={() => handleSendAiChatMessage()}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs px-5 py-2.5 rounded-2xl transition shadow shadow-indigo-600/30 flex items-center gap-1.5"
                      >
                        <span>Gửi</span>
                        <span>➤</span>
                      </button>
                    </div>
                  </div>
                )}

                {/* SUB-TAB 2: FEYNMAN ROOM */}
                {studyRoomTab === "FEYNMAN" && (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-xl space-y-6 overflow-y-auto">
                    <div>
                      <span className="px-3 py-1 rounded-full text-xs font-black bg-purple-500/20 text-purple-300 border border-purple-500/30">
                        🧠 PHƯƠNG PHÁP HỌC SÂU RICHARD FEYNMAN
                      </span>
                      <h3 className="text-xl font-bold text-white mt-2">Phòng Tự Giảng & Chấm Điểm Thấu Hiểu</h3>
                      <p className="text-xs text-slate-400 mt-1">
                        Hãy giải thích một khái niệm khó bằng ngôn ngữ đơn giản như đang dạy lại cho một người mới bắt đầu. AI sẽ phân tích và chấm điểm độ thấu hiểu của bạn!
                      </p>
                    </div>

                    <div className="space-y-4">
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-300">Khái niệm bạn muốn giảng:</label>
                        <input
                          type="text"
                          value={feynmanConcept}
                          onChange={(e) => setFeynmanConcept(e.target.value)}
                          placeholder="Ví dụ: Gradient Descent, Ma trận hiệp phương sai, Cây BST..."
                          className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-3 text-xs text-white outline-none"
                        />
                      </div>

                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-300">Lời giải thích của bạn (bằng ngôn ngữ giản dị, ví dụ thực tế):</label>
                        <textarea
                          value={feynmanText}
                          onChange={(e) => setFeynmanText(e.target.value)}
                          placeholder="Hãy giải thích khái niệm này như thể bạn đang giảng cho một học sinh cấp 3. Dùng ẩn dụ đời sống, không sao chép nguyên văn sách giáo khoa..."
                          className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none h-36 leading-relaxed"
                        />
                      </div>

                      <button
                        onClick={handleEvaluateFeynman}
                        disabled={isEvaluatingFeynman}
                        className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs py-3.5 rounded-2xl transition shadow-lg shadow-purple-600/30"
                      >
                        {isEvaluatingFeynman ? "⏳ AI Đang Thẩm Định Kiến Thức..." : "🔍 Chấm Điểm Độ Thấu Hiểu Bằng AI →"}
                      </button>

                      {/* EVALUATION RESULTS */}
                      {feynmanEvaluation && (
                        <div className="bg-slate-950 p-6 rounded-2xl border border-purple-500/30 space-y-4 animate-in fade-in">
                          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                            <div>
                              <span className="text-xs text-slate-400">Điểm số thấu hiểu Feynman:</span>
                              <div className="text-3xl font-black text-purple-400">
                                {feynmanEvaluation.mastery_score || 85}/100
                              </div>
                            </div>
                            <span className="bg-purple-500/20 text-purple-300 font-bold text-xs px-3 py-1 rounded-full border border-purple-500/30">
                              {feynmanEvaluation.passed ? "✓ Đạt Tiêu Chuẩn Feynman" : "Cần Bổ Sung"}
                            </span>
                          </div>

                          <div className="text-xs text-slate-300 space-y-2">
                            <span className="font-bold text-white block">Nhận xét sư phạm từ AI:</span>
                            <p className="leading-relaxed bg-slate-900 p-3 rounded-xl border border-slate-800">
                              {feynmanEvaluation.feedback || feynmanEvaluation.evaluation_summary}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* SUB-TAB 3: CRAMMING CHEAT SHEET 48H */}
                {studyRoomTab === "CRAMMING" && (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-xl space-y-6 overflow-y-auto">
                    <div className="flex justify-between items-start flex-wrap gap-4 border-b border-slate-800 pb-4">
                      <div>
                        <span className="px-3 py-1 rounded-full text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/30">
                          ⚡ CHẾ ĐỘ NƯỚC RÚT 48H (CRAMMING MODE)
                        </span>
                        <h3 className="text-xl font-bold text-white mt-2">
                          Tóm Tắt Trọng Tâm 1 Trang: {cheatSheetData?.topic_title || 'Chủ đề'}
                        </h3>
                        <p className="text-xs text-slate-400 mt-0.5">Tất cả những gì bạn bắt buộc phải nhớ trước khi bước vào phòng thi 48 giờ.</p>
                      </div>

                      <select
                        value={cheatSheetTopicId}
                        onChange={(e) => fetchCrammingCheatSheet(parseInt(e.target.value))}
                        className="bg-slate-950 border border-slate-800 text-xs font-bold text-white rounded-xl px-3 py-2 outline-none"
                      >
                        {(activeSubject?.topics || []).map(t => (
                          <option key={t.id} value={t.id}>{t.code}: {t.title}</option>
                        ))}
                      </select>
                    </div>

                    {cheatSheetData && (
                      <div className="space-y-6">
                        {/* 1-PAGE SUMMARY */}
                        <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-2">
                          <span className="text-xs font-extrabold text-indigo-400 uppercase tracking-wide">📌 Tóm tắt cốt lõi 1 trang:</span>
                          <p className="text-xs text-slate-200 leading-relaxed">{cheatSheetData.one_page_summary}</p>
                        </div>

                        {/* MUST REMEMBER FORMULAS */}
                        <div className="bg-slate-950 p-5 rounded-2xl border border-indigo-500/30 space-y-3">
                          <span className="text-xs font-extrabold text-emerald-400 uppercase tracking-wide">📐 Công thức sống còn bắt buộc nhớ:</span>
                          <div className="space-y-2">
                            {(cheatSheetData.must_remember_formulas || []).map((formula, fIdx) => (
                              <div key={fIdx} className="bg-slate-900 p-3 rounded-xl border border-slate-800 font-mono text-xs text-emerald-300 flex items-center gap-2">
                                <span>⚡</span>
                                <span>{formula}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* TOP EXAM TRAPS */}
                        <div className="bg-slate-950 p-5 rounded-2xl border border-rose-500/30 space-y-3">
                          <span className="text-xs font-extrabold text-rose-400 uppercase tracking-wide">⚠️ Top 3 bẫy đề thi mất điểm nhiều nhất:</span>
                          <div className="space-y-2">
                            {(cheatSheetData.top_exam_traps || []).map((trap, tIdx) => (
                              <div key={tIdx} className="bg-rose-950/20 p-3 rounded-xl border border-rose-500/30 text-xs text-rose-200 flex items-start gap-2">
                                <span className="text-rose-400 font-bold">●</span>
                                <span>{trap}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* SUB-TAB 4: FLASHCARDS SM-2 */}
                {studyRoomTab === "FLASHCARDS" && (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 lg:p-8 shadow-xl space-y-6 flex flex-col items-center justify-center text-center">
                    <div>
                      <span className="px-3 py-1 rounded-full text-xs font-black bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        🗂️ THẺ GHI NHỚ NGẮT QUÃNG SM-2 (SPACED REPETITION)
                      </span>
                      <h3 className="text-xl font-bold text-white mt-2">Flashcard Thông Minh (Thẻ {cardIdx + 1} / {flashcardsList.length || 1})</h3>
                      <p className="text-xs text-slate-400 mt-1">Bấm vào thẻ để lật mặt sau xem đáp án và giải thích sâu sắc.</p>
                    </div>

                    {flashcardsList.length > 0 ? (
                      <div className="w-full max-w-xl space-y-6">
                        {/* 3D FLIP CARD */}
                        <div
                          onClick={() => setIsCardFlipped(!isCardFlipped)}
                          className={`w-full min-h-[220px] p-8 rounded-3xl border transition cursor-pointer flex flex-col justify-between shadow-2xl ${isCardFlipped ? 'bg-gradient-to-br from-indigo-950 to-slate-900 border-indigo-500/60' : 'bg-slate-950 border-slate-800 hover:border-indigo-500/40'}`}
                        >
                          <div className="flex justify-between items-center text-xs text-slate-500">
                            <span className="font-mono font-bold text-indigo-400">{flashcardsList[cardIdx]?.topic_code}</span>
                            <span>{isCardFlipped ? "Mặt Sau (Lời Giải)" : "Mặt Trước (Câu Hỏi)"}</span>
                          </div>

                          <div className="my-auto py-4">
                            <p className="text-base sm:text-lg font-bold text-white leading-relaxed">
                              {isCardFlipped ? flashcardsList[cardIdx]?.back : flashcardsList[cardIdx]?.front}
                            </p>
                            {isCardFlipped && (
                              <p className="text-xs text-indigo-300 bg-indigo-950/60 p-3 rounded-xl border border-indigo-500/30 mt-4 text-left">
                                💡 <strong>Key Insight:</strong> {flashcardsList[cardIdx]?.key_insight}
                              </p>
                            )}
                          </div>

                          <span className="text-[11px] text-slate-500">
                            {isCardFlipped ? "Bấm lại để xem câu hỏi" : "Bấm vào thẻ để xem đáp án"}
                          </span>
                        </div>

                        {/* RATING BUTTONS */}
                        <div className="flex gap-3 justify-center">
                          <button
                            onClick={() => {
                              setIsCardFlipped(false);
                              setCardIdx((cardIdx + 1) % flashcardsList.length);
                            }}
                            className="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs px-5 py-2.5 rounded-xl border border-slate-700 transition"
                          >
                            Đã nhớ tốt ✓ Tiếp theo →
                          </button>
                        </div>
                      </div>
                    ) : (
                      <p className="text-xs text-slate-400">Đang tải thẻ ghi nhớ Flashcard...</p>
                    )}
                  </div>
                )}

              </div>
            )}

          </main>

          {/* ======================================================= */}
          {/* MODAL 1: 3-TIER RECOMMENDATION PRESENTATION MODAL */}
          {/* ======================================================= */}
          {isSearchModalOpen && searchModalData && (
            <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-4 overflow-y-auto">
              <div className="bg-slate-900 border border-indigo-500/40 rounded-3xl max-w-4xl w-full shadow-2xl p-6 lg:p-8 space-y-6 my-auto max-h-[92vh] flex flex-col overflow-hidden">

                {/* MODAL HEADER */}
                <div className="border-b border-slate-800 pb-4 flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        {searchModalData.matched_subject.code}
                      </span>
                      <span className="text-xs font-bold text-amber-400 bg-amber-500/10 px-2.5 py-0.5 rounded-full border border-amber-500/20">
                        🎯 Mục tiêu: {searchModalData.target_score} Điểm ({searchModalData.tier3_score_strategy.grade_letter})
                      </span>
                    </div>
                    <h3 className="text-xl lg:text-2xl font-black text-white">
                      {searchModalData.matched_subject.title}
                    </h3>
                    <p className="text-xs text-slate-400 mt-1 max-w-2xl">
                      {searchModalData.matched_subject.description}
                    </p>
                  </div>
                  <button
                    onClick={() => setIsSearchModalOpen(false)}
                    className="w-9 h-9 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center font-bold"
                  >
                    ✕
                  </button>
                </div>

                {/* MODAL SCROLLABLE CONTENT */}
                <div className="overflow-y-auto space-y-6 pr-1">

                  {/* TẦNG 1: TÀI LIỆU WEB & OFFICIAL DOCS CHỌN LỌC */}
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-xs font-bold">1</span>
                      <h4 className="text-sm font-extrabold text-white uppercase tracking-wider flex items-center gap-1.5">
                        <span>🌐 TẦNG 1: TÀI LIỆU WEB & OFFICIAL DOCS CHÍNH THỐNG</span>
                        <span className="text-[10px] text-indigo-400 font-semibold normal-case">(Tự học & Tra cứu sâu)</span>
                      </h4>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {(searchModalData.tier1_web_resources || []).map((web, wIdx) => (
                        <div key={wIdx} className="bg-slate-950 p-4 rounded-2xl border border-slate-800 hover:border-indigo-500/40 transition flex flex-col justify-between space-y-2">
                          <div className="space-y-1">
                            <div className="flex justify-between items-center text-[10px]">
                              <span className="font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded">
                                {web.institution}
                              </span>
                              <span className="text-slate-500 font-mono">Độ khó: {web.difficulty_level}/5</span>
                            </div>
                            <h5 className="font-bold text-white text-xs leading-snug">{web.title}</h5>
                            <p className="text-[11px] text-slate-400 line-clamp-2">{web.description}</p>
                          </div>

                          <div className="pt-2 border-t border-slate-800/80">
                            <a
                              href={web.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-xs text-indigo-400 hover:text-indigo-300 font-bold inline-flex items-center gap-1"
                            >
                              <span>Mở tài liệu đọc ↗</span>
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* TẦNG 2: VIDEO BÀI GIẢNG YOUTUBE CHẤT LƯỢNG CAO */}
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center text-xs font-bold">2</span>
                      <h4 className="text-sm font-extrabold text-white uppercase tracking-wider flex items-center gap-1.5">
                        <span>📺 TẦNG 2: VIDEO BÀI GIẢNG YOUTUBE CHỌN LỌC</span>
                        <span className="text-[10px] text-rose-400 font-semibold normal-case">(Trực quan hóa bản chất)</span>
                      </h4>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {(searchModalData.tier2_youtube_videos || []).map((yt, yIdx) => (
                        <div key={yIdx} className="bg-slate-950 p-4 rounded-2xl border border-slate-800 hover:border-rose-500/40 transition flex flex-col justify-between space-y-2">
                          <div className="space-y-1">
                            <div className="flex justify-between items-center text-[10px]">
                              <span className="font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded">
                                📺 {yt.channel}
                              </span>
                              <span className="text-slate-500 font-mono">⏱️ ~{yt.duration_minutes} phút</span>
                            </div>
                            <h5 className="font-bold text-white text-xs leading-snug">{yt.title}</h5>
                            <p className="text-[11px] text-slate-400 line-clamp-2">{yt.description}</p>
                          </div>

                          <div className="pt-2 border-t border-slate-800/80">
                            <a
                              href={yt.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-xs text-rose-400 hover:text-rose-300 font-bold inline-flex items-center gap-1"
                            >
                              <span>Xem video bài giảng ↗</span>
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* TẦNG 3: BỘ CÔNG CỤ CHINH PHỤC ĐIỂM SỐ CỦA AEGIS LEARN */}
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold">3</span>
                      <h4 className="text-sm font-extrabold text-white uppercase tracking-wider flex items-center gap-1.5">
                        <span>🏆 TẦNG 3: BỘ CÔNG CỤ CHINH PHỤC ĐIỂM SỐ CỦA AEGIS LEARN</span>
                        <span className="text-[10px] text-emerald-400 font-semibold normal-case">(Tối ưu hóa điểm thi)</span>
                      </h4>
                    </div>

                    <div className="bg-slate-950 p-5 rounded-2xl border border-indigo-500/30 space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                        <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                          <span className="text-slate-400 block">Thời gian học ước tính</span>
                          <span className="text-base font-bold text-indigo-400">⏱️ {searchModalData.tier3_score_strategy.estimated_study_hours} giờ</span>
                        </div>
                        <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                          <span className="text-slate-400 block">Cam kết mỗi ngày</span>
                          <span className="text-base font-bold text-amber-400">📅 {searchModalData.tier3_score_strategy.daily_commitment_minutes} phút/ngày</span>
                        </div>
                        <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                          <span className="text-slate-400 block">Tiêu chuẩn đầu ra</span>
                          <span className="text-base font-bold text-emerald-400">{searchModalData.tier3_score_strategy.grade_letter}</span>
                        </div>
                      </div>

                      {/* ACTION PLAN */}
                      <div className="space-y-2">
                        <span className="text-xs font-bold text-slate-300 block">Kế hoạch 5 bước độc quyền từ Aegis Learn:</span>
                        {(searchModalData.tier3_score_strategy.action_plan || []).map((act, aIdx) => (
                          <div key={aIdx} className="text-xs text-slate-300 flex items-start gap-2 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                            <span className="text-emerald-400 font-bold">✓</span>
                            <span>{act}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                </div>

                {/* MODAL FOOTER */}
                <div className="pt-4 border-t border-slate-800 flex flex-col sm:flex-row gap-3">
                  <button
                    onClick={() => handleApplySubjectFromSearch(searchModalData.matched_subject)}
                    className="flex-1 bg-gradient-to-r from-indigo-600 via-violet-600 to-purple-600 hover:from-indigo-500 hover:to-violet-500 text-white font-black text-sm py-3.5 px-6 rounded-2xl transition shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2"
                  >
                    <span>🚀 Bắt Đầu Học Môn Này Ngay ({searchModalData.matched_subject.title})</span>
                    <span>→</span>
                  </button>
                  <button
                    onClick={() => setIsSearchModalOpen(false)}
                    className="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs px-5 py-3 rounded-2xl transition border border-slate-700"
                  >
                    Đóng
                  </button>
                </div>

              </div>
            </div>
          )}

          {/* ======================================================= */}
          {/* MODAL 2: QUIZ PLAYER MODAL */}
          {/* ======================================================= */}
          {activeQuiz && (
            <div className="fixed inset-0 bg-slate-950/90 backdrop-blur-md z-50 flex items-center justify-center p-4 overflow-y-auto">
              <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full shadow-2xl p-6 lg:p-8 space-y-6 my-auto max-h-[95vh] flex flex-col overflow-hidden">
                <div className="flex justify-between items-center border-b border-slate-800 pb-4">
                  <div>
                    <h3 className="text-base font-bold text-white">{activeQuiz.title}</h3>
                    <span className="text-xs text-indigo-400">
                      Đã chọn {Object.keys(quizAnswers).length} / {activeQuiz.questions?.length || 0} câu
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-mono font-bold text-amber-400 bg-amber-500/10 px-3 py-1 rounded-xl border border-amber-500/20">
                      ⏱️ {formatPomodoro(quizTimer)}
                    </span>
                    <button onClick={() => setActiveQuiz(null)} className="text-slate-400 hover:text-white font-bold text-sm">✕</button>
                  </div>
                </div>

                {/* QUESTIONS */}
                <div className="overflow-y-auto space-y-6 pr-2">
                  {(activeQuiz.questions || []).map((q, idx) => (
                    <div key={q.id} className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3">
                      <span className="text-xs font-bold text-indigo-400">Câu {idx + 1}:</span>
                      <h4 className="text-sm font-bold text-white leading-relaxed">{q.content}</h4>

                      <div className="space-y-2">
                        {Object.keys(q.options || {}).map(optKey => {
                          const isSelected = quizAnswers[q.id] === optKey;
                          return (
                            <button
                              key={optKey}
                              onClick={() => setQuizAnswers(prev => ({ ...prev, [q.id]: optKey }))}
                              className={`w-full text-left p-3.5 rounded-xl text-xs font-medium transition flex items-center gap-3 border ${isSelected ? 'bg-indigo-600 text-white border-indigo-500 shadow-md' : 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800'}`}
                            >
                              <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs shrink-0 ${isSelected ? 'bg-white text-indigo-600' : 'bg-slate-800 text-slate-400'}`}>
                                {optKey}
                              </span>
                              <span className="flex-1">{q.options[optKey]}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>

                {/* FOOTER */}
                <div className="pt-4 border-t border-slate-800 flex justify-between items-center">
                  <span className="text-xs text-slate-400">
                    Hãy kiểm tra kỹ các câu hỏi trước khi nộp bài
                  </span>
                  <button
                    onClick={handleSubmitQuiz}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-6 py-3 rounded-xl transition shadow-lg shadow-emerald-600/30"
                  >
                    Nộp Bài Kiểm Tra ✓
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* ======================================================= */}
          {/* MODAL 3: INSTANT RESULT MODAL */}
          {/* ======================================================= */}
          {instantResultModal && (
            <QuizResultModal
              result={instantResultModal}
              onReviewDetails={() => {
                setActiveReviewDetailModal(instantResultModal);
                setInstantResultModal(null);
              }}
              onRetake={() => {
                setInstantResultModal(null);
                handleStartTopicDrill(selectedTopicId, 3.0);
              }}
              onClose={() => setInstantResultModal(null)}
            />
          )}

          {/* ======================================================= */}
          {/* MODAL 4: DETAILED REVIEW SCREEN MODAL */}
          {/* ======================================================= */}
          {activeReviewDetailModal && (
            <QuizReviewScreen
              attemptDetail={activeReviewDetailModal}
              onClose={() => setActiveReviewDetailModal(null)}
              onRetake={() => {
                setActiveReviewDetailModal(null);
                handleStartTopicDrill(selectedTopicId, 3.0);
              }}
            />
          )}

        </div>
      );
    }
'''

new_content = content[:start_idx] + new_student_app + "\n" + content[end_idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("[SUCCESS] Rebuilt index.html with 5 Workspaces and 3-Tier Search Recommendation Modal!")
