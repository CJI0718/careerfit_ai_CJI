function SourceCard({ sources }) {
  if (!sources || sources.length === 0) {
    return (
      <div className="bg-slate-50 rounded-2xl border border-slate-200 p-5 text-sm text-slate-600">
        참고한 공고 데이터가 없습니다.
      </div>
    );
  }
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200/70 overflow-hidden">
      <div className="flex items-center gap-2.5 px-6 sm:px-7 py-4 border-b border-slate-100">
        <span className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white text-sm shadow-sm shadow-blue-500/30" aria-hidden="true">📄</span>
        <h2 className="text-base font-semibold text-slate-800">참고한 공고 출처</h2>
        <span className="ml-auto text-xs font-medium text-slate-400">{sources.length}건</span>
      </div>
      <ul className="divide-y divide-slate-100">
        {sources.map((source) => (
          <li key={`${source.company}-${source.title}`} className="px-6 sm:px-7 py-3.5 transition hover:bg-slate-50/70">
            <p className="text-sm font-medium text-slate-800">
              {source.company} <span className="text-slate-400">—</span> {source.title}
            </p>
            <p className="text-xs text-slate-500 mt-1">필수 스킬: {source.required_skills || "정보 없음"}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default SourceCard;
