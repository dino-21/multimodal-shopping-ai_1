# DB 연결을 담당하는 공통 함수
# db.py는 DB 연결만 책임진다 (DB 연결은 한 곳에서 관리)
# 1. MySQL 라이브러리
import mysql.connector   # MySQL 연결용 라이브러리


# 2. 설정 파일 가져오기
from config import DB_CONFIG # config.py에서 DB 설정을 가져옴


# 3. DB 연결 함수
# 호출하면 DB 연결 객체를 반환
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

"""
공통함수를 만드는 이유
DB 연결할때 파일마다 계속 반복됨
conn = mysql.connector.connect(...)


이렇게 함수를 만들면 코드 재사용
conn = get_db_connection()
"""