# syntax=docker/dockerfile:1

# ── 1) 빌드 스테이지: React/Vite 정적 파일 생성 ──
FROM node:20-alpine AS build
WORKDIR /app

# 의존성 먼저 설치 (package 변경 없으면 레이어 캐시 재사용)
COPY package*.json ./
RUN npm ci

# 소스 복사 후 빌드
COPY . .

# 백엔드 주소는 "빌드 시점"에 번들에 박힌다(Vite 특성).
# Render는 서비스 환경변수를 Docker 빌드 인자로 전달하므로 ARG로 받는다.
# (로컬 빌드 기본값은 http://localhost:8000)
ARG VITE_API_BASE_URL="http://localhost:8000"
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# ── 2) 서빙 스테이지: nginx로 정적 파일 서빙 (경량) ──
FROM nginx:alpine AS serve

# SPA 라우팅 + $PORT 리슨용 템플릿 (nginx 이미지가 시작 시 envsubst로 치환)
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# 빌드 결과물(dist)만 가져온다 — node_modules 등은 포함하지 않아 이미지가 작다
COPY --from=build /app/dist /usr/share/nginx/html

# 로컬 기본 포트. Render는 PORT 환경변수로 덮어써 그 포트로 리슨한다.
ENV PORT=80
EXPOSE 80

# CMD는 nginx 이미지 기본값을 사용한다(템플릿 치환 후 nginx 자동 실행).
