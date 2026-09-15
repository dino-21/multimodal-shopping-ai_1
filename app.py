# 1. 기본 라이브러리
import os  # 파일/폴더 관련 작업

# 2. FastAPI 관련
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware   # CORS 허용 (프론트 연결용)
from fastapi.staticfiles import StaticFiles  # 정적 파일 (이미지 등)
from fastapi.responses import FileResponse   # HTML 파일 반환


# 3. Pydantic (요청/응답 데이터 구조)
from pydantic import BaseModel

# 4. 서비스 (비즈니스 로직)
from services.yolo_service import save_upload_file, classify_image_file
from services.product_service import (
    save_product_to_db,
    search_products_from_db,
    update_product_in_db,
    delete_product_from_db
)
from services.rag_service import ask_rag_chat




# 5. 설정
from config import UPLOAD_DIR   # 업로드 폴더 경로



# 6. 스키마 (DTO) : API 입출력 형태 정의
from schemas import ClassifyResult, ProductUpdateRequest





# FastAPI 서버 생성
app = FastAPI()


# 업로드 폴더 없으면 자동 생성
os.makedirs(UPLOAD_DIR, exist_ok=True)



# CORS 설정 (프론트에서 접근 가능하도록 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 모든 주소 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 정적 파일 설정
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images") # 업로드된 이미지 접근 가능
app.mount("/img", StaticFiles(directory="img"), name="img")  # 기본 이미지 폴더


# 기본 서버 확인 API
@app.get("/")
def home():
    return {"message": "서버 실행 중"}


# HTML 페이지 반환
@app.get("/page")
def page():
    return FileResponse("index.html")


# 이미지 업로드 → YOLO 분석 → DB 저장
@app.post("/classify-and-save", response_model=ClassifyResult)
async def classify_and_save(file: UploadFile = File(...)):
    try:
        # 1. 업로드 파일 저장
        save_path, public_path = save_upload_file(file)

        # 2. YOLO 분석
        result_data = classify_image_file(save_path, public_path)
        print("YOLO 결과:", result_data)

        # 3. DB 저장 (매핑 실패여도 무조건 DB 저장)
        saved_result = save_product_to_db(result_data)
        print("DB 저장 결과:", saved_result)

        # 4. 저장된 결과 반환 (id 포함)
        return ClassifyResult(**saved_result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"실제 에러: {str(e)}")
    


# 상품 검색 API
@app.get("/search-products")
def search_products(q: str = Query(default="")):
    try:
        rows = search_products_from_db(q) # DB에서 상품 검색
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류: {str(e)}")



# 상품 수정 API
@app.put("/update-product")
def update_product(req: ProductUpdateRequest):
    try:
        row = update_product_in_db(req) #DB 수정
        if not row:
            raise HTTPException(status_code=404, detail="수정할 상품을 찾지 못했습니다.")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"수정 중 오류: {str(e)}")




# 상품 삭제 API
@app.delete("/delete-product/{product_id}")
def delete_product(product_id: int):
    try:
        ok = delete_product_from_db(product_id) #  DB 삭제
        if not ok:
            raise HTTPException(status_code=404, detail="삭제할 상품을 찾지 못했습니다.")
        return {"message": "삭제 완료"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"삭제 중 오류: {str(e)}")



# RAG 챗봇 요청 데이터
class ChatRequest(BaseModel):
    question: str


# RAG 챗봇 응답 데이터
class ChatResponse(BaseModel):
    answer: str



# RAG 챗봇 API
@app.post("/rag-chat", response_model=ChatResponse)
def rag_chat(request: ChatRequest):
    answer = ask_rag_chat(request.question)
    return {"answer": answer}