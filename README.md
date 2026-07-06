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
| 프론트엔드 | React, Vite, Tailwind CSS v3 |
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

### 5. 프론트엔드 실행 (React + Vite + Tailwind)

프론트엔드는 `frontend/` 폴더에 있으며 Node.js 기반이다. (Vite 8 기준 **Node.js 20 이상** 권장)

```powershell
cd frontend
npm install          # 최초 1회 — 의존성 설치 (React, Vite, Tailwind CSS v3 등)
npm run dev          # 개발 서버 실행 → http://localhost:5173
```

- **Tailwind CSS v3**를 사용하며, 설정은 모두 `frontend/` 안에 위치한다:
  - `tailwind.config.js` — 스캔 대상(`content`) 지정
  - `postcss.config.js` — Tailwind + autoprefixer 연결
  - `src/index.css` 최상단의 `@tailwind base/components/utilities` 지시어
- 설정 파일은 `frontend`가 ESM(`"type": "module"`)이므로 `export default` 형식을 쓴다.
- 프로덕션 빌드는 `npm run build` (결과물 `frontend/dist/`는 재생성 가능하므로 Git에 커밋하지 않는다).

> 백엔드(8000)와 프론트엔드(5173)는 **별도 터미널**에서 각각 실행한다.

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

## 3일차 구현 내용

3일차 주제는 **데이터 파이프라인 구축**이다. 오전에는 LLM 호출 로직을 서비스 계층으로 분리했고(로직·라우터 분리), 오후에는 원본 CSV를 정제·저장하는 전처리 파이프라인을 구축했다.

### 오전 — LLM 서비스 계층 분리

`/analyze` 라우터에 하드코딩돼 있던 목업 응답을 걷어내고, LLM 호출 로직을 `services/llm_service.py`로 분리했다. **라우터는 요청·응답만, 서비스는 비즈니스 로직만** 담당하도록 구조를 정리한 것이다.

| 구성 요소 | 내용 |
|-----------|------|
| 클라이언트 초기화 | `.env`의 `MOCK_MODE`·`GEMINI_API_KEY`를 읽어, 실 호출 모드일 때만 Gemini(`gemini-2.5-flash-lite`) 클라이언트를 생성 |
| `build_prompt` | 사용자 질문 + 참고 데이터(RAG 문서)를 결합해 프롬프트 생성 (참고 데이터는 오후 전처리 이후 채워짐) |
| `get_llm_response` | LLM 응답을 `{"answer", "sources"}` 형태로 반환 |
| 폴백 처리 | `MOCK_MODE`이거나 API 오류(429·한도 초과 등) 발생 시 목업 응답으로 자동 폴백 |

- `/analyze` 라우터를 실제 `get_llm_response` 호출로 연결 (하드코딩 목업 제거)
- 라우터·진입점 코드 포맷 정리 (`health.py`, `jobs.py`, `main.py`)
- 개발 워크플로우 문서 보강 (`docs/DEVELOPMENT_WORKFLOW.md`) — Git 개념·브랜치 설명 및 문제 상황별 대처 추가

### 오후 — 데이터 전처리 파이프라인 (`backend/data/preprocess.py`)

원본 CSV를 정제해 SQLite와 RAG용 JSON으로 저장하는 전처리 파이프라인을 구축했다. `python data/preprocess.py`로 아래 단계가 순차 실행된다.

| 단계 | 함수 | 내용 |
|------|------|------|
| 1. 로드 | `load_data` | CSV 읽기 (UTF-8 실패 시 CP949 재시도) |
| 2. 결측치 확인 | `check_missing` | 컬럼별 결측치 수·비율 출력 |
| 3. 결측치 처리 | `handle_missing` | 핵심 컬럼(title·required_skills) 결측 행 제거, 나머지 텍스트 컬럼 빈 문자열 처리 |
| 4. 중복 제거 | `remove_duplicates` | company+title 조합 기준 중복 제거 |
| 5. 스킬 표준화 | `standardize_skills` | 사전 기반 표기 통일 (python→Python, ml→머신러닝 등) |
| 6. SQLite 저장 | `save_to_sqlite` | `jobs` 테이블로 저장 후 행 수 검증 |
| 7. RAG 문서 변환 | `convert_to_rag_documents` | 행별 자연어 문서 + metadata(id·company·title·job_type·deadline·source) 생성 |
| 8. JSON 저장 | `save_rag_documents` | `rag_documents.json`으로 중간 저장 (ChromaDB 적재 전 단계) |

