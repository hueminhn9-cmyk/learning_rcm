"""
Master Seed & ETL Pipeline: Seed Database SQLite 'learning_app.db'
Chuyên ngành duy nhất: "LẬP TRÌNH PYTHON & TRÍ TUỆ NHÂN TẠO (AI & MACHINE LEARNING)"
Đồng bộ 100% Tiếng Việt Chuyên ngành & Dữ liệu thật Kaggle EdX/OULAD.
Tổ chức chuẩn sư phạm: 5 Bài học rõ ràng -> Ngân hàng câu hỏi phân loại theo bài.
"""

import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import (
    Base, User, UserProfile, Subject, Topic, TopicPrerequisite,
    LearningMaterial, Question, Assessment, AssessmentQuestion, AssessmentResult, RecommendationConfig,
    KnowledgeProfile, PersonalNote, ContentFeedback,
    UserRole, MaterialType, QuestionType, AssessmentType, MasteryStatus
)

DATABASE_URL = "sqlite:///./learning_app.db"

def map_difficulty(level_str: str) -> float:
    if not isinstance(level_str, str):
        return 3.0
    level_lower = level_str.lower()
    if "beginner" in level_lower or "introductory" in level_lower:
        return 2.0
    elif "intermediate" in level_lower:
        return 3.5
    elif "advanced" in level_lower:
        return 4.5
    return 3.0

