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

### 4.0 먼저, Git의 개념부터 (회계 비유로 이해하기)

Git을 처음 다룬다면 **명령어를 외우기 전에 그림부터** 잡는 게 훨씬 빠릅니다.

**Git이란?**
코드의 모든 변경 이력을 시점별로 기록·보관하는 **버전 관리 시스템**입니다.
> 📘 **회계 비유**: Git은 **분개장(journal)** 과 같습니다. 언제, 누가, 무엇을, 왜 바꿨는지 전표(커밋)로 남기고, 필요하면 특정 시점으로 되돌릴 수 있습니다. "Ctrl+Z 무한 버전 + 협업 기능"이라고 생각하면 됩니다.

**핵심 용어 6개**

| 용어 | 뜻 | 회계 비유 |
|------|-----|-----------|
| **Repository (저장소)** | 프로젝트 전체 + 모든 이력이 담긴 공간 | 회사의 전체 회계 장부철 |
| **Commit (커밋)** | 변경 사항을 하나의 기록으로 확정하는 것 | 전표 한 장을 끊어 장부에 기표 |
| **Branch (브랜치)** | 본선(main)에서 갈라져 나온 **독립 작업 공간** | 확정 장부를 건드리지 않고 만드는 **가결산용 시산표** |
| **Merge (병합)** | 브랜치의 작업을 본선에 합치는 것 | 검토 끝난 가결산을 확정 장부에 반영 |
| **Remote (원격)** | GitHub 서버에 있는 저장소 | 회사 서버의 원본 장부 (내 PC는 사본) |
| **Push / Pull** | 내 기록을 서버로 올림 / 서버 기록을 내려받음 | 장부 서버에 업로드 / 다운로드 |

**브랜치가 왜 필요한가?**
`main`(본선)은 **언제나 정상 작동해야 하는 확정본**입니다. 새 기능을 만들다 보면 코드가 잠시 깨질 수 있는데, 이걸 `main`에서 바로 하면 프로젝트 전체가 망가집니다.
그래서 **별도 브랜치(작업용 사본)에서 마음껏 실험하고, 완성·검증된 것만 `main`에 합칩니다.**

```
                    (내가 만든 작업 공간)
              ┌──● feature/rag-chatbot ──●──●──┐
              │        커밋   커밋   커밋       │  ← 검증 끝나면 병합(merge)
   main ──●───┴──────────────────────────────●─┴──●──▶  (항상 정상 작동하는 확정본)
        기존 이력                          병합됨
```

> 📘 **회계 비유**: `main`은 **감사받은 확정 재무제표**, 브랜치는 **결산 작업 중인 워킹 페이퍼**입니다. 워킹 페이퍼에서 숫자를 이리저리 맞춰보다가, 확정되면 그때 정식 재무제표에 반영하는 것과 같습니다.

---

### 4.1 전체 흐름 한눈에 보기

하루 작업은 보통 이 순서로 돕니다. 아래 명령어는 4.2부터 하나씩 설명합니다.

```
① 최신화        git pull origin main           (서버 최신 내용 내려받기)
② 브랜치 생성   git checkout -b feature/xxx    (작업용 사본 만들기)
③ 코드 수정      ... 파일 편집 ...
④ 확인          git status                     (뭐가 바뀌었나 확인)
⑤ 담기          git add .                      (커밋할 파일 고르기)
⑥ 기록          git commit -m "feat: ..."      (전표 끊기)
   ③~⑥ 반복 (작은 단위로 여러 번 커밋)
⑦ 올리기        git push origin feature/xxx    (서버에 업로드)
⑧ PR 생성        GitHub에서 Pull Request        (본선에 합쳐달라고 요청)
⑨ 병합 후 복귀   git checkout main → git pull   (본선으로 돌아와 최신화)
```

---

### 4.2 작업 시작 전: 최신 코드 동기화 (매우 중요)

작업을 시작하기 **전에 반드시** 서버의 최신 코드를 내려받습니다.

```powershell
git checkout main          # 본선으로 이동 (혹시 다른 브랜치에 있을 수 있으니)
git pull origin main       # 서버(origin)의 main 최신 내용을 내 PC로 내려받기
```

- `git fetch` : 서버에 새 내용이 있는지 **확인만** (내 코드엔 반영 X)
- `git pull` : 확인 + **실제로 내려받아 합치기** (`fetch` + `merge`)

> ⚠️ **이 단계를 건너뛰면?** 남이 이미 바꿔놓은 옛날 코드 위에서 작업하게 되어, 나중에 push할 때 **충돌(conflict)** 이 잔뜩 생깁니다. 자세한 건 4.8 참고.

---

### 4.3 작업 브랜치 생성

`main`에서 직접 작업하지 말고, **항상 새 브랜치**를 만들어 그 안에서 작업합니다.

**브랜치 이름 규칙**

| 접두어 | 용도 | 예시 |
|--------|------|------|
| `feature/` | 새 기능 | `feature/rag-chatbot` |
| `fix/` | 버그 수정 | `fix/health-endpoint` |
| `docs/` | 문서 작업 | `docs/workflow-guide` |
| `refactor/` | 구조 개선 | `refactor/analyze-router` |

