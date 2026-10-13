"""
Kaggle Dataset Importer Script for Aegis Learn System
Script hỗ trợ đọc các file CSV tải về từ Kaggle Datasets và nạp trực tiếp vào CSDL SQLite 'learning_app.db'
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Subject, Topic, LearningMaterial, Question, User, UserRole, MaterialType, QuestionType

DATABASE_URL = "sqlite:///./learning_app.db"

def import_courses_from_kaggle_csv(csv_path: str):
    """
    Hàm mẫu nạp danh sách Khóa học / Học liệu từ Kaggle CSV (Coursera / EdX / OULAD) vào CSDL SQLite
    """
    if not os.path.exists(csv_path):
        print(f"❌ File CSV '{csv_path}' không tồn tại. Hãy tải về từ Kaggle và đặt vào thư mục này!")
        return

    print(f"⏳ Đang đọc dữ liệu từ Kaggle CSV: {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"📊 Đã tìm thấy {len(df)} dòng dữ liệu!")

    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        # Lấy Admin ID để tạo bài
        admin = session.query(User).filter_by(role=UserRole.ADMIN).first()
        admin_id = admin.id if admin else 1

        # Lấy Topic mẫu để gán học liệu
        topic = session.query(Topic).first()
        topic_id = topic.id if topic else 1

        imported_count = 0
        for idx, row in df.head(50).iterrows(): # Import 50 bản ghi mẫu
            # Giả định các cột thường có trong Kaggle EdTech datasets (title, type, difficulty)
            title = str(row.get('course_name') or row.get('title') or row.get('name') or f"Học liệu Kaggle #{idx+1}")
            
            material = LearningMaterial(
                topic_id=topic_id,
                title=title[:250],
                material_type=MaterialType.VIDEO,
                difficulty_level=3.0,
                created_by_id=admin_id
            )
            session.add(material)
            imported_count += 1

        session.commit()
        print(f"🎉 Đã nạp thành công {imported_count} học liệu từ Kaggle vào CSDL 'learning_app.db'!")

if __name__ == "__main__":
    print("=== KAGGLE DATASET IMPORTER ===")
    print("Để nạp dữ liệu Kaggle thực tế:")
    print("1. Tải file CSV từ Kaggle (ví dụ: edx_courses.csv hoặc courses.csv)")
    print("2. Đặt tệp CSV vào thư mục này và gọi hàm: import_courses_from_kaggle_csv('courses.csv')\n")
