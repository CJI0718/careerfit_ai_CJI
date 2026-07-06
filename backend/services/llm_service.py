import os
import requests
from dotenv import load_dotenv


# =========================
# 1. 환경변수 로드
# =========================

# .env 파일을 읽습니다.
# [요리] 비유: 비법 소스 보관함을 여는 단계입니다.
load_dotenv()

# MOCK_MODE=true이면 실제 LLM API를 호출하지 않습니다.
# [요리] 비유: 진짜 셰프를 부르지 않고 시식용 샘플 응답만 내는 상태입니다.
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# .env에서 사용할 모델명을 읽습니다.
# 예:
# - gemini-2.5-flash-lite
# - gemini-2.5-flash
# - mistral-small-latest
# - ollama:llama3.2:3b
# - huggingface:Qwen/Qwen2.5-0.5B-Instruct
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")

# provider별 API Key를 읽습니다.
# [요리] 비유: 셰프별 출입증입니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Ollama는 로컬 서버 주소를 사용합니다.
# 기본 주소는 http://localhost:11434 입니다.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


# =========================
# 2. LLM_MODEL → provider/model 분리
# =========================

def get_provider_and_model(model_name: str) -> tuple[str, str]:
    """
    LLM_MODEL 값을 보고 어떤 LLM provider를 사용할지 결정합니다.

    [요리] 비유:
    주문서에 적힌 셰프 이름을 보고
    Gemini 셰프, Mistral 셰프, Ollama 로컬 셰프, HuggingFace 셰프 중
    누구에게 보낼지 정합니다.
    """

    # 예: ollama:llama3.2:3b
    # provider = ollama
    # model = llama3.2:3b
    if model_name.startswith("ollama:"):
        return "ollama", model_name.replace("ollama:", "", 1)

    # 예: huggingface:Qwen/Qwen2.5-0.5B-Instruct
    # provider = huggingface
    # model = Qwen/Qwen2.5-0.5B-Instruct
    if model_name.startswith("huggingface:"):
        return "huggingface", model_name.replace("huggingface:", "", 1)

    # 예: mistral-small-latest
    if model_name.startswith("mistral"):
        return "mistral", model_name

    # 그 외는 Gemini로 처리합니다.
    # 예: gemini-2.5-flash-lite
    return "gemini", model_name


# 앱 실행 시점에 provider와 실제 모델명을 계산합니다.
PROVIDER, PROVIDER_MODEL = get_provider_and_model(LLM_MODEL)


# =========================
# 3. RAG 프롬프트 생성
# =========================

def build_rag_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문 + RAG 검색 문서 → LLM 프롬프트 구성

    [요리] 비유:
    query는 손님의 주문,
    context_docs는 레시피 카드,
    prompt는 셰프에게 전달하는 최종 주문서입니다.
    """

    if context_docs:
        context_text = "\n".join([
            f"""
[공고 {i + 1}]
{doc.get("text", "")}

출처: {doc.get("metadata", {}).get("company", "")} — {doc.get("metadata", {}).get("title", "")}
필요 역량: {doc.get("metadata", {}).get("required_skills", "")}
유사도 거리: {doc.get("distance", "")}
""".strip()
            for i, doc in enumerate(context_docs)
        ])

        context_section = f"""
[참고 데이터 — 실제 취업·공모전 공고]
{context_text}

위 데이터를 반드시 근거로 사용해 답변하세요.
답변에서 어떤 공고를 참고했는지 명시하세요.
검색된 데이터에 없는 회사명, 조건, 공모전 정보는 지어내지 마세요.
"""
    else:
        context_section = """
[참고 데이터 없음]
제공된 자료만으로는 판단하기 어렵습니다.
일반적인 커리어 조언만 간단히 제공하세요.
"""

    return f"""당신은 취업·공모전 전문 커리어 코치입니다.
다음 지원자 정보와 참고 데이터를 바탕으로 맞춤형 조언을 한국어로 제공하세요.

[지원자 정보]
{query}

{context_section}

[답변 형식]
1. 현재 역량 평가 (2문장 이내)
2. 추천 공고 또는 공모전 (1~2개, 이유 포함)
3. 부족한 역량 및 준비 방향 (3가지 이내)

