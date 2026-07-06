# CareerFit AI Design Skill

## 목적
CareerFit AI React UI를 **취업·공모전 포트폴리오 코치**답게 디자인한다.
사용자는 **대학생**이며, 화면은 **전문성(신뢰)** 과 **친근함(부담 없음)** 을 동시에 준다.

- 기준: **Tailwind CSS v3**
- 작업 범위: `frontend/` 안에서만 (harness 절대 규칙 준수)
- 톤: 발표 화면에서 한눈에 이해되는, 과하지 않은 디자인

---

## 1. 컬러 팔레트

톤 원리: **파랑(전문성·신뢰)** 을 중심으로, **초록(친근함·긍정 결과)** 을 포인트로 쓰고, 나머지는 **회색(slate) 무채색**으로 차분하게 받친다.

| 역할 | 의미 | Tailwind 클래스 | HEX | 사용처 |
|------|------|-----------------|-----|--------|
| **primary** | 핵심 액션·신뢰 | `blue-600` | `#2563eb` | 주 버튼, 강조 링크 |
| primary (hover) | 액션 hover | `blue-700` | `#1d4ed8` | 버튼 hover |
| primary (focus) | 입력 포커스 | `blue-500` | `#3b82f6` | `focus:ring-blue-500` |
| **secondary** | 긍정·결과 강조 | `emerald-500` | `#10b981` | 결과 카드 강조선, 성공 신호 |
| **background** | 페이지 배경 | `slate-50` | `#f8fafc` | 전체 배경 |
| background (surface) | 카드 표면 | `white` | `#ffffff` | 카드/폼 배경 |
| **text** (제목) | 주요 텍스트 | `slate-800` | `#1e293b` | h1, 강조 문구 |
| text (본문) | 일반 텍스트 | `slate-600` | `#475569` | 본문 |
| text (보조) | 흐린 텍스트 | `slate-500` | `#64748b` | 설명·캡션 |
| **border** | 기본 테두리 | `slate-200` | `#e2e8f0` | 카드 경계 |
| border (입력) | 입력창 테두리 | `slate-300` | `#cbd5e1` | input 경계 |
| **error** | 오류 | `red-700` / `red-50` / `red-200` | `#b91c1c` 등 | 오류 텍스트/배경/테두리 |

**규칙**
- 강조색(blue·emerald)은 **액션과 결과에만** 쓴다. 배경·본문은 무채색(slate)으로.
- 한 화면에 강조색은 **2종 이내**(파랑+초록)로 제한한다.
- 텍스트-배경 대비는 **WCAG AA(4.5:1) 이상**. 작은 회색 글씨는 `slate-500` 대신 `slate-600` 권장.

---

## 2. 타이포그래피 규칙

- **폰트**: 시스템 폰트(`system-ui`) 사용. 별도 웹폰트 로딩 없음(로딩 속도·단순성).
- **위계는 최대 3단계**(제목 / 소제목 / 본문)로 제한한다.

| 요소 | Tailwind 클래스 | 용도 |
|------|-----------------|------|
| 서비스명(h1) | `text-2xl font-bold text-slate-800` | 페이지 최상단 제목 |
| 카드 제목(h2) | `text-lg font-semibold text-slate-700` | 각 카드 헤더 |
| 라벨 | `text-sm font-medium text-slate-600` | 입력 라벨 |
| 본문 | `text-sm text-slate-600 leading-relaxed` | 답변·설명 |
| 보조/캡션 | `text-xs text-slate-500` | 메타 정보 |

**규칙**
- 굵기는 `font-medium` / `font-semibold` / `font-bold`만 사용(그 외 남발 금지).
- 여러 줄 답변(`answer`)은 `whitespace-pre-line`으로 **줄바꿈을 살린다**.
- 긴 문단은 `leading-relaxed`로 줄간격을 확보한다.

---

## 3. 컴포넌트 구조

실제 `frontend/src/`의 4개 컴포넌트를 기준으로 한다. **`/analyze` 응답은 `answer`와 `sources`만** 있으므로, 없는 필드를 지어내 표시하지 않는다.

