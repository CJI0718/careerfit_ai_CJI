import { useState } from "react";

function InputForm({ onSubmit, isLoading }) {
  const [major, setMajor] = useState("");
  const [skillsInput, setSkillsInput] = useState("");
  const [jobType, setJobType] = useState("");

  function handleSubmit() {
    const skills = skillsInput.split(",").map(s => s.trim()).filter(Boolean);
    onSubmit({ major, skills, jobType });
  }

  const inputClass =
    "w-full border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 placeholder-slate-400 transition focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500";
  const disabled = isLoading || !major || !skillsInput || !jobType;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200/70 p-6 sm:p-7">
      <h2 className="text-base font-semibold text-slate-800 mb-5">내 정보 입력</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1.5">전공</label>
          <input type="text" value={major} onChange={e => setMajor(e.target.value)}
            placeholder="예: 통계학과" className={inputClass} />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1.5">
            보유 스킬 <span className="text-slate-400 font-normal">(쉼표로 구분)</span>
          </label>
          <input type="text" value={skillsInput} onChange={e => setSkillsInput(e.target.value)}
            placeholder="예: Python, SQL, R" className={inputClass} />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-600 mb-1.5">관심 직무</label>
          <input type="text" value={jobType} onChange={e => setJobType(e.target.value)}
            placeholder="예: 데이터 분석" className={inputClass} />
        </div>
        <button onClick={handleSubmit} disabled={disabled}
          className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:from-slate-300 disabled:to-slate-300 disabled:cursor-not-allowed text-white font-medium py-2.5 px-4 rounded-lg shadow-sm shadow-blue-500/20 transition text-sm">
          {isLoading ? (
            <>
              <span className="w-4 h-4 border-2 border-white/50 border-t-white rounded-full animate-spin" aria-hidden="true"></span>
              분석 중...
            </>
          ) : "역량 분석 요청"}
        </button>
      </div>
    </div>
  );
}

export default InputForm;
