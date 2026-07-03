# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치



## 프로젝트 개요

**누구를 위한 것인가**
'미지정 회계사' 문제는 2023년부터 나타나 2025년에 심각해졌고, 2026년 합격자에게도 닥칠 것이 분명하다. CareerFit AI는 이 상황에서 살아남아야 하는 공인회계사 시험 합격자 — 사실상 '나'와 내 주변 — 를 위한 도구다.

**무엇이 불편한가**
미지정 회계사가 수습처로 갈 수 있는 곳은 빅펌·로컬펌·사기업·공기업/정부조직으로 다양하지만, 각각에 대한 정보가 부족하다.
- **빅펌**: 어떤 부서의 어떤 직무인지조차 파악이 어렵고, 자기소개서·면접을 무엇에 초점을 둬야 할지 모른다.
- **로컬펌**: 규모·주력 사업·평판, 원펌인지 독립채산제인지 등 구조를 알기 어렵다.
- **사기업**: 어떤 기업의 어떤 직무인지, 그곳의 수습이 향후 커리어(인더스트리 경험)에 어떤 의미인지 모른다.
- **공기업·정부조직**: 마찬가지로 정보가 거의 없다.
- 무엇보다 정보가 다 흩어져 있고, **실무수습 인정 기관과 인정 방법 자체를 잘 모른다.**

**기존 방식의 한계**
- 잡사이트·KICPA 구인 게시판: 공고만 나열할 뿐, "이 기관이 수습으로 인정되는지", "내 상황에 어떤 의미인지"는 설명하지 않는다.
- 일반 챗봇(ChatGPT 등): 그럴듯하게 답하지만 출처·근거 없이 지어내(환각) 신뢰하기 어렵다.

**CareerFit이 주는 것**
처음부터 매칭하지 않는다. 미지정 회계사는 자신의 역량·위치·산업에 대한 정보부터 부족하기 때문이다. 먼저 챗봇 Q&A로 배경지식(기관 유형·직무·실무수습 인정 기준)을 **출처와 함께** 상세히 알려 주고 방향을 제시한 뒤, 점차 역량 매칭으로 이어지는 **단계적 코치**를 지향한다.

**CareerFit이 문제를 해결하는 방식 (3단계 코치)**

CareerFit AI는 정보가 부족한 미지정 회계사를 위해 "곧바로 매칭"이 아니라 **배경지식 → 방향 → 매칭**의 3단계로 돕는다.

1. **배경지식 Q&A (RAG 챗봇)**
   - "빅펌 FAS는 무슨 일을 하나?", "이 로컬펌은 규모와 운용 방식이 어떠한가?", "자산운용사 수습이 커리어에 어떤 의미인가?" 같은 질문에, 흩어진 정보를 모아 **출처와 함께** 답한다.
   - 답변 근거로 「공인회계사 실무수습기관 지정고시」 조문·기관 유형 설명을 제시해, 일반 챗봇과 달리 **환각 없이** 신뢰할 수 있게 한다.

2. **방향 제시**
   - 사용자의 상황(전공·보유 역량·관심)을 바탕으로 "어떤 트랙(빅펌/로컬펌/사기업/공기업)이 본인에게 맞는지", "무엇을 준비해야 하는지"를 안내한다.

3. **역량 매칭**
   - 배경지식이 쌓인 뒤 보유 역량과 공고를 매칭한다. 이때 ① 고시 기준으로 **수습 인정되는 자리**만 거르고 ② 역량 적합도로 정렬하며 ③ "왜 이 자리가 수습으로 인정되고, 왜 당신에게 맞는지"를 **출처와 함께** 제시한다.

→ 핵심 차별점: 게시판(나열만)·일반 챗봇(근거 없는 환각)과 달리, CareerFit은 **출처 기반 맞춤 가이드**를 단계적으로 제공한다.



## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.12, FastAPI |
| AI API | Gemini 2.5 Flash-Lite |
| 데이터 | Pandas, SQLite, ChromaDB |
| 프론트엔드 | React, Vite |
| 실행 환경 | Docker |



## 로컬 실행 방법

### 1. 가상환경 세팅

**Python 3.12** 기반 venv를 사용한다. Python 3.14는 일부 패키지 빌드 실패로 사용 불가.

```powershell
# venv 생성 (최초 1회)
py -3.12 -m venv backend\venv

# venv 활성화 (매 세션마다)
cd backend
.\venv\Scripts\activate
```