```powershell
git checkout -b feature/rag-chatbot
```

- `git checkout -b <이름>` : 브랜치를 **새로 만들고 그 브랜치로 이동**까지 한 번에
- 이미 있는 브랜치로 옮길 때는 `-b` 없이: `git checkout feature/rag-chatbot`

**지금 내가 어느 브랜치에 있는지 확인**
```powershell
git branch          # 목록에서 * 표시가 현재 브랜치
```

> ⚠️ 브랜치를 만들기 전에 **4.2 최신화를 먼저** 하세요. 그래야 최신 `main`을 기준으로 브랜치가 갈라집니다.

---

### 4.4 코드 수정 및 커밋

**A. 무엇이 바뀌었는지 확인**
```powershell
git status          # 수정/추가/삭제된 파일 목록
git diff            # 구체적으로 어떤 줄이 바뀌었는지 (q 눌러서 나감)
```

**B. 커밋할 파일 담기 (staging)**
```powershell
git add .                    # 바뀐 파일 전부 담기
git add backend/main.py      # 특정 파일만 담기 (권장: 관련된 것만)
```
> 📘 **회계 비유**: `git add`는 **전표에 올릴 항목을 골라 대기시키는** 단계입니다. 아직 기표(commit)한 건 아니고, "이번 전표에 이 항목들을 넣겠다"고 표시만 한 상태입니다.

**C. 커밋 (기록 확정)**
```powershell
git commit -m "feat: RAG 챗봇 서비스 추가"
```

**커밋 메시지 규칙** — `타입: 설명` 형식

| 타입 | 의미 | 예시 |
|------|------|------|
| `feat` | 새 기능 | `feat: RAG 챗봇 서비스 추가` |
| `fix` | 버그 수정 | `fix: health 엔드포인트 응답 오류 해결` |
| `docs` | 문서 | `docs: 개발 루틴 문서 작성` |
| `refactor` | 코드 정리 | `refactor: routers/analyze.py 구조 개선` |
| `chore` | 설정·잡일 | `chore: .gitignore에 venv 추가` |

> 💡 **커밋 단위 원칙**: "하나의 커밋 = 하나의 의미 있는 변경". 여러 기능을 한 커밋에 몰아넣지 말고, **작게 자주** 커밋하세요. 나중에 문제를 되돌리기 훨씬 쉽습니다.

---

### 4.5 로컬에서 테스트

push하기 전에 코드가 실제로 동작하는지 확인합니다.

