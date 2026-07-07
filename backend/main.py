import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health, jobs, analyze

app = FastAPI(
    title="CareerFit AI",
    description="취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치",
    version="0.1.0",
)

# CORS 허용 origin
# - 기본(로컬 개발): localhost/127.0.0.1 의 5173(Vite)·3000
# - 배포: FRONTEND_ORIGINS 환경변수에 쉼표로 구분해 추가 (예: Render 프론트엔드 URL)
# ※ allow_origins=["*"]는 쓰지 않는다 — allow_credentials=True와 함께 못 쓰고 보안상 위험하다.
DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
_env_origins = [
    o.strip() for o in os.getenv("FRONTEND_ORIGINS", "").split(",") if o.strip()
]
# 순서 유지 + 중복 제거
ALLOWED_ORIGINS = list(dict.fromkeys(DEFAULT_ORIGINS + _env_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(jobs.router)
app.include_router(analyze.router)


@app.get("/")
def root():
    return {"message": "CareerFit AI 서버가 실행 중입니다."}
