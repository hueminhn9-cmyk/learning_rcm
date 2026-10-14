# -*- coding: utf-8 -*-
"""
Multi-Subject Dynamic Seeder & Kaggle EdX Pipeline
Populates diverse subjects, topics, Kaggle courses, curated YouTube videos,
official Web resources, and comprehensive question banks for the AI curriculum.
"""

import os
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import re
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import (
    Base, User, UserProfile, Subject, Topic, TopicPrerequisite,
    LearningMaterial, Question, Assessment, AssessmentQuestion, AssessmentResult, RecommendationConfig,
    KnowledgeProfile, PersonalNote, ContentFeedback, QuizAttempt, QuizAttemptAnswer,
    UserRole, MaterialType, QuestionType, AssessmentType, MasteryStatus, BloomLevel
)

DATABASE_URL = "sqlite:///./learning_app.db"

# 1. DANH MỤC ĐA MÔN HỌC CHUẨN NGÀNH AI
SUBJECTS_CONFIG = [
    {
        "code": "AI_PYTHON",
        "title": "Lập trình Python & Trí tuệ Nhân tạo (Python for AI & ML)",
        "description": "Nền tảng lập trình Python chuyên sâu, xử lý dữ liệu với NumPy/Pandas, giải thuật tối ưu và mô hình học máy Scikit-Learn.",
        "topics": [
            {"id": 101, "code": "PY101", "title": "Bài 1: Cú pháp Python cơ bản & Cấu trúc dữ liệu", "desc": "Biến, kiểu dữ liệu, List comprehension, Tuple, Dict, Set, hàm và xử lý file.", "order": 1},
            {"id": 102, "code": "PY102", "title": "Bài 2: Xử lý Mảng & Ma trận với NumPy", "desc": "Mảng ndarray, đại số mảng vector, broadcasting, slicing và reshape.", "order": 2},
            {"id": 103, "code": "PY103", "title": "Bài 3: Phân tích & Làm sạch Dữ liệu với Pandas", "desc": "DataFrame, loc/iloc, xử lý dữ liệu khuyết thiếu fillna/dropna, groupby và merge.", "order": 3},
            {"id": 104, "code": "MATH101", "title": "Bài 4: Nền tảng Toán & Tối ưu hóa Gradient Descent", "desc": "Đại số tuyến tính, đạo hàm riêng, hàm mất mát MSE và thuật toán Gradient Descent.", "order": 4},
            {"id": 105, "code": "AI101", "title": "Bài 5: Xây dựng Mô hình Học máy với Scikit-Learn", "desc": "Hồi quy tuyến tính, Logistic Regression, chia tập Train/Test, kiểm soát Overfitting.", "order": 5}
        ],
        "prereqs": [(102, 101), (103, 102), (104, 103), (105, 104)]
    },
    {
        "code": "MATH_AI",
        "title": "Toán học & Tối ưu hóa cho AI (Math Foundations for AI)",
        "description": "Toán học nền tảng bắt buộc của Trí tuệ nhân tạo: Đại số tuyến tính tính toán, Giải tích đa biến, Xác suất thống kê và Suy luận Bayes.",
        "topics": [
            {"id": 201, "code": "MATH201", "title": "Chương 1: Đại số Tuyến tính & Không gian Vector", "desc": "Ma trận, định thức, không gian vector, phép biến đổi tuyến tính, trị riêng và vector riêng (Eigenvalues & Eigenvectors).", "order": 1},
            {"id": 202, "code": "MATH202", "title": "Chương 2: Giải tích Đa biến & Tối ưu hóa Lồi", "desc": "Đạo hàm riêng, ma trận Gradient, ma trận Hessian, tối ưu hóa có điều kiện Lagrange và cực trị hàm số nhiều biến.", "order": 2},
            {"id": 203, "code": "MATH203", "title": "Chương 3: Xác suất Thống kê & Suy luận Bayes", "desc": "Biến ngẫu nhiên, các phân phối xác suất (Gaussian, Bernoulli), định lý Bayes, ước lượng hợp lý cực đại (MLE) và MAP.", "order": 3}
        ],
        "prereqs": [(202, 201), (203, 202)]
    },
    {
        "code": "CS_DSA",
        "title": "Cấu trúc Dữ liệu & Giải thuật AI (Data Structures & Algorithms)",
        "description": "Tư duy giải thuật và cấu trúc dữ liệu nền tảng cho khoa học máy tính: Mảng, Danh sách liên kết, Cây, Đồ thị và Thuật toán tìm kiếm tối ưu.",
        "topics": [
            {"id": 301, "code": "DSA301", "title": "Chương 1: Độ phức tạp Thuật toán & Cấu trúc Tuyến tính", "desc": "Ký pháp Big-O, Phân tích thời gian O(N) / không gian, Danh sách liên kết, Stack và Queue.", "order": 1},
            {"id": 302, "code": "DSA302", "title": "Chương 2: Cây Nhị phân & Hàng đợi Ưu tiên (Trees & Heaps)", "desc": "Cây nhị phân tìm kiếm (BST), Cây AVL cân bằng, Min-Heap, Max-Heap và thuật toán Heap Sort.", "order": 2},
            {"id": 303, "code": "DSA303", "title": "Chương 3: Thuật toán Đồ thị & Tìm kiếm A* trong AI", "desc": "Duyệt BFS, DFS, Thuật toán Dijkstra tìm đường ngắn nhất, Thuật toán heuristic A* trong AI.", "order": 3}
        ],
        "prereqs": [(302, 301), (303, 302)]
    },
    {
        "code": "DB_SQL",
        "title": "Cơ sở Dữ liệu & Truy vấn SQL (Databases & SQL for AI)",
        "description": "Thiết kế cơ sở dữ liệu quan hệ, kỹ thuật viết câu lệnh truy vấn SQL nâng cao, lập chỉ mục Indexing và xử lý dữ liệu lớn.",
        "topics": [
            {"id": 401, "code": "SQL401", "title": "Chương 1: Thiết kế CSDL Quan hệ & Chuẩn hóa (ERD & Normalization)", "desc": "Mô hình ERD, Khóa chính / Khóa ngoại, Các dạng chuẩn hóa dữ liệu 1NF, 2NF, 3NF.", "order": 1},
            {"id": 402, "code": "SQL402", "title": "Chương 2: Truy vấn SQL Nâng cao & Phép nối (Advanced SQL & Joins)", "desc": "INNER JOIN, LEFT JOIN, FULL JOIN, Subqueries lồng nhau, Group By, Having và Window Functions.", "order": 2},
            {"id": 403, "code": "SQL403", "title": "Chương 3: Tối ưu hóa Chỉ mục (Indexing) & CSDL NoSQL", "desc": "Cấu trúc B-Tree Index, Kế hoạch thực thi (EXPLAIN Query Plan), Giới thiệu MongoDB NoSQL cho dữ liệu phi cấu trúc.", "order": 3}
        ],
        "prereqs": [(402, 401), (403, 402)]
    },
    {
        "code": "DEEP_LEARNING",
        "title": "Học Sâu & Mạng Nơ-ron Nhân tạo (Deep Learning & Neural Networks)",
        "description": "Mô hình nơ-ron nhân tạo đa tầng, Mạng tích chập CNN xử lý ảnh, Mạng tuần hoàn RNN/LSTM và kiến trúc Transformer hiện đại.",
        "topics": [
            {"id": 501, "code": "DL501", "title": "Chương 1: Mạng Nơ-ron Nhân tạo & Lan truyền Ngược (Perceptron & Backprop)", "desc": "Hàm kích hoạt (ReLU, Sigmoid), Thuật toán lan truyền ngược (Backpropagation), Tối ưu hóa Adam.", "order": 1},
            {"id": 502, "code": "DL502", "title": "Chương 2: Thị giác Máy tính với Mạng Tích chập CNN (Computer Vision)", "desc": "Lớp tích chập (Convolution), Pooling, Kiến trúc VGG/ResNet, Nhận diện vật thể với YOLO.", "order": 2},
            {"id": 503, "code": "DL503", "title": "Chương 3: Xử lý Ngôn ngữ Tự nhiên & Kiến trúc Transformer (NLP & LLMs)", "desc": "Cơ chế tự chú ý (Self-Attention), Kiến trúc Transformer, Mô hình BERT/GPT và Fine-tuning LLM.", "order": 3}
        ],
        "prereqs": [(502, 501), (503, 502)]
    }
]

