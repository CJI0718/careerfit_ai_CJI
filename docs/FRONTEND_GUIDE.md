# 프론트엔드 코드 가이드 (Python 개발자를 위한 React/JSX 설명)

> 이 문서는 **Python은 알지만 JavaScript/JSX는 처음인 사람**을 위해,
> CareerFit AI 프론트엔드(`frontend/src/`)의 **각 파일과 코드가 무슨 역할을 하고 어떤 원리로 도는지**를
> Python에 빗대어 아주 상세히 설명합니다. 마지막에 `SourceCard.jsx` **코드 리뷰**(심각도별)도 정리했습니다.

---

## 0. 큰 그림 — 이 화면은 어떻게 도는가

사용자가 브라우저에서 정보를 입력 → "분석 요청" 버튼 → **우리 FastAPI 백엔드(`localhost:8000/analyze`)** 에 요청 → RAG 답변을 받아 화면에 표시하는 구조입니다.

```
[브라우저 화면]
   InputForm (입력창)  --사용자 입력-->  App (두뇌: 상태관리 + API호출)
                                          |
                                          |  fetch로 POST /analyze
                                          v
                                   [FastAPI 백엔드]  --RAG--> Gemini/Mistral
                                          |
                                          |  {answer, sources} 응답
                                          v
   App --answer--> ResultCard (분석결과 카드)
   App --sources--> SourceCard (출처 공고 카드)
```

파일 관계를 한눈에:

```
index.html          ← 브라우저가 처음 여는 껍데기 (빈 <div id="root">)
  └ main.jsx        ← 그 div에 React 앱을 "심는" 진입점
      └ App.jsx     ← 전체를 조율하는 두뇌 (상태 + 백엔드 호출)
          ├ InputForm.jsx   ← 입력 폼 (전공/스킬/직무)
          ├ ResultCard.jsx  ← AI 분석 결과 표시
          └ SourceCard.jsx  ← 참고한 공고 출처 표시
```

Python 웹앱에 빗대면: `index.html`은 진입 HTML, `main.jsx`는 `if __name__ == "__main__"`, `App.jsx`는 메인 컨트롤러, 나머지 `*Card`는 재사용 함수들입니다.

---

## 1. 먼저 알아야 할 React/JSX 핵심 개념 (Python 비유)

JSX 문법이 낯설어도, 아래 10개만 알면 이 프로젝트 코드는 거의 다 읽힙니다.

### ① 컴포넌트 = "HTML을 반환하는 함수"

```jsx
function ResultCard({ answer }) {
  return ( <div>...</div> );   // ← HTML 비슷한 걸 반환
}
```

- **컴포넌트(Component)** 는 화면의 한 조각을 만드는 **함수**입니다.
- Python 함수와 똑같은데, **반환값이 "화면(UI)"** 이라는 점만 다릅니다.
- **함수 이름 첫 글자를 대문자로** 씁니다(`ResultCard`). React가 "이건 컴포넌트다"라고 알아보는 관례예요.

### ② JSX = JS 안에 HTML을 섞어 쓰는 문법

`return ( <div>...</div> )` 처럼 코드 안에 HTML 태그가 들어갑니다.
이게 **JSX**입니다. 실제로는 브라우저가 이해하는 객체로 변환되지만, 우리가 쓸 땐 그냥 "HTML을 반환한다"고 생각하면 됩니다.
Python에는 없는 개념이지만, **"HTML 템플릿 문자열을 반환하는 함수"** 라고 이해하면 가깝습니다.

### ③ `{ 중괄호 }` = "여기는 JS 값이다" (f-string의 `{}`와 같음)

```jsx
<p>{source.company} — {source.title}</p>
```

JSX 안에서 `{ }`는 **"이 안은 자바스크립트 값을 넣는 자리"** 라는 뜻입니다.
→ Python **f-string**의 `f"{변수}"`와 **똑같은 역할**입니다.

### ④ props = "컴포넌트에 넘기는 인자" (키워드 인자)

