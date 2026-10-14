# -*- coding: utf-8 -*-
"""
Expand Curriculum Seeder
Adds 6 new comprehensive subjects in Data, Machine Learning, NLP, Computer Vision
to learning_app.db, complete with topics, EdX courses, YouTube lectures, and practice questions.
"""

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import sqlite3
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Subject, Topic, LearningMaterial, Question, MaterialType, QuestionType, BloomLevel

NEW_SUBJECTS = [
    {
        "code": "DATA_SCIENCE",
        "title": "Khoa học Dữ liệu & Phân tích Chuyên sâu (Data Science & Analytics)",
        "description": "Toàn cảnh ngành Data Science: Khám phá dữ liệu EDA, thống kê suy luận, trích chọn đặc trưng (Feature Engineering) và xây dựng pipeline phân tích dự báo.",
        "topics": [
            {
                "id": 601, "code": "DS101",
                "title": "Chương 1: Khám phá Dữ liệu EDA & Thống kê Mô tả",
                "desc": "Kỹ thuật phân tích dữ liệu khám phá (EDA), phân phối xác suất, độ lệch chuẩn, tứ phân vị IQR và phát hiện ngoại lai (Outliers).",
                "order": 1,
                "materials": [
                    {"title": "Harvard University: Data Science: R & Python Basics", "url": "https://www.edx.org/course/data-science-r-basics", "type": MaterialType.READING, "univ": "Harvard University", "level": 2.5, "desc": "Giáo trình nhập môn khoa học dữ liệu chuẩn quốc tế từ Harvard."},
                    {"title": "MIT The Analytics Edge: Exploratory Data Analysis & Statistics", "url": "https://ocw.mit.edu/courses/15-071-the-analytics-edge-spring-2017/", "type": MaterialType.READING, "univ": "MIT", "level": 3.0, "desc": "Các phương pháp phân tích thống kê thực nghiệm trên dữ liệu thực tế."},
                    {"title": "Video Bài Giảng: Toàn diện Khám phá Dữ liệu EDA với Python (Full Course)", "url": "https://www.youtube.com/watch?v=liv7_5yJp0M", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 2.5, "desc": "Hướng dẫn từng bước thực hành EDA và trực quan hóa phân phối."}
                ],
                "questions": [
                    {
                        "content": "Trong phân tích dữ liệu khám phá (EDA), chỉ số nào sau đây ít bị ảnh hưởng nhất bởi các giá trị ngoại lai (outliers)?",
                        "options": {"A": "Trung bình cộng (Mean)", "B": "Trung vị (Median)", "C": "Phương sai (Variance)", "D": "Độ lệch chuẩn (Standard Deviation)"},
                        "correct": "B",
                        "exp": "Trung vị (Median) là đại lượng thống kê bền vững (robust), không bị kéo lệch bởi các giá trị cực trị ngoại lai như Mean.",
                        "concept": "Robust Statistics trong EDA"
                    },
                    {
                        "content": "Quy tắc kiểm tra ngoại lai bằng khoảng tứ phân vị (IQR) xác định một điểm x là outlier nếu x nằm ngoài khoảng nào?",
                        "options": {"A": "[Q1 - 1.5*IQR, Q3 + 1.5*IQR]", "B": "[Q1 - 2*IQR, Q3 + 2*IQR]", "C": "[Mean - 1.5*Std, Mean + 1.5*Std]", "D": "[Q1 - IQR, Q3 + IQR]"},
                        "correct": "A",
                        "exp": "Phương pháp Tukey IQR định nghĩa outlier là các giá trị nhỏ hơn Q1 - 1.5*IQR hoặc lớn hơn Q3 + 1.5*IQR.",
                        "concept": "IQR Outlier Detection"
                    }
                ]
            },
            {
                "id": 602, "code": "DS102",
                "title": "Chương 2: Tiền xử lý, Xử lý Thiếu & Feature Engineering",
                "desc": "Kỹ thuật imputation điền giá trị khuyết thiếu, mã hóa biến phân loại (One-Hot, Target Encoding), chuẩn hóa MinMax / StandardScaler và chọn lọc đặc trưng.",
                "order": 2,
                "materials": [
                    {"title": "Scikit-Learn Guide: Preprocessing & Imputation Techniques", "url": "https://scikit-learn.org/stable/modules/preprocessing.html", "type": MaterialType.READING, "univ": "Scikit-Learn.org", "level": 3.0, "desc": "Cẩm nang tiền xử lý dữ liệu và chuẩn hóa đặc trưng khoa học."},
                    {"title": "Kaggle Feature Engineering Masterclass", "url": "https://www.kaggle.com/learn/feature-engineering", "type": MaterialType.READING, "univ": "Kaggle", "level": 3.5, "desc": "Nghệ thuật tạo đặc trưng mới giúp nâng cao độ chính xác mô hình."},
                    {"title": "Video Bài Giảng: Kỹ thuật Feature Engineering từ Cơ bản đến Nâng cao", "url": "https://www.youtube.com/watch?v=6WDFfaYtN6s", "type": MaterialType.VIDEO, "univ": "Data Science Dojo", "level": 3.0, "desc": "Hướng dẫn thực chiến xử lý dữ liệu bảng trước khi huấn luyện."}
                ],
                "questions": [
                    {
                        "content": "Khi dữ liệu có phân phối chuẩn (Gaussian) và chứa một số giá trị ngoại lai, kỹ thuật chuẩn hóa đặc trưng nào sau đây phù hợp nhất?",
                        "options": {"A": "Min-Max Scaling [0, 1]", "B": "RobustScaler (dựa trên Median và IQR)", "C": "Binarization", "D": "Bỏ qua không chuẩn hóa"},
                        "correct": "B",
                        "exp": "RobustScaler sử dụng trung vị và khoảng tứ phân vị nên không bị bóp méo bởi các giá trị ngoại lai như MinMaxScaler hay StandardScaler.",
                        "concept": "Feature Scaling Techniques"
                    }
                ]
            },
            {
                "id": 603, "code": "DS103",
                "title": "Chương 3: Phân tích Hồi quy & Phân cụm Khách hàng",
                "desc": "Mô hình hồi quy đa biến (Multiple Regression), đánh giá R-squared, RMSE, thuật toán phân cụm K-Means, DBSCAN và hệ số Silhouette Score.",
                "order": 3,
                "materials": [
                    {"title": "Stanford University: Unsupervised Learning & Clustering", "url": "https://cs229.stanford.edu/notes2022fall/cs229-notes7a.pdf", "type": MaterialType.READING, "univ": "Stanford University", "level": 3.5, "desc": "Lý thuyết nền tảng về giải thuật phân cụm và học không giám sát."},
                    {"title": "Video Bài Giảng: Thuật toán K-Means & Phương pháp Elbow (StatQuest)", "url": "https://www.youtube.com/watch?v=4b5d3muPQmA", "type": MaterialType.VIDEO, "univ": "StatQuest with Josh Starmer", "level": 3.0, "desc": "Giải thích trực quan thuật toán phân cụm K-Means cực kỳ dễ hiểu."}
                ],
                "questions": [
                    {
                        "content": "Để lựa chọn số cụm K tối ưu trong thuật toán K-Means Clustering, người ta thường dùng phương pháp nào?",
                        "options": {"A": "Phương pháp Elbow (Điểm khuỷu tay WCSS)", "B": "Gradient Descent", "C": "Backpropagation", "D": "Topological Sort"},
                        "correct": "A",
                        "exp": "Phương pháp Elbow vẽ đồ thị tổng bình phương khoảng cách nội cụm (WCSS) theo K, điểm uốn cong khuỷu tay là K hợp lý.",
                        "concept": "K-Means Optimal Clusters"
                    }
                ]
            }
        ]
    },
    {
        "code": "DATA_ENG",
        "title": "Kỹ thuật Dữ liệu & Xử lý Dữ liệu Lớn (Data Engineering & Big Data)",
        "description": "Thiết kế Data Pipeline quy mô lớn, luồng xử lý ETL tự động, hệ sinh thái Apache Spark phân tán, Data Lake và kiến trúc dữ liệu hiện đại.",
        "topics": [
            {
                "id": 701, "code": "DE101",
                "title": "Chương 1: Kiến trúc Data Pipeline & Luồng ETL/ELT",
                "desc": "Khái niệm trích xuất (Extract), biến đổi (Transform), nạp (Load), điều phối luồng dữ liệu (Data Orchestration) với Apache Airflow.",
                "order": 1,
                "materials": [
                    {"title": "Apache Airflow: Official Architecture & DAG Guide", "url": "https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html", "type": MaterialType.READING, "univ": "Apache Foundation", "level": 3.0, "desc": "Tài liệu kiến trúc điều phối data pipeline chính thức của Apache Airflow."},
                    {"title": "Video Bài Giảng: Data Engineering Crash Course (Data Pipelines & ETL)", "url": "https://www.youtube.com/watch?v=qWru-b6m030", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 3.0, "desc": "Khóa học nhập môn Data Engineering và xây dựng Data Pipeline hoàn chỉnh."}
                ],
                "questions": [
                    {
                        "content": "Sự khác biệt chính giữa kiến trúc ETL truyền thống và ELT hiện đại là gì?",
                        "options": {
                            "A": "ELT biến đổi dữ liệu trực tiếp trong Data Warehouse sau khi nạp, tận dụng sức mạnh tính toán của đám mây.",
                            "B": "ETL không hỗ trợ dữ liệu quan hệ.",
                            "C": "ELT không lưu trữ dữ liệu thô.",
                            "D": "ETL chạy nhanh hơn ELT trên dữ liệu lớn hàng Petabyte."
                        },
                        "correct": "A",
                        "exp": "ELT tận dụng năng lực tính toán phân tán mạnh mẽ của Modern Cloud Data Warehouses (Snowflake, BigQuery) để biến đổi dữ liệu sau khi nạp.",
                        "concept": "ETL vs ELT Paradigm"
                    }
                ]
            },
            {
                "id": 702, "code": "DE102",
                "title": "Chương 2: Xử lý Dữ liệu Phân tán với Apache Spark & PySpark",
                "desc": "Kiến trúc tính toán phân tán In-Memory RDD, DataFrame API, Lazy Evaluation và tối ưu hóa truy vấn Spark Catalyst Optimizer.",
                "order": 2,
                "materials": [
                    {"title": "Apache Spark Official Guide: Spark SQL, DataFrames & Datasets", "url": "https://spark.apache.org/docs/latest/sql-programming-guide.html", "type": MaterialType.READING, "univ": "Apache Spark", "level": 3.5, "desc": "Hướng dẫn lập trình Spark SQL và DataFrames hiệu năng cao."},
                    {"title": "Video Bài Giảng: PySpark Tutorial for Beginners (Apache Spark Full Course)", "url": "https://www.youtube.com/watch?v=_C8kWso4ne4", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 3.5, "desc": "Thực hành xử lý dữ liệu lớn với PySpark trên môi trường phân tán."}
                ],
                "questions": [
                    {
                        "content": "Trong Apache Spark, khái niệm 'Lazy Evaluation' có ý nghĩa là gì?",
                        "options": {
                            "A": "Spark trì hoãn thực thi các phép biến đổi (Transformations) cho đến khi một hành động (Action) được gọi.",
                            "B": "Spark chạy chậm hơn bình thường để tiết kiệm RAM.",
                            "C": "Spark tự động xóa cache sau mỗi 5 phút.",
                            "D": "Spark không hỗ trợ kiểm tra lỗi cú pháp."
                        },
                        "correct": "A",
                        "exp": "Lazy Evaluation cho phép Spark xây dựng biểu đồ DAG của các phép tính và tối ưu hóa kế hoạch thực thi tổng thể trước khi thực sự tính toán.",
                        "concept": "Spark Lazy Evaluation"
                    }
                ]
            },
            {
                "id": 703, "code": "DE103",
                "title": "Chương 3: Data Lakehouse & Kiến trúc Medallion (Bronze/Silver/Gold)",
                "desc": "Định dạng lưu trữ cột Parquet, Delta Lake ACID transactions, phân tầng dữ liệu Medallion Architecture (Bronze - Thô, Silver - Sạch, Gold - Báo cáo).",
                "order": 3,
                "materials": [
                    {"title": "Databricks: What is a Medallion Architecture (Bronze, Silver, Gold)?", "url": "https://www.databricks.com/glossary/medallion-architecture", "type": MaterialType.READING, "univ": "Databricks", "level": 3.5, "desc": "Mô hình thiết kế chuẩn công nghiệp cho Data Lakehouse."},
                    {"title": "Video Bài Giảng: Data Lakehouse Architecture Explained", "url": "https://www.youtube.com/watch?v=vVj44A4o7eU", "type": MaterialType.VIDEO, "univ": "Seattle Data Guy", "level": 3.0, "desc": "Giải thích chi tiết kiến trúc Delta Lake và các tầng lưu trữ dữ liệu."}
                ],
                "questions": [
                    {
                        "content": "Trong kiến trúc dữ liệu Medallion Architecture, tầng 'Silver Layer' chịu trách nhiệm cho việc gì?",
                        "options": {
                            "A": "Chứa dữ liệu thô nguyên bản từ nguồn (Raw Ingestion)",
                            "B": "Làm sạch, lọc trùng, chuẩn hóa cấu trúc dữ liệu (Cleaned & Conformed Data)",
                            "C": "Tổng hợp chỉ số KPI cấp cao cho giám đốc điều hành",
                            "D": "Lưu trữ bản sao lưu ngoại tuyến"
                        },
                        "correct": "B",
                        "exp": "Tầng Silver làm sạch, chuẩn hóa và khử trùng dữ liệu từ Bronze, chuẩn bị cho tầng Gold tổng hợp nghiệp vụ.",
                        "concept": "Medallion Data Architecture"
                    }
                ]
            }
        ]
    },
    {
        "code": "DATA_VIZ",
        "title": "Trực quan hóa Dữ liệu & Báo cáo Thông minh (Data Visualization & BI)",
        "description": "Kỹ năng trực quan hóa chuyên nghiệp, thiết kế biểu đồ tương tác, storytelling dữ liệu và xây dựng Dashboard phục vụ ra quyết định kinh doanh.",
        "topics": [
            {
                "id": 801, "code": "DV101",
                "title": "Chương 1: Nguyên lý Trực quan hóa & Storytelling bằng Dữ liệu",
                "desc": "Lựa chọn loại biểu đồ phù hợp (Bar, Line, Scatter, Heatmap), phối màu, giảm thiểu nhiễu hình ảnh (Data-to-Ink Ratio).",
                "order": 1,
                "materials": [
                    {"title": "Storytelling with Data: A Data Visualization Guide for Business", "url": "https://www.storytellingwithdata.com/", "type": MaterialType.READING, "univ": "Cole Nussbaumer", "level": 2.5, "desc": "Cẩm nang kinh điển về nghệ thuật truyền đạt thông điệp qua số liệu."},
                    {"title": "Video Bài Giảng: Data Visualization Best Practices & Design Principles", "url": "https://www.youtube.com/watch?v=4V_X7Qe2SjU", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 2.5, "desc": "Các nguyên tắc thiết kế đồ họa thông tin trực quan ấn tượng."}
                ],
                "questions": [
                    {
                        "content": "Khi cần so sánh tỷ trọng thành phần của một biến phân loại có hơn 10 nhóm nhỏ, loại biểu đồ nào sau đây NÊN TRÁNH DÙNG?",
                        "options": {"A": "Biểu đồ tròn (Pie Chart)", "B": "Biểu đồ cột ngang (Horizontal Bar Chart)", "C": "Treemap", "D": "Biểu đồ cột phân tầng (Stacked Bar Chart)"},
                        "correct": "A",
                        "exp": "Biểu đồ tròn (Pie Chart) rất khó so sánh góc và diện tích khi có quá nhiều lát cắt (> 5-7 lát). Nên thay bằng biểu đồ thanh ngang.",
                        "concept": "Chart Selection Principles"
                    }
                ]
            },
            {
                "id": 802, "code": "DV102",
                "title": "Chương 2: Biểu đồ Động & Trực quan Nâng cao với Seaborn & Plotly",
                "desc": "Xây dựng biểu đồ tương tác zoom, pan, hover tooltips, vẽ biểu đồ tương quan ma trận (Correlation Heatmap) và biểu đồ phân tán đa chiều (Pairplot).",
                "order": 2,
                "materials": [
                    {"title": "Plotly Python Open Source Graphing Library", "url": "https://plotly.com/python/", "type": MaterialType.READING, "univ": "Plotly", "level": 3.0, "desc": "Thư viện biểu đồ tương tác hàng đầu cho Web và Khoa học Dữ liệu."},
                    {"title": "Video Bài Giảng: Interactive Data Visualization with Plotly & Python", "url": "https://www.youtube.com/watch?v=GGL6U0k8WYA", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 3.0, "desc": "Tạo biểu đồ động, bản đồ địa lý và đồ thị tương tác trong trình duyệt."}
                ],
                "questions": [
                    {
                        "content": "Thư viện nào trong Python tạo ra các biểu đồ dạng HTML tương tác (cho phép rê chuột xem giá trị, phóng to/thu nhỏ)?",
                        "options": {"A": "Plotly", "B": "Matplotlib cơ bản", "C": "NumPy", "D": "Pickle"},
                        "correct": "A",
                        "exp": "Plotly biên dịch biểu đồ thành các thành phần Javascript tương tác trực tiếp trên trình duyệt web.",
                        "concept": "Interactive Visualization Libraries"
                    }
                ]
            },
            {
                "id": 803, "code": "DV103",
                "title": "Chương 3: Thiết kế Dashboard Quản trị Tương tác (BI Dashboards)",
                "desc": "Bố cục lưới (Grid Layout), thiết kế thẻ chỉ số KPI (Scorecard Cards), bộ lọc dữ liệu đa chiều (Cross-Filtering) và kết nối dữ liệu thời gian thực.",
                "order": 3,
                "materials": [
                    {"title": "Microsoft Power BI Official Documentation & Learning Path", "url": "https://learn.microsoft.com/en-us/power-bi/", "type": MaterialType.READING, "univ": "Microsoft", "level": 2.5, "desc": "Tài liệu học thiết kế báo cáo và Dashboard phân tích dữ liệu doanh nghiệp."},
                    {"title": "Video Bài Giảng: Power BI Full Course - Learn Power BI in 4 Hours", "url": "https://www.youtube.com/watch?v=3u7MQz1EyPY", "type": MaterialType.VIDEO, "univ": "Edureka", "level": 2.5, "desc": "Khóa học toàn diện xây dựng Dashboard phân tích nghiệp vụ."}
                ],
                "questions": [
                    {
                        "content": "Kỹ thuật 'Cross-filtering' trên Dashboard phân tích dữ liệu có nghĩa là gì?",
                        "options": {
                            "A": "Khi bấm chọn một phần tử trên biểu đồ này, các biểu đồ khác trên Dashboard tự động lọc theo phần tử đó.",
                            "B": "Xóa toàn bộ bộ nhớ cache khi đổi trang.",
                            "C": "Chặn người dùng xem dữ liệu nếu chưa đăng nhập.",
                            "D": "Sao chép dữ liệu sang một bảng khác."
                        },
                        "correct": "A",
                        "exp": "Cross-filtering liên kết tương tác giữa các biểu đồ, giúp người dùng đào sâu phân tích (drill-down) linh hoạt.",
                        "concept": "Dashboard Interactivity"
                    }
                ]
            }
        ]
    },
    {
        "code": "MACHINE_LEARNING",
        "title": "Học Máy Thực Chiến & Khai Phá Dữ Liệu (Applied Machine Learning)",
        "description": "Toàn diện các thuật toán học máy kinh điển: Hồi quy, Cây quyết định (Decision Trees), Rừng ngẫu nhiên (Random Forest), SVM, Gradient Boosting (XGBoost) và kỹ thuật tinh chỉnh siêu tham số.",
        "topics": [
            {
                "id": 901, "code": "ML101",
                "title": "Chương 1: Thuật toán Học Có Giám Sát (Supervised Learning)",
                "desc": "Cơ chế hoạt động của Hồi quy Logistic, Cây quyết định (Entropy/Gini Index), Rừng ngẫu nhiên (Bagging) và Support Vector Machines (SVM Kernel Trick).",
                "order": 1,
                "materials": [
                    {"title": "Stanford CS229: Supervised Learning Lecture Notes", "url": "https://cs229.stanford.edu/notes2022fall/cs229-notes1.pdf", "type": MaterialType.READING, "univ": "Stanford University", "level": 3.5, "desc": "Giáo trình học máy chuyên sâu từ Đại học Stanford."},
                    {"title": "Video Bài Giảng: Random Forests and Decision Trees (StatQuest)", "url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ", "type": MaterialType.VIDEO, "univ": "StatQuest with Josh Starmer", "level": 3.0, "desc": "Giải thích trực quan sinh động thuật toán Cây quyết định và Rừng ngẫu nhiên."}
                ],
                "questions": [
                    {
                        "content": "Kỹ thuật Ensemble Learning nào sử dụng việc lấy mẫu có hoàn lại (Bootstrap Aggregating) để kết hợp nhiều cây quyết định độc lập?",
                        "options": {"A": "Bagging (Random Forest)", "B": "Boosting (XGBoost)", "C": "Linear Regression", "D": "PCA"},
                        "correct": "A",
                        "exp": "Random Forest sử dụng kỹ thuật Bagging (lấy mẫu bootstrap) để huấn luyện nhiều cây song song nhằm giảm phương sai (variance).",
                        "concept": "Ensemble Learning Bagging"
                    }
                ]
            },
            {
                "id": 902, "code": "ML102",
                "title": "Chương 2: Thuật toán Tăng cường Gradient Boosting & XGBoost",
                "desc": "Ý tưởng học sửa sai tuần tự (Sequential Learning), AdaBoost, Gradient Boosting, XGBoost, LightGBM và kiểm soát tốc độ học (Learning Rate).",
                "order": 2,
                "materials": [
                    {"title": "XGBoost Documentation: A Scalable Tree Boosting System", "url": "https://xgboost.readthedocs.io/en/stable/", "type": MaterialType.READING, "univ": "DMLC", "level": 3.5, "desc": "Tài liệu chính thức về thuật toán thống trị các cuộc thi Kaggle."},
                    {"title": "Video Bài Giảng: Gradient Boost Part 1: Regression Main Ideas", "url": "https://www.youtube.com/watch?v=3CC4N4z3GJc", "type": MaterialType.VIDEO, "univ": "StatQuest with Josh Starmer", "level": 3.0, "desc": "Bản chất toán học và cơ chế sửa sai từng bước của Gradient Boosting."}
                ],
                "questions": [
                    {
                        "content": "Trong thuật toán Gradient Boosting, mỗi cây mới được huấn luyện để dự đoán đại lượng nào của cây trước đó?",
                        "options": {"A": "Phần dư / Sai số (Residuals)", "B": "Đặc trưng đầu vào nguyên bản", "C": "Nhãn lớp ngẫu nhiên", "D": "Số lượng mẫu"},
                        "correct": "A",
                        "exp": "Gradient Boosting tối ưu bằng cách cho cây tiếp theo học phần sai lệch (pseudo-residuals) của mô hình hiện tại.",
                        "concept": "Gradient Boosting Residuals"
                    }
                ]
            },
            {
                "id": 903, "code": "ML103",
                "title": "Chương 3: Đánh giá Mô hình, Ma trận Nhầm lẫn & Tối ưu Siêu tham số",
                "desc": "Confusion Matrix, Precision, Recall, F1-Score, ROC-AUC curve, K-Fold Cross Validation và tìm kiếm siêu tham số GridSearchCV / Optuna.",
                "order": 3,
                "materials": [
                    {"title": "Scikit-Learn Guide: Model Evaluation & Scoring Metrics", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html", "type": MaterialType.READING, "univ": "Scikit-Learn.org", "level": 3.0, "desc": "Bộ công cụ đánh giá độ chính xác và kiểm thử chéo toàn diện."},
                    {"title": "Video Bài Giảng: ROC and AUC, Clearly Explained!", "url": "https://www.youtube.com/watch?v=4jRBRDbJemM", "type": MaterialType.VIDEO, "univ": "StatQuest with Josh Starmer", "level": 3.0, "desc": "Đường cong ROC và chỉ số AUC trong bài toán phân loại."}
                ],
                "questions": [
                    {
                        "content": "Trong bài toán chẩn đoán y tế (phát hiện bệnh hiểm nghèo), chỉ số đánh giá nào cần được ưu tiên tối đa để hạn chế bỏ sót ca bệnh?",
                        "options": {"A": "Độ nhạy (Recall / True Positive Rate)", "B": "Độ chính xác (Accuracy)", "C": "Tốc độ huấn luyện", "D": "Mean Squared Error"},
                        "correct": "A",
                        "exp": "Trong y tế, bỏ sót người có bệnh (False Negative) cực kỳ nguy hiểm, do đó cần tối ưu Recall (tỷ lệ phát hiện đúng trên tổng số ca có bệnh).",
                        "concept": "Classification Metrics in Critical Domains"
                    }
                ]
            }
        ]
    },
    {
        "code": "NLP_LLM",
        "title": "Xử lý Ngôn ngữ Tự nhiên & Mô hình Ngôn ngữ Lớn (NLP & LLMs)",
        "description": "Công nghệ xử lý văn bản, biểu diễn vector từ vựng (Embeddings), kiến trúc Transformer đột phá, RAG (Retrieval-Augmented Generation) và Fine-tuning LLM.",
        "topics": [
            {
                "id": 1001, "code": "NLP101",
                "title": "Chương 1: Xử lý Văn bản, Tokenization & Word Embeddings",
                "desc": "Tách từ (Tokenization: BPE, WordPiece), làm sạch văn bản, ma trận nhúng Word2Vec, GloVe, tính khoảng cách Cosine giữa các vector ngữ nghĩa.",
                "order": 1,
                "materials": [
                    {"title": "Stanford CS224N: Natural Language Processing with Deep Learning", "url": "https://web.stanford.edu/class/cs224n/", "type": MaterialType.READING, "univ": "Stanford University", "level": 3.5, "desc": "Khóa học NLP đỉnh cao của Đại học Stanford."},
                    {"title": "Video Bài Giảng: Word Embedding and Word2Vec, Clearly Explained!", "url": "https://www.youtube.com/watch?v=viZrOnJclYQ", "type": MaterialType.VIDEO, "univ": "StatQuest with Josh Starmer", "level": 3.0, "desc": "Bản chất biểu diễn từ ngữ thành vector số trong không gian nhiều chiều."}
                ],
                "questions": [
                    {
                        "content": "Mục tiêu chính của kỹ thuật Word Embedding (như Word2Vec) là gì?",
                        "options": {
                            "A": "Biểu diễn các từ ngữ thành các vector số thực trong không gian sao cho các từ đồng nghĩa/liên quan nằm gần nhau.",
                            "B": "Mã hóa văn bản thành mã nhị phân ASCII.",
                            "C": "Đếm số lần xuất hiện của từ trong toàn bộ văn bản.",
                            "D": "Dịch văn bản sang tiếng Anh tự động."
                        },
                        "correct": "A",
                        "exp": "Word Embeddings ánh xạ từ vựng vào không gian vector ngữ nghĩa liên tục, bảo toàn các mối quan hệ ngữ nghĩa (King - Man + Woman = Queen).",
                        "concept": "Word Embeddings Semantic Space"
                    }
                ]
            },
            {
                "id": 1002, "code": "NLP102",
                "title": "Chương 2: Kiến trúc Transformer & Cơ chế Tự chú ý (Self-Attention)",
                "desc": "Bài báo kinh điển 'Attention Is All You Need', cơ chế Scaled Dot-Product Attention, Multi-Head Attention, mã hóa vị trí (Positional Encoding).",
                "order": 2,
                "materials": [
                    {"title": "The Illustrated Transformer by Jay Alammar", "url": "https://jalammar.github.io/illustrated-transformer/", "type": MaterialType.READING, "univ": "Jay Alammar", "level": 3.5, "desc": "Bài giảng trực quan minh họa từng bước kiến trúc Transformer nổi tiếng thế giới."},
                    {"title": "Video Bài Giảng: Attention is all you need (Transformer Architecture)", "url": "https://www.youtube.com/watch?v=TQQlZhbC5ps", "type": MaterialType.VIDEO, "univ": "Yannic Kilcher", "level": 4.0, "desc": "Phân tích chi tiết từng phương trình toán học trong bài báo Transformer."}
                ],
                "questions": [
                    {
                        "content": "Trong cơ chế Scaled Dot-Product Attention, ma trận trọng số tương quan giữa các từ được tính từ những thành phần nào?",
                        "options": {"A": "Query (Q) và Key (K)", "B": "Chỉ có Value (V)", "C": "Loss và Optimizer", "D": "Learning rate và Momentum"},
                        "correct": "A",
                        "exp": "Độ tương quan giữa các từ được tính bằng tích vô hướng Softmax(Q * K^T / sqrt(d_k)), sau đó nhân với Value (V).",
                        "concept": "Scaled Dot-Product Attention"
                    }
                ]
            },
            {
                "id": 1003, "code": "NLP103",
                "title": "Chương 3: Kiến trúc RAG (Retrieval-Augmented Generation) & Prompt Engineering",
                "desc": "Tích hợp Vector Database (ChromaDB, Pinecone, FAISS), quy trình tìm kiếm tương đồng ngữ nghĩa, kỹ thuật viết Prompt tối ưu và giảm ảo giác (Hallucination) cho LLM.",
                "order": 3,
                "materials": [
                    {"title": "LangChain & LlamaIndex Official Documentation: RAG Concepts", "url": "https://docs.langchain.com/oss/python/concepts/rag/", "type": MaterialType.READING, "univ": "LangChain", "level": 3.5, "desc": "Kiến trúc RAG kết hợp LLM và cơ sở tri thức doanh nghiệp."},
                    {"title": "Video Bài Giảng: RAG From Scratch (LangChain Masterclass)", "url": "https://www.youtube.com/watch?v=wd7TZ4w1mSw", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 3.5, "desc": "Xây dựng hệ thống Hỏi-Đáp AI RAG với Vector Database từ đầu."}
                ],
                "questions": [
                    {
                        "content": "Trong hệ thống RAG (Retrieval-Augmented Generation), vai trò của Vector Database là gì?",
                        "options": {
                            "A": "Lưu trữ vector nhúng của tài liệu tri thức để truy xuất nhanh các đoạn văn bản có độ tương đồng ngữ nghĩa cao nhất.",
                            "B": "Huấn luyện lại toàn bộ trọng số của mô hình GPT.",
                            "C": "Chuyển giọng nói thành văn bản.",
                            "D": "Tạo giao diện người dùng bằng React."
                        },
                        "correct": "A",
                        "exp": "Vector DB lưu trữ các chunk tài liệu dưới dạng vector embeddings, cho phép tìm kiếm ngữ nghĩa (semantic search) cung cấp ngữ cảnh cho LLM trả lời chính xác.",
                        "concept": "RAG Vector Retrieval"
                    }
                ]
            }
        ]
    },
    {
        "code": "COMPUTER_VISION",
        "title": "Thị giác Máy tính & Xử lý Ảnh AI (Computer Vision & OpenCV)",
        "description": "Xử lý ảnh số chuyên sâu, trích xuất đặc trưng hình ảnh, mạng nơ-ron tích chập CNN, phát hiện vật thể thời gian thực YOLO và phân đoạn ảnh.",
        "topics": [
            {
                "id": 1101, "code": "CV101",
                "title": "Chương 1: Xử lý Ảnh Số Cơ Bản với OpenCV",
                "desc": "Không gian màu (RGB, HSV, Grayscale), lọc nhiễu Gaussian, phát hiện cạnh Sobel, Canny Edge Detection và phép biến đổi hình học (Affine, Perspective).",
                "order": 1,
                "materials": [
                    {"title": "OpenCV-Python Tutorials: Official Image Processing Guide", "url": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html", "type": MaterialType.READING, "univ": "OpenCV.org", "level": 2.5, "desc": "Cẩm nang xử lý ảnh và thị giác máy tính chính thức của OpenCV."},
                    {"title": "Video Bài Giảng: OpenCV Course - Full Tutorial with Python", "url": "https://www.youtube.com/watch?v=oXlwWbU8l2o", "type": MaterialType.VIDEO, "univ": "freeCodeCamp", "level": 2.5, "desc": "Thực hành toàn bộ kỹ thuật xử lý ảnh và video với OpenCV."}
                ],
                "questions": [
                    {
                        "content": "Bộ lọc nào trong xử lý ảnh thường được sử dụng đầu tiên để làm mượt ảnh và loại bỏ nhiễu cao tần trước khi phát hiện biên cạnh?",
                        "options": {"A": "Bộ lọc Gaussian Blur", "B": "Bộ lọc Sobel", "C": "Laplacian filter", "D": "Thresholding"},
                        "correct": "A",
                        "exp": "Bộ lọc Gaussian tính trung bình có trọng số theo phân phối chuẩn, giúp khử nhiễu đốm trước khi dò biên cạnh bằng Canny.",
                        "concept": "Gaussian Filtering & Noise Reduction"
                    }
                ]
            },
            {
                "id": 1102, "code": "CV102",
                "title": "Chương 2: Nhận diện & Định vị Vật thể Thời gian thực với YOLO",
                "desc": "Kiến trúc One-Stage Detector YOLO (You Only Look Once), hàm mất mát Bounding Box IoU, Non-Maximum Suppression (NMS) và đánh giá mAP.",
                "order": 2,
                "materials": [
                    {"title": "Ultralytics YOLO Docs: Real-time Object Detection Guide", "url": "https://docs.ultralytics.com/", "type": MaterialType.READING, "univ": "Ultralytics", "level": 3.5, "desc": "Hướng dẫn thực chiến huấn luyện mô hình YOLO phát hiện vật thể."},
                    {"title": "Video Bài Giảng: YOLOv8 Object Detection Full Tutorial", "url": "https://www.youtube.com/watch?v=m9fH9OWn8YM", "type": MaterialType.VIDEO, "univ": "Nicolai Nielsen", "level": 3.0, "desc": "Triển khai nhận diện đối tượng thời gian thực trên video camera."}
                ],
                "questions": [
                    {
                        "content": "Thuật toán Non-Maximum Suppression (NMS) trong bài toán phát hiện vật thể (Object Detection) nhằm giải quyết vấn đề gì?",
                        "options": {
                            "A": "Loại bỏ các khung bao (Bounding Boxes) trùng lặp cùng phát hiện một đối tượng, chỉ giữ lại khung có độ tin cậy cao nhất.",
                            "B": "Tăng kích thước ảnh lên gấp đôi.",
                            "C": "Chuyển ảnh màu thành ảnh đen trắng.",
                            "D": "Huấn luyện lại trọng số mô hình."
                        },
                        "correct": "A",
                        "exp": "NMS lọc các khung bao dư thừa đè lên nhau dựa trên ngưỡng IoU (Intersection over Union), giữ lại đúng 1 khung tối ưu nhất cho mỗi vật thể.",
                        "concept": "Non-Maximum Suppression (NMS)"
                    }
                ]
            },
            {
                "id": 1103, "code": "CV103",
                "title": "Chương 3: Phân đoạn Ảnh Ngữ nghĩa (Semantic Segmentation) & Mô hình Generative",
                "desc": "Kiến trúc U-Net cho phân vùng tế bào/ảnh y tế, Mask R-CNN phân đoạn cá thể (Instance Segmentation), GANs và Diffusion Models tạo ảnh nghệ thuật.",
                "order": 3,
                "materials": [
                    {"title": "Stanford CS231n: Convolutional Neural Networks for Visual Recognition", "url": "https://cs231n.github.io/", "type": MaterialType.READING, "univ": "Stanford University", "level": 4.0, "desc": "Khóa học thị giác máy tính kinh điển của Stanford do Fei-Fei Li sáng lập."},
                    {"title": "Video Bài Giảng: U-Net Architecture Explained with Code", "url": "https://www.youtube.com/watch?v=u1loyDCo4gE", "type": MaterialType.VIDEO, "univ": "DigitalSreeni", "level": 3.5, "desc": "Kiến trúc Encoder-Decoder và Skip Connections trong bài toán phân đoạn ảnh."}
                ],
                "questions": [
                    {
                        "content": "Đặc trưng kiến trúc mang tính đột phá của mạng U-Net giúp khôi phục chi tiết vị trí không gian chính xác là gì?",
                        "options": {
                            "A": "Các đường nối tắt (Skip Connections) truyền trực tiếp bản đồ đặc trưng từ Encoder sang Decoder",
                            "B": "Loại bỏ hoàn toàn các lớp Convolution",
                            "C": "Chỉ dùng 1 nơ-ron duy nhất ở tầng cuối",
                            "D": "Không sử dụng hàm kích hoạt"
                        },
                        "correct": "A",
                        "exp": "Skip Connections trong U-Net chuyển thông tin độ phân giải cao từ các tầng đầu sang các tầng giải mã, giúp phân đoạn chi tiết ranh giới vật thể.",
                        "concept": "U-Net Skip Connections"
                    }
                ]
            }
        ]
    }
]

def seed_new_subjects():
    with SessionLocal() as session:
        print("Bắt đầu mở rộng danh mục môn học (Curriculum Expansion)...")
        for sub_data in NEW_SUBJECTS:
            existing = session.query(Subject).filter(Subject.code == sub_data["code"]).first()
            if existing:
                print(f"Môn {sub_data['code']} đã tồn tại. Bỏ qua.")
                continue
            
            sub = Subject(
                code=sub_data["code"],
                title=sub_data["title"],
                description=sub_data["description"]
            )
            session.add(sub)
            session.flush()
            print(f"-> Đã tạo môn học mới: {sub.code} (ID: {sub.id})")

            for t_data in sub_data["topics"]:
                topic = Topic(
                    id=t_data["id"],
                    subject_id=sub.id,
                    code=t_data["code"],
                    title=t_data["title"],
                    description=t_data["desc"],
                    order_index=t_data["order"]
                )
                session.add(topic)
                session.flush()

                # Materials
                for m_data in t_data.get("materials", []):
                    mat = LearningMaterial(
                        topic_id=topic.id,
                        title=m_data["title"],
                        content_url=m_data["url"],
                        material_type=m_data["type"],
                        university=m_data["univ"],
                        difficulty_level=m_data["level"],
                        text_content=m_data["desc"],
                        version=1,
                        is_latest=True,
                        created_by_id=1
                    )
                    session.add(mat)

                # Questions
                for q_data in t_data.get("questions", []):
                    q = Question(
                        topic_id=topic.id,
                        content=q_data["content"],
                        question_type=QuestionType.MULTIPLE_CHOICE,
                        difficulty_level=3.0,
                        options=q_data["options"],
                        correct_answer=q_data["correct"],
                        explanation=q_data["exp"]
                    )
                    session.add(q)
            
            session.commit()
            print(f"   ✓ Đã thêm {len(sub_data['topics'])} chương và học liệu cho môn {sub.code}")

        # In tổng kết
        all_subs = session.query(Subject).all()
        print(f"\n=> TỔNG CỘNG HIỆN CÓ {len(all_subs)} MÔN HỌC TRONG HỆ THỐNG:")
        for s in all_subs:
            t_count = session.query(Topic).filter(Topic.subject_id == s.id).count()
            print(f"   [{s.id}] {s.code}: {s.title} ({t_count} bài học)")

if __name__ == "__main__":
    seed_new_subjects()
