# AI Hỗ Trợ Học Tập (Aegis Learn System)

Hệ thống hỗ trợ học tập cá nhân hóa và quản lý học tập thông minh ứng dụng AI (FastAPI + React UI + SQLAlchemy).

## ✨ Tính năng chính

- **Lộ trình học cá nhân hóa:** Đề xuất tài liệu học tập theo năng lực, phong cách học và mục tiêu của học viên.
- **Hệ thống Kiểm tra & Đánh giá (Quiz & Assessments):**
  - Thi trắc nghiệm trực tuyến với ngân hàng câu hỏi đa dạng theo mức độ Bloom.
  - Chấm điểm tự động và đề xuất lời giải chi tiết.
  - Lịch sử làm bài thi và xem lại bài làm chi tiết (Quiz Attempt History & Review).
  - Đề xuất bài kiểm tra cải thiện (Remedial Quiz).
- **Ôn tập ngắt quãng (Spaced Repetition):** Thuật toán ghi nhớ ngắt quãng giúp củng cố kiến thức theo chu kỳ.
- **Phương pháp Feynman:** Ghi nhận và phản hồi giải thích kiến thức của học viên.
- **Bảng điều khiển Quản trị (Admin Dashboard):**
  - Theo dõi tiến độ học viên, tỷ lệ hoàn thành.
  - Quản lý ngân hàng câu hỏi, bài đánh giá và cấu hình trọng số đề xuất AI.

## 🛠️ Công nghệ sử dụng

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy 2.0, Pydantic, SQLite
- **Frontend:** React, HTML5, Vanilla CSS, Tailwind-like styling, Babel standalone
- **Dữ liệu:** Tích hợp Kaggle & EdX Educational Datasets

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Cài đặt thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### 2. Khởi tạo dữ liệu mẫu (Tùy chọn)

```bash
python seed_data.py
python seed_more_questions.py
```

### 3. Khởi chạy hệ thống

```bash
python main.py
```
Hoặc:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

- Giao diện Học viên: [http://localhost:8000/](http://localhost:8000/)
- Giao diện Quản trị: [http://localhost:8000/admin.html](http://localhost:8000/admin.html)
- Tài liệu API (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