```jsx
<SourceCard sources={result.sources} />        // 넘기는 쪽
function SourceCard({ sources }) { ... }        // 받는 쪽
```

- 부모가 자식 컴포넌트에 데이터를 내려줄 때 쓰는 게 **props**입니다.
- Python의 **키워드 인자**와 같습니다: `SourceCard(sources=result.sources)`.
- 받는 쪽 `{ sources }`는 **구조 분해(destructuring)** 로, Python의 dict 언패킹과 비슷합니다.
  (원래는 `function SourceCard(props)` 로 받고 `props.sources`로 꺼내지만, `{ sources }`로 바로 꺼낸 것.)

### ⑤ state(상태)와 `useState` = "바꾸면 화면이 자동 갱신되는 변수"

```jsx
const [result, setResult] = useState(null);
```

- `result`: **현재 값** (초깃값 `null`)
- `setResult`: **값을 바꾸는 전용 함수**
- 핵심 원리: **`setResult(새값)`을 호출하면 React가 화면을 자동으로 다시 그립니다(재렌더링).**
- Python에는 직접 대응이 없지만 비유하면 **엑셀 셀**입니다 — A1 값을 바꾸면 A1을 참조하는 모든 셀이 자동 갱신되듯, state를 바꾸면 그 값을 쓰는 화면이 자동 갱신됩니다.
- `const [a, b] = ...`는 **배열 구조 분해**로, Python의 튜플 언패킹 `a, b = (1, 2)`와 동일합니다.

> ⚠️ 왜 `result = 새값`으로 직접 안 바꾸고 `setResult(새값)`을 쓰나?
> React는 **setter를 통해 바뀐 것만 감지**해서 화면을 다시 그립니다. 직접 대입하면 화면이 안 바뀝니다.

### ⑥ `map()` = 리스트 컴프리헨션

```jsx
{sources.map((source, index) => ( <div key={index}>...</div> ))}
```

- 배열의 각 원소를 화면 조각으로 변환합니다.
- Python **리스트 컴프리헨션** `[render(s) for s in sources]`와 **완전히 같은 원리**입니다.
- `index`는 반복 순번(0,1,2…)입니다.

### ⑦ 화살표 함수 `=>` = `lambda`

```jsx
s => s.trim()          // JS
lambda s: s.strip()    # Python (같은 뜻)
```

`=>`는 익명 함수를 짧게 쓰는 문법으로, Python `lambda`에 해당합니다.

### ⑧ `&&` 조건부 렌더링 = "조건이 참이면 보여줘"

```jsx
{error && ( <div>{error}</div> )}
```

- "`error`가 있으면(참이면) 오른쪽 `<div>`를 화면에 보여줘"라는 뜻.
- Python의 단축 평가 `error and something`과 같은 원리입니다.

### ⑨ 삼항 연산자 `조건 ? A : B` = `A if 조건 else B`

```jsx
{isLoading ? "분석 중..." : "역량 분석 요청"}
// Python: "분석 중..." if isLoading else "역량 분석 요청"
```

### ⑩ `import` / `export` = Python의 import와 동일

```jsx
export default App;              // 이 파일의 대표 결과물을 내보냄
import App from "./App.jsx";     // 다른 파일에서 가져옴
```

Python `import`와 거의 같습니다. `export default`는 "이 파일의 메인 export"라는 뜻이고, 가져올 때 이름을 자유롭게 붙일 수 있습니다.

### 보너스: `className`은 왜 `class`가 아닌가?

JSX에서 `class`는 JS 예약어라 못 씁니다. 그래서 HTML의 `class` 속성을 **`className`** 으로 씁니다.
값에 들어가는 `"bg-white rounded-xl p-6"` 같은 건 **Tailwind CSS** 스타일 이름입니다(4절 참고).

---

## 2. 파일별 상세 설명

### 2-1. `index.html` — 브라우저가 처음 여는 껍데기

핵심은 딱 두 줄입니다(개념):

