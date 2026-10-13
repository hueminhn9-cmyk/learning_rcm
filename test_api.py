import sys
import urllib.request
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_ai_generate_remedial():
    payload = {
        "topic_code": "T103",
        "topic_title": "Bài 3: Phân tích & Làm sạch Dữ liệu với Pandas",
        "count": 3
    }
    req = urllib.request.Request(f"{BASE_URL}/admin/ai/generate-remedial-quiz", data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    print("AI Generate Remedial Quiz Test:")
    print(f"Generated {len(data['remedial_questions'])} questions for {data['topic_code']} - {data['topic_title']}")
    for q in data['remedial_questions']:
        print(f"  Q: {q['content']} (Correct: {q['correct_answer']})")

if __name__ == "__main__":
    test_ai_generate_remedial()
