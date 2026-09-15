# StyleFinder AI

이미지를 업로드하면 YOLO가 상품 종류를 분류하고, 분석 결과를 MySQL에 저장하는 멀티모달 쇼핑 AI 서비스입니다. 상품 검색·수정·삭제 기능과 쇼핑몰 문서를 참고하는 OpenAI 챗봇 기능도 제공합니다.

## 주요 기능

- 상품 이미지 업로드
- YOLO11 이미지 분류
- YOLO 영문 라벨을 한글 상품 카테고리로 변환
- 이미지 분석 결과 MySQL 저장
- 상품 검색·수정·삭제
- 상품·배송·교환·환불 문서를 참고하는 AI 상담
- FastAPI Swagger 문서 제공

## 서비스 동작 흐름

```text
사용자 이미지 업로드
        ↓
Frontend (index.html)
        ↓
FastAPI Backend (app.py)
        ↓
YOLO 이미지 분류
        ↓
category.py 상품 정보 변환
        ↓
MySQL 상품 정보 저장
        ↓
JSON 응답 및 화면 출력
```

챗봇은 다음과 같이 동작합니다.

```text
사용자 질문
    ↓
FastAPI /rag-chat
    ↓
rag_docs 문서 읽기
    ↓
참고 문서와 질문을 OpenAI에 전달
    ↓
AI 답변 반환
```

> 현재 챗봇은 Vector DB에서 관련 문서를 검색하는 방식이 아닙니다. `rag_docs`의 텍스트 문서 전체를 프롬프트에 넣어 답변하는 간단한 문서 기반 방식입니다.

## 기술 스택

| 구분 | 기술 | 역할 |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | 이미지 업로드와 결과 화면 |
| Backend | FastAPI | REST API와 전체 작업 순서 관리 |
| 데이터 검증 | Pydantic | API 요청·응답 형식 검사 |
| Vision AI | Ultralytics YOLO11 Classification | 상품 이미지 분류 |
| Database | MySQL | 상품과 분석 결과 저장 |
| 생성형 AI | OpenAI API | 쇼핑몰 문서 기반 상담 |
| 환경설정 | python-dotenv | API 키와 DB 접속 정보 관리 |

## 프로젝트 구조

```text
multimodal-shopping-ai_1/
├── app.py                     # FastAPI 서버와 API 주소
├── category.py                # YOLO 라벨을 상품 정보로 변환
├── config.py                  # 모델·DB·폴더 경로 설정
├── db.py                      # MySQL 연결
├── download_model.py          # YOLO 모델 다운로드 및 복사
├── index.html                 # Frontend 화면
├── schemas.py                 # API 요청·응답 데이터 형식
├── style_finder.sql           # DB와 product 테이블 생성 SQL
├── yolo11s-cls.pt             # YOLO 이미지 분류 모델
├── img/                       # 화면에서 사용하는 기본 이미지
├── uploads/                   # 사용자가 업로드한 이미지
├── rag_docs/                  # 챗봇 참고 문서
│   ├── product.txt
│   └── shop_data.txt
└── services/
    ├── product_service.py     # 상품 DB CRUD
    ├── rag_service.py         # 문서 기반 AI 챗봇
    └── yolo_service.py        # 이미지 저장과 YOLO 분석
```

## 코드 리뷰 권장 순서

```text
[프로젝트 준비]
1. download_model.py     # YOLO 모델 준비
2. style_finder.sql      # DB와 상품 테이블 생성
3. .env                  # API 키와 DB 접속 정보 설정

[공통 설정]
4. config.py             # 모델·DB·폴더 경로 설정
5. db.py                 # MySQL 연결
6. schemas.py            # API 요청·응답 형식 정의

[서버 시작점]
7. app.py                # FastAPI 서버와 API 관리

[이미지 분석]
8. index.html            # 이미지 업로드
9. /classify-and-save    # 전체 분석 순서 관리
10. yolo_service.py      # 이미지 저장과 YOLO 분류
11. category.py          # 상품 카테고리 변환
12. product_service.py   # 분석 결과 DB 저장

[상품 관리]
13. 검색·수정·삭제 API
14. product_service.py CRUD

[챗봇]
15. rag_docs
16. rag_service.py
17. /rag-chat
18. index.html 결과 출력
```

## 실행 준비

### 1. 저장소 내려받기

```bash
git clone https://github.com/dino-21/multimodal-shopping-ai_1.git
cd multimodal-shopping-ai_1
```

### 2. 가상환경 만들기

Windows PowerShell 기준입니다.

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. 라이브러리 설치

```bash
pip install fastapi uvicorn python-multipart ultralytics mysql-connector-python python-dotenv openai
```

### 4. MySQL 설정

MySQL에서 `style_finder.sql`을 실행하여 DB와 테이블을 만듭니다.

```bash
mysql -u root -p < style_finder.sql
```

MySQL Workbench에서 `style_finder.sql` 파일을 열고 직접 실행해도 됩니다.

