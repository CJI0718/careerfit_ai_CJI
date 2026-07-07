import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import SourceCard from "./components/SourceCard";
import { analyzeCareer } from "./api";
// ⚠️ API 주소는 api.js의 API_BASE_URL로 관리한다. API Key는 절대 프론트엔드에 넣지 않는다.

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze(formData) {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeCareer({
        major: formData.major,
        skills: formData.skills,
        job_type: formData.jobType,
      });
      setResult(data);

    } catch (err) {
      if (err.message.includes("Failed to fetch")) {
        setError("FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.");
      } else {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-blue-50/40">
      <div className="max-w-2xl mx-auto px-4 py-12">

        {/* 헤더: 그라데이션 아이콘 배지 + 제목 */}
        <header className="mb-8">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white text-xl shadow-lg shadow-blue-500/25">
              <span aria-hidden="true">🎯</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900 leading-none">CareerFit AI</h1>
              <p className="text-slate-500 text-sm mt-1.5">취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치</p>
            </div>
          </div>
        </header>

        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />

        {error && (
          <div className="mt-5 flex items-start gap-2 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
            <span aria-hidden="true">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {isLoading && (
          <div className="mt-8 flex items-center justify-center gap-3 text-slate-500">
            <span className="w-5 h-5 border-2 border-slate-300 border-t-blue-600 rounded-full animate-spin" aria-hidden="true"></span>
            <span className="text-sm">AI가 공고를 분석하고 있습니다...</span>
          </div>
        )}

        {result && (
          <div className="mt-8 space-y-4 animate-fade-in-up">
            <ResultCard answer={result.answer} />
            {result.sources && result.sources.length > 0 && (
              <SourceCard sources={result.sources} />
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
