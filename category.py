# category.py
# YOLO 라벨 → 서비스용 데이터 변환 (AI 결과 → 쇼핑몰 데이터로 변환)
# AI 결과(영어)를 우리 쇼핑몰 데이터(한글)로 바꿔주는 역할

# 카테고리 매핑 테이블
# YOLO에서 나온 label을 기준으로 상품 정보(카테고리 + 제목 + 설명 + 태그)를 정의
# YOLO → label-> normalize -> CATEGORY_MAP 조회 -> 상품 정보 생성


CATEGORY_MAP = {
    # 치마 종류
    "miniskirt": {
        "category": "치마",      # 화면에 보여줄 카테고리
        "main_cat": "패션의류",  # 대분류
        "mid_cat": "하의",       # 중분류
        "sub_cat": "스커트",     # 소분류
        "title": "A라인 미니스커트",    # 상품명
        "description": "심플한 A라인 실루엣으로 다양한 코디에 잘 어울리는 스커트입니다.",
        "tags": ["치마", "스커트", "데일리"]   # 검색용 태그
    },
    "skirt": {
        "category": "치마",
        "main_cat": "패션의류",
        "mid_cat": "하의",
        "sub_cat": "스커트",
        "title": "기본 스커트",
        "description": "다양한 스타일에 매치하기 좋은 기본 스커트입니다.",
        "tags": ["치마", "스커트", "데일리"]
    },
    "mini_skirt": {
        "category": "치마",
        "main_cat": "패션의류",
        "mid_cat": "하의",
        "sub_cat": "스커트",
        "title": "미니스커트",
        "description": "발랄하고 캐주얼한 스타일의 미니스커트입니다.",
        "tags": ["치마", "미니스커트"]
    },
    "pleated_skirt": {
        "category": "치마",
        "main_cat": "패션의류",
        "mid_cat": "하의",
        "sub_cat": "플리츠스커트",
        "title": "플리츠 스커트",
        "description": "주름 디자인으로 여성스러운 분위기의 스커트입니다.",
        "tags": ["치마", "플리츠"]
    },
   
    # 상의
    "sweatshirt": {
        "category": "맨투맨",
        "main_cat": "패션의류",
        "mid_cat": "상의",
        "sub_cat": "맨투맨",
        "title": "캐주얼 맨투맨",
        "description": "편안하게 입기 좋은 캐주얼 맨투맨입니다.",
        "tags": ["맨투맨", "상의", "캐주얼"]
    },
    "tshirt": {
        "category": "티셔츠",
        "main_cat": "패션의류",
        "mid_cat": "상의",
        "sub_cat": "티셔츠",
        "title": "기본 티셔츠",
        "description": "편하게 입기 좋은 기본 티셔츠입니다.",
        "tags": ["티셔츠", "상의", "캐주얼"]
    },
    # 하의
    "jean": {
        "category": "청바지",
        "main_cat": "패션의류",
        "mid_cat": "하의",
        "sub_cat": "청바지",
        "title": "데일리 청바지",
        "description": "다양한 상의와 매치하기 좋은 기본 청바지입니다.",
        "tags": ["청바지", "하의", "데님"]
    },
     # 원피스
    "velvet": {
        "category": "원피스",
        "main_cat": "패션의류",
        "mid_cat": "원피스",
        "sub_cat": "슬립원피스",
        "title": "슬립 원피스",
        "description": "가볍고 여성스러운 분위기로 연출하기 좋은 슬립 원피스입니다.",
        "tags": ["원피스", "슬립원피스", "데일리"]
    },
    "dress": {
        "category": "원피스",
        "main_cat": "패션의류",
        "mid_cat": "원피스",
        "sub_cat": "드레스",
        "title": "기본 원피스",
        "description": "깔끔하게 착용하기 좋은 기본 원피스입니다.",
        "tags": ["원피스", "드레스", "패션"]
    },
    # 잡화
    "wool": {
        "category": "모자",
        "main_cat": "패션잡화",
        "mid_cat": "패션소품",
        "sub_cat": "캡모자",
        "title": "캐주얼 캡모자",
        "description": "일상에서 편하게 착용하기 좋은 캐주얼 캡모자입니다.",
        "tags": ["모자", "캡모자", "캐주얼"]
    },
    "mailbag": {
        "category": "가방",
        "main_cat": "패션잡화",
        "mid_cat": "가방",
        "sub_cat": "숄더백",
        "title": "데일리 숄더백",
        "description": "일상에서 편하게 들기 좋은 데일리 숄더백입니다.",
        "tags": ["가방", "숄더백", "데일리"]
    },
     # 운동화
    "running_shoe": {
        "category": "운동화",
        "main_cat": "패션잡화",
        "mid_cat": "신발",
        "sub_cat": "러닝화",
        "title": "데일리 러닝화",
        "description": "가볍고 편하게 신기 좋은 러닝화입니다.",
        "tags": ["운동화", "러닝화", "신발"]
    },
    # 신발
    "loafer": {
        "category": "로퍼",
        "main_cat": "패션잡화",
        "mid_cat": "신발",
        "sub_cat": "로퍼",
        "title": "클래식 로퍼",
        "description": "단정하고 깔끔한 느낌으로 신기 좋은 로퍼입니다.",
        "tags": ["로퍼", "신발", "클래식"]
    },
}

# 라벨 정리 함수 : YOLO 결과값을 깨끗하게 정리 (공백 제거 + 소문자 변환)
def normalize_label(label):
    if not label:
        return "unknown"
    return str(label).strip().lower()

# 카테고리 정보 가져오기 : YOLO 결과(label)를 넣으면 해당 상품 정보 반환
def get_category_info(yolo_label):
    label = normalize_label(yolo_label)
    return CATEGORY_MAP.get(label)