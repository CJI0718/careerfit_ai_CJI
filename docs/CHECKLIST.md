# CareerFit AI 제출 체크리스트

최종 제출 전에 저장소, 코드 동작, 문서, 보안을 점검한다.
상태 기준일: 2026-07-07

## Step 3. 제출 체크리스트 최종 확인

### GitHub Repository

- [x] `careerfit_ai_CJI` Repository가 Public으로 설정되어 있는가?
  - 확인: GitHub API `private=false`.
- [ ] `README.md`가 GitHub에서 정상 렌더링되는가?
  - 최종 README 커밋/푸시 후 GitHub 화면에서 Mermaid 렌더링까지 확인한다.
- [x] `backend/`, `frontend/`, `docs/` 폴더가 모두 있는가?
- [x] `.env` 파일이 Repository에 없는가?
  - 확인: Git 추적 파일에는 `.env.example`, `backend/.env.example`, `frontend/.env.example`만 있음.
- [x] `chroma_db/`가 Repository에 없는가?
  - 확인: `backend/chroma_db/`는 `.gitignore` 및 `backend/.dockerignore`에서 제외.
- [x] `Dockerfile`이 `backend/` 폴더 안에 있는가?

### 코드 동작

- [x] `uvicorn`으로 FastAPI 실행 후 `/health` 응답 확인
  - 확인: 로컬 uvicorn 실행 후 `http://127.0.0.1:8000/health` 200 응답.
- [x] `/analyze`가 `sources` 포함 응답을 반환하는가?
  - 확인: Render 백엔드 `/analyze` 응답에 `answer`, `sources` 포함.
- [x] React UI에서 결과 카드·출처 카드가 출력되는가?
  - 코드 확인: `App.jsx`가 `ResultCard`, `SourceCard`를 조건 렌더링.
  - 최종 화면 확인은 프론트 배포 URL에서 직접 수행한다.
- [x] Docker build가 성공하는가?
  - 확인: `docker build -t careerfit-ai ./backend` 성공.
- [x] Docker run 후 `/health` 응답이 오는가?
  - 확인: 컨테이너 실행 후 `/health` 200 응답.

### 문서

- [x] README에 실행 방법이 있는가?
- [x] `docs/` 폴더에 프로젝트 문서가 4개 이상 있는가?
- [x] `harness/` 폴더에 하네스 파일이 4개 이상 있는가?
- [x] 구현하지 않은 기능이 "향후 개선"으로 분리되어 있는가?

### 보안

- [x] `.gitignore`에 `.env`가 있는가?
- [x] 코드 어디에도 실제 API Key가 직접 포함되어 있지 않은가?
  - 확인: 실제 키 파일은 Git 추적 대상이 아님. `.env.example`에는 placeholder만 둔다.
- [x] `.env.example` 파일이 있는가?

## 최종 제출 직전 명령어

```powershell
# Git 추적 파일 확인
git ls-files

# 실제 .env가 추적되지 않는지 확인
git ls-files | Select-String -Pattern '(^|/|\\)\.env($|\.)'

# 프론트엔드 빌드 확인
cd frontend
npm.cmd run build

# 백엔드 문법 확인
cd ..
python -m py_compile backend/main.py

# Docker 백엔드 빌드 확인
docker build -t careerfit-ai ./backend
```
