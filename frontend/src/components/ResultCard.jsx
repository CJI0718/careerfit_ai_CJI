function ResultCard({ answer }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200/70 overflow-hidden">
      <div className="flex items-center gap-2.5 px-6 sm:px-7 py-4 border-b border-slate-100 bg-gradient-to-r from-emerald-50 to-transparent">
        <span className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-white text-sm shadow-sm shadow-emerald-500/30" aria-hidden="true">📊</span>
        <h2 className="text-base font-semibold text-slate-800">AI 분석 결과</h2>
      </div>
      <p className="px-6 sm:px-7 py-5 text-slate-700 text-[15px] leading-7 whitespace-pre-line">{answer}</p>
    </div>
  );
}
export default ResultCard;
