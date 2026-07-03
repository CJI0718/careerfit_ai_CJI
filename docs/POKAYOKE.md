# 개발 환경 실수 방지 가이드 (Poka-Yoke)

---

## 1. VSCode Python 인터프리터 설정

**언제:** 처음 프로젝트 열 때, 또는 import 오류가 뜰 때

```
Ctrl+Shift+P → "Python: Select Interpreter"
→ backend\venv\Scripts\python.exe (Python 3.12.x) 선택
```

> ❌ 틀리기 쉬운 것: 시스템 Python(3.14)이 기본 선택되어 있음 — 반드시 venv 것으로 바꿀 것

---

## 2. venv 활성화

**위치: 반드시 `backend` 폴더 안에서 실행**

```powershell
cd c:\Users\CJI\Documents\GitHub\careerfit_ai_CJI\backend
.\venv\Scripts\activate
```

활성화 성공 시 터미널 앞에 `(venv)` 표시됨:
```
(venv) PS C:\...\backend>
```

> ❌ 틀리기 쉬운 것: 루트 폴더에서 activate 시도하거나, `source venv/bin/activate` (Linux 방식) 입력

---

## 3. 패키지 설치

**venv 활성화 후, `backend` 폴더 안에서:**

```powershell
pip install -r requirements.txt
```

> ❌ 틀리기 쉬운 것:
> - venv 활성화 전에 pip 실행 → 시스템에 설치됨
> - Python 3.14로 venv 생성 → pandas 등 빌드 실패. **반드시 Python 3.12로 venv 생성**

venv 새로 만들어야 할 때:
```powershell
py -3.12 -m venv venv
```

---

## 4. 백엔드 서버 실행

**위치: 반드시 `backend` 폴더 안에서 실행**

```powershell
cd c:\Users\CJI\Documents\GitHub\careerfit_ai_CJI\backend
.\venv\Scripts\uvicorn main:app --reload --port 8000
```

또는 venv 활성화 후:
```powershell
uvicorn main:app --reload --port 8000
```

서버 정상 실행 시:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

> ❌ 틀리기 쉬운 것:
> - 루트 폴더(`careerfit_ai_CJI`)에서 실행 → `Could not import module "main"` 에러
> - `--port` 없이 실행 → 기본 8000 포트 사용 (괜찮지만 명시 권장)

---

## 5. API 동작 확인

서버 실행 후 브라우저에서:

| URL | 용도 |
|-----|------|
| http://localhost:8000 | 루트 응답 확인 |
| http://localhost:8000/docs | Swagger UI (API 테스트) |
| http://localhost:8000/redoc | ReDoc 문서 |

---

## 6. 프론트엔드 실행

**위치: 반드시 `frontend` 폴더 안에서 실행**

```powershell
cd c:\Users\CJI\Documents\GitHub\careerfit_ai_CJI\frontend
npm run dev
```

실행 후 → http://localhost:5173

---

## 7. venv 실행 안 될때 권한 우회 방법

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

위의 권한 부여 후

```powershell
venv\Scripts\Activate.ps1
```

## 체크리스트 (매번 개발 시작 전)

- [ ] VSCode 인터프리터가 `venv\Scripts\python.exe (3.12.x)` 인지 확인
- [ ] 터미널이 `backend` 폴더에 있는지 확인 (`cd backend`)
- [ ] `(venv)` 표시 확인 후 uvicorn 실행
- [ ] http://localhost:8000/docs 열어서 서버 정상 응답 확인
