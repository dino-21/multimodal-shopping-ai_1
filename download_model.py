# YOLO 모델을 cache에서 찾아 프로젝트로 복사하는 코드
# YOLO 모델 다운로드 + 프로젝트 폴더로 복사
# YOLO 모델을 처음 실행하면 cache에 저장됨, 
# 그 파일을 찾아서 프로젝트 폴더로 복사하는 코드

from ultralytics import YOLO # YOLO 모델 사용
import shutil                # 파일 복사
import os                    # 경로 관련 작업


# 1. 모델 이름 / 프로젝트 경로
MODEL_NAME = "yolo11s-cls.pt"   # 사용할 YOLO 모델 이름
PROJECT_PATH = r"C:\multimodal-shopping-ai_1"  # 프로젝트 폴더

print("모델 다운로드 시작...")

# 2. 모델 다운로드 (cache에 저장됨)
# 처음 실행하면 자동으로 인터넷에서 다운로드됨, 다운로드된 파일은 cache 폴더에 저장됨
model = YOLO(MODEL_NAME)

# 3. cache 폴더 위치 (YOLO가 자동 저장하는 위치)
cache_dir = os.path.expanduser("~/.cache/ultralytics")

# 4. cache에서 모델 파일 찾기
found_path = None

# 폴더 전체를 뒤져서 모델 파일 찾기
for root, dirs, files in os.walk(cache_dir):
    if MODEL_NAME in files:
        found_path = os.path.join(root, MODEL_NAME)
        break


# 5. 프로젝트 폴더로 복사
if found_path:
    dest_path = os.path.join(PROJECT_PATH, MODEL_NAME)
    shutil.copy(found_path, dest_path) # 파일 복사
    print(f"복사 완료 → {dest_path}")
else:
    print("모델 파일 못 찾음")