# 프론트엔드 배포 가이드 (Render · Docker)

React/Vite 프론트엔드를 백엔드와 연결하고, **로컬**과 **Render 클라우드** 양쪽에서 동작시키는 방법을 정리한다. 초보자 기준으로 따라 할 수 있게 순서대로 설명한다.

> 백엔드(FastAPI)는 이미 Docker 기반 Render Web Service로 배포돼 있다.
> 예시 백엔드 URL: `https://careerfit-ai-jawa.onrender.com` (본인 값으로 바꿔서 사용)

---

## 1. 로컬 실행 방법

백엔드와 프론트엔드는 **각각 별도 터미널**에서 실행한다.

**① 백엔드 (터미널 1)**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```
→ http://localhost:8000/docs 로 확인

**② 프론트엔드 (터미널 2)**
```powershell
cd frontend
npm install          # 최초 1회
npm run dev          # http://localhost:5173
```

브라우저에서 http://localhost:5173 접속 → 폼 제출 시 백엔드 `/analyze`가 호출된다.

---

## 2. 프론트엔드 환경변수 설정

프론트엔드가 호출할 백엔드 주소는 **`VITE_API_BASE_URL`** 하나로 관리한다.

- 설정하지 않으면 기본값 `http://localhost:8000` 사용 (로컬 개발용).
- 값을 바꾸려면 `frontend/.env` 파일을 만든다 (`frontend/.env.example` 복사):

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

코드에서는 [frontend/src/api.js](../frontend/src/api.js)가 이 값을 읽는다:
```js
export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/$/, "");
```

> ⚠️ **중요**: Vite는 `VITE_` 변수를 **빌드 시점**에 코드에 박아 넣는다(런타임 주입 아님).
> 따라서 값을 바꾸면 `npm run build`(또는 Render 재배포)를 **다시** 해야 반영된다.

---

## 3. 백엔드 CORS 환경변수 설정

브라우저는 다른 origin(도메인:포트)으로의 요청을 기본 차단한다(CORS). 백엔드가 프론트엔드 주소를 **명시적으로 허용**해야 한다.

- 백엔드는 **`FRONTEND_ORIGINS`** 환경변수(쉼표 구분)로 허용 목록을 받는다.
- 로컬 기본값(`localhost:5173`, `127.0.0.1:5173`, `localhost:3000`, `127.0.0.1:3000`)은 [backend/main.py](../backend/main.py)에 **이미 코드로 포함**돼 있어, 로컬은 별도 설정 없이 동작한다.
- 배포 시엔 Render 프론트엔드 URL을 추가한다:

```bash
# backend/.env  (또는 Render 백엔드 서비스의 Environment)
FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-service.onrender.com
```

> `allow_origins=["*"]`는 쓰지 않는다 — 자격증명 허용과 함께 못 쓰고 보안상 위험하다.

---

## 4. 프론트엔드 Dockerfile 설명

[frontend/Dockerfile](../frontend/Dockerfile)은 **멀티 스테이지 빌드**다.

| 스테이지 | 이미지 | 하는 일 |
|----------|--------|---------|
| ① build | `node:20-alpine` | `npm ci` → `npm run build`로 정적 파일(`dist/`) 생성 |
| ② serve | `nginx:alpine` | `dist/`만 복사해 nginx로 서빙 (경량) |

핵심 포인트:
- **빌드 인자 `VITE_API_BASE_URL`**: 백엔드 주소는 빌드 시점에 박히므로 `ARG`로 받는다. Render는 서비스 환경변수를 Docker 빌드 인자로 전달한다.
- **`nginx.conf.template`의 `${PORT}`**: nginx가 시작 시 `PORT` 환경변수 값으로 치환한다. Render가 지정하는 포트로 리슨하게 된다.
- **SPA 라우팅**: `try_files $uri $uri/ /index.html;`로 새로고침·직접 접속도 처리한다.

---

## 5. Render에서 프론트엔드를 Docker Web Service로 배포하기

1. Render 대시보드 → **New +** → **Web Service**
2. GitHub 저장소(`careerfit_ai_CJI`) 연결
3. 설정:
   | 항목 | 값 |
   |------|-----|
   | Name | `careerfit-frontend` (원하는 이름) |
   | Branch | `main` |
   | **Language / Runtime** | **Docker** ⭐ |
   | **Root Directory** | `frontend` |
   | Instance Type | Free (무료로 충분) |