[중요 규칙]
- 반드시 한국어로 답변하세요.
- 참고 데이터가 있으면 반드시 그 데이터를 근거로 답변하세요.
- 참고 데이터가 부족하면 "제공된 자료만으로는 판단하기 어렵습니다"라고 말하세요.
- 간결하고 실용적으로 작성하세요.
""".strip()


# =========================
# 4. sources 응답 생성
# =========================

def build_sources(context_docs: list) -> list:
    """
    RAG 검색 문서를 API 응답용 sources 형식으로 변환합니다.

    [요리] 비유:
    어떤 레시피 카드를 참고했는지 영수증처럼 정리하는 단계입니다.
    """

    sources = []

    for doc in context_docs:
        metadata = doc.get("metadata", {})

        sources.append({
            "company": metadata.get("company", ""),
            "title": metadata.get("title", ""),
            "required_skills": metadata.get("required_skills", ""),
            "job_type": metadata.get("job_type", ""),
            "distance": doc.get("distance", 0),
        })

    return sources


# =========================
# 5. provider별 실제 API 호출
# =========================

def _call_gemini(prompt: str) -> str:
    """
    Gemini API 호출 (google-generativeai SDK).
    [요리] 비유: Gemini 셰프에게 주문서를 넘기고 요리를 받아옵니다.
    """
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(PROVIDER_MODEL)  # 예: gemini-2.5-flash-lite
    response = model.generate_content(prompt)
    return response.text


def _call_mistral(prompt: str) -> str:
    """
    Mistral API 호출 (REST chat/completions 엔드포인트를 requests로 호출).
    Gemini와 달리 전용 SDK 없이 HTTP로 직접 부른다.
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",  # 셰프 출입증
        "Content-Type": "application/json",
    }
    payload = {
        "model": PROVIDER_MODEL,  # 예: mistral-small-latest
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()  # 4xx/5xx면 예외 발생 → 아래 get_llm_response에서 처리
    data = resp.json()
    # OpenAI 호환 응답 형식: choices[0].message.content
    return data["choices"][0]["message"]["content"]


# =========================
# 6. 메인 진입 함수 (analyze.py가 호출)
# =========================

def get_llm_response(query: str, context_docs: list) -> dict:
    """
    RAG 검색 문서와 함께 LLM 응답을 생성합니다.

    .env의 LLM_MODEL로 결정된 PROVIDER에 따라 Gemini/Mistral을 분기 호출합니다.
    [요리] 비유: 주문서(prompt)를 만들고, 이름표에 적힌 셰프에게 전달해 요리를 받아옵니다.

    Returns:
        {"answer": str, "sources": list}
    """
    # sources는 어느 provider든 동일하게 RAG 검색 결과에서 만든다 (모델과 무관).
    sources = build_sources(context_docs)

    # MOCK 모드: 실제 API 호출 없이 테스트용 응답 (어떤 provider로 갈지도 함께 표시)
    if MOCK_MODE:
        return {
            "answer": (
                f"[MOCK 응답] provider={PROVIDER}, model={PROVIDER_MODEL}, "
                f"참고 문서 {len(context_docs)}개. MOCK_MODE=false로 실제 응답을 받습니다."
            ),
            "sources": sources,
        }

    prompt = build_rag_prompt(query, context_docs)

    try:
        # PROVIDER 이름표를 보고 실제 셰프에게 전달 (get_provider_and_model 결과)
        if PROVIDER == "gemini":
            if not GEMINI_API_KEY:
                return {"answer": "[설정 오류] GEMINI_API_KEY가 없습니다. .env를 확인하세요.", "sources": []}
            answer = _call_gemini(prompt)

        elif PROVIDER == "mistral":
            if not MISTRAL_API_KEY:
                return {"answer": "[설정 오류] MISTRAL_API_KEY가 없습니다. .env를 확인하세요.", "sources": []}
            answer = _call_mistral(prompt)

        else:
            # ollama / huggingface 는 아직 미구현 (자리만 표시 — 한 번에 다 만들지 않음)
            return {
                "answer": f"[미구현] provider '{PROVIDER}'는 아직 연결되지 않았습니다. 현재는 gemini/mistral만 지원합니다.",
                "sources": [],
            }

        return {"answer": answer, "sources": sources}

    except Exception as e:
        error_msg = str(e)
        # 한도 초과 안내 (Gemini 429 / Mistral rate limit)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "rate limit" in error_msg.lower():
            return {"answer": "[API 한도 초과] 잠시 후 다시 시도하거나 MOCK_MODE=true 로 전환하세요.", "sources": []}
        return {"answer": f"[오류] {PROVIDER} 호출 실패: {error_msg}", "sources": []}