```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

API 정상 작동 확인 후 `Ctrl + C`로 중지

> ⚠️ **금지 사항 (CLAUDE.md)**: 검증하지 않고 push하지 않습니다. "될 것 같다"가 아니라 "돌려봤더니 된다"를 확인한 뒤 올리세요.

---

### 4.6 원격 저장소에 푸시

```powershell
git push origin feature/rag-chatbot
```

- `origin` = 원격 저장소(GitHub) 별명
- `feature/rag-chatbot` = 올릴 브랜치 이름
- 그 브랜치의 **첫 push**라면 이렇게 안내가 뜰 수 있습니다:
  ```powershell
  git push --set-upstream origin feature/rag-chatbot
  ```
  안내에 나온 명령을 그대로 복사해 실행하면 됩니다. 이후부터는 `git push`만 해도 됩니다.

---

### 4.7 Pull Request(PR) 생성 및 병합

**PR이란?** "내 브랜치 작업을 `main`에 합쳐도 될까요?" 하고 **검토를 요청하는 절차**입니다.
> 📘 **회계 비유**: 결산 워킹 페이퍼를 상급자에게 **결재 올리는** 것과 같습니다. 검토·승인이 나야 확정 장부(main)에 반영됩니다.

GitHub에서:
1. push 후 저장소 페이지에 뜨는 **"Compare & pull request"** 클릭
2. 제목·설명 작성 (무엇을, 왜 바꿨는지)
3. 리뷰 요청 → 승인 후 **"Merge pull request"** 클릭
4. 병합 후 **"Delete branch"** 로 다 쓴 브랜치 정리 (선택)

---

### 4.8 메인 브랜치로 돌아와 정리하기

병합이 끝나면 본선으로 돌아와 최신 상태로 맞춥니다.

```powershell
git checkout main               # 본선으로 이동
git pull origin main            # 방금 병합된 내 작업 포함 최신 내용 내려받기
git branch -d feature/rag-chatbot   # 다 쓴 로컬 브랜치 삭제 (선택)
```

이제 다음 작업을 위해 다시 4.2부터 반복하면 됩니다.

---

### 4.9 문제 상황별 대처 (자주 겪는 Git 사고)

Git은 **거의 모든 실수를 되돌릴 수 있습니다.** 당황하지 말고 상황에 맞는 방법을 찾으세요.

#### ① `main`에서 실수로 작업/커밋해버렸다
브랜치를 안 만들고 `main`에서 바로 코드를 고쳤을 때.

- **아직 커밋 전이라면** — 변경분을 그대로 새 브랜치로 옮기기:
  ```powershell
  git checkout -b feature/실제작업이름   # 지금까지 바뀐 내용이 새 브랜치로 따라옴
  ```
- **이미 커밋까지 했다면** — 새 브랜치를 만들고, main은 커밋 이전으로 되돌리기:
  ```powershell
  git branch feature/실제작업이름   # 현재 커밋을 새 브랜치에 저장
  git reset --hard origin/main      # main을 서버 기준으로 되돌림 (⚠️ 주의: 아래 설명)
  git checkout feature/실제작업이름 # 작업 브랜치로 이동
  ```
  > ⚠️ `reset --hard`는 되돌린 이후의 변경을 **완전히 삭제**합니다. 위 순서처럼 `git branch`로 먼저 백업한 뒤에만 사용하세요.

#### ② `git pull`을 안 하고 작업해서 push가 거부됨 (rejected)
> `error: failed to push ... Updates were rejected because the remote contains work that you do not have`

서버에 남이 올린 새 내용이 있는데 내가 옛날 기준으로 작업했다는 뜻.
```powershell
git pull origin feature/브랜치이름   # 서버 내용을 먼저 내려받아 합친 뒤
git push origin feature/브랜치이름   # 다시 push
```

#### ③ 병합 충돌(Merge Conflict)이 났다
같은 파일의 같은 줄을 나와 다른 사람이 각각 고쳤을 때 발생. pull이나 merge 중에 이런 표시가 뜹니다:
```
<<<<<<< HEAD
내가 쓴 코드
=======
남이 쓴 코드
>>>>>>> origin/main
```
**해결 순서**:
1. 해당 파일을 열어 `<<<<<<<`, `=======`, `>>>>>>>` 표시를 찾습니다.
2. **어느 쪽을 남길지(또는 둘을 합칠지) 직접 결정**하고, 이 표시 기호 3줄을 모두 지웁니다.
3. 정리한 파일을 다시 담고 커밋:
   ```powershell
   git add 충돌났던파일
   git commit                # 병합 커밋 메시지가 자동으로 채워짐 → 저장하면 됨
   ```
> ⚠️ 충돌은 **에러가 아니라 정상적인 협업 과정**입니다. 겁내지 말고 어느 코드가 맞는지 판단해서 정리하면 됩니다.

#### ④ 잘못된 브랜치에서 작업 중이었다 (아직 커밋 전)
```powershell
git stash                       # 지금 변경분을 잠시 보관(서랍에 넣기)
git checkout 올바른브랜치        # 원하는 브랜치로 이동
git stash pop                   # 보관했던 변경분을 여기서 다시 꺼내기
```

#### ⑤ 방금 한 커밋 메시지를 잘못 썼다 (아직 push 전)
```powershell
git commit --amend -m "fix: 올바른 메시지"
```
> ⚠️ 이미 push한 커밋은 `--amend`로 고치지 마세요(이력이 꼬입니다). push 전에만 사용.

#### ⑥ `git add`를 잘못했다 (커밋 전, 담기 취소)
```powershell
git restore --staged 파일이름    # 담기(staging)만 취소, 코드 수정 내용은 유지
```

#### ⑦ 방금 커밋을 통째로 되돌리고 싶다 (아직 push 전)
```powershell
git reset --soft HEAD~1     # 커밋만 취소, 수정 내용은 그대로 남김 (안전)
git reset --hard HEAD~1     # 커밋 + 수정 내용까지 전부 삭제 (⚠️ 복구 어려움)
```
> 💡 확신이 없으면 항상 `--soft`를 쓰세요. `--hard`는 정말 버려도 되는 경우에만.

#### ⑧ 방금 명령이 뭘 했는지 모르겠고 이전 상태로 돌아가고 싶다
```powershell
git reflog                  # 내가 한 모든 이동/커밋 이력이 나옴
git reset --hard <해시>      # 돌아가고 싶은 시점의 해시로 복귀
```
> 📘 `reflog`는 Git의 **CCTV**입니다. 웬만한 실수는 여기서 시점을 찾아 되돌릴 수 있습니다.

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
| 현재 브랜치 확인 | `git branch` |
| 새 브랜치 생성 + 이동 | `git checkout -b feature/<이름>` |
| 기존 브랜치로 이동 | `git checkout <이름>` |
| 변경 내용 확인 | `git status` / `git diff` |
| 커밋할 파일 담기 | `git add .` |
| 담기 취소 | `git restore --staged <파일>` |
| 커밋하기 | `git commit -m "feat: 기능 설명"` |
| 커밋 메시지 수정 (push 전) | `git commit --amend -m "새 메시지"` |
| 푸시하기 | `git push origin feature/<이름>` |
| 변경분 잠시 보관/꺼내기 | `git stash` / `git stash pop` |
| 실수 이력 추적 (CCTV) | `git reflog` |

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