원본 채용공고 18건 → 결측·중복 정제 후 15건.

**데이터셋**
- `data/jobs.csv`: 채용공고 데이터 (18건, 데이터 분석·엔지니어링·AI 등)
- `data/competitions.csv`: 공모전 데이터 (12건)

**로컬 LLM 연동** (`backend/services/ollama_service.py`)
Ollama 로컬 추론 서버 연동 함수 추가 — Gemini 외 대체 추론 경로. 연결 실패·타임아웃 시 사용자 안내 메시지를 반환한다.

> 생성물(`careerfit.db`, `rag_documents.json`)은 `preprocess.py`로 재생성 가능하므로 Git에 커밋하지 않는다.

---

## 4일차 구현 내용

4일차 주제는 **RAG 파이프라인 완성**이다. 먼저 필터링을 위해 metadata를 확장하고(전반부), 이어서 ChromaDB 저장·검색과 `/analyze` 연결로 **출처 기반 RAG 답변**을 완성했다(후반부).

### (전반부) RAG 필터링을 위한 metadata 확장

ChromaDB에 적재하기 전, "마감월·기업유형으로 공고를 걸러내고, 최초 저장일을 추적"할 수 있도록 metadata 스키마를 넓혔다. (ChromaDB metadata 값은 모두 문자열이어야 하므로 전 필드를 `str`로 저장한다.)

### 확장 필드 3개 (`convert_to_rag_documents`)

기존 6개(`id·company·title·job_type·deadline·source`)를 유지한 채 3개를 추가했다.

| 필드 | 목적(필터 요구사항) | 생성 방식 |
|------|--------------------|-----------|
| `company_type` | "스타트업/회계법인 공고만 보여줘" 같은 **기업유형 필터** | `jobs.csv`에 컬럼으로 추가 (규모+업권 혼합: 스타트업·대기업·회계법인·증권사·은행·공기업 등) |
| `deadline_month` | "9월 마감 공고만 보여줘" 같은 **마감월 필터** | `deadline`에서 `YYYY-MM` 추출 (`to_deadline_month` 헬퍼가 형식 오류·빈값 방어) |
| `created_at` | 각 공고의 **최초 저장일 추적** | 기존 JSON에서 이월 (아래 참조) |

### `created_at` 이월(carry-over) 메커니즘

`preprocess.py`는 실행할 때마다 `rag_documents.json`을 새로 굽기 때문에, 단순히 오늘 날짜를 넣으면 "최초 저장일"이 매번 갱신되는 문제가 있다. 이를 막기 위해 **기존 JSON을 '장부'처럼 먼저 읽어(`load_existing_created_at`) 최초 저장일을 물려받도록** 했다.

- 식별 키는 `company + title` 조합 (중복 제거 기준과 동일)
- 기존 공고 → 과거 `created_at` 이월 / 신규 공고 → 오늘 날짜 부여
- 변환 시 `이월 N개 / 신규 M개`를 출력해 눈으로 검증 가능

> 회계 비유: `created_at`은 **취득원가**와 같아, 매 결산(preprocess)마다 재평가하지 않고 최초 인식 시점의 값을 계속 이월한다.

### 데이터 보강·정제

- **회계법인 공고 3건 추가** (감사·택스·FAS) — 미지정 회계사의 핵심 수습 트랙인 빅펌/로컬펌 필터를 시험하기 위함
- **결측 마감일 정리** — `handle_missing`의 빈 문자열 처리 대상에 `deadline` 추가 (기존엔 마감일 없는 공고가 `"nan"` 문자열로 metadata를 오염시켰음)