### App (`App.jsx`) — 두뇌 · 레이아웃
- 역할: 상태(`result`·`isLoading`·`error`) 관리, `POST /analyze` 호출, 상태별 화면 전환.
- 레이아웃: `min-h-screen bg-slate-50 py-10 px-4` → 내부 `max-w-2xl mx-auto`.
- 헤더: 서비스명(h1) + 한 줄 설명(`text-slate-500 text-sm`).
- 하위 렌더 순서: `InputForm` → (에러) → (로딩) → `ResultCard` + `SourceCard`.

### InputForm (`InputForm.jsx`) — 입력
- 흰 카드(`bg-white rounded-xl shadow-sm border border-slate-200 p-6`).
- 입력 3개: 전공 / 보유 스킬(쉼표 구분) / 관심 직무. 각 `<label>` + `<input>`.
- 입력창: `border-slate-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500`.
- 버튼: `bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white rounded-lg`.
  - 빈 칸이 있거나 로딩 중이면 `disabled`.

### ResultCard (`ResultCard.jsx`) — AI 분석 결과
- 흰 카드 + **왼쪽 강조선** `border-l-4 border-emerald-500`(결과=긍정 포인트).
- 제목: `📊 AI 분석 결과`(h2).
- 본문: `answer`를 `text-slate-600 text-sm leading-relaxed whitespace-pre-line`으로.

### SourceCard (`SourceCard.jsx`) — 참고 공고 출처
- 흰 카드. 제목: `📄 참고한 공고 출처`(h2).
- `sources` 목록을 나열(각 항목: 회사 — 직무, 필수 스킬).
- **접근성**: 반복 목록은 `<ul>`/`<li>`로 구성. 항목 `key`는 순번(index) 대신 내용 기반 값 권장.
- 빈 상태(`sources` 없음): "참고한 공고 데이터가 없습니다." 안내 박스.

---

## 4. 레이아웃 규칙

- **단일 컬럼, 세로 스택**: 모든 카드는 위→아래로 쌓는다. 좌우 분할 레이아웃은 쓰지 않는다(발표·모바일 친화).
- **컨테이너 폭**: `max-w-2xl mx-auto`로 가운데 정렬, 가독 폭 유지.
- **여백 일관성**:
  - 페이지: `py-10 px-4`
  - 카드 내부: `p-6`
  - 카드 간격: `space-y-4`
  - 요소 간격: `space-y-3` / `space-y-4`
- **카드 스타일 통일**: `bg-white rounded-xl shadow-sm border border-slate-200`.
- **반응형**: 모바일 우선. 입력·버튼은 `w-full`, 좌우 여백 `px-4` 유지. 고정 픽셀 폭 금지.
- **상태별 화면(반드시 구분)**:
  - `empty`(분석 전) / `loading`(분석 중) / `success`(결과) / `error`(실패) / `no sources`(출처 없음).

---

## 5. 금지 사항

- **보안**
  - React 코드에 API Key·토큰·비밀번호를 넣지 않는다.
  - `.env` 값을 코드·화면·문서에 노출하지 않는다.
  - 프론트가 Gemini/Mistral을 **직접 호출하지 않는다** (반드시 FastAPI 경유).
- **데이터 정직성**
  - `/analyze` 응답에 **없는 필드**(confidence·matched_skills 등)를 지어내 표시하지 않는다.
  - 실제로 없는 채용 정보처럼 꾸미지 않는다.
  - `sources`(출처)를 숨기지 않는다.
- **스키마**
  - `/analyze` 요청·응답 스키마를 임의로 바꾸지 않는다.
- **디자인 절제**
  - 강조색을 3종 이상 남발하지 않는다.
  - 과도한 애니메이션·그림자·그라데이션을 넣지 않는다.
  - 대비가 낮은 색 조합(예: `slate-400` 본문)을 쓰지 않는다.
- **작업 방식**(harness 규칙)
  - 한 번에 하나의 컴포넌트, 하나의 변경만 다룬다. 전체를 한꺼번에 갈아엎지 않는다.

---

## 발표용 체크
발표자가 화면만 보고 다음을 설명할 수 있어야 한다.
1. 사용자가 무엇을 입력하는가? (InputForm)
2. AI가 어떤 분석 결과를 주는가? (ResultCard)
3. 어떤 공고가 근거인가? (SourceCard)
4. 데이터가 없을 때 화면은 어떻게 반응하는가? (empty / error 상태)
