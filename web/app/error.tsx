"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="max-w-xl mx-auto px-4 py-32 text-center space-y-5">
      <div className="text-5xl">⚠️</div>
      <h1 className="text-2xl font-bold text-np-navy">Something went wrong</h1>
      <p className="text-np-gray text-sm">{error.message}</p>
      <button onClick={reset} className="btn-primary mt-2">
        Try Again
      </button>
    </div>
  );
}