원본 채용공고 21건 → 정제 후 18건.

### (후반부) ChromaDB 저장·검색 + 한국어 임베딩

확장된 `rag_documents.json`을 ChromaDB에 적재하고 의미 기반 검색을 구현했다. (`data/test_search.py`로 저장·검색을 검증하고, 앱이 실제 사용하는 로직은 `services/rag_service.py`에 둔다.)

- 초기엔 ChromaDB 기본 임베딩 모델(`all-MiniLM-L6-v2`)이 자동 적용됐으나, **영어 전용 모델이라 한국어 검색이 무작위에 가까웠다** ("회계 및 재무" 질문에 프론트엔드 공고가 1위).
- **한국어 특화 임베딩 `jhgan/ko-sroberta-multitask`로 교체**하자 순위가 정상화됐다 ("회계"→회계법인, "인공지능"→머신러닝 엔지니어).
- 저장(`add`)과 검색(`query`)은 **반드시 같은 임베딩 함수**를 써야 의미공간(차원 768)이 일치한다. 다르면 `InvalidDimensionException` 발생.

### metadata 사전 필터 (`search_documents`)

벡터 유사도만으로는 "정확히 이 조건만"을 보장하지 못하므로, ChromaDB `where` 필터를 얹어 **2단계 검색**(① 조건 정확 일치 → ② 유사도 순위)을 구현했다.

| 인자 | 거르는 metadata | 예시 |
|------|-----------------|------|
| `job_type` | 직무 분류 | `"데이터 분석"` |
| `deadline_month` | 마감 연-월 | `"2026-09"` |
| `company_type` | 기업 유형 | `"회계법인"` |

- 조건 개수에 따라 `None`/단일/`$and`로 자동 조립.
- ※ 필터는 **자연어 질문에서 자동 추출되지 않는다.** 호출 시 명시적 인자로 넘겨야 한다 (자연어→필터값 변환은 향후 LLM 단계).

### `/analyze` RAG 연결 완성

검색(retrieval)과 생성(generation)을 이어 **진짜 RAG**를 완성했다.

- `routers/analyze.py`: 질문으로 `search_documents()` 검색 → 결과를 `context_docs`로 `get_llm_response()`에 전달 (기존 `context_docs=[]` 하드코딩 제거).
- `services/llm_service.py`: `build_rag_prompt`가 검색된 공고를 `[참고 데이터]`로 프롬프트에 주입하고 **어떤 공고를 근거로 삼았는지 명시**하도록 지시. 응답 `sources`에 실제 공고(회사·직무·거리)를 담아 반환.

> 결과: 세무학과+KICPA 질문에 `sources`로 **회계법인 공고 3건**이 실제로 담기고, 답변이 그 공고를 인용하는 출처 기반 응답으로 동작함을 확인.

**의존성 추가**: 한국어 임베딩용 `sentence-transformers` (`requirements.txt`).

### LLM provider 전환 지원 (Gemini ↔ Mistral)

답변 생성 모델을 코드 수정 없이 `.env`의 `LLM_MODEL` 값만으로 바꿀 수 있게 했다. (초기엔 `gemini-2.5-flash-lite`가 하드코딩돼 `.env`를 바꿔도 반영되지 않았음.)

- `get_provider_and_model()`: `LLM_MODEL` 값의 접두어를 보고 provider를 판별한다. 예) `mistral-small-latest`→mistral, `ollama:...`→ollama, `huggingface:...`→huggingface, 그 외→gemini.
- `get_llm_response()`: 판별된 provider에 따라 `_call_gemini()`(SDK) / `_call_mistral()`(REST, `requests`)로 분기 호출한다.
- **검색(retrieval)은 provider와 무관**하다. 벡터 검색은 항상 ko-sroberta로 동작하고, 바뀌는 것은 답변 생성(generation) 부분뿐이다.
- 현재 **Gemini·Mistral만 실호출** 구현. `ollama`/`huggingface`는 자리만 확보(미구현 안내 반환).

