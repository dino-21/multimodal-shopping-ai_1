# OpenAI 연결 + RAG 문서 위치 설정
import os      # 파일/폴더 경로 처리 (저장 위치 만들기)
from openai import OpenAI     # OpenAI API 사용 (챗봇)
from config import OPENAI_API_KEY, RAG_DIR   # API 키 (OpenAI 인증) + RAG 문서 폴더 경로 가져오기


# OpenAI 클라이언트 생성
client = OpenAI(api_key=OPENAI_API_KEY)


# RAG 문서 불러오기
def load_rag_documents():
    texts = []


    # 폴더 없으면 빈 문자열 반환
    if not os.path.exists(RAG_DIR):
        return ""


    # rag_docs 폴더 안의 txt 파일 읽기
    for filename in os.listdir(RAG_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(RAG_DIR, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    texts.append(f.read())
            except Exception as e:
                print(f"[RAG 파일 읽기 실패] {filename}: {e}")


    # 여러 문서를 하나로 합치기
    return "\n\n".join(texts)



# RAG 챗봇 질문 처리
def ask_rag_chat(question: str) -> str:
    context = load_rag_documents()  # 문서 불러오기

    # 문서 없으면 안내 메시지
    if not context.strip():
        return "현재 참고할 상품 문서가 없습니다. rag_docs 폴더를 확인해주세요."


 # 시스템 역할 정의 (챗봇 성격 설정)
    system_prompt = """
당신은 TrendyFit Mall의 쇼핑몰 상담 챗봇입니다.
반드시 제공된 참고 문서 내용을 바탕으로만 답변하세요.
문서에 없는 내용은 추측하지 말고 '문서에서 확인되지 않습니다.'라고 답하세요.
답변은 친절하고 자연스러운 한국어로 작성하세요.
배송, 환불, 교환, 적립금, 상품 추천, 코디 추천 질문에 잘 답변하세요.
"""

    # 사용자 질문 + 문서 함께 전달
    user_prompt = f"""
[참고 문서]
{context}

[사용자 질문]
{question}
"""

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3   # 낮을수록 정확한 답변
    )

    # 답변 반환
    return response.choices[0].message.content.strip()


# 간단 호출용 함수
def simple_rag_answer(question: str) -> str:
    return ask_rag_chat(question)


"""
1. rag_docs 폴더에 txt 파일 넣어야 작동
2. 문서 없으면 답변 안됨
3. temperature 낮으면 정확 ↑
"""