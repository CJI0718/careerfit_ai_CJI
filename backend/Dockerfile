# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# 로컬 venv(3.12.4)와 버전을 맞춰야 "로컬은 되는데 컨테이너는 안 됨" 문제를 막을 수 있음
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
ENV ANONYMIZED_TELEMETRY=False

# appuser 홈이 /nonexistent(쓰기 불가)라, ChromaDB 기본 임베딩(all-MiniLM) 모델을
# 받아 둘 쓰기 가능한 위치를 HOME으로 지정한다. (chroma는 ~/.cache/chroma 에 내려받음)
ENV HOME=/opt/appcache

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# 캐시 디렉토리를 미리 만들고 appuser 소유로 지정 (런타임에 임베딩 모델을 받아 저장)
RUN mkdir -p /opt/appcache && chown appuser /opt/appcache

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# chroma_db(벡터DB)는 재생성물이라 Git에 없어 이미지에도 복사되지 않는다.
# 앱이 시작 시 이 경로를 새로 만드는데, /app은 root 소유라 그대로면 생성이 실패한다.
# → 디렉토리를 미리 만들고 appuser 소유로 지정한다. (Render 등 배포 환경에서 필수)
RUN mkdir -p /app/chroma_db && chown appuser:appuser /app/chroma_db

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
# --chown: 파일 소유자를 appuser로 지정. 이래야 런타임에 appuser가
# chroma_db(벡터DB) 폴더에 쓸 수 있음. 없으면 root 소유가 되어 Permission denied.
COPY --chown=appuser:appuser . .

# RAG 데이터 산출물은 배포 환경에서 누락될 수 있으므로 빌드 시 CSV에서 재생성한다.
# 이렇게 하면 Render가 GitHub 소스만으로 빌드해도 rag_documents.json과 SQLite DB가 이미지 안에 생긴다.
RUN python data/preprocess.py

# ChromaDB 컬렉션을 빌드 시 미리 채워 첫 /analyze 요청에서 파일 누락/모델 다운로드가 터지지 않게 한다.
# 기본 임베딩 모델 다운로드와 문서 적재를 이미지에 포함한다.
RUN python -c "from services.rag_service import get_or_create_collection; c = get_or_create_collection(); print(f'ChromaDB warmup complete: {c.count()} documents')"

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
# FastAPI 앱(main.py 안의 app 객체)을 uvicorn으로 실행. 0.0.0.0 이어야 컨테이너 외부에서 접근 가능
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


