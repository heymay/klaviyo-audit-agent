"use client";

export default function PrintButton() {
  return (
    <button
      onClick={() => window.print()}
      className="flex items-center gap-2 text-sm text-np-gray hover:text-np-navy border border-gray-300 hover:border-np-navy rounded-lg px-4 py-2 transition-colors"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a1 1 0 001-1v-5a1 1 0 00-1-1H9a1 1 0 00-1 1v5a1 1 0 001 1zm1-12V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3" />
      </svg>
      Export PDF
    </button>
  );
}
