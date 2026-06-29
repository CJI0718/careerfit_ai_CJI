# CareerFit AI — 목표 프로젝트 구조

> 이 문서는 **우리가 지향하는 최종 디렉터리 구조**를 설명합니다.  
> 아직 모든 파일과 폴더가 구현된 상태는 아니며, 개발을 진행하면서 이 설계를 기준으로 맞춰 나갑니다.

전체 구조는 **레스토랑**에 비유합니다. 손님(사용자)이 홀(프론트엔드)에서 주문하면, 주방(백엔드)이 데이터와 AI를 활용해 요리(분석·추천)를 만들어 돌려주는 흐름입니다.

```
careerfit_ai/
├── .cursor/rules/          # Cursor AI 조교 규칙
├── .gitignore
├── .env.example
├── README.md
│
├── backend/                # 🍳 주방 — 서버·데이터·AI 로직
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── data/
│   ├── chroma_db/          # (자동 생성, Git 제외)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env                # (Git 제외)
│
├── frontend/               # 🪑 홀 — 사용자 화면
│   └── src/
│       ├── App.jsx
│       └── components/
│
└── docs/                   # 📖 주방 매뉴얼 — 규칙·프롬프트
    ├── AI_TA_RULES.md
    ├── PROMPTS.md
    └── PROJECT_STRUCTURE.md   # ← 이 문서
```

---

## 한눈에 보기

| 영역 | 비유 | 역할 | 핵심 파일·폴더 |
|------|------|------|----------------|
| `backend/` | 주방 | API 서버, DB, AI 분석 | `main.py`, `routers/`, `services/`, `data/`, `chroma_db/` |
| `frontend/` | 홀 | 사용자가 보는 UI | `src/App.jsx`, `src/components/` |
| `docs/` | 주방 매뉴얼 | 개발 규칙, AI 프롬프트 | `AI_TA_RULES.md`, `PROMPTS.md` |

---

## 루트(Root) — 레스토랑 건물

프로젝트 최상단은 **레스토랑 전체**를 대표합니다. 코드 본체는 `backend/`, `frontend/`, `docs/` 세 구역으로 나뉘고, 루트에는 **공통 설정·소개**만 둡니다.

### `.cursor/rules/`

Cursor IDE의 AI 조교(에이전트)가 따를 **프로젝트 전용 규칙**을 모아 둔 폴더입니다.

- 코딩 스타일, 네이밍, 금지 사항(API Key 하드코딩 등)을 명시합니다.
- 팀원이 Cursor로 작업할 때 **일관된 코드와 답변**을 유도합니다.
- 예: "서비스 로직은 `services/`에만 작성", "라우터는 HTTP 처리만 담당" 같은 규칙.

### `.gitignore`

GitHub 등 원격 저장소에 **올리면 안 되는 파일·폴더 목록**입니다.

- `.env` (API Key), `node_modules/`, `chroma_db/`, `*.db` 등이 포함됩니다.
- 실수로 비밀 정보가 공개되는 것을 막는 **안전장치**입니다.

### `.env.example`

환경 변수의 **형식만 보여 주는 공개용 템플릿**입니다.

- 실제 Key 값은 넣지 않고, `GEMINI_API_KEY=your_key_here`처럼 **자리표시자**만 적습니다.
- 새로 합류한 개발자가 `.env` 파일을 어떻게 만들어야 하는지 바로 알 수 있습니다.

### `README.md`

레스토랑 **소개서·포트폴리오** 역할입니다.

- 프로젝트가 무엇을 하는지, 어떻게 실행하는지, 기술 스택은 무엇인지 설명합니다.
- GitHub 방문자(채용 담당자, 협업자)가 **첫인상**을 얻는 문서입니다.

---

## `backend/` — 주방 (서버·데이터·AI)

손님의 주문을 받아 **실제로 처리하는 모든 로직**이 모이는 곳입니다. 프론트엔드는 주방 내부를 직접 들여다보지 않고, **정해진 창구(API)** 로만 요청합니다.

### `main.py` — 주방 입구

FastAPI(또는 유사 프레임워크) **애플리케이션의 시작점**입니다.

- 서버를 켜고, CORS·미들웨어·라우터 등록을 한곳에서 수행합니다.
- 레스토랑으로 치면 **주방 문** — 모든 요청이 여기를 거쳐 각 담당자(라우터)에게 전달됩니다.
- `uvicorn main:app`처럼 실행할 때 진입하는 파일입니다.

