# -*- coding: utf-8 -*-
"""
End-to-End Automated Test Suite for Aegis Learn (FastAPI + SQLAlchemy 2.0)
Tests:
1. Real JWT Authentication (Register, Login, Password Hashing)
2. Admin Protection (RBAC: 401 No Token, 403 Student Token, 200 Admin Token)
3. Spaced Repetition (Dynamic Database Query per User, JWT User ID extraction)
4. Analytics Progress (Filtered by User ID, JWT User ID extraction)
5. AI Tutor & Admin AI Assistant
"""

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import unittest
from fastapi.testclient import TestClient
from main import app
from auth import decode_access_token

client = TestClient(app)

class TestAegisLearnSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Login as Admin (user_id = 1)
        admin_login = client.post("/api/v1/auth/login", json={
            "email": "admin@aegislearn.edu.vn",
            "password": "admin"
        })
        assert admin_login.status_code == 200, f"Admin login failed: {admin_login.text}"
        cls.admin_token = admin_login.json()["access_token"]
        cls.admin_headers = {"Authorization": f"Bearer {cls.admin_token}"}
        cls.admin_user_id = admin_login.json()["user_id"]

        # 2. Login as Student (user_id = 2)
        student_login = client.post("/api/v1/auth/login", json={
            "email": "student.a@aegislearn.edu.vn",
            "password": "student"
        })
        assert student_login.status_code == 200, f"Student login failed: {student_login.text}"
        cls.student_token = student_login.json()["access_token"]
        cls.student_headers = {"Authorization": f"Bearer {cls.student_token}"}
        cls.student_user_id = student_login.json()["user_id"]

    def test_01_real_jwt_token_payload(self):
        """Test token contains sub, user_id, email, and correct role"""
        admin_claims = decode_access_token(self.admin_token)
        self.assertEqual(admin_claims["role"], "ADMIN")
        self.assertEqual(int(admin_claims["user_id"]), self.admin_user_id)

        student_claims = decode_access_token(self.student_token)
        self.assertEqual(student_claims["role"], "STUDENT")
        self.assertEqual(int(student_claims["user_id"]), self.student_user_id)
        print("  [PASS] Test 1: Real JWT Tokens signed and verified successfully")

    def test_02_register_new_user(self):
        """Test registering a new student account with bcrypt hash"""
        import time
        unique_email = f"student.test.{int(time.time())}@aegislearn.edu.vn"
        res = client.post("/api/v1/auth/register", json={
            "email": unique_email,
            "password": "MySecurePassword123!",
            "full_name": "Trần Thị B",
            "role": "STUDENT"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data["access_token"]) > 30)
        self.assertNotEqual(data["access_token"], "mock_jwt_access_token_12345")
        self.assertEqual(data["email"], unique_email)
        self.assertEqual(data["full_name"], "Trần Thị B")
        print("  [PASS] Test 2: User registration creates DB record and signs real JWT")

    def test_03_admin_rbac_protection(self):
        """Test Admin endpoints security: 401 (No Token), 403 (Student), 200 (Admin)"""
        # A. Truy cập không có Token -> Bắt buộc trả về 401 Unauthorized
        res_no_token = client.get("/api/v1/admin/stats")
        self.assertEqual(res_no_token.status_code, 401)

        # B. Truy cập bằng Student Token -> Bắt buộc bị từ chối với 403 Forbidden
        res_student = client.get("/api/v1/admin/stats", headers=self.student_headers)
        self.assertEqual(res_student.status_code, 403)

        # C. Truy cập bằng Admin Token -> Cho phép truy cập 200 OK
        res_admin = client.get("/api/v1/admin/stats", headers=self.admin_headers)
        self.assertEqual(res_admin.status_code, 200)
        data = res_admin.json()
        self.assertIn("total_students", data)
        print("  [PASS] Test 3: Admin RBAC protection strictly enforced (401 -> 403 -> 200)")

    def test_04_spaced_repetition_user_data(self):
        """Test spaced repetition computes retention using real user data from JWT"""
        # A. Có Token học sinh (User 2) -> Tự động trích xuất user_id=2 từ JWT
        res_jwt = client.get("/api/v1/learning-path/spaced-repetition/1", headers=self.student_headers)
        self.assertEqual(res_jwt.status_code, 200)
        data_jwt = res_jwt.json()
        self.assertEqual(data_jwt["user_id"], self.student_user_id)
        self.assertTrue("review_recommendations" in data_jwt)

        # B. Không có Token -> Sử dụng user_id từ URL path
        res_path = client.get("/api/v1/learning-path/spaced-repetition/1")
        self.assertEqual(res_path.status_code, 200)
        data_path = res_path.json()
        self.assertEqual(data_path["user_id"], 1)

        print(f"  [PASS] Test 4: Spaced Repetition dynamically bound to authenticated user_id ({data_jwt['user_id']})")

    def test_05_progress_analytics_filtered_by_user(self):
        """Test progress dashboard is personalized and filtered by user_id from JWT"""
        # Khi có JWT Token -> Lấy dữ liệu chính xác của user đăng nhập
        res = client.get("/api/v1/analytics/progress/1", headers=self.student_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["user_id"], self.student_user_id)
        self.assertIn("overall_progress_percentage", data)
        self.assertIn("recent_assessments", data)
        print(f"  [PASS] Test 5: Progress report personalized for user {data['user_id']} ({data['full_name']})")

    def test_06_ai_tutor_chat(self):
        """Test AI Tutor chat endpoint with intelligent fallback response"""
        res = client.post("/api/v1/ai/chat", json={
            "message": "Cho em hỏi lộ trình học Python cho người mới bắt đầu?",
            "topic_id": 101
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data["reply"]) > 50)
        self.assertTrue(len(data["suggested_followups"]) > 0)
        print(f"  [PASS] Test 6: AI Tutor answered using [{data['model_used']}]")

    def test_07_admin_ai_generate_remedial(self):
        """Test Admin AI remedial quiz generator endpoint (secured with admin token)"""
        res = client.post("/api/v1/admin/ai/generate-remedial-quiz", headers=self.admin_headers, json={
            "topic_code": "T103",
            "topic_title": "Bài 3: Phân tích & Làm sạch Dữ liệu với Pandas",
            "count": 3
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["remedial_questions"]), 3)
        print(f"  [PASS] Test 7: Admin AI Remedial Quiz generated {len(data['remedial_questions'])} questions")

    def test_08_multi_subject_catalog_and_3tier_search(self):
        """Test Multi-Subject Catalog & 3-Tier Search Recommendation (Web -> YouTube -> High-Score Strategy)"""
        # A. Lấy danh sách tất cả các môn học đa dạng (AI_PYTHON, MATH_AI, CS_DSA, DB_SQL, DEEP_LEARNING)
        res_list = client.get("/api/v1/subjects")
        self.assertEqual(res_list.status_code, 200)
        subjects = res_list.json()
        self.assertGreaterEqual(len(subjects), 5)
        subject_codes = [s["code"] for s in subjects]
        self.assertIn("MATH_AI", subject_codes)
        self.assertIn("CS_DSA", subject_codes)
        self.assertIn("DEEP_LEARNING", subject_codes)
        print(f"  [PASS] Test 8A: Loaded {len(subjects)} diverse AI subjects ({', '.join(subject_codes)})")

        # B. Tìm kiếm môn Toán AI + mục tiêu điểm 9.5
        res_search = client.get("/api/v1/subjects/search?q=toán ai&target_score=9.5")
        self.assertEqual(res_search.status_code, 200)
        data = res_search.json()
        self.assertEqual(data["matched_subject"]["code"], "MATH_AI")
        self.assertGreaterEqual(len(data["tier1_web_resources"]), 1)
        self.assertGreaterEqual(len(data["tier2_youtube_videos"]), 1)
        self.assertEqual(data["tier3_score_strategy"]["target_score"], 9.5)
        self.assertIn("A+", data["tier3_score_strategy"]["grade_letter"])
        print(f"  [PASS] Test 8B: 3-Tier search returned {len(data['tier1_web_resources'])} Web Docs, {len(data['tier2_youtube_videos'])} YouTube Videos, and Tier 3 Strategy: {data['tier3_score_strategy']['grade_letter']}")

    def test_09_high_score_prediction_and_error_vault(self):
        """Test High-Score Prediction, Radar Gaps, and Smart Error Vault"""
        # A. Score Prediction
        res_pred = client.get(f"/api/v1/analytics/score-prediction/{self.student_user_id}", headers=self.student_headers)
        self.assertEqual(res_pred.status_code, 200)
        pred_data = res_pred.json()
        self.assertIn("current_predicted_score", pred_data)
        self.assertIn("topics_radar", pred_data)
        self.assertGreaterEqual(len(pred_data["topics_radar"]), 3)
        print(f"  [PASS] Test 9A: Score Prediction: Predicted {pred_data['current_predicted_score']}/10.0 vs Target {pred_data['target_score']}")

        # B. Error Vault
        res_vault = client.get(f"/api/v1/quiz/errors/{self.student_user_id}", headers=self.student_headers)
        self.assertEqual(res_vault.status_code, 200)
        vault_items = res_vault.json()
        self.assertGreaterEqual(len(vault_items), 1)
        self.assertIn("trap_warning", vault_items[0])
        print(f"  [PASS] Test 9B: Smart Error Vault contains {len(vault_items)} tracked traps and mistakes")

        # C. 48h Cramming Cheat Sheet
        res_cheat = client.get("/api/v1/cramming/cheat-sheet/103")
        self.assertEqual(res_cheat.status_code, 200)
        cheat_data = res_cheat.json()
        self.assertIn("must_remember_formulas", cheat_data)
        self.assertIn("top_exam_traps", cheat_data)
        print(f"  [PASS] Test 9C: 48h Cramming Cheat Sheet loaded with {len(cheat_data['must_remember_formulas'])} formulas and {len(cheat_data['top_exam_traps'])} traps")

    def test_10_ai_tutor_google_grounding(self):
        """Test AI Tutor chat endpoint with Google Search Grounding & Web Citations"""
        res = client.post("/api/v1/ai/chat", json={
            "message": "Giải thích chi tiết về hàm loc và iloc trong Pandas kèm ví dụ?",
            "topic_id": 103
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(len(data["reply"]) > 50)
        self.assertIn("sources", data)
        self.assertGreaterEqual(len(data["sources"]), 1)
        self.assertIn("pandas", data["sources"][0]["url"].lower())
        print(f"  [PASS] Test 10: AI Tutor answered with Google Grounded citation: {data['sources'][0]['title']}")


if __name__ == "__main__":
    print("\n=======================================================")
    print("CHẠY BỘ KIỂM THỬ TỰ ĐỘNG HỆ THỐNG AEGIS LEARN (BACKEND)")
    print("=======================================================")
    unittest.main()