```html
<div id="root"></div>              <!-- 텅 빈 상자 -->
<script type="module" src="/src/main.jsx"></script>  <!-- 여기에 앱을 심어라 -->
```

- 브라우저는 이 **빈 `<div id="root">`** 하나만 가지고 시작합니다.
- 실제 화면은 전부 JS(React)가 **런타임에 채워 넣습니다.**
- Python 비유: 빈 컨테이너를 하나 만들고, 파이썬 코드가 내용을 동적으로 채우는 것.

### 2-2. `main.jsx` — 진입점 (앱을 심는 곳)

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'          // ← 전역 CSS(+Tailwind) 로드
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

한 줄씩:
- `import './index.css'` — 전역 스타일을 불러옵니다. 여기 안에 `@tailwind` 지시어가 있어 Tailwind가 활성화됩니다.
- `document.getElementById('root')` — 위 `index.html`의 빈 상자를 찾습니다.
- `createRoot(...).render(<App />)` — **그 상자 안에 `App` 컴포넌트를 그려 넣습니다.** 여기서부터 화면이 시작됩니다.
- `<StrictMode>` — React가 개발 중 실수를 잡아주는 "엄격 모드" 껍데기입니다. 실제 화면엔 영향 없습니다.
- Python 비유: `main.jsx`는 `if __name__ == "__main__":` 블록. "앱을 실제로 실행시키는" 시작점.

### 2-3. `App.jsx` — 두뇌 (상태 관리 + 백엔드 호출)

이 파일이 가장 중요합니다. **화면 전체를 조율하고, 백엔드에 요청을 보냅니다.**

#### (a) 세 개의 상태

```jsx
const [result, setResult] = useState(null);       // 백엔드 응답 결과
const [isLoading, setIsLoading] = useState(false); // 로딩 중인지
const [error, setError] = useState(null);          // 에러 메시지
```

이 3개가 화면의 "현재 상황"을 기억합니다. 이 값들이 바뀔 때마다 화면이 자동으로 다시 그려집니다.
Python 비유: 함수 안에 `result`, `is_loading`, `error` 지역 변수를 두되, **바꾸면 UI가 자동 갱신되는** 특별한 변수.

#### (b) 백엔드 호출 함수 `handleAnalyze`

```jsx
async function handleAnalyze(formData) {
  setIsLoading(true);   // 1) 로딩 시작 표시
  setError(null);
  setResult(null);

  try {
    const response = await fetch(`${API_BASE}/analyze`, {   // 2) POST 요청
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({                                // 3) 파이썬 dict→JSON
        major: formData.major,
        skills: formData.skills,
        job_type: formData.jobType,
      }),
    });

    if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
    const data = await response.json();   // 4) 응답 JSON 파싱
    setResult(data);                       // 5) 결과 저장 → 화면 갱신

  } catch (err) {                          // 6) 실패 시 에러 처리
    if (err.message.includes("Failed to fetch")) {
      setError("FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.");
    } else {
      setError(err.message);
    }
  } finally {
    setIsLoading(false);                   // 7) 성공/실패 무관하게 로딩 종료
  }
}
```

Python으로 옮기면 거의 이렇습니다:

```python
import requests, json

def handle_analyze(form_data):
    # setIsLoading(True) ...
    try:
        response = requests.post(
            f"{API_BASE}/analyze",
            headers={"Content-Type": "application/json"},
            json={"major": form_data["major"],
                  "skills": form_data["skills"],
                  "job_type": form_data["job_type"]},
        )
        response.raise_for_status()          # if not response.ok
        data = response.json()
        # setResult(data)
    except Exception as err:
        ...                                   # setError(...)
    finally:
        ...                                   # setIsLoading(False)
```

핵심 개념 매핑:
- `fetch` ≈ Python `requests.post` (브라우저 내장 HTTP 도구)
- `async` / `await` ≈ Python `async def` / `await` — "이 작업(네트워크)이 끝날 때까지 기다렸다가 다음 줄로"
- `JSON.stringify(dict)` ≈ `json.dumps(dict)` (파이썬 dict → JSON 문자열)
- `await response.json()` ≈ `response.json()` (JSON → 객체)
- `try / catch / finally` ≈ Python `try / except / finally` (이름만 `catch`)

