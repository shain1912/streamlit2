import streamlit as st
import pandas as pd
from google.cloud import firestore
from io import BytesIO
from google.oauth2 import service_account
# Firestore 클라이언트 초기화
#db = firestore.Client.from_service_account_json("firestore-key.json")
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)
# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요.", type="password")

# 올바른 비밀번호 정의
correct_password = "1234"  # 실제 사용할 때는 보다 안전한 방법으로 관리 필요

# 데이터 조회 및 계산 함수
def fetch_data():
    posts_ref = db.collection("posts")
    docs = posts_ref.stream()

    data = []
    user_scores = {}

    for doc in docs:
        doc_data = doc.to_dict()
        score = sum(doc_data.values())
        data.append([doc.id] + list(doc_data.values()) + [score, score / 5])
        user_scores[doc.id] = score

    return data, user_scores

# 사용자 데이터와 점수 표시
if password == correct_password:
    data, user_scores = fetch_data()

    # 사용자 랭킹 계산
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    ranking = {name: rank + 1 for rank, (name, _) in enumerate(sorted_scores)}

    # 데이터 프레임 생성
    columns = ["사용자 이름", "문제1", "문제2", "문제3", "문제4", "문제5", "총점", "평균"]
    df = pd.DataFrame(data, columns=columns)
    df['랭킹'] = df['사용자 이름'].map(ranking)

    # 결과 테이블 표시
    st.write("사용자 점수 테이블")
    st.dataframe(df)

    # CSV 파일로 저장 및 다운로드 링크 제공
    def convert_df_to_excel(df):
        # 엑셀 파일로 변환
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

    excel_data = convert_df_to_excel(df)

    st.download_button(
        label="엑셀로 다운로드",
        data=excel_data,
        file_name="user_scores.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    if st.button('Submit'):
        st.error("잘못된 비밀번호입니다.")