> 주의: `PROVIDER`는 서버 시작 시점에 한 번 계산되므로, `.env`의 `LLM_MODEL`을 바꾸면 **서버를 재시작**해야 적용된다. (`--reload`는 `.py` 변경만 감지하고 `.env`는 감지하지 못함.)

### (프론트엔드) React UI 초기 구성

완성된 `/analyze` RAG API를 실제 화면에서 쓰기 위한 프론트엔드 초기 구성을 진행했다. `frontend/`(Vite + React) 기반이다.

**환경 설정**
- **Tailwind CSS v3** 설정을 `frontend/`로 통일(설치·`tailwind.config.js`·`postcss.config.js`·`index.css`의 `@tailwind` 지시어). 루트에 잘못 생성됐던 설정 잔재는 제거했다.
- `frontend`는 ESM(`"type": "module"`)이므로 설정 파일은 `export default` 형식을 쓴다.

**컴포넌트 구조** (`frontend/src/`)

| 파일 | 역할 |
|------|------|
| `main.jsx` | 진입점 — `index.html`의 `#root`에 `App`을 렌더 |
| `App.jsx` | 두뇌 — 상태(`result`·`isLoading`·`error`) 관리, `fetch`로 `POST /analyze` 호출, 상태에 따라 하위 컴포넌트 렌더 |
| `components/InputForm.jsx` | 입력 폼(전공·스킬·직무), 제출 시 `App`의 핸들러 호출 |
| `components/ResultCard.jsx` | AI 분석 답변(`answer`) 표시 |
| `components/SourceCard.jsx` | 참고한 공고 출처(`sources`) 표시 |

- 흐름: `InputForm` 입력 → `App.handleAnalyze`가 백엔드 `/analyze` 호출 → 응답 `{answer, sources}`를 `ResultCard`·`SourceCard`로 표시.
- **보안**: API Key는 프론트에 두지 않고 **백엔드(`.env`)를 경유**해서만 LLM을 호출한다(프론트 코드는 브라우저에 그대로 노출되므로).

**문서**
- `docs/FRONTEND_GUIDE.md` — **Python 개발자를 위한** 프론트엔드 코드 해설(React/JSX 개념을 Python에 비유) + `SourceCard.jsx` 코드 리뷰(보안·응답구조·접근성)를 정리했다.

### (프론트엔드) UI/UX 리디자인 — 발표용 세련화

발표 가독성과 완성도를 높이기 위해 전체 UI를 리디자인했다. 아래 `design-skill.md`를 기준으로 삼았다.

- **레이아웃 근본 정리**: `index.css`에 남아 있던 Vite 템플릿 잔재(`#root` 고정폭 1126px·테두리·중앙정렬 등)를 제거해, Tailwind 레이아웃이 제대로 적용되도록 했다. (이게 "변경이 화면에 안 보이던" 원인이기도 했다.)
- **디자인 요소**: 부드러운 배경 그라데이션(slate→white→blue), 헤더의 그라데이션 아이콘 배지, 파랑→인디고 그라데이션 주 버튼, 결과·출처 카드의 컬러 헤더바(emerald/blue 아이콘 배지 + 구분선), 로딩 **스피너**, 결과 등장 **fade-in** 모션, 출처 카드 "N건" 카운트.
- **접근성**: 장식 이모지 `aria-hidden`, 출처 목록을 `<ul>/<li>`로 전환, 낮은 대비(`slate-500→600`) 개선.
- **원칙**: 그라데이션·모션·그림자는 **포인트(배지·버튼·진입 효과)에만 절제**해서 사용(화면 전체 남용 금지).

### AI 도구 공통 harness 체계

여러 AI 도구(Claude·Cursor·Gemini·Continue·Google AI Studio)가 규칙을 각자 복붙하며 어긋나는 문제를 막기 위해, 규칙을 `harness/` 한 곳으로 모으고 각 도구 설정은 harness를 가리키는 **얇은 게이트**로 통일했다.

