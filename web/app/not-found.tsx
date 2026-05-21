import Link from "next/link";

export default function NotFound() {
  return (
    <div className="max-w-xl mx-auto px-4 py-32 text-center space-y-5">
      <div className="text-6xl font-black text-np-navy opacity-10">404</div>
      <h1 className="text-2xl font-bold text-np-navy">Audit not found</h1>
      <p className="text-np-gray">
        This audit link may have expired or the ID is invalid.
      </p>
      <Link href="/" className="btn-primary inline-block mt-2">
        Run a New Audit →
      </Link>
    </div>
  );
}