### `routers/` — 메뉴별 조리 담당자 (API 엔드포인트)

HTTP **요청·응답을 받고 돌려주는 창구**입니다. **비즈니스 로직은 직접 쓰지 않고**, `services/`에 위임합니다.

| 파일 | 엔드포인트 | 역할 |
|------|------------|------|
| `jobs.py` | `/jobs` | 채용 공고 목록 조회, 필터링, 검색 |
| `analyze.py` | `/analyze` | **핵심 기능** — 이력서·직무 적합도 AI 분석 |

**설계 원칙**

- 라우터: 요청 검증, 파라미터 파싱, HTTP 상태 코드, JSON 응답 형식만 담당.
- 복잡한 AI 호출·DB 조회·RAG 검색은 `services/`에서 처리.
- 메뉴(기능)가 늘어나면 `routers/`에 파일을 추가 — **관심사 분리**로 유지보수가 쉬워집니다.

### `services/` — 실제 조리 기술 (비즈니스·AI 로직)

**실제 일을 하는 주방 스태프**입니다. 라우터와 분리해 두면 테스트·재사용·교체가 수월합니다.

| 파일 | 역할 |
|------|------|
| `llm_service.py` | **Gemini 셰프** — LLM API 호출, 프롬프트 조립, 응답 파싱 |
| `rag_service.py` | **레시피 북 검색** — ChromaDB에서 관련 직무·스킬 문맥을 검색해 LLM에 전달 |

**왜 분리하는가?**

- `llm_service`: "어떻게 Gemini와 대화할 것인가" (모델, 온도, 토큰, 에러 처리).
- `rag_service`: "어떤 참고 자료를 가져올 것인가" (임베딩, 유사도 검색, 청크 조합).
- 나중에 Gemini → 다른 모델로 바꿔도 **라우터와 RAG 코드는 거의 그대로** 둘 수 있습니다.

### `data/` — 냉장고 (원재료 데이터)

앱이 사용하는 **정적·원본 데이터**를 보관합니다.

| 파일 | 설명 |
|------|------|
| `jobs.csv` | 채용 공고 원본 또는 시드 데이터 |
| `careerfit.db` | SQLite 등 관계형 DB 파일 (공고·분석 이력 등) |

- Git에는 **용량·민감도**에 따라 포함 여부를 결정합니다 (대용량·개인정보는 제외).
- `chroma_db/`와 달리, 사람이 직접 관리·교체하는 **원재료**에 가깝습니다.

### `chroma_db/` — 레시피 북 (벡터 DB, 자동 생성)

RAG용 **벡터 저장소**입니다. ChromaDB가 실행 중 자동으로 생성·갱신합니다.

- 직무 설명, 스킬, FAQ 등을 임베딩해 **의미 기반 검색**에 사용합니다.
- `.gitignore`에 포함 — **재생성 가능**하므로 저장소에 올리지 않습니다.
- `rag_service.py`가 이 "레시피 북"을 펼쳐 읽고, LLM에게 맥락을 넘깁니다.

### `requirements.txt` — 장보기 목록

Python **의존성 패키지 목록**입니다.

- FastAPI, uvicorn, chromadb, google-generativeai 등 버전을 고정합니다.
- `pip install -r requirements.txt` 한 번으로 주방 설비를 갖춥니다.

### `Dockerfile` — 도시락 통 포장 설명서

백엔드를 **컨테이너 이미지**로 빌드하는 방법을 정의합니다.

- 로컬·클라우드·CI/CD 어디서든 **동일한 환경**에서 서버를 띄울 수 있습니다.
- Python 버전, 의존성 설치, `main.py` 실행 명령을 담습니다.

### `.env` — 비밀 재료 (절대 공개 금지)

실제 **API Key·DB URL·비밀 설정**이 들어가는 파일입니다.

- `GEMINI_API_KEY`, `MOCK_MODE` 등 런타임에만 필요한 값.
- `.gitignore`로 Git 추적에서 제외 — **유출 시 즉시 키 폐기·재발급** 필요.

---

## `frontend/` — 홀 (사용자 화면)