def run_seed_pipeline():
    print("[SEED] BAT DAU CHAY SEED DATA PIPELINE: PYTHON & TRI TUE NHAN TAO (AI)...")
    
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("[SEED] Da lam sach va khoi tao lai cau truc bang CSDL SQLite thanh cong!")

    with Session(engine) as session:
        # 1. Tạo Tài khoản User (Admin & Student)
        admin_user = User(email="admin@aegislearn.edu.vn", hashed_password="hashed_admin_pass", role=UserRole.ADMIN)
        student_user = User(email="student.a@aegislearn.edu.vn", hashed_password="hashed_student_pass", role=UserRole.STUDENT)
        session.add_all([admin_user, student_user])
        session.flush()

        student_profile = UserProfile(
            user_id=student_user.id,
            full_name="Nguyễn Văn A",
            learning_style="VISUAL",
            preferences={"preferred_format": "VIDEO", "daily_goal_minutes": 45},
            study_streak_days=5,
            total_study_minutes=420,
            exp_points=350
        )
        session.add(student_profile)

        # 2. Tạo Môn học duy nhất: Lập trình Python & Trí tuệ Nhân tạo
        subject_ai = Subject(
            code="AI101",
            title="Chuyên ngành Lập trình Python & Trí tuệ Nhân tạo (AI Fundamentals)",
            description="Lộ trình đào tạo chuẩn sư phạm 5 bài học từ Lập trình Python căn bản đến Xây dựng Mô hình AI thực tế."
        )
        session.add(subject_ai)
        session.flush()

        # 3. Tạo Đồ thị tiên quyết (DAG) gồm 5 Bài học chuẩn sư phạm
        topics_data = [
            (101, "PY101", "Bài 1: Cú pháp Python cơ bản & Cấu trúc dữ liệu", "Cú pháp Python, biến, cấu trúc List/Dict, khai báo Hàm và thao tác Xử lý File text/json.", 1),
            (102, "PY102", "Bài 2: Xử lý Mảng & Ma trận với NumPy", "Khởi tạo mảng ndarray, các phép toán đại số mảng vector, nhát cắt slicing và biến đổi hình dạng reshape (Tiên quyết: Bài 1).", 2),
            (103, "PY103", "Bài 3: Phân tích & Làm sạch Dữ liệu với Pandas", "Thao tác DataFrames, lọc dữ liệu với loc/iloc, xử lý khuyết thiếu fillna/dropna, gộp nhóm groupby (Tiên quyết: Bài 2).", 3),
            (104, "MATH101", "Bài 4: Nền tảng Toán & Tối ưu hóa Gradient Descent", "Đại số tuyến tính với NumPy, phép nhân ma trận vector, hàm mất mát MSE và thuật toán tối ưu Gradient Descent (Tiên quyết: Bài 3).", 4),
            (105, "ML101", "Bài 5: Thuật toán Học máy với Scikit-Learn", "Mô hình Hồi quy Linear Regression, Phân loại Logistic Regression, chia tập Train/Test và đánh giá Overfitting (Tiên quyết: Bài 4).", 5)
        ]

        topics = []
        for tid, code, title, desc, idx in topics_data:
            t = Topic(id=tid, subject_id=subject_ai.id, code=code, title=title, description=desc, order_index=idx)
            topics.append(t)
        
        session.add_all(topics)
        session.flush()

        # Tạo Liên kết Tiên quyết DAG (Bài 1 -> Bài 2 -> Bài 3 -> Bài 4 -> Bài 5)
        pre1 = TopicPrerequisite(topic_id=topics[1].id, prerequisite_topic_id=topics[0].id)
        pre2 = TopicPrerequisite(topic_id=topics[2].id, prerequisite_topic_id=topics[1].id)
        pre3 = TopicPrerequisite(topic_id=topics[3].id, prerequisite_topic_id=topics[2].id)
        pre4 = TopicPrerequisite(topic_id=topics[4].id, prerequisite_topic_id=topics[3].id)
        session.add_all([pre1, pre2, pre3, pre4])

        # 4. Hồ sơ Năng lực Kiến thức ban đầu của Sinh viên (KnowledgeProfile)
        kp1 = KnowledgeProfile(user_id=student_user.id, topic_id=topics[0].id, status=MasteryStatus.MASTERED, mastery_score=90.0)
        kp2 = KnowledgeProfile(user_id=student_user.id, topic_id=topics[1].id, status=MasteryStatus.MASTERED, mastery_score=80.0)
        kp3 = KnowledgeProfile(user_id=student_user.id, topic_id=topics[2].id, status=MasteryStatus.WEAK, mastery_score=45.0)
        kp4 = KnowledgeProfile(user_id=student_user.id, topic_id=topics[3].id, status=MasteryStatus.NEEDS_ASSESSMENT, mastery_score=0.0)
        kp5 = KnowledgeProfile(user_id=student_user.id, topic_id=topics[4].id, status=MasteryStatus.NEEDS_ASSESSMENT, mastery_score=0.0)
        session.add_all([kp1, kp2, kp3, kp4, kp5])

        # 5. Kho Học liệu Chuẩn Tiếng Việt & Dữ liệu EdX Kaggle (`learning_materials`)
        edx_materials_data = [
            # Bài 1: PY101
            {"topic_id": 101, "title": "Video: Cú pháp Python & Cấu trúc dữ liệu List, Dictionary", "univ": "MITx", "type": MaterialType.VIDEO, "url": "https://docs.python.org/3/tutorial/", "diff": 2.0, "text": "Bài giảng nhập môn cú pháp Python, cách khai báo biến, câu lệnh điều kiện if-else, vòng lặp for/while và các thao tác chuẩn trên List và Dictionary."},
            {"topic_id": 101, "title": "Bài đọc: Khai báo Hàm & Xử lý File trong Python", "univ": "HarvardX", "type": MaterialType.READING, "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions", "diff": 2.5, "text": "Tài liệu chi tiết hướng dẫn định nghĩa hàm def, truyền tham số, giá trị trả về return và kỹ thuật đọc/ghi file văn bản with open()."},
            {"topic_id": 101, "title": "Slide: Lập trình Hướng đối tượng OOP trong Python", "univ": "IBM", "type": MaterialType.SLIDE, "url": "https://docs.python.org/3/tutorial/classes.html", "diff": 3.0, "text": "Slide tổng quan về Class, Object, thuộc tính self, hàm khởi tạo __init__ và tính đóng gói trong Python."},

            # Bài 2: PY102 (NumPy)
            {"topic_id": 102, "title": "Video: Thao tác mảng nhiều chiều với NumPy Array", "univ": "IBM", "type": MaterialType.VIDEO, "url": "https://numpy.org/doc/stable/user/quickstart.html", "diff": 3.0, "text": "Hướng dẫn khởi tạo mảng ndarray, các phép toán đại số mảng vector, reshape và cắt mảng slicing cực nhanh với NumPy."},
            {"topic_id": 102, "title": "Bài đọc: Phép toán Vector & Đại số Mảng NumPy", "univ": "MITx", "type": MaterialType.READING, "url": "https://numpy.org/doc/stable/user/absolute_beginners.html", "diff": 3.2, "text": "Tài liệu chuyên sâu về Broadcasting, tích vô hướng np.dot() và các hàm thống kê np.mean(), np.std() trên mảng NumPy."},
            {"topic_id": 102, "title": "Slide: Kỹ thuật Indexing & Slicing trên Ma trận NumPy", "univ": "edX", "type": MaterialType.SLIDE, "url": "https://numpy.org/doc/stable/user/basics.indexing.html", "diff": 3.0, "text": "Slide minh họa truy xuất phần tử 2D, chọn hàng/cột và lọc mảng theo điều kiện Boolean Indexing."},

            # Bài 3: PY103 (Pandas)
            {"topic_id": 103, "title": "Video: Phân tích Dữ liệu Bảng với Pandas DataFrames", "univ": "HarvardX", "type": MaterialType.VIDEO, "url": "https://pandas.pydata.org/docs/getting_started/index.html", "diff": 3.5, "text": "Hướng dẫn đọc file CSV/Excel bằng pd.read_csv(), thao tác trên DataFrames và các kỹ thuật khám phá dữ liệu EDA."},
            {"topic_id": 103, "title": "Bài đọc: Làm sạch Dữ liệu & Xử lý Giá trị Khuyết thiếu NaN", "univ": "IBM", "type": MaterialType.READING, "url": "https://pandas.pydata.org/docs/user_guide/missing_data.html", "diff": 3.5, "text": "Kỹ thuật lọc dữ liệu với loc/iloc, điền giá trị khuyết fillna(), xóa dữ liệu trống dropna() và nhóm dữ liệu bằng groupby()."},
            {"topic_id": 103, "title": "Slide: Trực quan hóa Dữ liệu Pandas với Matplotlib & Seaborn", "univ": "edX", "type": MaterialType.SLIDE, "url": "https://pandas.pydata.org/docs/user_guide/visualization.html", "diff": 3.0, "text": "Slide hướng dẫn vẽ biểu đồ đường, biểu đồ cột, scatter plot và heatmap biểu diễn tương quan dữ liệu."},

            # Bài 4: MATH101
            {"topic_id": 104, "title": "Video: Phép nhân Ma trận & Đại số tuyến tính trong AI", "univ": "MITx", "type": MaterialType.VIDEO, "url": "https://www.edx.org/search?q=linear+algebra", "diff": 3.5, "text": "Giải thích bản chất đại số nhân ma trận vector, ma trận chuyển vị và ứng dụng nhân trọng số W*X trong mô hình AI."},
            {"topic_id": 104, "title": "Slide: Thuật toán Tối ưu hóa Gradient Descent & Loss Function", "univ": "Stanford Online", "type": MaterialType.SLIDE, "url": "https://www.edx.org/search?q=gradient+descent", "diff": 4.0, "text": "Slide bài giảng về hàm mất mát MSE, đạo hàm riêng Gradient và thuật toán cập nhật trọng số ngược chiều Gradient Descent."},
            {"topic_id": 104, "title": "Bài đọc: Tốc độ học Learning Rate & Kỹ thuật Chuẩn hóa Dữ liệu", "univ": "HarvardX", "type": MaterialType.READING, "url": "https://scikit-learn.org/stable/modules/preprocessing.html", "diff": 3.5, "text": "Phân tích ảnh hưởng của Learning Rate alpha (quá lớn gây bùng nổ, quá nhỏ gây hội tụ chậm) và phương pháp Standard Scaler."},

            # Bài 5: ML101
            {"topic_id": 105, "title": "Video: Mô hình Hồi quy tuyến tính Linear Regression với Scikit-Learn", "univ": "IBM", "type": MaterialType.VIDEO, "url": "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html", "diff": 3.5, "text": "Hướng dẫn xây dựng mô hình dự đoán giá trị liên tục bằng thư viện sklearn.linear_model.LinearRegression."},
            {"topic_id": 105, "title": "Bài đọc: Mô hình Phân loại Logistic Regression & Hàm Sigmoid", "univ": "HarvardX", "type": MaterialType.READING, "url": "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html", "diff": 4.0, "text": "Lý thuyết phân loại nhị phân, công thức hàm Sigmoid biến đổi giá trị về khoảng (0, 1) và ma trận nhầm lẫn Confusion Matrix."},
            {"topic_id": 105, "title": "Slide: Đánh giá Mô hình Học máy & Hiện tượng Overfitting", "univ": "MITx", "type": MaterialType.SLIDE, "url": "https://scikit-learn.org/stable/modules/cross_validation.html", "diff": 4.0, "text": "Slide giải thích kỹ thuật chia tập Train/Test, các chỉ số Accuracy, Precision, Recall, F1-Score và biện pháp khắc phục Overfitting."}
        ]

        # Nạp thêm từ EdX.csv nếu có file
        edx_csv_path = os.path.join("dataset", "EdX.csv")
        if os.path.exists(edx_csv_path):
            print("[SEED] Dang nap bo sung danh muc tu Kaggle EdX.csv...")
            try:
                df_edx = pd.read_csv(edx_csv_path).dropna(subset=["Name"]).head(100)
                topic_working_urls = {
                    101: "https://docs.python.org/3/tutorial/",
                    102: "https://numpy.org/doc/stable/user/quickstart.html",
                    103: "https://pandas.pydata.org/docs/getting_started/index.html",
                    104: "https://scikit-learn.org/stable/modules/sgd.html",
                    105: "https://scikit-learn.org/stable/tutorial/index.html"
                }

                for idx, row in df_edx.iterrows():
                    diff_val = map_difficulty(str(row.get("Difficulty Level")))
                    assigned_topic = topics[idx % len(topics)]
                    clean_url = topic_working_urls.get(assigned_topic.id, "https://docs.python.org/3/tutorial/")

                    edx_materials_data.append({
                        "topic_id": assigned_topic.id,
                        "title": f"Khóa học EdX: {row['Name']}"[:255],
                        "univ": str(row.get("University") or "edX")[:255],
                        "type": MaterialType.VIDEO if idx % 2 == 0 else MaterialType.READING,
                        "url": clean_url,
                        "diff": diff_val,
                        "text": str(row.get("About") or row.get("Course Description") or "Khóa học Python & AI chất lượng cao từ đối tác EdX.")[:1000]
                    })
            except Exception as e:
                pass

        mat_objects = []
        for mdata in edx_materials_data:
            mat = LearningMaterial(
                topic_id=mdata["topic_id"],
                title=mdata["title"],
                university=mdata["univ"],
                material_type=mdata["type"],
                content_url=mdata["url"],
                text_content=mdata["text"],
                difficulty_level=mdata["diff"],
                version=1,
                is_latest=True,
                created_by_id=admin_user.id
            )
            mat_objects.append(mat)

        session.add_all(mat_objects)
        session.flush()
        print(f"[SEED] Da nap {len(mat_objects)} hoc lieu Python & AI chuan Tieng Viet vao 'learning_materials'!")
        # 6. NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM CHUYÊN BIỆT THEO TỪNG BÀI HỌC (QUESTIONS)
        questions_data = [
            # === BÀI 1: PY101 - CÚ PHÁP PYTHON CƠ BẢN & CẤU TRÚC DỮ LIỆU (12 CÂU) ===
            {
                "topic_id": 101,
                "content": "[Bài 1] Cú pháp đúng để tạo một từ điển (Dictionary) lưu thông tin điểm số trong Python là gì?",
                "options": {"A": "scores = {'Nam': 8.5, 'An': 9.0}", "B": "scores = ['Nam': 8.5, 'An': 9.0]", "C": "scores = ('Nam': 8.5, 'An': 9.0)", "D": "scores = <'Nam': 8.5, 'An': 9.0>"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Trong Python, từ điển (Dictionary) được khởi tạo bằng cặp dấu ngoặc nhọn { } chứa các cặp Key: Value."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Kết quả của đoạn mã Python `print(type([1, 2, 3]))` là gì?",
                "options": {"A": "<class 'list'>", "B": "<class 'array'>", "C": "<class 'tuple'>", "D": "<class 'dict'>"},
                "correct": "A", "difficulty": 1.5,
                "explanation": "Cấu trúc đặt trong dấu ngoặc vuông [ ] là kiểu dữ liệu danh sách List trong Python."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Phương thức nào dùng để thêm một phần tử mới vào cuối danh sách (List) trong Python?",
                "options": {"A": "append()", "B": "add()", "C": "insert_last()", "D": "push()"},
                "correct": "A", "difficulty": 1.5,
                "explanation": "Hàm list.append(item) được dùng để chèn phần tử mới vào cuối danh sách."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Từ khóa nào trong Python được dùng để khai báo một định nghĩa hàm tự tạo?",
                "options": {"A": "def", "B": "function", "C": "func", "D": "define"},
                "correct": "A", "difficulty": 1.5,
                "explanation": "Từ khóa 'def' được dùng để khai báo định nghĩa hàm trong Python."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Cú pháp an toàn nhất để mở và tự động đóng file trong Python là gì?",
                "options": {"A": "with open('data.txt', 'r') as f:", "B": "f = open('data.txt'); f.close()", "C": "open file 'data.txt' as f:", "D": "file.open('data.txt')"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Cú pháp context manager `with open(...) as f:` đảm bảo file luôn được đóng an toàn kể cả khi có ngoại lệ."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Kết quả của biểu thức Python `len({'a': 1, 'b': 2, 'c': 3})` bằng bao nhiêu?",
                "options": {"A": "3", "B": "6", "C": "2", "D": "1"},
                "correct": "A", "difficulty": 1.5,
                "explanation": "Hàm len() trả về số lượng cặp key-value trong từ điển (ở đây có 3 cặp)."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Cho `my_list = [10, 20, 30, 40, 50]`. Kết quả của thao tác cắt lát `my_list[1:4]` là gì?",
                "options": {"A": "[20, 30, 40]", "B": "[10, 20, 30]", "C": "[20, 30, 40, 50]", "D": "[30, 40, 50]"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Cắt lát [start:stop] lấy từ chỉ số start đến stop-1. Ở đây lấy từ index 1 (20) đến 3 (40)."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Cú pháp List Comprehension `[x**2 for x in range(4)]` cho kết quả danh sách nào?",
                "options": {"A": "[0, 1, 4, 9]", "B": "[1, 4, 9, 16]", "C": "[0, 2, 4, 6]", "D": "[0, 1, 2, 3]"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "range(4) sinh ra 0, 1, 2, 3. Bình phương tương ứng là 0, 1, 4, 9."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Hàm ẩn danh (Lambda) `f = lambda a, b: a * b + 2`. Gọi `f(3, 4)` trả về giá trị nào?",
                "options": {"A": "14", "B": "10", "C": "12", "D": "24"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "3 * 4 + 2 = 12 + 2 = 14."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Phương thức `d.get('score', 0)` trên từ điển `d = {'name': 'An'}` sẽ trả về giá trị nào?",
                "options": {"A": "0 (giá trị mặc định fallback)", "B": "Báo lỗi KeyError", "C": "None", "D": "'An'"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Hàm dict.get(key, default) trả về giá trị default an toàn nếu key không tồn tại, tránh gây lỗi KeyError."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Đặc tính quan trọng nhất phân biệt cấu trúc Tuple với List trong Python là gì?",
                "options": {"A": "Tuple có tính bất biến (Immutable), không thể sửa/thêm/xóa sau khi tạo", "B": "Tuple chỉ chứa được số nguyên", "C": "Tuple không thể duyệt qua vòng lặp for", "D": "Tuple chiếm bộ nhớ gấp 10 lần List"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Tuple là kiểu dữ liệu bất biến (immutable), trong khi List là khả biến (mutable)."
            },
            {
                "topic_id": 101,
                "content": "[Bài 1] Trong cấu trúc xử lý ngoại lệ `try ... except ... finally`, khối `finally` có đặc điểm gì?",
                "options": {"A": "Luôn luôn được thực thi dù ngoại lệ có xảy ra hay không", "B": "Chỉ chạy khi có ngoại lệ xảy ra", "C": "Chỉ chạy khi không có ngoại lệ", "D": "Bị bỏ qua nếu chương trình chạy đúng"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Khối finally luôn được chạy, rất thích hợp để giải phóng tài nguyên như đóng file, ngắt kết nối database."
            },

            # === BÀI 2: PY102 - XỬ LÝ MẢNG & MA TRẬN VỚI NUMPY (12 CÂU) ===
            {
                "topic_id": 102,
                "content": "[Bài 2] Thư viện Python nào cung cấp cấu trúc mảng n-chiều (ndarray) tối ưu tốc độ tính toán đại số ma trận?",
                "options": {"A": "NumPy", "B": "Pandas", "C": "Matplotlib", "D": "Requests"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "NumPy cung cấp kiểu mảng ndarray được tối ưu bằng C giúp tính toán số học mảng vector nhanh vượt trội."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Để chuyển đổi mảng 1D 12 phần tử thành mảng 2D kích thước (3, 4) trong NumPy, ta dùng phương thức nào?",
                "options": {"A": "arr.reshape(3, 4)", "B": "arr.resize(3, 4)", "C": "arr.transpose(3, 4)", "D": "arr.convert(3, 4)"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Hàm arr.reshape(3, 4) thay đổi kích thước các chiều của mảng NumPy mà không làm thay đổi dữ liệu."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Hàm nào trong NumPy tạo một ma trận toàn số 0 với kích thước chỉ định?",
                "options": {"A": "np.zeros((3, 3))", "B": "np.nulls((3, 3))", "C": "np.empty_zero((3, 3))", "D": "np.create_zeros((3, 3))"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "np.zeros(shape) tạo mảng NumPy khởi tạo các giá trị bằng 0.0."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Thuộc tính nào của mảng NumPy `arr` cho biết kích thước số hàng và số cột?",
                "options": {"A": "arr.shape", "B": "arr.size", "C": "arr.dimension", "D": "arr.length"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "arr.shape trả về một tuple mô tả số chiều và kích thước từng chiều của mảng."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Kỹ thuật Boolean Indexing `arr[arr > 5]` trong NumPy thực hiện chức năng gì?",
                "options": {"A": "Lọc các phần tử trong mảng arr có giá trị lớn hơn 5", "B": "Gán tất cả phần tử trong mảng bằng 5", "C": "Xóa mảng arr khỏi bộ nhớ", "D": "Đếm số dòng có giá trị lớn hơn 5"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Boolean Indexing áp dụng mặt nạ True/False để trích xuất chính xác các phần tử thỏa mãn điều kiện."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Phép toán nhân từng phần tử tương ứng (element-wise multiplication) giữa 2 mảng NumPy A và B là gì?",
                "options": {"A": "A * B", "B": "A @ B", "C": "np.dot(A, B)", "D": "np.matmul(A, B)"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Trong NumPy, dấu * thực hiện nhân từng phần tử tương ứng, trong khi A @ B hoặc np.dot() là nhân ma trận đại số."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Lệnh `np.arange(1, 10, 2)` trong NumPy sinh ra mảng nào sau đây?",
                "options": {"A": "array([1, 3, 5, 7, 9])", "B": "array([1, 2, 3, 4, 5, 6, 7, 8, 9])", "C": "array([2, 4, 6, 8, 10])", "D": "array([1, 3, 5, 7])"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "np.arange(start, stop, step) sinh ra các phần tử từ 1 đến dưới 10 với bước nhảy 2: 1, 3, 5, 7, 9."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Cơ chế nào trong NumPy cho phép thực hiện phép cộng giữa ma trận 2D (3, 3) và một vector 1D (3,)?",
                "options": {"A": "Broadcasting (Khuếch đại chiều tự động)", "B": "Vector Folding", "C": "Type Casting", "D": "Loop Fusion"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Broadcasting tự động sao chép ảo các chiều có kích thước 1 để thực hiện phép toán số học song song hiệu quả."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Trong NumPy, hàm nào dùng để tính giá trị trung bình cộng của tất cả các phần tử trong mảng?",
                "options": {"A": "np.mean(arr)", "B": "np.average_all(arr)", "C": "np.mid(arr)", "D": "np.sum_div(arr)"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "np.mean(arr) tính giá trị trung bình cộng của mảng."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Tham số `axis=0` trong hàm `np.sum(matrix, axis=0)` thực hiện phép tính theo hướng nào?",
                "options": {"A": "Tính tổng theo từng cột (chiều dọc, gộp các hàng)", "B": "Tính tổng theo từng hàng (chiều ngang)", "C": "Tính tổng toàn bộ ma trận ra một số duy nhất", "D": "Tính tổng đường chéo chính"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "axis=0 chỉ chiều dọc (dọc theo các hàng), kết quả là mảng 1D chứa tổng từng cột."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Cú pháp `arr.T` trên một ma trận 2D NumPy thực hiện thao tác gì?",
                "options": {"A": "Chuyển vị ma trận (Transpose: đổi hàng thành cột)", "B": "Nghịch đảo ma trận", "C": "Chuẩn hóa ma trận về [0, 1]", "D": "Cắt ma trận thành 2 nửa"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "arr.T trả về ma trận chuyển vị của mảng arr."
            },
            {
                "topic_id": 102,
                "content": "[Bài 2] Hàm nào trong NumPy dùng để ghép nối hai ma trận có cùng số cột chồng lên nhau theo chiều dọc?",
                "options": {"A": "np.vstack([A, B])", "B": "np.hstack([A, B])", "C": "np.dstack([A, B])", "D": "np.c_[A, B]"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "np.vstack nối mảng theo chiều thẳng đứng (vertical stack), tức là thêm hàng mới."
            },

            # === BÀI 3: PY103 - PHÂN TÍCH & LÀM SẠCH DỮ LIỆU VỚI PANDAS (12 CÂU) ===
            {
                "topic_id": 103,
                "content": "[Bài 3] Trong Pandas, hàm nào được sử dụng phổ biến nhất để đọc dữ liệu từ file CSV thành DataFrame?",
                "options": {"A": "pd.read_csv()", "B": "pd.open_csv()", "C": "pd.load_csv()", "D": "pd.parse_csv()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "pd.read_csv('filename.csv') là hàm chuẩn nạp tập dữ liệu bảng CSV vào Pandas DataFrame."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Trong Pandas DataFrame, thuộc tính `.loc[]` dùng để truy xuất dữ liệu theo phương thức nào?",
                "options": {"A": "Theo Nhãn (Label) tên hàng và tên cột", "B": "Theo Chỉ số số nguyên (Integer index)", "C": "Theo giá trị ngẫu nhiên", "D": "Theo dung lượng dữ liệu"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "df.loc[] định vị dữ liệu dựa trên tên nhãn cột/hàng, còn df.iloc[] dựa trên vị trí số nguyên."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Phương thức nào trong Pandas được dùng để điền giá trị thay thế cho các ô dữ liệu bị khuyết thiếu (NaN)?",
                "options": {"A": "fillna()", "B": "dropna()", "C": "replace_null()", "D": "clean_nan()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.fillna(value) thay thế các giá trị khuyết thiếu NaN bằng giá trị chỉ định."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Phương thức nào trong Pandas giúp gộp nhóm dữ liệu theo một cột để tính các chỉ số thống kê (Mean, Sum)?",
                "options": {"A": "groupby()", "B": "aggregate()", "C": "pivot_table()", "D": "sort_values()"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "df.groupby('col_name').mean() gom nhóm các hàng cùng giá trị để tính chỉ số thống kê."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Phương thức nào trong Pandas loại bỏ hoàn toàn các hàng có chứa giá trị khuyết thiếu (NaN)?",
                "options": {"A": "dropna()", "B": "remove_null()", "C": "clear_nan()", "D": "delete_missing()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.dropna() loại bỏ các hàng hoặc cột có ô dữ liệu trống NaN."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Thuộc tính `.iloc[]` trong Pandas DataFrame chọn dữ liệu dựa trên tiêu chuẩn nào?",
                "options": {"A": "Vị trí số nguyên (Integer index 0, 1, 2...)", "B": "Tên cột chuỗi văn bản", "C": "Kiểu dữ liệu float64", "D": "Ngày tháng năm"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.iloc[row_idx, col_idx] truy cập chính xác theo tọa độ số nguyên của dòng và cột."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Phương thức `df.info()` trong Pandas cung cấp thông tin gì về bảng dữ liệu?",
                "options": {"A": "Số dòng, số cột, tên các cột, số ô không khuyết thiếu (non-null) và kiểu dữ liệu từng cột", "B": "Chỉ in ra 5 dòng đầu tiên", "C": "Vẽ biểu đồ phân phối dữ liệu", "D": "Xóa toàn bộ các dòng lỗi"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.info() tóm tắt cấu trúc kỹ thuật của DataFrame: kích thước bộ nhớ, kiểu dữ liệu và giá trị non-null."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Để đếm số lần xuất hiện của từng giá trị khác nhau trong cột `df['gender']`, ta dùng lệnh nào?",
                "options": {"A": "df['gender'].value_counts()", "B": "df['gender'].count_unique()", "C": "df['gender'].freq()", "D": "df['gender'].group_count()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "Series.value_counts() tính bảng phân phối tần suất của các giá trị phân loại."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Lệnh nào kiểm tra và tính tổng số ô khuyết thiếu (NaN) trên từng cột của DataFrame?",
                "options": {"A": "df.isna().sum()", "B": "df.null_total()", "C": "df.count_missing()", "D": "df.empty_sum()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.isna().sum() tạo mặt nạ boolean các ô NaN và cộng tổng lại trên từng cột."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Để xóa cột `id_assessment` khỏi DataFrame `df`, cú pháp chuẩn nào được sử dụng?",
                "options": {"A": "df.drop(columns=['id_assessment'])", "B": "df.delete('id_assessment')", "C": "df.remove_column('id_assessment')", "D": "del df['id_assessment']"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.drop(columns=['col_name']) hoặc df.drop('col_name', axis=1) là cú pháp chuẩn xóa cột trong Pandas."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Phương thức `df['score'].apply(lambda x: x * 10)` thực hiện chức năng gì?",
                "options": {"A": "Nhân 10 với từng giá trị trong cột score", "B": "Lọc các dòng có điểm lớn hơn 10", "C": "Xóa cột score", "D": "Tạo 10 cột score mới"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "apply() áp dụng hàm truyền vào lên từng phần tử của Series."
            },
            {
                "topic_id": 103,
                "content": "[Bài 3] Để loại bỏ các hàng trùng lặp hoàn toàn trong DataFrame, phương thức nào được dùng?",
                "options": {"A": "df.drop_duplicates()", "B": "df.remove_same()", "C": "df.unique_rows()", "D": "df.clean_duplicates()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "df.drop_duplicates() xóa các hàng có nội dung trùng lặp và giữ lại bản ghi đầu tiên."
            },

            # === BÀI 4: MATH101 - NỀN TẢNG TOÁN & TỐI ƯU HÓA GRADIENT DESCENT (12 CÂU) ===
            {
                "topic_id": 104,
                "content": "[Bài 4] Trong thuật toán Gradient Descent, véc-tơ Gradient đại diện cho điều gì của Hàm mất mát (Loss Function)?",
                "options": {"A": "Hướng tăng nhanh nhất của hàm số", "B": "Hướng giảm nhanh nhất của hàm số", "C": "Độ dài đường viền ma trận", "D": "Số lượng cực đại ngẫu nhiên"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "Gradient chỉ hướng tăng nhanh nhất. Do đó tối ưu hóa phải cập nhật trọng số đi NGƯỢC chiều Gradient."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Biểu thức cập nhật trọng số w trong thuật toán Gradient Descent với Tốc độ học alpha là gì?",
                "options": {"A": "w_new = w_old - alpha * grad", "B": "w_new = w_old + alpha * grad", "C": "w_new = w_old * alpha / grad", "D": "w_new = alpha - w_old * grad"},
                "correct": "A", "difficulty": 3.5,
                "explanation": "Công thức cập nhật: w = w - alpha * (dw) để đi xuống điểm cực tiểu của hàm mất mát."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Hàm mất mát Mean Squared Error (MSE) thường được sử dụng cho bài toán Học máy nào?",
                "options": {"A": "Bài toán Hồi quy (Regression)", "B": "Bài toán Phân loại (Classification)", "C": "Bài toán Phân cụm (Clustering)", "D": "Bài toán Học tăng cường"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "MSE đo bình phương khoảng cách giữa giá trị dự đoán liên tục và giá trị thực tế."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Hàm số nào trong Python NumPy được dùng để tính tích ma trận đại số (Matrix Multiplication) giữa 2 ma trận A và B?",
                "options": {"A": "np.dot(A, B) hoặc A @ B", "B": "A * B", "C": "np.multiply(A, B)", "D": "np.cross(A, B)"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Dấu * trong NumPy nhân từng phần tử, còn np.dot() hoặc toán tử @ mới là phép nhân ma trận đại số."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Điều gì xảy ra nếu cài đặt Tốc độ học (Learning Rate alpha) quá lớn trong Gradient Descent?",
                "options": {"A": "Hàm mất mát phân kỳ (Diverge) và nhảy vọt qua điểm tối ưu", "B": "Mô hình hội tụ cực kỳ nhanh và chính xác", "C": "Mô hình bị khóa ở điểm xuất phát", "D": "Trọng số bằng 0 tuyệt đối"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "Learning Rate quá lớn khiến bước nhảy quá dài, vượt qua cực tiểu làm Loss phân kỳ bùng nổ."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Độ đo Cosine Similarity giữa 2 véc-tơ đặc trưng bằng 1.0 thể hiện điều gì?",
                "options": {"A": "Hai véc-tơ hoàn toàn trùng hướng (Tương đồng tuyệt đối)", "B": "Hai véc-tơ vuông góc (Không liên quan)", "C": "Hai véc-tơ ngược hướng hoàn toàn", "D": "Hai véc-tơ có độ dài bằng 0"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Cos(0 deg) = 1.0 nghĩa là góc giữa 2 véc-tơ bằng 0, trùng hướng hoàn toàn."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Trong Hồi quy Tuyến tính $y = wx + b$, đạo hàm riêng của hàm MSE theo $w$ có dạng tỷ lệ thuận với đại lượng nào?",
                "options": {"A": "Tích của sai số dự đoán (y_pred - y_true) và đặc trưng đầu vào x", "B": "Bình phương đặc trưng x", "C": "Căn bậc hai của hệ số chặn b", "D": "Số lượng mẫu N lũy thừa 2"},
                "correct": "A", "difficulty": 3.5,
                "explanation": "Đạo hàm theo w là (2/N) * sum((y_pred - y) * x), phản ánh sai số nhân với giá trị đặc trưng x."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Biến thể Stochastic Gradient Descent (SGD) khác với Batch Gradient Descent truyền thống ở điểm nào?",
                "options": {"A": "SGD chỉ dùng 1 mẫu dữ liệu ngẫu nhiên ở mỗi bước lặp để cập nhật trọng số", "B": "SGD tính toán trên toàn bộ dataset ở mỗi bước lặp", "C": "SGD không cần tính đạo hàm", "D": "SGD chỉ áp dụng cho phân loại 3 lớp"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "SGD dùng 1 mẫu ngẫu nhiên (hoặc Mini-batch dùng 32-64 mẫu), cập nhật nhanh và vượt qua các điểm cực tiểu cục bộ."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Thuật toán Gradient Descent đảm bảo luôn tìm được điểm Cực tiểu Toàn cục (Global Minimum) khi hàm mất mát là hàm gì?",
                "options": {"A": "Hàm lồi (Convex Function)", "B": "Hàm lõm (Concave Function)", "C": "Hàm phi tuyến đa cực trị phức tạp", "D": "Hàm bậc 5 bất kỳ"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "Trên hàm lồi (như MSE trong Hồi quy Tuyến tính), mọi cực tiểu cục bộ đều là cực tiểu toàn cục."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Kỹ thuật Gradient Descent with Momentum giúp giải quyết nhược điểm nào của Gradient Descent cơ bản?",
                "options": {"A": "Giảm dao động ngoằn ngoèo ở các rãnh dốc hẹp và tăng tốc theo hướng gradient nhất quán", "B": "Loại bỏ hoàn toàn tập kiểm thử", "C": "Giảm dung lượng bộ nhớ RAM về 0", "D": "Không cần thiết lập Learning Rate"},
                "correct": "A", "difficulty": 3.5,
                "explanation": "Momentum tích lũy vận tốc từ các bước trước giúp trượt nhanh qua vùng bằng phẳng và giảm dao động ngang."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Tầm quan trọng của việc Chuẩn hóa Đặc trưng (Feature Scaling / Standard Scaler) trước khi chạy Gradient Descent là gì?",
                "options": {"A": "Giúp các đường mức hàm mất mát tròn đều, tránh bước nhảy zigzag và tăng tốc độ hội tụ", "B": "Tăng số lượng dòng dữ liệu lên gấp đôi", "C": "Biến bài toán phi tuyến thành tuyến tính", "D": "Đổi nhãn từ văn bản sang hình ảnh"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "Nếu các đặc trưng có thang đo chênh lệch lớn, hàm mất mát sẽ bị méo hình elip dẹt, Gradient Descent sẽ dao động rất lâu mới hội tụ."
            },
            {
                "topic_id": 104,
                "content": "[Bài 4] Nếu Learning Rate alpha quá nhỏ (ví dụ 1e-8), điều gì sẽ xảy ra?",
                "options": {"A": "Mô hình học cực kỳ chậm, mất rất nhiều Epochs để hội tụ hoặc bị kẹt", "B": "Mô hình bị phân kỳ ra vô cùng", "C": "Mô hình tự động dừng lại ở Epoch 1", "D": "Loss Function bằng 0 ngay lập tức"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Learning rate quá nhỏ làm mỗi bước đi quá ngắn, tốn tài nguyên tính toán và có thể kẹt ở vùng yên ngựa (saddle point)."
            },

            # === BÀI 5: ML101 - THUẬT TOÁN HỌC MÁY VỚI SCIKIT-LEARN (12 CÂU TRẮC NGHIỆM & 2 TỰ LUẬN) ===
            {
                "topic_id": 105,
                "content": "[Bài 5] Hàm Sigmoid f(z) = 1 / (1 + e^-z) biến đổi giá trị đầu ra nằm trong khoảng nào?",
                "options": {"A": "Khoảng (0, 1)", "B": "Khoảng (-1, 1)", "C": "Khoảng (0, +infinity)", "D": "Khoảng (-infinity, +infinity)"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Hàm Sigmoid biến đổi số thực z về xác suất trong khoảng (0, 1) cho bài toán Phân loại nhị phân."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Lớp nào trong thư viện Scikit-Learn được dùng để huấn luyện mô hình Hồi quy tuyến tính Linear Regression?",
                "options": {"A": "sklearn.linear_model.LinearRegression", "B": "sklearn.tree.DecisionTreeRegressor", "C": "sklearn.cluster.KMeans", "D": "sklearn.svm.SVC"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "LinearRegression từ module sklearn.linear_model là lớp chuẩn để fit mô hình hồi quy."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Hiện tượng mô hình đạt điểm số rất cao trên tập Huấn luyện (Train) nhưng kém trên tập Kiểm thử (Test) gọi là gì?",
                "options": {"A": "Overfitting (Học tủ / Quá khớp)", "B": "Underfitting (Chưa khớp)", "C": "Convergence (Hội tụ)", "D": "Normalization"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "Overfitting xảy ra khi mô hình học thuộc lòng nhiễu của tập train làm mất khả năng tổng quát hóa."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Hàm nào trong Scikit-Learn được dùng để chia tập dữ liệu ngẫu nhiên thành tập Train và Test?",
                "options": {"A": "train_test_split()", "B": "split_data()", "C": "cross_val_score()", "D": "partition()"},
                "correct": "A", "difficulty": 2.0,
                "explanation": "from sklearn.model_selection import train_test_split giúp phân chia tập dữ liệu chuẩn."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Độ đo nào đánh giá tỷ lệ các trường hợp dự đoán TÍCH CỰC thực sự đúng trong Ma trận nhầm lẫn (Confusion Matrix)?",
                "options": {"A": "Precision (Độ chính xác tích cực)", "B": "Recall (Độ gợi nhớ)", "C": "Accuracy (Độ chính xác tổng thể)", "D": "Loss"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "Precision = TP / (TP + FP) đo độ chính xác của các dự đoán tích cực."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Kỹ thuật Chuẩn hóa Dữ liệu `StandardScaler` trong Scikit-Learn biến đổi dữ liệu về phân phối có Trung bình (Mean) và Độ lệch chuẩn (Std) bằng bao nhiêu?",
                "options": {"A": "Mean = 0, Std = 1", "B": "Mean = 1, Std = 0", "C": "Mean = 0, Std = 0", "D": "Mean = 100, Std = 15"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "StandardScaler trừ trung bình và chia độ lệch chuẩn, đưa dữ liệu về z-score (Mean=0, Std=1)."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Trong bài toán Phân loại dữ liệu lệch lớp (Imbalanced Data), độ đo nào kết hợp cân bằng giữa Precision và Recall?",
                "options": {"A": "F1-Score (Trung bình điều hòa giữa Precision và Recall)", "B": "Accuracy", "C": "Mean Absolute Error", "D": "R-squared"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "F1-Score = 2 * (Precision * Recall) / (Precision + Recall) là độ đo tối ưu khi dữ liệu mất cân bằng nhãn."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Kỹ thuật Regularization L2 trong Ridge Regression giúp giảm Overfitting bằng cách nào?",
                "options": {"A": "Phạt các trọng số w có độ lớn quá cao bằng số hạng lambda * sum(w_i^2)", "B": "Xóa ngẫu nhiên 50% số hàng dữ liệu", "C": "Tăng số lượng tham số mô hình lên gấp đôi", "D": "Ép toàn bộ trọng số về 0 tuyệt đối"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "L2 regularization co nhỏ độ lớn các trọng số, làm trơn đường biên quyết định và giảm phương sai (variance)."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Phương thức nào trong Scikit-Learn vừa tính toán tham số thống kê (Mean/Std) trên tập Train vừa áp dụng biến đổi lên tập dữ liệu?",
                "options": {"A": "fit_transform()", "B": "predict_proba()", "C": "transform_only()", "D": "score_fit()"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "fit_transform() tính các tham số của transformer trên dữ liệu và biến đổi nó. Lưu ý chỉ dùng trên tập Train!"
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Kỹ thuật K-Fold Cross Validation thực hiện quy trình đánh giá như thế nào?",
                "options": {"A": "Chia dữ liệu thành K phần, lần lượt dùng 1 phần để test và K-1 phần để train, sau đó lấy trung bình điểm", "B": "Chạy mô hình K lần trên cùng một tập dữ liệu", "C": "Nhân bản dữ liệu lên K lần", "D": "Sử dụng K mô hình khác nhau để bầu chọn"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "K-Fold Cross Validation đảm bảo mọi mẫu dữ liệu đều được kiểm thử một lần, cho ước lượng khách quan không phụ thuộc cách chia train/test."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Lớp nào trong `sklearn.preprocessing` được dùng để chuyển đổi các cột đặc trưng chuỗi văn bản danh mục (như 'Đỏ', 'Xanh') thành các cột nhị phân 0/1?",
                "options": {"A": "OneHotEncoder", "B": "MinMaxScaler", "C": "SimpleImputer", "D": "Normalizer"},
                "correct": "A", "difficulty": 2.5,
                "explanation": "OneHotEncoder mã hóa từng giá trị phân loại thành một cột nhị phân riêng biệt (Dummy variables)."
            },
            {
                "topic_id": 105,
                "content": "[Bài 5] Chỉ số AUC-ROC (Area Under the Receiver Operating Characteristic Curve) đo lường khả năng nào của mô hình phân loại?",
                "options": {"A": "Khả năng phân biệt giữa lớp tích cực (Positive) và tiêu cực (Negative) ở mọi ngưỡng xác suất", "B": "Tốc độ huấn luyện trên GPU", "C": "Độ phức tạp tính toán O(N)", "D": "Số lượng đặc trưng cần thiết"},
                "correct": "A", "difficulty": 3.0,
                "explanation": "AUC càng gần 1.0 thể hiện mô hình phân tách giữa hai lớp càng hoàn hảo."
            },
            {
                "topic_id": 105,
                "content": "[Tự luận Dự án] Trình bày quy trình xây dựng Mô hình AI dự đoán nguy cơ trượt môn của sinh viên từ tập dữ liệu OULAD bằng Scikit-Learn.",
                "type": QuestionType.ESSAY,
                "options": {},
                "correct": "Sinh viên nộp báo cáo tự luận...",
                "difficulty": 4.5,
                "explanation": "Sinh viên trình bày kiến trúc Pipeline: Đọc CSV -> Lọc đặc trưng -> Standard Scaler -> Logistic Regression -> Đánh giá F1-score."
            },
            {
                "topic_id": 105,
                "content": "[Tự luận Dự án] Giải thích thuật toán Gradient Descent và tự lập trình mã Python tính đạo hàm cập nhật trọng số cho mô hình Hồi quy tuyến tính.",
                "type": QuestionType.ESSAY,
                "options": {},
                "correct": "Sinh viên nộp mã nguồn Python...",
                "difficulty": 4.5,
                "explanation": "Sinh viên viết hàm Python tự định nghĩa loss MSE và loop cập nhật w = w - lr * dw không dùng thư viện."
            }
        ]

        q_objects = []
        for qd in questions_data:
            q = Question(
                topic_id=qd["topic_id"],
                content=qd["content"],
                question_type=qd.get("type", QuestionType.MULTIPLE_CHOICE),
                options=qd.get("options"),
                correct_answer=qd.get("correct", "A"),
                explanation=qd.get("explanation"),
                difficulty_level=qd.get("difficulty", 2.0)
            )
            q_objects.append(q)

        session.add_all(q_objects)
        session.flush()
        print(f"[SEED] Da nap {len(q_objects)} cau hoi trac nghiem & tu luan phan loai theo tung bai vao 'questions'!")

        # 7. NẠP ĐIỂM THI THỰC TẾ KAGGLE OULAD VÀO CSDL (`assessment_results`)
        ass_path = os.path.join("dataset", "assessments.csv")
        st_ass_path = os.path.join("dataset", "studentAssessment.csv")

        if os.path.exists(ass_path) and os.path.exists(st_ass_path):
            try:
                df_ass = pd.read_csv(ass_path)
                df_st_ass = pd.read_csv(st_ass_path)
                df_merged = pd.merge(df_st_ass, df_ass, on="id_assessment", how="inner").dropna(subset=["score"])

                assessments_to_add = []
                ass_map = {}

                for idx, row in df_ass.drop_duplicates(subset=["id_assessment"]).iterrows():
                    assigned_topic = topics[idx % len(topics)]
                    assessment = Assessment(
                        subject_id=subject_ai.id,
                        topic_id=assigned_topic.id,
                        title=f"Đánh giá Kaggle OULAD - Mod {row['code_module']} {row['code_presentation']}",
                        assessment_type=AssessmentType.WEEKLY_CHECKPOINT if idx % 2 == 0 else AssessmentType.MONTHLY_PROJECT,
                        time_limit_minutes=20 if idx % 2 == 0 else 60,
                        passing_score=60.0
                    )
                    assessments_to_add.append(assessment)
                    ass_map[row["id_assessment"]] = assessment

                session.add_all(assessments_to_add)
                session.flush()

                # Nạp 500 kết quả thi thực tế
                results_to_add = []
                for idx, row in df_merged.head(500).iterrows():
                    ass_obj = ass_map.get(row["id_assessment"])
                    if not ass_obj: continue
                    score_val = float(row["score"])
                    results_to_add.append(AssessmentResult(
                        user_id=student_user.id,
                        assessment_id=ass_obj.id,
                        score=score_val,
                        passed=score_val >= 60.0,
                        user_answers={"q1": "A", "score": score_val},
                        completed_at=datetime.now()
                    ))

                session.add_all(results_to_add)
                print(f"[SEED] Da nap {len(results_to_add)} ban ghi ket qua diem thi thuc te OULAD vao 'assessment_results'!")
            except Exception as e:
                pass

        # 8. Cấu hình Trọng số Khuyến nghị AI
        session.add(RecommendationConfig(
            config_key="RECOMMENDATION_WEIGHTS",
            description="Trọng số hệ thống AI gợi ý học liệu Python & AI",
            weight_value=1.0,
            parameters={"w_prerequisite": 1.5, "w_difficulty_gap": 1.2, "w_bloom_match": 1.0, "min_passing_score": 60.0}
        ))

        session.commit()
        print("\n[SEED] HOAN THANH TAO DU LIEU CO SO CHUYEN NGANH PYTHON & AI CHUAN SU PHAM!")
        print("[SEED] CSDL SQLite san sang tai: ./learning_app.db\n")

if __name__ == "__main__":
    run_seed_pipeline()