> 🔒 보안 포인트: 6번 줄 주석 `// ⚠️ API Key는 절대 여기에 넣지 않습니다` 는 매우 중요합니다.
> 프론트엔드 코드는 **브라우저에서 누구나 볼 수 있습니다.** API Key를 여기 넣으면 그대로 노출됩니다.
> 그래서 Key는 **백엔드(.env)에만** 두고, 프론트는 백엔드를 통해서만 AI를 호출합니다. 지금 구조가 올바릅니다.

#### (c) 화면 반환부 (JSX)

```jsx
return (
  <div className="min-h-screen bg-slate-50 py-10 px-4">
    <div className="max-w-2xl mx-auto">
      <h1>CareerFit AI</h1>
      <p>...</p>

      <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />   {/* 입력 폼 */}

      {error && ( <div>...{error}</div> )}          {/* 에러가 있으면 표시 */}
      {isLoading && ( <div>분석 중입니다...</div> )}  {/* 로딩 중이면 표시 */}

      {result && (                                   {/* 결과가 있으면 표시 */}
        <div>
          <ResultCard answer={result.answer} />
          {result.sources && result.sources.length > 0 && (
            <SourceCard sources={result.sources} />
          )}
        </div>
      )}
    </div>
  </div>
);
```

- `<InputForm onSubmit={handleAnalyze} .../>` — 입력 폼에 **"제출되면 `handleAnalyze`를 실행해"** 라고 함수를 넘겨줍니다. (함수를 값처럼 넘김 = Python에서 함수를 인자로 전달하는 것과 동일)
- `{error && ...}`, `{isLoading && ...}`, `{result && ...}` — 세 가지 상태에 따라 **보여줄 화면을 갈아끼웁니다.** 이게 "상태 기반 UI"의 핵심입니다.
- 정리하면 App은: 입력을 받고(InputForm) → 백엔드를 호출하고(handleAnalyze) → 상태(result/error/isLoading)에 따라 결과를 그립니다.

### 2-4. `InputForm.jsx` — 입력 폼

```jsx
function InputForm({ onSubmit, isLoading }) {
  const [major, setMajor] = useState("");
  const [skillsInput, setSkillsInput] = useState("");
  const [jobType, setJobType] = useState("");

  function handleSubmit() {
    const skills = skillsInput.split(",").map(s => s.trim()).filter(Boolean);
    onSubmit({ major, skills, jobType });
  }
  return ( ...입력창 3개 + 버튼... );
}
```

- **각 입력창마다 state가 하나씩** 있습니다(`major`, `skillsInput`, `jobType`).
- 입력창은 이렇게 연결됩니다:
  ```jsx
  <input value={major} onChange={e => setMajor(e.target.value)} />
  ```
  - `value={major}` — 입력창의 현재 내용은 state `major`가 결정.
  - `onChange={e => setMajor(e.target.value)}` — 사용자가 글자를 칠 때마다 `e.target.value`(입력값)로 state를 갱신.
  - 이 패턴을 **"제어 컴포넌트(controlled component)"** 라 합니다: **화면 입력값과 state를 항상 일치**시키는 방식.
- `handleSubmit`의 스킬 처리:
  ```jsx
  skillsInput.split(",").map(s => s.trim()).filter(Boolean)
  ```
  Python으로: `[s.strip() for s in skills_input.split(",") if s.strip()]`
  - `split(",")` → 쉼표로 나눔
  - `.map(s => s.trim())` → 각 항목 공백 제거
  - `.filter(Boolean)` → 빈 문자열 제거 (Python의 `if s` 필터)
  - 즉 `"Python, SQL, "` → `["Python", "SQL"]`
