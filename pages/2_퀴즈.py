import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
# Firestore 클라이언트 초기화
#db = firestore.Client.from_service_account_json("firestore-key.json")
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
# 문제, 선택지, 그리고 정답 정의
questions = [
    {"question": "대한민국의 수도는 어디입니까?", "options": ["서울", "부산", "인천", "대구", "광주"], "answer": "서울"},
    {"question": "파이썬의 창시자는 누구입니까?", "options": ["가이도 반 로섬", "제임스 고슬링", "린 머코비츠", "마크 저커버그", "스티브 잡스"], "answer": "가이도 반 로섬"},
    {"question": "HTML은 무엇의 약자입니까?", "options": ["Hyper Text Markup Language", "High Text Markup Language", "Hyper Tabular Markup Language", "None of these", "Hyper Tech Markup Language"], "answer": "Hyper Text Markup Language"},
    {"question": "인터넷에서 웹 페이지를 보기 위해 사용하는 프로그램은 무엇입니까?", "options": ["웹 브라우저", "웹 서버", "웹 페이지", "인터넷 서비스", "HTML"], "answer": "웹 브라우저"},
    {"question": "윈도우 운영체제를 만든 회사는 어디입니까?", "options": ["애플", "마이크로소프트", "구글", "IBM", "삼성"], "answer": "마이크로소프트"}
]

# 사용자 이름 입력
user_name = st.text_input("이름을 입력하세요.")

# 각 문제에 대한 사용자 응답 저장
responses = {}
score = 0
correct_answers = {}

for i, question in enumerate(questions):
    responses[i] = st.radio(question["question"], question["options"])
    correct_answers[i] = responses[i] == question["answer"]  # 정답 여부 확인

# 점수 계산
score = sum(20 for correct in correct_answers.values() if correct)

# 제출 버튼 (이름이 입력되었을 때만 활성화)
if st.button("제출하기") and user_name:
    st.success("제출되었습니다! 점수: " + str(score))
    doc_ref = db.collection("posts").document(user_name)  # 사용자 이름을 문서 ID로 사용
    doc_data = {f"문제{i+1}": 20 if correct_answers[i] else 0 for i in range(5)}
    doc_ref.set(doc_data)  # 점수 데이터 Firestore에 저장
else:
    st.warning("이름을 입력하세요.")
