from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AnalyzeRequest(BaseModel):
    major: str          # 예: "세무학과"
    skills: list[str]   # 예: ["Excel", "회계감사"]
    job_type: str       # 예: "공인회계사"
    experience_years: int = 0           # 0이면 신입
    preferred_company_size: str = "무관"  # 무관 / 대기업 / 중견기업 / 스타트업

class AnalyzeResponse(BaseModel):
    answer: str
    sources: list[dict]

@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])
def analyze_career(request: AnalyzeRequest):
    """
    사용자의 전공·스킬·관심 직무를 기반으로 취업·공모전 맞춤 분석을 제공한다.
    현재는 목업 응답을 반환하며, 실습 8에서 Gemini API와 연결한다.
    """
    mock_answer = (
        f"{request.major} 학생으로서 {request.job_type} 직무에 지원하려면, "
        f"현재 보유하신 {', '.join(request.skills)} 역량을 바탕으로 "
        f"다음과 같은 준비를 추천드립니다. (목업 응답 — 실습 8에서 Gemini로 교체)"
    )

    mock_sources = [{"title": "목업 데이터 — 삼일회계법인 FAS", "content": "요구 스킬: 재무모델링, IFRS, 회계감사"}]

    return AnalyzeResponse(answer=mock_answer, sources=mock_sources)
