# product_service = DB CRUD 담당 (저장 / 검색 / 수정 / 삭제)

from db import get_db_connection   # DB 연결 함수


# 상품 저장
def save_product_to_db(result_data: dict):
    conn = get_db_connection()   # DB 연결
    cursor = conn.cursor()


    # 상품 INSERT SQL
    sql = """
        INSERT INTO product
        (
            image_path, yolo_label, category, main_cat, mid_cat, sub_cat,
            title, description, tags, confidence, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # tags 리스트 → 문자열 변환 ("a,b,c")
    tags_str = ",".join(result_data["tags"]) if result_data.get("tags") else ""


    # SQL 실행
    cursor.execute(sql, (
        result_data.get("image_path"),
        result_data.get("yolo_label"),
        result_data.get("category"),
        result_data.get("main_cat"),
        result_data.get("mid_cat"),
        result_data.get("sub_cat"),
        result_data.get("title"),
        result_data.get("description"),
        tags_str,
        result_data.get("confidence"),
        result_data.get("status")
    ))

    conn.commit()  # 저장 확정


     # 방금 저장된 id 가져오기
    result_data["id"] = cursor.lastrowid

    cursor.close()
    conn.close()

    return result_data



# 상품 검색
def search_products_from_db(q: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # 결과를 dict 형태로 받음

    like = f"%{q}%"  # 검색용 LIKE

    sql = """
        SELECT *
        FROM product
        WHERE title LIKE %s
           OR category LIKE %s
           OR tags LIKE %s
           OR description LIKE %s
           OR yolo_label LIKE %s
           OR status LIKE %s
        ORDER BY id DESC
    """

    cursor.execute(sql, (like, like, like, like, like, like))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()


    # DB 데이터 → 화면용으로 변환
    for row in rows:
        row["tags"] = row["tags"].split(",") if row.get("tags") else []  # 문자열 → 리스트
        row["confidence"] = float(row["confidence"]) if row.get("confidence") is not None else 0.0
        row["status"] = row["status"] if row.get("status") else "READY"

    return rows


# 상품 수정
def update_product_in_db(req):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 기존 데이터 조회
    cursor.execute("SELECT * FROM product WHERE id = %s", (req.id,))
    old_row = cursor.fetchone()

    if not old_row:
        cursor.close()
        conn.close()
        return None

    # 값이 없으면 기존 값 유지 (부분 수정)
    category = req.category if req.category is not None else old_row["category"]
    main_cat = req.main_cat if req.main_cat is not None else old_row["main_cat"]
    mid_cat = req.mid_cat if req.mid_cat is not None else old_row["mid_cat"]
    sub_cat = req.sub_cat if req.sub_cat is not None else old_row["sub_cat"]
    title = req.title if req.title is not None else old_row["title"]
    description = req.description if req.description is not None else old_row["description"]


    # tags 처리
    if req.tags is None:
        tags_str = old_row["tags"] if old_row["tags"] else ""
    else:
        tags_str = ",".join(req.tags)

      # status도 선택적으로 수정
    status = req.status if req.status is not None else old_row["status"]


    # UPDATE SQL
    update_sql = """
        UPDATE product
        SET category = %s,
            main_cat = %s,
            mid_cat = %s,
            sub_cat = %s,
            title = %s,
            description = %s,
            tags = %s,
            status = %s
        WHERE id = %s
    """

    cursor.execute(update_sql, (
        category,
        main_cat,
        mid_cat,
        sub_cat,
        title,
        description,
        tags_str,
        status,
        req.id
    ))
    conn.commit()


    # 수정 결과 다시 조회
    cursor.execute("SELECT * FROM product WHERE id = %s", (req.id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None


    # 데이터 변환
    row["tags"] = row["tags"].split(",") if row.get("tags") else []
    row["confidence"] = float(row["confidence"]) if row.get("confidence") is not None else 0.0
    row["status"] = row["status"] if row.get("status") else "READY"

    return row


# 상품 삭제
def delete_product_from_db(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()


    # 존재 여부 확인
    cursor.execute("SELECT id FROM product WHERE id = %s", (product_id,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return False


    # 삭제
    cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return True


"""
1. tags는 리스트 → 문자열로 변환해서 DB 저장
2. 조회할 때 다시 문자열 → 리스트 변환
3. 수정은 Optional → 기존 값 유지 방식
4. commit() 해야 DB 저장됨
"""