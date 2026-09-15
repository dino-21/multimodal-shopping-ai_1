# chemas.py = API 데이터 형식 정의 파일
# BaseModel = 데이터 틀 / List, Optional = 타입 지정


from pydantic import BaseModel       # 데이터 구조(모델) 만들 때 사용 (API 입력/출력 형식 정의)
from typing import List, Optional    # 자료형 지정 (List=배열, Optional=값 없어도 됨)


# 이미지 분석 + DB 저장 결과
class ClassifyResult(BaseModel):
    id: Optional[int] = None   # DB id (없을 수도 있음)
    image_path: str            # 이미지 경로
    yolo_label: str          # YOLO 분석 결과 (영어)
    category: str            # 한글 카테고리
    main_cat: str            # 대분류
    mid_cat: str             # 중분류
    sub_cat: str             # 소분류
    confidence: float        # AI 신뢰도
    title: str               # 상품명
    description: str         # 상품 설명
    tags: List[str]          # 태그 (여러 개)
    status: str              # 상태 (READY 등)


# 상품 수정 요청 데이터
class ProductUpdateRequest(BaseModel):  
    id: int                            # 수정할 상품 id
    category: Optional[str] = None
    main_cat: Optional[str] = None
    mid_cat: Optional[str] = None
    sub_cat: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None # Optional = 값 없어도 됨



# 챗봇 질문 데이터
class ChatRequest(BaseModel):
    question: str     # 사용자 질문


# 챗봇 응답 데이터
class ChatResponse(BaseModel):
    answer: str       # AI 답변

