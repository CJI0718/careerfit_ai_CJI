from fastapi import APIRouter
from typing import List

router = APIRouter()

# 목업 데이터: 3일차에 실제 CSV 데이터로 교체한다
# MOCK_JOBS = [
#     {
#         "id": 1,
#         "company": "테크스타트업A",
#         "title": "데이터 분석가",
#         "required_skills": ["Python", "SQL", "통계"],
#         "preferred_skills": ["R", "Tableau", "머신러닝"],
#         "description": "사용자 행동 데이터를 분석해 비즈니스 인사이트를 도출합니다.",
#         "deadline": "2026-07-31"
#     },

#     {
#         "id": 2,
#         "company": "금융서비스B",
#         "title": "백엔드 개발자",
#         "required_skills": ["Python", "FastAPI", "PostgreSQL"],
#         "preferred_skills": ["Docker", "AWS", "Redis"],
#         "description": "금융 데이터 처리 API 서버를 개발하고 운영합니다.",
#         "deadline": "2026-08-15"
#     },

#     {
#         "id": 3,
#         "company": "공공기관C",
#         "title": "AI 연구원",
#         "required_skills": ["Python", "딥러닝", "PyTorch"],
#         "preferred_skills": ["논문 작성", "NLP", "컴퓨터 비전"],
#         "description": "공공 서비스 개선을 위한 AI 모델을 연구·개발합니다.",
#         "deadline": "2026-08-01"
#     }
# ]

MOCK_JOBS = [
    {
        "id": 1,
        "company": "삼일회계법인",
        "title": "FAS 기업가치평가 어소시에이트",
        "required_skills": ["재무모델링", "IFRS", "회계감사", "Excel"],
        "preferred_skills": ["M&A 실무", "Bloomberg", "VBA"],
        "description": "인수합병(M&A) 거래 지원을 위한 대상 기업의 가치평가 및 재무실사(FDD)를 수행합니다. 공인회계사 실무수습 인정 기관으로, 수습 기간 내 다양한 산업군의 딜 경험을 쌓을 수 있습니다.",
        "deadline": "2026-08-31",
    },
    {
        "id": 2,
        "company": "LG에너지솔루션",
        "title": "재무회계 담당 (배터리 사업부)",
        "required_skills": ["IFRS", "원가회계", "SAP ERP", "재무제표 분석"],
        "preferred_skills": ["연결재무제표", "Power BI", "세무신고"],
        "description": "배터리 사업부의 월 결산, 원가 분석, 외부감사 대응 업무를 담당합니다. 제조업 인더스트리 회계 경험을 통해 사기업 재무 커리어의 기반을 마련할 수 있습니다.",
        "deadline": "2026-08-31",
    },
    {
        "id": 3,
        "company": "IBK기업은행",
        "title": "재무기획 및 내부회계관리 담당",
        "required_skills": ["공공회계기준", "재무제표 분석", "내부통제", "Excel"],
        "preferred_skills": ["예산관리", "세무조정", "K-IFRS"],
        "description": "은행 본점 재무기획 부서에서 재무 보고서 작성, 내부회계관리제도 운영, 예산 편성 업무를 수행합니다. 금융기관 실무수습 인정 기관으로, 금융·공공 트랙 커리어를 원하는 합격자에게 적합합니다.",
        "deadline": "2026-08-31",
    },
]


@router.get("/jobs", tags=["Jobs"])
def get_jobs():
    """
    취업 공고 목록을 반환하는 엔드포인트.
    현재는 목업 데이터를 반환하며, 3일차에 실제 데이터로 교체한다.
    """

    return {"count": len(MOCK_JOBS), "jobs": MOCK_JOBS}


@router.get("/jobs/{job_id}", tags=["Jobs"])
def get_job_by_id(job_id: int):
    """
    특정 공고의 상세 정보를 반환한다.
    """

    for job in MOCK_JOBS:
        if job["id"] == job_id:
            return job

    # 찾지 못한 경우
    from fastapi import HTTPException

    raise HTTPException(status_code=404, detail=f"공고 ID {job_id}를 찾을 수 없습니다.")
