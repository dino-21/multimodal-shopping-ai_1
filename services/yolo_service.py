# 파일 저장 + YOLO 분석 + 카테고리 변환을 위해 필요한 라이브러리들
import os      # 파일/폴더 경로 처리 (저장 위치 만들기)
import uuid    # 파일 이름 중복 방지 (랜덤 이름 생성)
import shutil  # 파일 복사 (업로드 파일 저장할 때 사용)
from ultralytics import YOLO   # YOLO AI 모델 (이미지 분석)
from config import UPLOAD_DIR, MODEL_PATH  # 업로드 폴더 경로, YOLO 모델 경로 가져오기
from category import get_category_info  # YOLO 결과(영어)를 한글 카테고리로 변환하는 함수


# YOLO 모델 1번만 로딩 (서버 시작 시 실행)
model = YOLO(MODEL_PATH)


# 이미지 파일 저장
def save_upload_file(file):
    # 업로드 폴더 없으면 생성
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 파일명 중복 방지 (uuid 사용)
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"

    save_path = os.path.join(UPLOAD_DIR, unique_name)   # 실제 저장 경로
    public_path = f"/images/{unique_name}"              # 브라우저 접근 경로

    # 파일 저장
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return save_path, public_path


# 이미지 분석 (YOLO)
def classify_image_file(save_path, public_path):
    results = model(save_path) # YOLO 실행

     # 기본값 (분석 실패 대비)
    yolo_label = "unknown"
    confidence = 0.0


    # 결과가 있을 경우
    if results and len(results) > 0:
        probs = results[0].probs

        if probs is not None:
            top1_index = int(probs.top1)            # 가장 높은 확률 index
            confidence = float(probs.top1conf)      # 신뢰도
            yolo_label = results[0].names[top1_index]   # 라벨 (영어)

    # category.py 에서 매핑 정보 가져오기
    mapped = get_category_info(yolo_label)


     # 매핑 실패 (등록 안된 라벨)
    if mapped is None:
        return {
            "id": None,
            "image_path": public_path,
            "yolo_label": yolo_label,
            "category": "기타",
            "main_cat": "기타",
            "mid_cat": "기타",
            "sub_cat": "기타",
            "confidence": confidence,
            "title": "지원하지 않은 상품",
            "description": f"YOLO는 '{yolo_label}'로 예측했지만 category.py에 등록되지 않았습니다.",
            "tags": ["매핑실패", yolo_label],
            "status": "MAPPING_FAILED"
        }
    
    # 매핑 성공
    return {
        "id": None,
        "image_path": public_path,
        "yolo_label": yolo_label,
        "category": mapped["category"],
        "main_cat": mapped["main_cat"],
        "mid_cat": mapped["mid_cat"],
        "sub_cat": mapped["sub_cat"],
        "confidence": confidence,
        "title": mapped["title"],
        "description": mapped["description"],
        "tags": mapped["tags"],
        "status": "READY"
    }

"""
1. uuid = 파일명 중복 방지
2. YOLO 결과는 영어 → category.py에서 변환
3. 매핑 실패해도 DB 저장해야 함
4. 모델은 1번만 로딩
"""