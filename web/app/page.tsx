import AuditForm from "@/components/AuditForm";
import Image from "next/image";

export default function HomePage() {
  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-12">
      {/* Hero */}
      <div className="text-center mb-10">
        {/* NP logo */}
        <div className="flex items-center justify-center mb-8">
          <Image src="/logo.png" alt="National Positions" width={160} height={48} className="object-contain" />
        </div>

        {/* Divider */}
        <div className="flex items-center gap-3 mb-8">
          <div className="flex-1 h-px bg-gray-200" />
          <span className="inline-flex items-center gap-2 bg-np-navy text-white text-xs font-semibold px-3 py-1.5 rounded-full">
            <span className="w-1.5 h-1.5 bg-np-red rounded-full animate-pulse" />
            Free AI-Powered Klaviyo Audit
          </span>
          <div className="flex-1 h-px bg-gray-200" />
        </div>

        <h1 className="text-4xl font-bold text-np-navy mb-3">
          How healthy is your<br />
          <span className="text-np-red">Klaviyo</span> account?
        </h1>
        <p className="text-np-gray text-lg">
          Connect your account and get a scored audit — deliverability,
          flows, campaigns, SMS, segmentation, and more — in under 2 minutes.
        </p>
      </div>

      <AuditForm />

      {/* Stats */}
      <div className="mt-10 grid grid-cols-3 gap-4 text-center">
        {[
          { label: "Categories Audited", value: "10" },
          { label: "Decision Rules", value: "125+" },
          { label: "Read-Only Access", value: "Always" },
        ].map(({ label, value }) => (
          <div key={label} className="card">
            <div className="text-2xl font-bold text-np-navy">{value}</div>
            <div className="text-xs text-np-gray mt-1">{label}</div>
          </div>
        ))}
      </div>

      <p className="text-center text-xs text-np-gray mt-8">
        Your API key is used only to pull read-only account data and is never
        stored. All findings are diagnostic estimates.
      </p>
    </div>
  );
}