손님이 **직접 보고 클릭하는 UI**입니다. 주방의 복잡한 로직은 모르고, API만 호출합니다.

### `src/App.jsx`

React **앱의 뼈대**입니다.

- 라우팅, 전역 레이아웃, 페이지 간 전환을 담당합니다.
- "홀 전체 배치도" — 어떤 화면이 어디에 붙는지 정의합니다.

### `src/components/`

**재사용 가능한 UI 조각** 모음입니다.

- 버튼, 입력 폼, 채용 카드, 분석 결과 패널 등.
- `App.jsx`는 이 블록들을 조립해 **완성된 화면**을 만듭니다.
- 컴ponent 단위로 나누면 디자인 수정·테스트가 쉬워집니다.

**프론트 ↔ 백엔드 관계**

- 홀(프론트)은 `/jobs`, `/analyze` 같은 **메뉴판(API)** 만 부릅니다.
- AI·DB·RAG는 전부 주방(백엔드) 안에서 처리 — **관심사 분리**와 보안(API Key가 브라우저에 노출되지 않음)에 유리합니다.

---

## `docs/` — 주방 매뉴얼 (규칙·프롬프트)

코드가 아닌 **지식·규칙·운영 문서**를 모읍니다. AI와 사람 모두가 같은 기준으로 일하게 합니다.

### `AI_TA_RULES.md`

AI 튜터·조교(TA) 또는 팀 내 AI 사용 **행동 규칙**입니다.

- 어떤 톤으로 답할지, 허용·금지 답변, 코드 리뷰 기준 등.
- Cursor `.cursor/rules/`와 함께 쓰면 **AI 보조 개발 품질**을 맞출 수 있습니다.

### `PROMPTS.md`

LLM에 넣는 **프롬프트 템플릿·버전 기록**입니다.

- 이력서 분석, 직무 매칭, 피드백 생성 등 **핵심 프롬프트** 원문.
- `llm_service.py`가 참조하거나, 프롬프트 변경 이력을 문서로 관리합니다.
- "레시피 카드" — 셰프(Gemini)에게 **매번 같은 품질**로 지시하기 위한 매뉴얼.

### `PROJECT_STRUCTURE.md`

**이 문서** — 목표 폴더 구조와 각 역할 설명.

---

## 요청이 흐르는 방식 (데이터 플로우)

사용자가 이력서 분석을 요청했을 때의 예시입니다.

```
[사용자]
    ↓ 클릭·입력
[frontend/src/components/]  →  화면에서 폼 제출
    ↓ HTTP POST /analyze
[backend/routers/analyze.py]  →  요청 검증, services 호출
    ↓
[backend/services/rag_service.py]  →  chroma_db + data에서 관련 맥락 검색
    ↓
[backend/services/llm_service.py]  →  Gemini에 프롬프트(docs/PROMPTS.md) + 맥락 전달
    ↓
[backend/routers/analyze.py]  →  JSON 응답 반환
    ↓
[frontend/]  →  분석 결과 화면 표시
```

---

## 구현 시 유의사항

1. **`routers/`와 `services/`는 반드시 분리** — 라우터에 AI·DB 로직을 섞지 않습니다.
2. **비밀 정보는 `.env`만** — `.env.example`에는 예시만, 실제 Key는 Git에 올리지 않습니다.
3. **`chroma_db/`는 생성물** — 삭제 후 재구축 가능; `.gitignore` 유지.
4. **프롬프트 변경**은 `docs/PROMPTS.md`와 `llm_service.py`를 함께 갱신합니다.
5. **새 API**는 `routers/`에 파일 추가 → 필요한 로직은 `services/`에 추가 → `main.py`에서 라우터 등록.

---

## 현재 상태 vs 목표

| 항목 | 목표 | 비고 |
|------|------|------|
| `backend/routers/` | ✅ 목표 구조 | `jobs.py`, `analyze.py` 등 |
| `backend/services/` | ✅ 목표 구조 | `llm_service.py`, `rag_service.py` |
| `backend/main.py` | 🔲 미구현 | 진입점 |
| `frontend/` | 🔲 미구현 | React UI |
| `docs/` | 🔄 진행 중 | 이 문서 포함 |

개발이 진행되면 위 표를 업데이트하며, **이 문서의 설계와 실제 코드가 어긋나지 않도록** 맞춰 나갑니다.
