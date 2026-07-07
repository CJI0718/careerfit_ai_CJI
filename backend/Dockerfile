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

# HuggingFace 모델 캐시 위치. appuser 홈이 /nonexistent(쓰기 불가)라
# 기본 캐시 경로를 못 쓰므로, 쓰기 가능한 전용 디렉토리로 지정한다.
ENV HF_HOME=/opt/hf_cache

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

# 모델 캐시 디렉토리를 미리 만들고 appuser 소유로 지정 (아래 빌드 단계·런타임에서 쓰기 위함)
RUN mkdir -p /opt/hf_cache && chown appuser /opt/hf_cache

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# 임베딩 모델(ko-sroberta)을 빌드 시점에 미리 내려받아 이미지에 포함시킨다.
# → 컨테이너 실행 때마다 400MB를 다시 받지 않아 시작이 빠르고, 네트워크 없이도 뜬다.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('jhgan/ko-sroberta-multitask')"

# 위에서 캐시를 이미 채웠으므로 런타임엔 네트워크 조회 없이 캐시만 사용한다.
ENV HF_HUB_OFFLINE=1

# Copy the source code into the container.
# --chown: 파일 소유자를 appuser로 지정. 이래야 런타임에 appuser가
# chroma_db(벡터DB) 폴더에 쓸 수 있음. 없으면 root 소유가 되어 Permission denied.
COPY --chown=appuser:appuser . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
# FastAPI 앱(main.py 안의 app 객체)을 uvicorn으로 실행. 0.0.0.0 이어야 컨테이너 외부에서 접근 가능
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


