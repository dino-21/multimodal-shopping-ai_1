show databases;

-- 1. 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS style_finder
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;


-- 2. 데이터베이스 선택
USE style_finder;

-- 3. 기존 테이블 삭제 (초기화)
DROP TABLE IF EXISTS product;


-- 4. 상품 테이블 생성
-- YOLO 분석 결과 + 상품 정보를 저장하는 테이블
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- 상품 고유번호
    image_path VARCHAR(255),            -- 이미지 경로 (/images/xxx.jpg)
    yolo_label VARCHAR(100),           -- YOLO가 예측한 라벨
    category VARCHAR(50),          -- 카테고리 (운동화, 치마 등)
    main_cat VARCHAR(50),       -- 대분류 (패션의류, 패션잡화)
    mid_cat VARCHAR(50),     -- 중분류 (상의, 하의, 신발 등)
    sub_cat VARCHAR(50),     -- 소분류 (러닝화, 스커트 등)
    title VARCHAR(255),     -- 상품명
    description TEXT,     -- 상품 설명
    tags VARCHAR(255),     -- 태그 (콤마로 구분)
    confidence FLOAT,     -- YOLO 예측 정확도
    status VARCHAR(50) DEFAULT 'READY'    -- 상태 (READY, MAPPING_FAILED 등)
);


-- product 테이블이 존재하면 삭제
DROP TABLE IF EXISTS product;

-- 테이블 삭제 (비추천 방식)
-- product 테이블이 없으면 에러 발생
DROP TABLE product;



-- 5. 테이블 구조 확인
DESC product;

-- 6. 데이터 확인
-- 저장된 데이터 조회
SELECT * FROM product;


-- 현재 DB의 테이블 목록 확인
SHOW TABLES;

-- 현재 DB의 테이블 목록 확인
-- 매핑 실패 상황 테스트용 데이터
INSERT INTO product
(image_path, yolo_label, category, main_cat, mid_cat, sub_cat, title, description, tags, confidence, status)
VALUES
('/images/test.jpg', 'velvet', '기타', '기타', '기타', '기타',
 '분류 확인 필요 상품',
 '카테고리 매핑 실패로 사용자 확인이 필요합니다.',
 '매핑실패,velvet',
 0.85,
 'MAPPING_FAILED');

select * from product;

-- 매핑 실패 상황 테스트용 데이터
TRUNCATE TABLE product;

-- DB 전체 삭제 (데이터 완전 제거)
DROP DATABASE IF EXISTS style_finder;


DROP DATABASE style_finder;

