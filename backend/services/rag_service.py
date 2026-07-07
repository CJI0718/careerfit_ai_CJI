import chromadb
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CHROMA_PATH = str(BASE_DIR / "chroma_db")
RAG_JSON = str(BASE_DIR / "data" / "rag_documents.json")

client = chromadb.PersistentClient(path=CHROMA_PATH)

# 임베딩 함수를 지정하지 않으면 ChromaDB 기본 모델(all-MiniLM-L6-v2, 384차원)을 쓴다.
# 이 모델은 onnxruntime 기반이라 torch가 필요 없어 가볍고 배포(무료 인스턴스)에 유리하다.
# 단, 영어 위주 모델이라 한국어 검색 품질은 ko-sroberta보다 떨어진다. (배포 우선 절충)
# ※ 저장(add)과 검색(query)이 같은 기본 함수를 쓰므로 의미공간(차원)은 항상 일치한다.


def get_or_create_collection() -> chromadb.Collection:
    """
    ChromaDB 컬렉션을 가져오거나, 비어있으면 RAG 문서를 로드합니다.
    요리 비유: 레시피 북을 열고, 비어있으면 레시피 카드를 채워넣습니다.
    """
    collection = client.get_or_create_collection(
        name="careerfit_jobs",
        metadata={"description": "CareerFit AI 취업·공모전 데이터"},
        # embedding_function 미지정 → ChromaDB 기본 임베딩(all-MiniLM, 384차원) 사용
    )

    if collection.count() == 0:
        print("⚠️  ChromaDB가 비어있습니다. RAG 문서를 다시 저장합니다...")
        _load_documents(collection)

    return collection


def _load_documents(collection: chromadb.Collection) -> None:
    """rag_documents.json에서 문서를 읽어 ChromaDB에 저장합니다."""
    with open(RAG_JSON, "r", encoding="utf-8") as f:
        documents = json.load(f)

    collection.add(
        documents=[doc["text"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
        ids=[doc["doc_id"] for doc in documents],
    )
    print(f"✅ {collection.count()}개 문서 저장 완료")


def search_documents(
    query: str,
    n_results: int = 3,
    job_type: str = None,
    deadline_month: str = None,
    company_type: str = None,
) -> list:
    """
    사용자 질문과 의미적으로 유사한 문서를 ChromaDB에서 검색합니다.

    검색은 2단계로 동작한다:
      ① (선택) metadata 필터: 조건에 '정확히 일치'하는 공고만 후보로 좁힘
      ② 벡터 유사도: 좁혀진 후보 안에서 질문과 의미가 가까운 순으로 정렬
    → 필터가 없으면(①생략) 전체 문서에서 유사도만으로 검색한다.

    ※ 중요: 필터는 query(자연어)에서 '자동 추출'되지 않는다.
      벡터 검색만 query 텍스트를 쓰고, 아래 필터들은 '별도 인자로 명시'해야 적용된다.
      (예: "9월 마감 스타트업"이라고 물어도 deadline_month/company_type이 저절로 채워지지 않음.
       자연어→필터값 변환은 나중에 LLM이 담당할 별도 단계다.)

    Args:
        query: 사용자 질문 텍스트 (벡터 유사도 검색에만 사용)
        n_results: 반환할 문서 수 (기본값 3)
        job_type: (선택) 직무 분류 정확 일치. 예) "데이터 분석"
        deadline_month: (선택) 마감 연-월 정확 일치. 예) "2026-09"
        company_type: (선택) 기업 유형 정확 일치. 예) "스타트업", "회계법인"
        → 셋 다 None이면 필터 없이 전체에서 검색.

    Returns:
        [{"text": str, "metadata": dict, "distance": float}, ...]
    """
    collection = get_or_create_collection()

    # ── ① metadata 필터 준비 ──
    # 벡터 유사도(의미)만으로는 "정확히 이 조건만" 을 보장하지 못한다.
    # (예: "데이터 분석"과 의미가 가까운 "데이터 엔지니어"도 섞여 나올 수 있음)
    # where 필터를 걸면 조건에 '정확히 일치'하는 문서만 후보로 남긴다. (SQL WHERE 절과 같은 역할)
    #
    # 넘어온 인자들만 골라 조건 목록을 만든다. (None인 인자는 조건에서 제외)
    conditions = []
    if job_type:
        conditions.append({"job_type": job_type})
    if deadline_month:
        conditions.append({"deadline_month": deadline_month})
    if company_type:
        conditions.append({"company_type": company_type})

    # ChromaDB where 조립 규칙:
    #   - 조건 0개 → None (필터 없음, 전체 검색)
    #   - 조건 1개 → 그 조건 딕셔너리 그대로   예) {"job_type": "데이터 분석"}
    #   - 조건 2개+ → 반드시 $and 로 묶어야 함  예) {"$and": [{...}, {...}]}
    #     (여러 조건을 한 딕셔너리에 나열하는 방식은 ChromaDB에서 허용되지 않음)
    if not conditions:
        where_filter = None
    elif len(conditions) == 1:
        where_filter = conditions[0]
    else:
        where_filter = {"$and": conditions}

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
        where=where_filter,  # None이면 필터 없이 전체에서 검색
    )

    return [
        {"text": text, "metadata": metadata, "distance": round(distance, 4)}
        for text, metadata, distance in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        )
    ]