# 2. TÀI NGUYÊN YOUTUBE & WEB CHỌN LỌC THEO TỪNG MÔN
CURATED_RESOURCES = {
    "AI_PYTHON": {
        "web": [
            {"title": "Tài liệu Chính thức Ngôn ngữ Python (Python 3 Documentation)", "url": "https://docs.python.org/3/tutorial/", "type": "READING", "level": 2.0, "univ": "Python.org"},
            {"title": "Cẩm nang Tự học NumPy & Phân tích Ma trận (NumPy Official Quickstart)", "url": "https://numpy.org/doc/stable/user/quickstart.html", "type": "READING", "level": 3.0, "univ": "NumPy.org"},
            {"title": "Hướng dẫn Xử lý Bảng Dữ liệu Toàn diện với Pandas (10 Minutes to Pandas)", "url": "https://pandas.pydata.org/docs/user_guide/10min.html", "type": "READING", "level": 3.5, "univ": "Pandas.pydata.org"},
            {"title": "Thực hành Học máy với Thư viện Scikit-Learn (User Guide & Tutorials)", "url": "https://scikit-learn.org/stable/tutorial/index.html", "type": "READING", "level": 3.5, "univ": "Scikit-Learn.org"},
            {"title": "Khóa học Kaggle: Python & Pandas Cấp tốc cho Khoa học Dữ liệu", "url": "https://www.kaggle.com/learn/python", "type": "EXERCISE", "level": 2.5, "univ": "Kaggle Learn"}
        ],
        "youtube": [
            {"title": "Khóa học Python cho Người mới bắt đầu (Full Course 6 Giờ)", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "type": "VIDEO", "level": 2.0, "univ": "freeCodeCamp"},
            {"title": "Trực quan hóa Thuật toán Gradient Descent trong Học máy (StatQuest)", "url": "https://www.youtube.com/watch?v=sDv4f4s2SB8", "type": "VIDEO", "level": 3.5, "univ": "StatQuest with Josh Starmer"},
            {"title": "CS50's Introduction to Programming with Python (Harvard University)", "url": "https://www.youtube.com/watch?v=nLRL_NcnK-4", "type": "VIDEO", "level": 2.5, "univ": "Harvard University"},
            {"title": "Pandas Data Analysis Tutorial: Từ Làm sạch đến Trực quan hóa Dữ liệu", "url": "https://www.youtube.com/watch?v=vmEHCJofslg", "type": "VIDEO", "level": 3.0, "univ": "Keith Galli"}
        ]
    },
    "MATH_AI": {
        "web": [
            {"title": "Giáo trình Toán học cho Học máy (Mathematics for Machine Learning Free Book)", "url": "https://mml-book.github.io/", "type": "READING", "level": 4.0, "univ": "Cambridge University"},
            {"title": "Đại số Tuyến tính Trực quan Tương tác (Immersive Linear Algebra)", "url": "http://immersivemath.com/ila/index.html", "type": "READING", "level": 3.0, "univ": "Immersive Math"},
            {"title": "Kho tài liệu Giải tích & Xác suất Khan Academy", "url": "https://www.khanacademy.org/math/linear-algebra", "type": "EXERCISE", "level": 2.5, "univ": "Khan Academy"}
        ],
        "youtube": [
            {"title": "Bản chất Hình học của Đại số Tuyến tính (Essence of Linear Algebra - 15 Tập)", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "type": "VIDEO", "level": 3.0, "univ": "3Blue1Brown"},
            {"title": "Bản chất của Giải tích & Đạo hàm Đa biến (Essence of Calculus)", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr", "type": "VIDEO", "level": 3.5, "univ": "3Blue1Brown"},
            {"title": "MIT 18.06 Linear Algebra: Bài giảng Đại số Tuyến tính Kinh điển của GS. Gilbert Strang", "url": "https://www.youtube.com/playlist?list=PLE7DDD91010BC51F8", "type": "VIDEO", "level": 3.8, "univ": "MIT OpenCourseWare"},
            {"title": "Xác suất Thống kê cho Machine Learning (StatQuest)", "url": "https://www.youtube.com/watch?v=qBigTkBLU6g", "type": "VIDEO", "level": 3.0, "univ": "StatQuest"}
        ]
    },
    "CS_DSA": {
        "web": [
            {"title": "Trực quan hóa Cấu trúc Dữ liệu & Giải thuật Tương tác (VisuAlgo)", "url": "https://visualgo.net/en", "type": "READING", "level": 3.0, "univ": "National Univ. of Singapore"},
            {"title": "GeeksforGeeks: Cẩm nang Toàn diện Cấu trúc Dữ liệu & Giải thuật", "url": "https://www.geeksforgeeks.org/data-structures/", "type": "READING", "level": 3.5, "univ": "GeeksforGeeks"},
            {"title": "LeetCode: Kho 2000+ Bài tập Luyện phỏng vấn Thuật toán", "url": "https://leetcode.com/explore/", "type": "EXERCISE", "level": 4.0, "univ": "LeetCode"}
        ],
        "youtube": [
            {"title": "Cấu trúc Dữ liệu & Giải thuật Đầy đủ từ A-Z (Full Course 8 Giờ)", "url": "https://www.youtube.com/watch?v=RBSGKlAvoiM", "type": "VIDEO", "level": 3.0, "univ": "freeCodeCamp"},
            {"title": "CS50's Introduction to Computer Science 2024 (Đại học Harvard)", "url": "https://www.youtube.com/watch?v=8mAITcNt710", "type": "VIDEO", "level": 2.5, "univ": "Harvard University"},
            {"title": "Giải thích Thuật toán Tìm đường A* và Dijkstra (Computerphile)", "url": "https://www.youtube.com/watch?v=ySN5Wnu88nE", "type": "VIDEO", "level": 3.5, "univ": "Computerphile"}
        ]
    },
    "DB_SQL": {
        "web": [
            {"title": "Khóa học SQL Tương tác Trực quan (SQLBolt: Learn SQL Interactively)", "url": "https://sqlbolt.com/", "type": "EXERCISE", "level": 2.0, "univ": "SQLBolt"},
            {"title": "W3Schools: Hướng dẫn Lệnh SQL & Thực hành Sandbox", "url": "https://www.w3schools.com/sql/", "type": "READING", "level": 2.5, "univ": "W3Schools"},
            {"title": "Tài liệu Thiết kế Cơ sở Dữ liệu Quan hệ & Chuẩn hóa (PostgreSQL Docs)", "url": "https://www.postgresql.org/docs/", "type": "READING", "level": 3.5, "univ": "PostgreSQL Global"}
        ],
        "youtube": [
            {"title": "Khóa học SQL Toàn diện cho Người mới bắt đầu (Full Course 4 Giờ)", "url": "https://www.youtube.com/watch?v=HXV3zeRRNYc", "type": "VIDEO", "level": 2.5, "univ": "freeCodeCamp"},
            {"title": "Kỹ thuật Thiết kế CSDL & Chuẩn hóa 1NF, 2NF, 3NF (Caleb Curry)", "url": "https://www.youtube.com/watch?v=UrYLYV7WSHM", "type": "VIDEO", "level": 3.0, "univ": "Caleb Curry"},
            {"title": "Tối ưu hóa Truy vấn SQL & Cách thức Chỉ mục B-Tree Index hoạt động", "url": "https://www.youtube.com/watch?v=clhao_8b_k8", "type": "VIDEO", "level": 4.0, "univ": "Hussein Nasser"}
        ]
    },
    "DEEP_LEARNING": {
        "web": [
            {"title": "Giáo trình Học Sâu Miễn phí của Ian Goodfellow & Yoshua Bengio (Deep Learning Book)", "url": "https://www.deeplearningbook.org/", "type": "READING", "level": 4.5, "univ": "MIT Press"},
            {"title": "Hướng dẫn Chính thức Thư viện PyTorch (Deep Learning with PyTorch)", "url": "https://pytorch.org/tutorials/", "type": "READING", "level": 3.5, "univ": "PyTorch.org"},
            {"title": "Hugging Face: Khóa học Xử lý Ngôn ngữ Tự nhiên & Mô hình Transformer", "url": "https://huggingface.co/learn/nlp-course/", "type": "EXERCISE", "level": 4.0, "univ": "Hugging Face"}
        ],
        "youtube": [
            {"title": "Bản chất Mạng Nơ-ron Nhân tạo & Giải thuật Lan truyền ngược (3Blue1Brown)", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi", "type": "VIDEO", "level": 3.5, "univ": "3Blue1Brown"},
            {"title": "Stanford CS231n: Mạng Tích chập CNN cho Thị giác Máy tính (GS. Fei-Fei Li)", "url": "https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv", "type": "VIDEO", "level": 4.5, "univ": "Stanford University"},
            {"title": "Deep Learning Specialization của GS. Andrew Ng (DeepLearning.AI)", "url": "https://www.youtube.com/playlist?list=PLkDaE6sCZn6Ec-XTbcX1uRg2_u4xOEky0", "type": "VIDEO", "level": 3.8, "univ": "DeepLearning.AI"},
            {"title": "Giải thích Kiến trúc Transformer & Cơ chế Tự chú ý Attention (StatQuest)", "url": "https://www.youtube.com/watch?v=zxQyTK8quyY", "type": "VIDEO", "level": 4.0, "univ": "StatQuest"}
        ]
    }
}

# 3. NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM ĐA MÔN CHỌN LỌC
DIVERSE_QUESTIONS = [
    # MÔN: TOÁN HỌC CHO AI (MATH_AI)
    {
        "topic_id": 201,
        "content": "Cho ma trận vuông A kích thước n x n. Nếu định thức det(A) = 0 thì kết luận nào sau đây là CHÍNH XÁC?",
        "options": {"A": "Ma trận A khả nghịch (tồn tại A^-1)", "B": "Ma trận A suy biến (không tồn tại A^-1)", "C": "Các hàng của A độc lập tuyến tính", "D": "Hạng của ma trận rank(A) = n"},
        "correct_answer": "B",
        "explanation": "Khi det(A) = 0, ma trận A bị suy biến (singular matrix), các vector hàng/cột phụ thuộc tuyến tính và không tồn tại ma trận nghịch đảo A^-1.",
        "difficulty": 3.0,
        "bloom": BloomLevel.UNDERSTAND
    },
    {
        "topic_id": 201,
        "content": "Tích vô hướng giữa 2 vector u và v trong không gian Euclid bằng 0 (u . v = 0) biểu thị mối quan hệ hình học gì?",
        "options": {"A": "Hai vector song song cùng chiều", "B": "Hai vector song song ngược chiều", "C": "Hai vector vuông góc (trực giao) với nhau", "D": "Hai vector có độ dài bằng nhau"},
        "correct_answer": "C",
        "explanation": "u . v = ||u|| * ||v|| * cos(theta). Khi cos(theta) = 0 (theta = 90 độ), 2 vector vuông góc trực giao với nhau.",
        "difficulty": 2.5,
        "bloom": BloomLevel.REMEMBER
    },
    {
        "topic_id": 202,
        "content": "Vector Gradient grad(f) của một hàm số nhiều biến f(x, y) tại một điểm chỉ ra điều gì?",
        "options": {"A": "Hướng mà tại đó giá trị hàm số giảm nhanh nhất", "B": "Hướng mà tại đó giá trị hàm số tăng nhanh nhất", "C": "Độ cong của hàm số theo mọi hướng", "D": "Điểm uốn của đồ thị hàm số"},
        "correct_answer": "B",
        "explanation": "Vector Gradient luôn chỉ về hướng hàm số tăng trưởng nhanh nhất (steepest ascent). Do đó thuật toán Gradient Descent phải đi ngược chiều gradient (- grad) để tìm cực tiểu.",
        "difficulty": 3.5,
        "bloom": BloomLevel.UNDERSTAND
    },
    {
        "topic_id": 203,
        "content": "Công thức định lý Bayes biểu diễn xác suất có điều kiện P(A|B) là gì?",
        "options": {"A": "P(A|B) = [P(B|A) * P(A)] / P(B)", "B": "P(A|B) = [P(A|B) * P(B)] / P(A)", "C": "P(A|B) = P(A) * P(B)", "D": "P(A|B) = P(A) + P(B) - P(A và B)"},
        "correct_answer": "A",
        "explanation": "Định lý Bayes: P(A|B) = [P(B|A) * P(A)] / P(B), trong đó P(A) là Prior, P(B|A) là Likelihood, P(B) là Evidence, P(A|B) là Posterior.",
        "difficulty": 3.0,
        "bloom": BloomLevel.APPLY
    },

    # MÔN: CẤU TRÚC DỮ LIỆU & GIẢI THUẬT (CS_DSA)
    {
        "topic_id": 301,
        "content": "Độ phức tạp thời gian trung bình để tìm kiếm một phần tử trong Bảng băm (Hash Table) với hàm băm tốt là bao nhiêu?",
        "options": {"A": "O(1)", "B": "O(log N)", "C": "O(N)", "D": "O(N log N)"},
        "correct_answer": "A",
        "explanation": "Bảng băm tra cứu theo khóa (Key) bằng hàm băm trực tiếp nên có độ phức tạp trung bình lý tưởng là O(1).",
        "difficulty": 2.5,
        "bloom": BloomLevel.REMEMBER
    },
    {
        "topic_id": 301,
        "content": "Cấu trúc dữ liệu nào hoạt động theo nguyên lý LIFO (Last In First Out - Vào sau ra trước)?",
        "options": {"A": "Queue (Hàng đợi)", "B": "Stack (Ngăn xếp)", "C": "Linked List (Danh sách liên kết)", "D": "Binary Search Tree (Cây nhị phân tìm kiếm)"},
        "correct_answer": "B",
        "explanation": "Stack hoạt động theo cơ chế LIFO (phần tử thêm vào cuối cùng sẽ được lấy ra đầu tiên). Ngược lại Queue là FIFO.",
        "difficulty": 2.0,
        "bloom": BloomLevel.REMEMBER
    },
    {
        "topic_id": 302,
        "content": "Trong một Cây nhị phân tìm kiếm (Binary Search Tree), nếu thực hiện duyệt theo thứ tự In-order (Left - Node - Right), dãy khóa nhận được có đặc điểm gì?",
        "options": {"A": "Dãy khóa được sắp xếp theo thứ tự giảm dần", "B": "Dãy khóa được sắp xếp theo thứ tự tăng dần", "C": "Dãy khóa ngẫu nhiên", "D": "Khóa của nút gốc luôn đứng đầu tiên"},
        "correct_answer": "B",
        "explanation": "Duyệt In-order (Trái -> Gốc -> Phải) trên BST luôn trả về một dãy số có thứ tự tăng dần nghiêm ngặt.",
        "difficulty": 3.5,
        "bloom": BloomLevel.UNDERSTAND
    },
    {
        "topic_id": 303,
        "content": "Thuật toán tìm kiếm A* sử dụng hàm đánh giá f(n) = g(n) + h(n). Trong đó h(n) đại diện cho điều gì?",
        "options": {"A": "Chi phí thực tế từ điểm xuất phát đến nút n", "B": "Chi phí ước lượng (heuristic) từ nút n đến điểm đích", "C": "Số lượng nút đã duyệt qua", "D": "Độ sâu của nút n trong cây tìm kiếm"},
        "correct_answer": "B",
        "explanation": "Trong thuật toán A*: g(n) là chi phí thực tế đã đi từ điểm bắt đầu đến n, còn h(n) là hàm Heuristic ước tính chi phí từ n tới đích.",
        "difficulty": 4.0,
        "bloom": BloomLevel.APPLY
    },

    # MÔN: CƠ SỞ DỮ LIỆU & SQL (DB_SQL)
    {
        "topic_id": 401,
        "content": "Một bảng cơ sở dữ liệu đạt chuẩn 1NF (Chuẩn 1) khi thỏa mãn điều kiện nào sau đây?",
        "options": {"A": "Mọi thuộc tính đều là đơn trị (atomic / nguyên tố), không chứa danh sách hoặc mảng lồng nhau", "B": "Không có phụ thuộc hàm bộ phận vào khóa chính", "C": "Không có phụ thuộc hàm bắc cầu", "D": "Mọi cột đều phải có chỉ mục Index"},
        "correct_answer": "A",
        "explanation": "Dạng chuẩn 1 (1NF) yêu cầu mọi giá trị trong các ô dữ liệu phải là đơn trị nguyên tử (atomic), không được chứa tập hợp hay mảng giá trị.",
        "difficulty": 2.5,
        "bloom": BloomLevel.REMEMBER
    },
    {
        "topic_id": 402,
        "content": "Phép nối nào trong SQL trả về TẤT CẢ các dòng từ bảng bên trái (Left table), và các giá trị khớp từ bảng bên phải (nếu không khớp sẽ điền NULL)?",
        "options": {"A": "INNER JOIN", "B": "LEFT JOIN (LEFT OUTER JOIN)", "C": "RIGHT JOIN", "D": "CROSS JOIN"},
        "correct_answer": "B",
        "explanation": "LEFT JOIN giữ lại toàn bộ các bản ghi của bảng bên trái và ghép các cột tương ứng từ bảng bên phải. Nếu không có dòng khớp thì điền NULL.",
        "difficulty": 2.5,
        "bloom": BloomLevel.UNDERSTAND
    },
    {
        "topic_id": 402,
        "content": "Để lọc dữ liệu sau khi đã thực hiện phép gom nhóm GROUP BY trong SQL, mệnh đề nào bắt buộc được sử dụng?",
        "options": {"A": "WHERE", "B": "HAVING", "C": "ORDER BY", "D": "LIMIT"},
        "correct_answer": "B",
        "explanation": "Mệnh đề WHERE lọc dữ liệu từng dòng TRƯỚC khi nhóm. Mệnh đề HAVING dùng để lọc các nhóm SAU khi đã GROUP BY.",
        "difficulty": 3.0,
        "bloom": BloomLevel.APPLY
    },
    {
        "topic_id": 403,
        "content": "Cấu trúc dữ liệu nào được sử dụng phổ biến nhất để xây dựng Chỉ mục (Index) trong các hệ quản trị CSDL quan hệ như MySQL hay PostgreSQL?",
        "options": {"A": "B-Tree (Balanced Tree) / B+ Tree", "B": "Đồ thị có hướng DAG", "C": "Ngăn xếp LIFO", "D": "Danh sách liên kết đơn"},
        "correct_answer": "A",
        "explanation": "B-Tree và B+ Tree là cấu trúc chỉ mục tiêu chuẩn trong RDBMS vì giữ được cây cân bằng, cho phép tìm kiếm, thêm, xóa và duyệt khoảng (range query) với chi phí O(log N).",
        "difficulty": 3.5,
        "bloom": BloomLevel.UNDERSTAND
    },

    # MÔN: HỌC SÂU & THỊ GIÁC MÁY TÍNH (DEEP_LEARNING)
    {
        "topic_id": 501,
        "content": "Tại sao hàm kích hoạt ReLU (Rectified Linear Unit) f(x) = max(0, x) lại được ưa chuộng hơn Sigmoid trong các mạng nơ-ron sâu?",
        "options": {"A": "ReLU làm triệt tiêu hoàn toàn đạo hàm", "B": "ReLU giảm thiểu hiện tượng biến mất gradient (Vanishing Gradient) và tính toán cực nhanh", "C": "ReLU giới hạn giá trị đầu ra trong khoảng (0, 1)", "D": "ReLU giúp mô hình luôn hội tụ về cực tiểu toàn cục"},
        "correct_answer": "B",
        "explanation": "Với x > 0, đạo hàm của ReLU luôn bằng 1, giúp dòng gradient lan truyền ngược không bị tiêu biến như Sigmoid (đạo hàm cực đại chỉ 0.25).",
        "difficulty": 3.5,
        "bloom": BloomLevel.UNDERSTAND
    },
    {
        "topic_id": 502,
        "content": "Trong Mạng nơ-ron tích chập (CNN), lớp Max-Pooling có mục đích chính là gì?",
        "options": {"A": "Tăng kích thước không gian của ảnh để học chi tiết hơn", "B": "Giảm kích thước không gian đặc trưng (Spatial Dimensions), giảm số lượng tham số và chống overfitting", "C": "Chuẩn hóa giá trị pixel về khoảng [0, 1]", "D": "Tính toán ma trận phân loại đầu ra"},
        "correct_answer": "B",
        "explanation": "Max-Pooling giữ lại giá trị nổi bật nhất trong mỗi cửa sổ trượt, giúp giảm kích thước chiều cao và chiều rộng của feature map, tiết kiệm tính toán và tạo tính bất biến dịch chuyển nhẹ.",
        "difficulty": 3.5,
        "bloom": BloomLevel.UNDERSTAND
    },
    {
        "topic_id": 503,
        "content": "Cơ chế nào là đột phá cốt lõi của kiến trúc Transformer (trong bài báo 'Attention Is All You Need') thay thế cho các mạng tuần hoàn RNN/LSTM?",
        "options": {"A": "Cơ chế Tự chú ý Đa đầu (Multi-Head Self-Attention)", "B": "Giải thuật Di truyền (Genetic Algorithm)", "C": "Lớp Tích chập 3D", "D": "Cổng quên Forget Gate trong LSTM"},
        "correct_answer": "A",
        "explanation": "Cơ chế Self-Attention cho phép mô hình tính toán mối tương quan giữa mọi từ trong câu đồng thời (xử lý song song), vượt qua hạn chế tuần tự từng bước của RNN.",
        "difficulty": 4.0,
        "bloom": BloomLevel.UNDERSTAND
    }
]

def run_multi_subject_pipeline():
    print("[ETL] =================================================================")
    print("[ETL] KHOI TAO PIPELINE NẠP DỮ LIỆU ĐA MÔN HỌC (MULTI-SUBJECT PIPELINE)")
    print("[ETL] =================================================================")

    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # 1. Khởi tạo User Admin & User Học sinh
        admin = session.query(User).filter_by(role=UserRole.ADMIN).first()
        if not admin:
            admin = User(email="admin@aegislearn.edu.vn", hashed_password="hashed_admin_pass", role=UserRole.ADMIN)
            session.add(admin)
            session.flush()

        student = session.query(User).filter_by(role=UserRole.STUDENT).first()
        if not student:
            student = User(email="student.a@aegislearn.edu.vn", hashed_password="hashed_student_pass", role=UserRole.STUDENT)
            session.add(student)
            session.flush()
            profile = UserProfile(
                user_id=student.id,
                full_name="Nguyễn Văn A",
                learning_style="VISUAL",
                preferences={"preferred_format": "VIDEO", "daily_goal_minutes": 45},
                study_streak_days=5,
                total_study_minutes=420,
                exp_points=350
            )
            session.add(profile)
            session.flush()

        # 2. Tạo Đa Môn Học (Subjects & Topics)
        total_topics_created = 0
        for subj_dict in SUBJECTS_CONFIG:
            s_obj = session.query(Subject).filter_by(code=subj_dict["code"]).first()
            if not s_obj:
                s_obj = Subject(
                    code=subj_dict["code"],
                    title=subj_dict["title"],
                    description=subj_dict["description"]
                )
                session.add(s_obj)
                session.flush()
                print(f"[ETL] -> Da tao Mon hoc: [{s_obj.code}] {s_obj.title}")

            for t_dict in subj_dict["topics"]:
                t_obj = session.query(Topic).filter_by(id=t_dict["id"]).first()
                if not t_obj:
                    t_obj = Topic(
                        id=t_dict["id"],
                        subject_id=s_obj.id,
                        code=t_dict["code"],
                        title=t_dict["title"],
                        description=t_dict["desc"],
                        order_index=t_dict["order"]
                    )
                    session.add(t_obj)
                    total_topics_created += 1

            session.flush()

            # Tạo Liên kết Tiên quyết DAG
            for child_id, parent_id in subj_dict.get("prereqs", []):
                chk = session.query(TopicPrerequisite).filter_by(topic_id=child_id, prerequisite_topic_id=parent_id).first()
                if not chk:
                    pre = TopicPrerequisite(topic_id=child_id, prerequisite_topic_id=parent_id)
                    session.add(pre)

        session.commit()
        print(f"[ETL] Hoan tat tao {len(SUBJECTS_CONFIG)} Mon hoc va cac Chuyen de DAG!")

        # 3. Nạp Tài nguyên Web & Video YouTube Tuyển chọn
        materials_added = 0
        for subj_code, res_dict in CURATED_RESOURCES.items():
            subj_obj = session.query(Subject).filter_by(code=subj_code).first()
            if not subj_obj:
                continue
            topic_ids = [t.id for t in session.query(Topic).filter_by(subject_id=subj_obj.id).all()]
            if not topic_ids:
                continue

            # Nạp web links
            for idx, w in enumerate(res_dict.get("web", [])):
                t_id = topic_ids[idx % len(topic_ids)]
                chk = session.query(LearningMaterial).filter_by(title=w["title"]).first()
                if not chk:
                    mat = LearningMaterial(
                        topic_id=t_id,
                        title=w["title"],
                        university=w["univ"],
                        material_type=MaterialType.READING if w["type"] == "READING" else MaterialType.EXERCISE,
                        content_url=w["url"],
                        text_content=f"Tài liệu học tập uy tín quốc tế từ {w['univ']}. Hướng dẫn thực hành và lý thuyết chuyên sâu.",
                        difficulty_level=w["level"],
                        created_by_id=admin.id
                    )
                    session.add(mat)
                    materials_added += 1

            # Nạp youtube links
            for idx, y in enumerate(res_dict.get("youtube", [])):
                t_id = topic_ids[idx % len(topic_ids)]
                chk = session.query(LearningMaterial).filter_by(title=y["title"]).first()
                if not chk:
                    mat = LearningMaterial(
                        topic_id=t_id,
                        title=f"📺 [YouTube] {y['title']}",
                        university=y["univ"],
                        material_type=MaterialType.VIDEO,
                        content_url=y["url"],
                        text_content=f"Bài giảng video trực quan hóa chất lượng cao trên YouTube từ kênh {y['univ']}. Khuyến nghị xem để nắm bản chất.",
                        difficulty_level=y["level"],
                        created_by_id=admin.id
                    )
                    session.add(mat)
                    materials_added += 1

        session.commit()
        print(f"[ETL] Da nap {materials_added} Tai nguyen Web va YouTube uy tin vao CSDL!")

        # 4. Đọc thêm từ file Kaggle EdX.csv để nạp đa dạng các trường đại học
        edx_path = os.path.join(os.path.dirname(__file__), "dataset", "EdX.csv")
        kaggle_added = 0
        if os.path.exists(edx_path):
            try:
                df_edx = pd.read_csv(edx_path)
                print(f"[ETL] Tim thay tệp Kaggle EdX.csv ({len(df_edx)} khoa hoc). Bat dau phan loai...")

                # Dictionary từ khóa ánh xạ sang Subject
                mapping_keywords = {
                    "MATH_AI": ["math", "calculus", "algebra", "probability", "statistic", "linear"],
                    "CS_DSA": ["computer science", "algorithm", "data structure", "programming", "code", "software"],
                    "DB_SQL": ["database", "sql", "data management", "big data"],
                    "DEEP_LEARNING": ["deep learning", "neural", "vision", "nlp", "artificial intelligence", "ai"],
                    "AI_PYTHON": ["python", "machine learning", "data science", "analytics"]
                }

                for _, row in df_edx.iterrows():
                    name = str(row.get("Name", "")).strip()
                    desc = str(row.get("About", "")) + " " + str(row.get("Course Description", ""))
                    full_text = (name + " " + desc).lower()
                    univ = str(row.get("University", "edX Global"))
                    diff_str = str(row.get("Difficulty Level", "Intermediate"))
                    diff_val = 2.0 if "beginner" in diff_str.lower() else (4.5 if "advanced" in diff_str.lower() else 3.5)
                    link = str(row.get("Link", "https://www.edx.org"))

                    # Tìm môn tương ứng
                    matched_subj_code = None
                    for scode, kws in mapping_keywords.items():
                        if any(kw in full_text for kw in kws):
                            matched_subj_code = scode
                            break

                    if matched_subj_code:
                        s_obj = session.query(Subject).filter_by(code=matched_subj_code).first()
                        if s_obj and s_obj.topics:
                            target_topic = s_obj.topics[0]
                            chk = session.query(LearningMaterial).filter_by(title=name).first()
                            if not chk:
                                mat = LearningMaterial(
                                    topic_id=target_topic.id,
                                    title=name[:250],
                                    university=univ[:250],
                                    material_type=MaterialType.READING,
                                    content_url=link[:490],
                                    text_content=desc[:500],
                                    difficulty_level=diff_val,
                                    created_by_id=admin.id
                                )
                                session.add(mat)
                                kaggle_added += 1

                session.commit()
                print(f"[ETL] Da phan loai va nap thanh cong {kaggle_added} khoa hoc EdX tu Kaggle vao CSDL!")
            except Exception as e:
                print(f"[ETL] Loi doc tệp EdX.csv: {e}")

        # 5. Nạp Ngân hàng Câu hỏi Trắc nghiệm Đa Môn
        questions_added = 0
        for q in DIVERSE_QUESTIONS:
            chk = session.query(Question).filter_by(content=q["content"]).first()
            if not chk:
                new_q = Question(
                    topic_id=q["topic_id"],
                    content=q["content"],
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=q["options"],
                    correct_answer=q["correct_answer"],
                    explanation=q["explanation"],
                    difficulty_level=q["difficulty"]
                )
                session.add(new_q)
                questions_added += 1

        session.commit()
        print(f"[ETL] Da nap {questions_added} cau hoi trac nghiem da mon vao Question Bank!")

        # 6. Khởi tạo KnowledgeProfile mẫu cho sinh viên
        all_topics = session.query(Topic).all()
        for t in all_topics:
            kp = session.query(KnowledgeProfile).filter_by(user_id=student.id, topic_id=t.id).first()
            if not kp:
                st = MasteryStatus.MASTERED if t.id in (101, 102) else (MasteryStatus.WEAK if t.id == 103 else MasteryStatus.NEEDS_ASSESSMENT)
                sc = 90.0 if t.id == 101 else (82.0 if t.id == 102 else (52.0 if t.id == 103 else 0.0))
                session.add(KnowledgeProfile(user_id=student.id, topic_id=t.id, status=st, mastery_score=sc))

        session.commit()
        print("[ETL] Hoan tat khoi tao KnowledgeProfile da mon cho sinh vien!")
        print("[ETL] =================================================================")
        print("[ETL] SEED HOAN TAT THANH CONG 100%! CSDL 'learning_app.db' DA SAN SANG!")
        print("[ETL] =================================================================")

if __name__ == "__main__":
    run_multi_subject_pipeline()
