"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { pollStatus } from "@/lib/api";

const MESSAGES: Record<string, string> = {
  pending: "Connecting to Klaviyo…",
  running: "Analyzing your account data…",
};

interface Props {
  auditId: string;
}

export default function ProgressPoller({ auditId }: Props) {
  const router = useRouter();
  const [status, setStatus] = useState("pending");
  const [error, setError] = useState("");
  const [dots, setDots] = useState(".");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((d) => (d.length >= 3 ? "." : d + "."));
    }, 500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let stopped = false;

    async function poll() {
      while (!stopped) {
        try {
          const data = await pollStatus(auditId);
          setStatus(data.status);
          if (data.status === "complete") {
            router.refresh();
            return;
          }
          if (data.status === "error") {
            setError(data.error ?? "Audit failed. Please try again.");
            return;
          }
        } catch {
          // transient error — keep polling
        }
        await new Promise((r) => setTimeout(r, 2500));
      }
    }

    poll();
    return () => {
      stopped = true;
    };
  }, [auditId, router]);

  if (error) {
    return (
      <div className="max-w-xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="text-5xl">⚠️</div>
        <h1 className="text-2xl font-bold text-np-navy">Audit Failed</h1>
        <p className="text-np-gray">{error}</p>
        <a href="/" className="btn-primary inline-block mt-2">
          Try Again
        </a>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-24 text-center space-y-6">
      <div className="relative w-20 h-20 mx-auto">
        <div className="absolute inset-0 border-4 border-np-navy/20 rounded-full" />
        <div className="absolute inset-0 border-4 border-np-navy rounded-full border-t-transparent animate-spin" />
      </div>
      <div>
        <h1 className="text-2xl font-bold text-np-navy mb-2">
          Running Your Audit
        </h1>
        <p className="text-np-gray">
          {MESSAGES[status] ?? "Processing…"}
          {dots}
        </p>
      </div>
      <div className="card max-w-sm mx-auto text-left space-y-2 text-sm text-np-gray">
        {[
          "Pulling account & profile data",
          "Analyzing flows and campaigns",
          "Checking deliverability signals",
          "Running 125+ decision rules",
          "Generating recommendations",
        ].map((step, i) => (
          <div key={i} className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-np-navy rounded-full shrink-0" />
            {step}
          </div>
        ))}
      </div>
    </div>
  );
}
