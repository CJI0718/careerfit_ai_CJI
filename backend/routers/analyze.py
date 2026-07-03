from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.llm_service import get_llm_response

router = APIRouter()


class AnalyzeRequest(BaseModel):
    major: str  # 예: "세무학과"
    skills: list[str]  # 예: ["KICPA", "AI", "데이터 분석"]
    job_type: str  # 예: "공인회계사"
    experience_years: int = 0  # 0이면 신입
    preferred_company_size: str = "무관"  # 무관 / 대기업 / 중견기업 / 스타트업


class AnalyzeResponse(BaseModel):
    answer: str
    sources: list[dict]


@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])
def analyze_career(request: AnalyzeRequest):
    # 사용자 질문 구성
    query = (
        f"전공: {request.major}, "
        f"보유 스킬: {', '.join(request.skills)}, "
        f"관심 직무: {request.job_type}"
    )

    # llm_service 호출 (실습 8에서 Gemini + RAG로 교체)
    result = get_llm_response(query=query, context_docs=[])

    return AnalyzeResponse(
        answer=result["answer"],
        sources=result["sources"]
    )