4. **Environment** 에 환경변수 추가 (아래 6번 표)
5. **Create Web Service** → 빌드·배포 진행
6. 완료되면 `https://careerfit-frontend-xxxx.onrender.com` 형태의 URL이 나온다

> Start Command는 비워둔다 — Dockerfile이 nginx를 실행한다.

---

## 6. Render 환경변수 설정값

**프론트엔드 서비스 (careerfit-frontend)**
| Key | 값(예시) | 비고 |
|-----|----------|------|
| `VITE_API_BASE_URL` | `https://careerfit-ai-jawa.onrender.com` | 백엔드 URL. 빌드 시 번들에 박힘 |

**백엔드 서비스 (careerfit-ai)** — 프론트 URL이 정해진 뒤 추가
| Key | 값(예시) | 비고 |
|-----|----------|------|
| `FRONTEND_ORIGINS` | `https://careerfit-frontend-xxxx.onrender.com` | 프론트 URL(로컬 기본값은 코드에 포함) |
| `GEMINI_API_KEY` | (본인 키) | 절대 노출 금지 |
| `PYTHON_VERSION` | `3.12.4` | 3.14 빌드 실패 방지 |

> 순서 팁: 프론트 배포 → 나온 URL을 백엔드 `FRONTEND_ORIGINS`에 넣고 백엔드 재배포 → 프론트 `VITE_API_BASE_URL`에 백엔드 URL 넣고 프론트 재배포.

---

## 7. 배포 후 확인 방법

1. **백엔드 단독**: `https://<백엔드>/health` → `{"status":"ok"}` 나오면 정상
2. **프론트 접속**: `https://<프론트>/` → 화면이 뜨는지
3. **연동 확인**: 폼 제출 → 브라우저 **개발자도구(F12) → Network** 탭에서 `/analyze` 요청이 **백엔드 URL**로 나가고 200 응답인지 확인
4. **응답 렌더링**: 결과 카드(answer)와 출처 카드(sources)가 표시되는지

> 무료 인스턴스는 일정 시간 미사용 시 잠들어 **첫 요청이 30초~1분** 느릴 수 있다(콜드 스타트). 정상이다.

---

## 8. CORS 오류 해결 방법

브라우저 콘솔에 `... has been blocked by CORS policy` 가 뜨면:

1. **백엔드 `FRONTEND_ORIGINS`에 프론트 URL이 있는가?**
   - 정확히 일치해야 한다: `https` 여부, 끝 슬래시 없음, 포트까지 동일
   - 예: `https://careerfit-frontend-abcd.onrender.com` (끝에 `/` 붙이지 말 것)
2. 값 추가/수정 후 **백엔드를 재배포**했는가? (환경변수는 재배포해야 반영)
3. 프론트가 실제로 그 백엔드로 요청하는가? → Network 탭에서 요청 URL 확인
   - 다르면 프론트 `VITE_API_BASE_URL`이 잘못됨 → 고치고 **프론트 재빌드/재배포**
4. `localhost`로 테스트 중이면 백엔드 기본 origin에 이미 포함돼 있으니, 프론트를 `5173`/`3000`에서 띄우고 있는지 확인

---

## 9. Git에 올리면 안 되는 파일 목록

`.gitignore`로 제외된다. **실제 키가 든 파일은 절대 커밋하지 않는다.**

| 파일/폴더 | 이유 |
|-----------|------|
| `.env`, `.env.*` | API Key·비밀값 포함 (단, `*.example` 견본은 허용) |
| `node_modules/` | 용량 큼·재설치 가능 |
| `dist/` | 빌드 산출물·재생성 가능 |
| `__pycache__/`, `*.pyc` | 파이썬 캐시 |
| `.venv/`, `venv/` | 가상환경 |
| `backend/chroma_db/` | 벡터 DB 재생성물 |

> 커밋해도 되는 것: `.env.example`(값은 `your_..._here` 같은 견본만).
> **API Key는 비법 소스 보관함인 `.env`에 넣고, React 화면이나 GitHub에는 절대 노출하지 않는다.**
