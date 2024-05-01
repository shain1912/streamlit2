import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
# Firestore 클라이언트 초기화
#db = firestore.Client.from_service_account_json("firestore-key.json")
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
# 사용자 이름 입력
user_name = st.text_input("사용자 이름을 입력하세요.")

# 데이터 조회 및 계산 함수
def fetch_data():
    posts_ref = db.collection("posts")
    docs = posts_ref.stream()

    total_scores = []
    user_scores = {}
    question_correct_counts = {f"문제{i+1}": 0 for i in range(5)}
    question_total_counts = {f"문제{i+1}": 0 for i in range(5)}

    for doc in docs:
        doc_data = doc.to_dict()
        score = sum(doc_data.values())
        total_scores.append(score)
        user_scores[doc.id] = score
        
        for i in range(5):
            question_key = f"문제{i+1}"
            if doc_data[question_key] == 20:
                question_correct_counts[question_key] += 1
            question_total_counts[question_key] += 1

    return total_scores, user_scores, question_correct_counts, question_total_counts

total_scores, user_scores, question_correct_counts, question_total_counts = fetch_data()

# 1. 전체 평균 점수 계산
average_score = sum(total_scores) / len(total_scores) if total_scores else 0

# 2. 사용자 랭킹 계산
sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
ranking = {name: rank + 1 for rank, (name, _) in enumerate(sorted_scores)}
user_ranking = ranking.get(user_name, 'N/A')

# 3. 각 문제의 정답률 계산
question_accuracy = {key: (question_correct_counts[key] / question_total_counts[key]) * 100 for key in question_correct_counts}

# 결과 표시
st.write(f"전체 평균 점수: {average_score:.2f}")
if user_name:
    st.write(f"{user_name}의 랭킹: {user_ranking}")
else:
    st.write("사용자 이름을 입력하세요.")

st.write("각 문제의 정답률:")
for question, accuracy in question_accuracy.items():
    st.write(f"{question}: {accuracy:.2f}%")