### 5. `.env` 작성

프로젝트 최상위 폴더에 `.env` 파일을 만들고 다음 내용을 입력합니다.

```env
OPENAI_API_KEY=발급받은_OpenAI_API_KEY

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=본인의_MySQL_비밀번호
DB_NAME=style_finder
```

> `.env`에는 중요한 정보가 들어 있으므로 GitHub에 올리지 마세요.

### 6. YOLO 모델 준비

프로젝트에 `yolo11s-cls.pt`가 없다면 다음 코드를 실행해 모델을 내려받습니다.

```bash
python download_model.py
```

`config.py`의 모델 경로는 다음과 같습니다.

```python
MODEL_PATH = os.path.join(BASE_DIR, "yolo11s-cls.pt")
```

## 서버 실행

```bash
uvicorn app:app --reload
```

서버가 실행되면 다음 주소를 사용할 수 있습니다.

- 서버 확인: `http://127.0.0.1:8000/`
- 서비스 화면: `http://127.0.0.1:8000/page`
- Swagger API 문서: `http://127.0.0.1:8000/docs`

## API 목록

| Method | 주소 | 기능 |
|---|---|---|
| GET | `/` | 서버 실행 상태 확인 |
| GET | `/page` | `index.html` 화면 반환 |
| POST | `/classify-and-save` | 이미지 분석 후 DB 저장 |
| GET | `/search-products?q=검색어` | 상품 검색 |
| PUT | `/update-product` | 상품 정보 수정 |
| DELETE | `/delete-product/{product_id}` | 상품 삭제 |
| POST | `/rag-chat` | 쇼핑몰 문서 기반 AI 상담 |

## 이미지 분석 API 예시

### 요청

```text
POST /classify-and-save
Content-Type: multipart/form-data
file: 상품 이미지
```

### 응답 예시

```json
{
  "id": 1,
  "image_path": "/images/example.jpg",
  "yolo_label": "runningShoes",
  "category": "운동화",
  "main_cat": "패션잡화",
  "mid_cat": "신발",
  "sub_cat": "운동화",
  "confidence": 0.94,
  "title": "러닝화",
  "description": "러닝과 운동에 적합한 신발입니다.",
  "tags": ["운동화", "러닝"],
  "status": "READY"
}
```

> 위 JSON은 데이터 구조를 보여주기 위한 예시입니다. 실제 카테고리와 값은 `category.py`의 매핑 결과에 따라 달라집니다.

## 핵심 코드 흐름

```python
@app.post("/classify-and-save", response_model=ClassifyResult)
async def classify_and_save(file: UploadFile = File(...)):

    # 업로드한 이미지를 서버에 저장
    save_path, public_path = save_upload_file(file)

    # 저장한 이미지를 YOLO로 분석
    result_data = classify_image_file(save_path, public_path)

    # 분석 결과를 MySQL에 저장
    saved_result = save_product_to_db(result_data)

    # 저장 결과를 정해진 JSON 형식으로 반환
    return ClassifyResult(**saved_result)
```

## 현재 구현의 특징

- API 코드와 Service 코드를 분리했습니다.
- YOLO 모델을 서버 시작 시 한 번만 불러옵니다.
- SQL 파라미터 바인딩을 사용합니다.
- Pydantic으로 응답 데이터 형식을 검사합니다.
- 카테고리 매핑에 실패한 결과도 `MAPPING_FAILED` 상태로 저장합니다.
- 수정 요청에서 전달하지 않은 값은 기존 값을 유지합니다.

## 개선하면 좋은 사항

- `config.py`에서 기본 DB 비밀번호 제거
- 이미지 MIME 형식과 파일 크기 검사
- DB 연결 풀과 오류 발생 시 `rollback()` 적용
- `ChatRequest`, `ChatResponse` 중복 정의 제거
- 운영 환경에서 CORS 허용 주소 제한
- 시간이 걸리는 YOLO와 DB 작업을 별도 스레드에서 처리
- 로그와 자동 테스트 코드 추가
- RAG 문서 청크 분할, 임베딩, Vector DB 검색 추가
- JWT 로그인과 사용자별 권한 관리 추가

## 주의사항

- `yolo11s-cls.pt`는 이미지 전체를 하나의 종류로 분류하는 Classification 모델입니다.
- 사진 속 여러 객체의 위치를 박스로 찾는 Detection 모델과 동작 방식이 다릅니다.
- OpenAI 챗봇을 사용하려면 유효한 API 키가 필요하며 사용량에 따라 비용이 발생할 수 있습니다.
- 개발 단계의 `allow_origins=["*"]` 설정은 운영 배포 전에 실제 Frontend 주소로 제한하는 것이 안전합니다.

## 프로젝트 요약

Frontend에서 이미지를 받아 FastAPI가 요청을 처리하고, YOLO 분류 결과를 서비스 카테고리로 변환해 MySQL에 저장했습니다. 또한 상품 문서를 OpenAI와 연결해 상담 기능을 구현했습니다.
