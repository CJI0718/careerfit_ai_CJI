import chromadb
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAG_JSON = os.path.join(BASE_DIR, "rag_documents.json")
CHROMA_PATH = os.path.join(os.path.dirname(BASE_DIR), "chroma_db")

# 임베딩은 ChromaDB 기본 모델(all-MiniLM-L6-v2, 384차원)을 쓴다.
# torch가 필요 없어(onnxruntime 기반) 가볍고 배포에 유리하다.
# 단, 영어 위주라 한국어 검색 품질은 낮다. (배포 우선 절충 — rag_service.py와 동일 방침)
# ※ 저장(add)과 검색(query)이 같은 기본 함수를 쓰므로 의미공간(차원)은 항상 일치한다.


def load_rag_documents(json_path: str) -> list:
    """저장된 RAG 문서 JSON을 불러옵니다."""
    with open(json_path, "r", encoding="utf-8") as f:
        documents = json.load(f)
    print(f"✅ RAG 문서 {len(documents)}개 로드됨")
    return documents


def save_to_chromadb(documents: list, chroma_path: str) -> chromadb.Collection:
    """
    RAG 문서를 ChromaDB에 저장합니다.

    요리 비유:
    레시피 카드를 레시피 북(ChromaDB)에 정리해서 꽂아놓는 단계입니다.
    """
    print(f"\n=== ChromaDB 저장 ===")

    # PersistentClient: 데이터를 디스크에 영구 저장합니다
    # chroma_path 폴더에 자동으로 DB 파일이 생성됩니다
    client = chromadb.PersistentClient(path=chroma_path)

    # 임베딩을 바꾸면 벡터 차원이 달라져 기존 벡터와 섞을 수 없다.
    # → 기존 컬렉션을 통째로 삭제하고 새로 만든다.
    try:
        client.delete_collection(name="careerfit_jobs")
        print("   기존 컬렉션 발견 → 삭제 후 재생성합니다")
    except Exception:
        pass  # 최초 실행: 삭제할 컬렉션이 없음

    # embedding_function 미지정 → ChromaDB 기본 임베딩(all-MiniLM, 384차원) 사용
    # → 이후 add/query 모두 같은 기본 함수로 벡터를 만든다 (의미공간 일치 보장)
    collection = client.create_collection(
        name="careerfit_jobs",
        metadata={"description": "CareerFit AI 취업·공모전 데이터"},
    )

    # 문서 저장 (배치 처리)
    texts = [doc["text"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    ids = [doc["doc_id"] for doc in documents]

    collection.add(documents=texts, metadatas=metadatas, ids=ids)

    print(f"   ✅ {collection.count()}개 문서 저장 완료")
    print(f"   저장 위치: {chroma_path}")
    return collection


def test_search(collection: chromadb.Collection) -> None:
    """
    저장된 문서로 질문 기반 검색을 테스트합니다.

    요리 비유:
    레시피 북에 "오늘 닭고기에 어울리는 요리"를 검색하는 단계입니다.
    """
    print("\n=== ChromaDB 검색 테스트 ===")

    test_queries = [
        "데이터 분석 직무에 Python이 필요한 공고",
        "통계학과 학생에게 적합한 취업 공고",
        "프론트엔드 개발자 채용 공고",
        "마감일이 임박한 공고",
        "인공지능 관련 직무",
        "회계 및 재무 관련 직무",
    ]

    for query in test_queries:
        print(f"\n  질문: '{query}'")
        results = collection.query(
            query_texts=[query],
            n_results=2,  # 가장 유사한 문서 2개 반환
        )

        for i, (doc, meta) in enumerate(
            zip(results["documents"][0], results["metadatas"][0])
        ):
            print(f"  결과 {i + 1}:")
            print(
                f"    회사: {meta.get('company', '?')} | 직무: {meta.get('title', '?')}"
            )
            print(f"    거리: {results['distances'][0][i]:.4f}")
            # 거리가 낮을수록 질문과 더 유사합니다
            print(f"    문서: {doc[:80]}...")


if __name__ == "__main__":
    documents = load_rag_documents(RAG_JSON)
    collection = save_to_chromadb(documents, CHROMA_PATH)
    test_search(collection)
    print("\n✅ ChromaDB 저장 및 검색 테스트 완료")
