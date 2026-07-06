import pandas as pd
import sqlite3
import json
import os
from datetime import datetime  # created_at(최초 저장일) 부여 및 마감일 파싱에 사용


# ─── 1. 파일 경로 설정

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_CSV = os.path.join(BASE_DIR, "jobs.csv")
DB_PATH = os.path.join(BASE_DIR, "careerfit.db")
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")

# ─── 2. CSV 읽기


def load_data(filepath: str) -> pd.DataFrame:
    """
    CSV 파일을 읽어 DataFrame으로 반환합니다.
    인코딩 오류가 발생하면 cp949로 재시도합니다.
    """

    try:
        df = pd.read_csv(filepath, encoding="utf-8")
        print(f"✅ 파일 읽기 성공 (UTF-8): {filepath}")

    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="cp949")
        print(f"✅ 파일 읽기 성공 (CP949): {filepath}")

    print(f"   행 수: {len(df)}, 열 수: {len(df.columns)}")
    print(f"   컬럼: {df.columns.tolist()}")

    return df


# 결측치 확인


def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    각 컬럼의 결측치(빈값) 수와 비율을 확인합니다.
    요리 비유: 재료 중 빠진 것이 있는지 확인하는 단계입니다.
    """

    print("\n=== 결측치 확인 ===")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(1)
    result = pd.DataFrame({"결측치 수": missing, "결측치 비율(%)": missing_pct})

    print(result[result["결측치 수"] > 0])  # 결측치 있는 컬럼만 출력

    if missing.sum() == 0:
        print("   ✅ 결측치 없음")

    else:
        print(f"   ⚠️  총 {missing.sum()}개 결측치 발견")

    return df


# 결측치 처리


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치를 처리합니다.
    - 텍스트 컬럼: 빈 문자열로 채웁니다
    - 핵심 컬럼이 비어있는 행은 제거합니다
    """

    print("\n=== 결측치 처리 ===")
    before = len(df)

    # 핵심 컬럼(title, required_skills)이 비어있는 행 제거
    # 이 정보가 없으면 RAG 검색에 의미가 없기 때문입니다

    df = df.dropna(subset=["title", "required_skills"])

    # 나머지 텍스트 컬럼은 빈 문자열로 채웁니다
    # deadline 포함: 마감일이 비면 NaN → str 변환 시 "nan"이 되어 metadata를 오염시키므로 빈 문자열로 채움
    text_cols = ["preferred_skills", "description", "company", "job_type", "deadline"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")

    after = len(df)

    print(f" 처리 전: {before}행 → 처리 후: {after}행")
    print(f" 제거된 행: {before - after}행")

    return df


# 중복값 제거


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    중복 행을 확인하고 제거합니다.
    company + title 조합이 같으면 중복으로 판단합니다.
    """

    print("\n=== 중복 확인 ===")

    before = len(df)

    # company + title 기준으로 중복 확인
    duplicated = df.duplicated(subset=["company", "title"], keep=False)

    if duplicated.sum() > 0:
        print(f"   ⚠️  중복 발견: {duplicated.sum()}행")
        print(df[duplicated][["company", "title"]])

    else:
        print("   ✅ 중복 없음")

    # 첫 번째 행만 남기고 중복 제거
    df = df.drop_duplicates(subset=["company", "title"], keep="first")

    after = len(df)

    print(f"   제거 후: {after}행 (제거: {before - after}행)")

    return df




SKILL_NORMALIZATION = {
    "python": "Python",
    "sql": "SQL",
    "ai": "AI",
    "ml": "머신러닝",
    "machine learning": "머신러닝",
    "deep learning": "딥러닝",
    "r": "R",  # 대소문자 주의
    "js": "JavaScript",
    "javascript": "JavaScript",
    "tableau": "Tableau",
    "powerbi": "Power BI",
    "power bi": "Power BI",
}


def normalize_skills(skills_str: str) -> str:
    """
    스킬 키워드 문자열을 표준화합니다.
    입력: "python, sql, Machine Learning"
    출력: "Python, SQL, 머신러닝"
    """

    if not isinstance(skills_str, str) or not skills_str.strip():
        return ""

    skills = [s.strip() for s in skills_str.split(",")]

    normalized = []

    for skill in skills:
        # 소문자로 변환해서 사전에서 찾기
        lower = skill.lower()

        # 사전에 있으면 표준화된 이름으로, 없으면 원래 값 유지
        normalized.append(SKILL_NORMALIZATION.get(lower, skill))

    return ", ".join(normalized)


def standardize_skills(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 스킬 키워드 표준화 ===")

    # 표준화 전 원본을 미리 복사 (비교용) — 덮어쓰기 전에!
    before = df["required_skills"].copy()

    for col in ["required_skills", "preferred_skills"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_skills)

    print(" ✅ 표준화 완료")

    # 표준화 전후 비교 샘플
    print("\n [표준화 전후 비교 샘플]")
    compare = pd.DataFrame({
        "표준화 전": before,
        "표준화 후": df["required_skills"],
    })
    print(compare.head(3).to_string())

    return df


# SQLite 저장

def save_to_sqlite(df: pd.DataFrame, db_path: str) -> None:
    """
    전처리된 DataFrame을 SQLite 데이터베이스에 저장합니다.

    요리 비유:
    손질이 끝난 재료를 냉장고(SQLite)에 정리해서 넣는 단계입니다.
    """
    print("\n=== SQLite 저장 ===")

    conn = sqlite3.connect(db_path)

    # DataFrame을 SQL 테이블로 저장
    # if_exists="replace": 테이블이 이미 있으면 덮어씁니다
    df.to_sql("jobs", conn, if_exists="replace", index=False)

    # 저장 확인
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    print(f"   ✅ 저장 완료: careerfit.db에 {count}행 저장됨")
    print(f"   파일 위치: {db_path}")

    conn.close()


def query_sqlite(db_path: str) -> None:
    """
    SQLite에서 데이터를 조회해 저장 결과를 확인합니다.
    """
    print("\n=== SQLite 조회 테스트 ===")
    conn = sqlite3.connect(db_path)

    # 1. 전체 행 수
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM jobs")
    print(f"   전체 공고 수: {cursor.fetchone()[0]}개")

    # 2. 직무 분류별 개수
    print("\n   [직무 분류별 공고 수]")
    cursor.execute("""
        SELECT job_type, COUNT(*) as count
        FROM jobs
        GROUP BY job_type
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]}개")

    # 3. Python 필수 스킬 공고만 조회
    print("\n   [Python이 필요한 공고]")
    cursor.execute("""
        SELECT company, title, required_skills
        FROM jobs
        WHERE required_skills LIKE '%Python%'
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"   - {row[0]} | {row[1]}")
        print(f"     스킬: {row[2]}")

    conn.close()

# ─── metadata 확장용 헬퍼 2개 ───

def to_deadline_month(deadline: str) -> str:
    """
    마감일 문자열에서 '연-월(YYYY-MM)'만 뽑아냅니다.
    → ChromaDB에서 "9월 마감 공고" 같은 필터의 검색 키로 씁니다.

    회계 비유: 마감일이라는 전표에서 '귀속 월(月)' 계정만 따로 분개해 두는 것.

    처리 예시:
      "2026-09-15" → "2026-09"   (정상 ISO 형식)
      "26.09.10"   → "2026-09"   (11번 공고: 축약 형식도 보정 시도)
      ""           → ""          (12번 공고: 마감일 없음 → 필터에서 자연히 제외)
    """
    s = str(deadline).strip()
    if not s:
        # 빈 마감일: 억지로 값을 만들지 않고 빈 문자열 반환 (오염 데이터를 조용히 지어내지 않음)
        return ""

    # 알려진 날짜 형식을 순서대로 시도 (ISO 표준 → YY.MM.DD 축약형)
    for fmt in ("%Y-%m-%d", "%y.%m.%d"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m")
        except ValueError:
            continue  # 이 형식이 아니면 다음 형식 시도

    # 어떤 형식에도 안 맞으면 빈 문자열 (알 수 없는 형식은 필터 대상에서 제외)
    return ""


def load_existing_created_at(json_path: str) -> dict:
    """
    기존 rag_documents.json을 '취득원가 장부'처럼 읽어,
    "회사명||직무명 → created_at" 지도를 만듭니다.
    → 이미 등록됐던 공고의 '최초 저장일'을 이월(carry-over)하기 위한 조회용 지도.

    식별 키(identity)는 사용자가 정한 대로 company + title 조합을 씁니다.
    (remove_duplicates()의 중복 판단 기준과 동일 → 일관성 유지)

    - 파일이 아직 없으면(=최초 실행) 빈 지도를 반환합니다.
    """
    if not os.path.exists(json_path):
        return {}  # 최초 실행: 이월할 과거 기록이 없음

    with open(json_path, "r", encoding="utf-8") as f:
        old_docs = json.load(f)

    created_map = {}
    for doc in old_docs:
        meta = doc.get("metadata", {})
        # "회사명||직무명"을 키로 사용 ('||'는 회사/직무명에 안 쓰이는 구분자)
        key = f"{meta.get('company', '')}||{meta.get('title', '')}"
        created = meta.get("created_at", "")
        if created:  # created_at이 기록돼 있던 기존 문서만 지도에 등록
            created_map[key] = created

    return created_map


def convert_to_rag_documents(df: pd.DataFrame, json_path: str) -> list:
    """
    DataFrame의 각 행을 RAG 검색에 적합한 자연어 문서로 변환합니다.

    요리 비유:
    냉장고의 재료 목록을 셰프가 바로 읽을 수 있는 레시피 카드로 변환합니다.

    json_path: 기존 rag_documents.json 경로.
               → 이 파일에서 과거 created_at을 읽어와 최초 저장일을 이월합니다.
    """
    print("\n=== RAG 문서 변환 ===")
    documents = []

    # (1) 기존 문서에서 '최초 저장일 지도'를 먼저 불러옵니다 (저장은 이 뒤에 일어나므로 안전)
    created_map = load_existing_created_at(json_path)
    today = datetime.now().strftime("%Y-%m-%d")  # 새 공고에 부여할 오늘 날짜

    # 이월 vs 신규 개수 집계용 (변환 결과를 눈으로 검증하기 위한 카운터)
    carried_over = 0
    newly_added = 0

    for _, row in df.iterrows():
        # 자연어 문서 텍스트 생성
        doc_text = (
            f"{row.get('company', '')}에서 {row.get('title', '')}를 채용합니다. "
            f"필수 스킬은 {row.get('required_skills', '정보 없음')}입니다. "
            f"우대 스킬: {row.get('preferred_skills', '없음')}. "
            f"업무 내용: {row.get('description', '정보 없음')}"
        )

        company = str(row.get("company", ""))
        title = str(row.get("title", ""))

        # (2) 이 공고의 '최초 저장일(created_at)' 결정
        #     식별 키 "회사명||직무명"으로 과거 기록을 조회
        #       - 지도에 있으면  → 과거 날짜 그대로 이월 (기존 공고: 취득원가 유지)
        #       - 지도에 없으면  → 오늘 날짜 부여        (신규 공고)
        identity_key = f"{company}||{title}"
        if identity_key in created_map:
            created_at = created_map[identity_key]
            carried_over += 1
        else:
            created_at = today
            newly_added += 1

        # metadata: 검색 결과를 필터링하거나 출처를 표시할 때 사용합니다
        # ※ ChromaDB metadata 값은 모두 str이어야 하므로 전부 문자열로 변환
        metadata = {
            "id": str(row.get("id", "")),
            "company": company,
            "title": title,
            "job_type": str(row.get("job_type", "")),
            "deadline": str(row.get("deadline", "")),
            "source": "jobs.csv",
            # ── 확장 필드 3개 ──
            "company_type": str(row.get("company_type", "")),          # 요구①: "스타트업 공고만" 필터
            "deadline_month": to_deadline_month(row.get("deadline", "")),  # 요구②: "9월 마감" 필터 (헬퍼로 안전 변환)
            "created_at": created_at,                                   # 요구③: 최초 저장일 (이월 처리됨)
        }

        documents.append({
            "text": doc_text,
            "metadata": metadata,
            "doc_id": f"job_{row.get('id', '')}"  # ChromaDB의 고유 ID
        })

    # (3) 이월/신규 집계를 출력해 created_at 처리가 의도대로 됐는지 눈으로 검증
    print(f"   ✅ {len(documents)}개 문서 변환 완료 "
          f"(created_at 이월: {carried_over}개, 신규: {newly_added}개)")
    print("\n   [첫 번째 문서 미리보기]")
    print(f"   ID: {documents[0]['doc_id']}")
    print(f"   텍스트: {documents[0]['text'][:100]}...")
    print(f"   메타데이터: {documents[0]['metadata']}")

    return documents


def save_rag_documents(documents: list, json_path: str) -> None:
    """
    RAG 문서를 JSON 파일로 저장합니다.
    ChromaDB에 저장하기 전 중간 저장 역할을 합니다.
    """
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
    print(f"\n   ✅ RAG 문서 JSON 저장: {json_path}")



if __name__ == "__main__":
    # 1. 읽기
    df_jobs = load_data(JOBS_CSV)

    # 2. 결측치 확인
    df_jobs = check_missing(df_jobs)

    # 3. 결측치 처리
    df_jobs = handle_missing(df_jobs)

    # 4. 중복 제거
    df_jobs = remove_duplicates(df_jobs)

    # 5. 스킬 키워드 표준화
    df_jobs = standardize_skills(df_jobs)

    # 6. SQLite 저장
    save_to_sqlite(df_jobs, DB_PATH)

    # 7. 저장 결과 조회
    query_sqlite(DB_PATH)

    # 8. RAG 문서 변환 (RAG_JSON을 넘겨 기존 created_at을 이월)
    rag_documents = convert_to_rag_documents(df_jobs, RAG_JSON)

    # 9. RAG 문서 JSON 저장
    save_rag_documents(rag_documents, RAG_JSON)

    print(f"\n✅ 전처리 완료: 최종 RAG 문서 {len(rag_documents)}개 생성됨")