| 파일/폴더 | 역할 |
|-----------|------|
| `harness/MAIN_HARNESS.md` | 공통 운영 매뉴얼(절대 규칙·작업 흐름·API 계약·토큰 절약) |
| `harness/ROUTING.md` | 요청 유형 → 참조할 agent/skill/check 파일 라우팅 |
| `harness/agents/` | 역할별 5종: `ai-tutor`·`ui-designer`·`react-reviewer`·`api-connector`·`token-optimizer` |
| `harness/checks/security-check.md` | 보안 체크리스트(API Key·`.env` 노출 방지) |
| `harness/skills/design-skill.md` | 디자인 시스템(팔레트·타이포그래피·컴포넌트·레이아웃·금지) |
| 진입 게이트 | `CLAUDE.md`·`.cursor/rules`·`AGENTS.md`·`GEMINI.md`·`Google_AI_STUDIO.md`·`.continue/rules` |

- 효과: 규칙을 harness **한 곳만 고치면 모든 도구에 반영**된다(중복·불일치 제거).
- `design-skill.md`는 이번 UI 리디자인의 실제 기준이 되었고, 팔레트(파랑·인디고·초록·slate)와 금지 조항을 코드와 일치시켰다.

---

## 진행 현황

- [x] **1일차**: 프로젝트 기획 및 개발 환경 세팅
- [x] **2일차**: FastAPI 서버 구축 및 Gemini API 연결
  - `/health`, `/jobs`, `/analyze` 엔드포인트 구현
  - Python 3.12 가상환경(venv) 세팅 및 의존성 설치
  - Gemini 2.5 Flash-Lite API 연결 준비 및 `MOCK_MODE` 환경변수 설정
  - 미지정 회계사 대상 목업 채용공고 3건 추가 (빅펌·사기업·공기업 트랙)
- [x] **3일차**: 데이터 파이프라인 구축
  - **오전**: LLM 서비스 계층 분리(`services/llm_service.py`), `/analyze` 실 호출 연결, 라우터·진입점 포맷 정리, 워크플로 문서 보강
  - **오후**: 데이터 전처리 파이프라인 구축(`data/preprocess.py`), 데이터셋 추가(`jobs.csv`·`competitions.csv`), Ollama 로컬 LLM 연동(`services/ollama_service.py`)
  - *(남은 작업: ChromaDB 벡터 인덱싱, RAG 검색 연결)*
- [x] **4일차**: RAG 파이프라인 완성
  - **전반부**: RAG 필터링용 metadata 확장(`company_type`·`deadline_month`·`created_at`), `created_at` 이월 로직, 회계법인 공고 3건 추가(감사·택스·FAS), 결측 마감일 정리 — 원본 21건 → 정제 후 18건
  - **후반부**: ChromaDB 저장·검색 구현, 한국어 임베딩(`ko-sroberta`) 적용, metadata 사전 필터(`job_type`·`deadline_month`·`company_type`), `/analyze`에 RAG 연결 → 출처 기반 답변 완성
  - **LLM provider 전환**: `.env`의 `LLM_MODEL`만으로 Gemini ↔ Mistral 전환 지원 (`_call_gemini`/`_call_mistral` 분기)
  - **프론트엔드 초기 구성**: Tailwind v3 설정을 `frontend/`로 통일, React 컴포넌트 구조(`App`·`InputForm`·`ResultCard`·`SourceCard`) 및 `/analyze` 연동, `docs/FRONTEND_GUIDE.md` 작성(Python 개발자용 해설 + 코드 리뷰)
  - **UI/UX 리디자인**: Vite 템플릿 잔재 제거 후 발표용 세련화(그라데이션·아이콘 배지·스피너·fade-in·접근성 개선), `design-skill.md` 기준 적용
  - **AI 도구 공통 harness 도입**: `harness/`(운영 매뉴얼·라우팅·agents·checks·skills)로 규칙 중앙화, 각 도구 설정을 얇은 게이트로 통일
- [ ] **5일차**: UI 다듬기 + Docker + 포트폴리오 완성
  - *(남은 작업: UI 스타일 보강·접근성 개선, Docker 컨테이너화)*