- 버튼:
  ```jsx
  <button onClick={handleSubmit}
    disabled={isLoading || !major || !skillsInput || !jobType}>
    {isLoading ? "분석 중..." : "역량 분석 요청"}
  </button>
  ```
  - `onClick={handleSubmit}` — 클릭하면 `handleSubmit` 실행 → 부모(App)의 `onSubmit`(=handleAnalyze) 호출.
  - `disabled={...}` — **로딩 중이거나 빈 칸이 하나라도 있으면 버튼 비활성화.** (`!major`는 "major가 비었으면")
  - `{isLoading ? ... : ...}` — 로딩 중이면 버튼 글자를 "분석 중..."으로.

### 2-5. `ResultCard.jsx` — AI 분석 결과 카드

```jsx
function ResultCard({ answer }) {
  return (
    <div className="... whitespace-pre-line">
      <h2>📊 AI 분석 결과</h2>
      <p className="whitespace-pre-line">{answer}</p>
    </div>
  );
}
```

- `answer`(백엔드가 준 LLM 답변 텍스트)를 받아 그대로 보여주는 **단순 표시용** 컴포넌트.
- `whitespace-pre-line` — 답변 속 **줄바꿈(\n)을 화면에서도 줄바꿈으로** 살려주는 Tailwind 클래스. (없으면 줄바꿈이 공백 하나로 뭉개짐)

### 2-6. `SourceCard.jsx` — 참고 공고 출처 카드

