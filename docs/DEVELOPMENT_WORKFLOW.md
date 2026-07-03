# CareerFit AI — 개발 워크플로우 및 일일 루틴

> Git 방식, 가상환경 관리, 일일 루틴을 정리한 가이드



## 1. 프로젝트 시작 (최초 1회만)

### 1.1 저장소 클론
```powershell
git clone <repository_url>
cd careerfit_ai_CJI
```

### 1.2 Python 3.12 가상환경 생성
```powershell
py -3.12 -m venv backend\venv
```

### 1.3 의존성 설치
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

활성화 성공 시: 터미널 앞에 `(venv)` 표시됨

---

## 2. 일일 개발 루틴

### 2.1 작업 시작

**A. 프로젝트 폴더로 이동**
```powershell
cd c:\Users\CJI\Documents\GitHub\careerfit_ai_CJI
```

**B. 백엔드 폴더로 이동 후 venv 활성화**
```powershell
cd backend
.\venv\Scripts\activate
```

터미널 앞에 `(venv)`가 표시되면 성공

**C. 백엔드 서버 실행** (backend 폴더에서)
```powershell
uvicorn main:app --reload --port 8000
```

서버가 `http://127.0.0.1:8000` 에서 실행됨

### 2.2 프론트엔드 작업 (새 터미널 창에서)

```powershell
cd c:\Users\CJI\Documents\GitHub\careerfit_ai_CJI\frontend
npm run dev
```

React가 `http://localhost:5173` 에서 실행됨

### 2.3 API 테스트

| URL | 설명 |
|-----|------|
| http://localhost:8000/docs | **Swagger UI** — 브라우저에서 API 직접 테스트 |
| http://localhost:8000/health | 헬스체크 |
| http://localhost:8000/jobs | 채용공고 목록 |

---

## 3. 작업 종료 (루틴)

### 3.1 서버 중지

터미널에서 **`Ctrl + C`** 누르기

### 3.2 venv 비활성화

```powershell
deactivate
```

터미널 앞의 `(venv)` 표시가 사라짐

### 3.3 폴더 이동

```powershell
cd ..
```

이제 `careerfit_ai_CJI` 폴더로 돌아옴

### 3.4 한 줄 명령어

```powershell
deactivate; cd ..
```

---

## 4. Git 워크플로우

### 4.1 작업 시작 전: 최신 코드 동기화

```powershell
git fetch origin
git pull origin main
```

### 4.2 작업 브랜치 생성

**브랜치 이름 규칙**: `feature/<기능>` 또는 `fix/<버그>`

```powershell
git checkout -b feature/rag-chatbot
```

### 4.3 코드 수정 및 커밋

**변경 내용 확인**:
```powershell
git status
```

**파일 추가**:
```powershell
git add .
```

**커밋 메시지 규칙**:
- ✅ `feat: RAG 챗봇 서비스 추가` (새 기능)
- ✅ `fix: health 엔드포인트 응답 오류 해결` (버그 수정)
- ✅ `docs: 개발 루틴 문서 작성` (문서)
- ✅ `refactor: routers/analyze.py 구조 개선` (코드 정리)

```powershell
git commit -m "feat: RAG 챗봇 서비스 추가"
```

### 4.4 로컬에서 테스트

```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

API 정상 작동 확인 후 `Ctrl + C`로 중지

### 4.5 원격 저장소에 푸시

```powershell
git push origin feature/rag-chatbot
```

### 4.6 Pull Request 생성

GitHub에서:
1. "Compare & pull request" 클릭
2. 제목 및 설명 작성
3. 리뷰 요청 후 병합

### 4.7 메인 브랜치로 돌아오기

```powershell
git checkout main
git pull origin main
```

---

## 5. 환경변수 관리

### 5.1 `.env` 파일 생성

```powershell
cd backend
cp .env.example .env
```

### 5.2 `.env` 파일 내용 수정

```
GEMINI_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
MOCK_MODE=true
LLM_MODEL=gemini-2.5-flash-lite
```

### 5.3 주의사항

- **`.env` 파일은 절대 Git에 올리지 않기** (`.gitignore`에 이미 등록됨)
- API 키는 코드에 직접 입력하지 말고 `os.getenv()` 사용

---

## 6. 자주 쓰는 명령어 빠른 참조

| 상황 | 명령어 |
|------|--------|
| venv 활성화 | `cd backend && .\venv\Scripts\activate` |
| venv 비활성화 | `deactivate` |
| 폴더 이동 (backend → root) | `cd ..` |
| 한 줄로 venv 비활성화 + 폴더 이동 | `deactivate; cd ..` |
| 서버 시작 | `uvicorn main:app --reload --port 8000` |
| 서버 중지 | `Ctrl + C` |
| 최신 코드 가져오기 | `git pull origin main` |
| 새 브랜치 생성 | `git checkout -b feature/<이름>` |
| 커밋하기 | `git commit -m "feat: 기능 설명"` |
| 푸시하기 | `git push origin feature/<이름>` |

---

## 7. 트러블슈팅

### PowerShell 실행 정책 오류
**오류**: `cannot be loaded because running scripts is disabled`

**해결**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
메시지에서 `Y` 입력

### venv 활성화 안 됨
**확인**: `Get-ExecutionPolicy` 결과가 `Restricted`인지 확인
→ 위의 "PowerShell 실행 정책 오류" 해결 방법 참고

### 패키지 설치 오류
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 포트 이미 사용 중
```powershell
# 8000 포트 사용 프로세스 확인
netstat -ano | findstr :8000
# 프로세스 종료 (필요시)
taskkill /PID <PID> /F
```

---

## 8. 개발 원칙 (CLAUDE.md 기준)

- 코드 수정 전: 원인과 구조를 먼저 설명
- API Key: 절대 코드에 직접 입력 X → `os.getenv()` 사용
- 새 기능 추가 순서: routers/ → services/ → main.py 등록
- 불확실한 내용: 추측하지 말고 "확인 필요" 표시
- 향후 개선 사항: 코드 주석이 아닌 README 기록