활성화 성공 시 터미널 앞에 `(venv)` 표시됨.

### 2. 의존성 설치

```powershell
pip install -r requirements.txt
```

설치되는 주요 패키지:

| 패키지 | 버전 | 용도 |
|--------|------|------|
| fastapi | 0.115.5 | API 서버 프레임워크 |
| uvicorn | 0.32.1 | ASGI 서버 (FastAPI 실행기) |
| pydantic | 2.10.3 | 요청·응답 데이터 검증 |
| google-generativeai | 0.8.3 | Gemini API 클라이언트 |
| pandas | 2.2.3 | CSV 데이터 처리 |
| chromadb | 0.5.23 | 벡터 DB (RAG용) |
| python-dotenv | 1.0.1 | `.env` 환경변수 로드 |

### 3. 백엔드 서버 실행

**반드시 `backend` 폴더 안에서 실행한다.**

```powershell
cd backend
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```
서버 정상 실행 시:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 4. API 확인

| URL | 설명 |
|-----|------|
| http://localhost:8000 | 서버 상태 확인 |
| http://localhost:8000/docs | Swagger UI — 브라우저에서 API 직접 테스트 가능 |
| http://localhost:8000/redoc | ReDoc 문서 |
| http://localhost:8000/health | 헬스체크 엔드포인트 |
| http://localhost:8000/jobs | 채용공고 목록 |
| http://localhost:8000/analyze | 역량 분석 (POST) |

> `/docs` 페이지에서 각 엔드포인트의 **Try it out** 버튼으로 요청을 직접 보내고 응답을 확인할 수 있다.

---

## 2일차 구현 내용

### 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 서버 상태 확인 |
| GET | `/jobs` | 목업 채용공고 목록 반환 |
| GET | `/jobs/{id}` | 특정 공고 상세 조회 |
| POST | `/analyze` | 전공·스킬·관심직무 기반 분석 결과 반환 |

### 목업 채용공고 (3건)

실제 CSV 데이터 연결 전까지 사용하는 임시 데이터. 미지정 회계사의 3가지 수습 트랙을 반영했다.

| # | 회사 | 직무 | 트랙 |
|---|------|------|------|
| 1 | 삼일회계법인 | FAS 기업가치평가 어소시에이트 | 빅펌 |
| 2 | LG에너지솔루션 | 재무회계 담당 (배터리 사업부) | 사기업 |
| 3 | IBK기업은행 | 재무기획 및 내부회계관리 담당 | 공기업·금융 |

### 환경변수

`.env.example` 참고. 실제 `.env` 파일은 Git에 올리지 않는다.

```
GEMINI_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here 
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
MOCK_MODE=true   # true이면 Gemini 호출 없이 목업 응답 반환
LLM_MODEL=gemini-2.5-flash-lite 
```

---

## 진행 현황

- [x] **1일차**: 프로젝트 기획 및 개발 환경 세팅
- [x] **2일차**: FastAPI 서버 구축 및 Gemini API 연결
  - `/health`, `/jobs`, `/analyze` 엔드포인트 구현
  - Python 3.12 가상환경(venv) 세팅 및 의존성 설치
  - Gemini 2.5 Flash-Lite API 연결 준비 및 `MOCK_MODE` 환경변수 설정
  - 미지정 회계사 대상 목업 채용공고 3건 추가 (빅펌·사기업·공기업 트랙)
- [ ] **3일차**: 데이터 파이프라인 구축 *(진행 중 🔄)*
  - LLM 서비스 계층 분리 (`services/llm_service.py`) — Gemini 클라이언트 초기화, `MOCK_MODE` 분기, 프롬프트 생성(`build_prompt`), 응답 처리(`get_llm_response`), API 오류(429 등) 시 목업 폴백
  - `/analyze` 라우터를 실제 LLM 서비스 호출로 연결 (하드코딩 목업 제거)
  - 라우터·진입점 코드 포맷 정리 (`health.py`, `jobs.py`, `main.py`)
  - 개발 워크플로우 문서 보강 (`docs/DEVELOPMENT_WORKFLOW.md`) — Git 개념·브랜치 설명 및 문제 상황별 대처 추가
  - *(남은 작업: CSV 채용 데이터 적재, ChromaDB 벡터 인덱싱, RAG 검색 연결)*
- [ ] **4일차**: RAG 기반 서비스 + React UI
- [ ] **5일차**: Docker + 포트폴리오 완성