```jsx
function SourceCard({ sources }) {
  if (!sources || sources.length === 0) {
    return <div>참고한 공고 데이터가 없습니다.</div>;   // ① 빈 경우
  }
  return (
    <div>
      <h2>📄 참고한 공고 출처</h2>
      <div>
        {sources.map((source, index) => (              // ② 각 공고를 카드로
          <div key={index}>
            <p>{source.company} — {source.title}</p>
            <p>필수 스킬: {source.required_skills || "정보 없음"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- `sources`(공고 배열)를 받아, **비었으면** "데이터 없음" 박스를, **있으면** 각 공고를 카드로 나열.
- `!sources || sources.length === 0` — "sources가 없거나(null) 길이가 0이면". Python: `if not sources: ...`
- `source.required_skills || "정보 없음"` — 값이 비었으면 "정보 없음"으로 대체. Python: `source.get("required_skills") or "정보 없음"`
- 이 파일의 리뷰는 **4절**에 자세히 있습니다.

---

## 3. Tailwind CSS와 `className` (스타일의 원리)

`className="bg-white rounded-xl shadow-sm border p-6"` 처럼 나열된 짧은 단어들이 **Tailwind CSS** 스타일입니다.

- 원리: 미리 정의된 **작은 유틸리티 클래스**를 조합해 스타일을 만듭니다.
  - `bg-white` = 배경 흰색, `p-6` = 안쪽 여백(padding) 24px, `rounded-xl` = 모서리 둥글게, `text-sm` = 작은 글씨, `mb-3` = 아래 여백(margin-bottom).
- Python 비유: CSS를 직접 쓰는 대신, **미리 만든 레고 블록(클래스)** 을 끼워 맞추는 방식.
- 이 프로젝트는 **Tailwind v3** 를 쓰며, 설정은 `frontend/tailwind.config.js`, `frontend/postcss.config.js`, `frontend/src/index.css`(맨 위 `@tailwind` 3줄)에 있습니다.
- 자세한 설치/실행은 루트 `README.md`의 "5. 프론트엔드 실행" 참고.

---

## 4. `SourceCard.jsx` 코드 리뷰 (심각도별)

보안 · 응답 구조 · 접근성 기준으로 검토한 결과입니다.

### 🔴 Critical — 없음

치명적 결함은 없습니다. 특히 **보안(XSS) 문제는 없습니다** — 아래 설명 참고.

### 보안 (Security) — 안전, 주의점만

- **React는 `{source.company}` 같은 값을 화면에 넣을 때 자동으로 이스케이프**합니다. 공고 데이터에 `<script>` 같은 게 있어도 **코드로 실행되지 않고 그냥 글자로** 표시됩니다 → XSS 취약점 없음.
- **[Suggestion]** 향후 이 값을 `dangerouslySetInnerHTML`로 렌더링하거나 `<a href={값}>` 링크로 바꾸면 그때부터 위험. 지금 구조를 유지하면 안전합니다.

### 응답 구조 (Response Structure)

| 심각도 | 문제 | 설명 |
|---|---|---|
| 🟡 Warning | `required_skills`가 항상 "정보 없음" | 프론트는 `source.required_skills`를 기대하지만, **백엔드 metadata에 `required_skills`가 없어** `build_sources`가 항상 `""`을 반환 → `|| "정보 없음"` 폴백이 매번 걸림. **프론트-백엔드 필드 불일치.** (백엔드 metadata에 필드를 추가하거나 이 줄을 제거) |
| 🟡 Warning | `key={index}` 안티패턴 | 리스트 항목의 "이름표"로 배열 순번을 사용. 목록이 재정렬·삭제되면 잘못된 항목에 상태가 붙을 수 있음 → `key={source.company + source.title}` 같은 **내용 기반 고유값** 권장. |
| 🟡 Warning | `company`/`title` 폴백·null 방어 없음 | 값이 없으면 화면에 " — "(대시만) 남고, 배열 원소가 `null`이면 런타임 에러 가능(가능성 낮음). |

### 접근성 (Accessibility)

| 심각도 | 문제 | 설명 |
|---|---|---|
| 🟡 Warning | 목록에 `<ul>/<li>` 미사용 | 공고를 `<div>`로만 나열. 스크린 리더가 "목록, N개 중 1번째"를 안내 못 함 → 반복부를 `<ul>`/`<li>`로. |
| 🔵 Suggestion | 장식 이모지 `📄` | 스크린 리더가 이모지를 읽음 → `<span aria-hidden="true">📄</span>`로 감싸기. |
| 🔵 Suggestion | 제목 계층 확인 | 이 컴포넌트의 `<h2>` 앞에 페이지 `<h1>`(App의 "CareerFit AI")이 있는지 확인 — 지금 App엔 `<h1>`이 있으니 대체로 OK. |
| 🔵 Suggestion | 작은 회색 글씨 대비 | `text-xs`(12px) + `text-slate-500`은 AA를 아슬아슬 통과. "데이터 없음" 박스는 경계선 → `text-slate-600` 권장. |

### 가장 먼저 고칠 것

**Warning 1 (`required_skills` 불일치)** — 실제로 항상 "정보 없음"이 뜨는 눈에 보이는 문제라 우선순위가 가장 높습니다.

---

## 5. 용어 빠른 대조표 (JS ↔ Python)

| JavaScript / React | Python 대응 | 비고 |
|---|---|---|
| `function App() { return <div/> }` | UI를 반환하는 함수 | 컴포넌트 |
| `{ 값 }` (JSX 안) | f-string `f"{값}"` | 값 삽입 |
| `const [x, setX] = useState(0)` | 바꾸면 화면 갱신되는 변수 | 상태 |
| `arr.map(x => ...)` | `[... for x in arr]` | 리스트 변환 |
| `x => x + 1` | `lambda x: x + 1` | 익명 함수 |
| `a && B` (JSX) | `a and B` | 조건부 표시 |
| `c ? A : B` | `A if c else B` | 삼항 |
| `fetch(url, {...})` | `requests.post(url, ...)` | HTTP 요청 |
| `async` / `await` | `async def` / `await` | 비동기 |
| `JSON.stringify(o)` | `json.dumps(o)` | 객체→JSON |
| `await res.json()` | `res.json()` | JSON 파싱 |
| `try/catch/finally` | `try/except/finally` | 예외 처리 |
| `import/export` | `import` | 모듈 |
| `className` | (HTML `class`) | JSX 예약어 회피 |

---

*작성 목적: Python 배경 개발자가 프론트엔드 코드를 스스로 읽고 리뷰할 수 있도록 돕기 위함. 코드 변경 없이 설명·리뷰만 담았습니다.*
