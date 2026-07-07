// 공통 API 설정
// 모든 백엔드 호출은 이 파일의 API_BASE_URL을 기준으로 한다.
// - 로컬: 기본값 http://localhost:8000
// - 배포: 빌드 시 VITE_API_BASE_URL(예: Render 백엔드 URL)을 주입
//   ※ Vite는 VITE_ 접두 변수를 "빌드 시점"에 정적으로 넣는다(런타임 주입 아님).
//     따라서 값을 바꾸면 반드시 다시 빌드해야 반영된다.
// 끝의 슬래시(/)는 제거해 `${API_BASE_URL}/analyze`가 이중 슬래시로 깨지지 않게 한다.
export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/$/, "");

// 서버 상태 확인 (GET /health)
export async function checkHealth() {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) throw new Error(`서버 오류: ${res.status}`);
  return res.json();
}

// 채용공고 목록 (GET /jobs)
export async function getJobs() {
  const res = await fetch(`${API_BASE_URL}/jobs`);
  if (!res.ok) throw new Error(`서버 오류: ${res.status}`);
  return res.json();
}

// 역량 분석 (POST /analyze)
// 응답 스키마({answer, sources})는 백엔드 계약이므로 그대로 반환한다.
export async function analyzeCareer(payload) {
  const res = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`서버 오류: ${res.status}`);
  return res.json();
}
