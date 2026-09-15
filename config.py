# 환경 설정 파일 (config.py)
# 프로젝트에서 사용하는 경로 / 키 / DB 설정을 모아놓은 파일
# 다른 파일에서 import 해서 사용


# 1. 기본 라이브러리
import os

# .env 파일 읽기
from dotenv import load_dotenv


# 2. .env 파일 로드
load_dotenv() # 환경변수 (API KEY, DB 정보 등)를 가져옴


# 3. 프로젝트 기본 경로, 현재 파일(config.py)의 위치 기준
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 4. 폴더 / 파일 경로 설정
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads") # 업로드 폴더 (이미지 저장 위치)
MODEL_PATH = os.path.join(BASE_DIR, "yolo11s-cls.pt") # YOLO 모델 파일 경로
RAG_DIR = os.path.join(BASE_DIR, "rag_docs")   # RAG 문서 폴더


# OpenAI 키 (.env 파일에서 가져옴)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 6. DB 연결 정보
# MySQL 접속 정보
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),   # DB 서버 주소
    "port": int(os.getenv("DB_PORT", "3306")),   # 포트 번호
    "user": os.getenv("DB_USER", "root"),        # 사용자
    "password": os.getenv("DB_PASSWORD", "1234"),   # 비밀번호
    "database": os.getenv("DB_NAME", "style_finder"),  # DB 이름
    "charset": "utf8mb4"
}