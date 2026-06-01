"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { pollStatus } from "@/lib/api";
import type { AuditStatus } from "@/types/audit";

const STEPS = [
  { min: 0,  max: 7,  label: "Connecting to Klaviyo…" },
  { min: 8,  max: 14, label: "Validating API key & reading account info…" },
  { min: 15, max: 21, label: "Pulling profile & list data…" },
  { min: 22, max: 34, label: "Pulling campaigns & analysing segmentation…" },
  { min: 35, max: 47, label: "Pulling campaign performance metrics…" },
  { min: 48, max: 57, label: "Pulling flows & flow messages…" },
  { min: 58, max: 64, label: "Pulling signup forms…" },
  { min: 65, max: 71, label: "Checking deliverability signals (SPF / DKIM / DMARC)…" },
  { min: 72, max: 77, label: "Normalising account data…" },
  { min: 78, max: 83, label: "Scoring 10 audit categories…" },
  { min: 84, max: 90, label: "Running 125+ decision rules…" },
  { min: 91, max: 95, label: "Evaluating findings & building recommendations…" },
  { min: 96, max: 99, label: "Calculating revenue opportunity & finalising report…" },
];

function stepIndex(pct: number): number {
  const idx = STEPS.findIndex(s => pct >= s.min && pct <= s.max);
  return idx >= 0 ? idx + 1 : pct >= 100 ? STEPS.length : 1;
}

export default function ProgressPoller({ auditId }: { auditId: string }) {
  const router = useRouter();
  const [status, setStatus] = useState<AuditStatus | null>(null);
  const [displayPct, setDisplayPct] = useState(0);
  const targetPctRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Smoothly animate progress toward target
  useEffect(() => {
    function tick() {
      setDisplayPct(prev => {
        const target = targetPctRef.current;
        if (Math.abs(prev - target) < 0.5) return target;
        return prev + (target - prev) * 0.1;
      });
      timerRef.current = setTimeout(tick, 50);
    }
    timerRef.current = setTimeout(tick, 50);
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, []);

  // Poll every 2.5 s
  useEffect(() => {
    let cancelled = false;

    async function poll() {
      try {
        const data = await pollStatus(auditId);
        if (cancelled) return;
        setStatus(data);
        if (data.progress != null) targetPctRef.current = data.progress;

        if (data.status === "complete") {
          targetPctRef.current = 100;
          setTimeout(() => router.refresh(), 800);
          return;
        }
        if (data.status === "error") return;
      } catch {
        // keep polling on transient errors
      }
      if (!cancelled) setTimeout(poll, 2500);
    }

    poll();
    return () => { cancelled = true; };
  }, [auditId, router]);

  const pct = Math.min(99, Math.round(displayPct));
  const serverPct = status?.progress ?? 0;
  const stepNum = stepIndex(serverPct);
  const circumference = 2 * Math.PI * 52;

  if (status?.status === "error") {
    return (
      <div className="max-w-xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="text-5xl">⚠️</div>
        <h1 className="text-2xl font-bold text-np-navy">Audit Failed</h1>
        <p className="text-np-gray">{status.error ?? "Unknown error"}</p>
        <a href="/" className="btn-primary inline-block mt-2">Try Again</a>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-16 text-center space-y-7">

      {/* Ring gauge with % and step counter */}
      <div className="relative inline-flex items-center justify-center">
        <svg className="w-40 h-40 -rotate-90" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r="52" fill="none" stroke="#E8ECF4" strokeWidth="9" />
          <circle
            cx="60" cy="60" r="52"
            fill="none"
            stroke="#1B2D50"
            strokeWidth="9"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * (1 - pct / 100)}
            style={{ transition: "stroke-dashoffset 0.15s ease-out" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold text-np-navy leading-none">{pct}%</span>
          <span className="text-[11px] text-np-gray mt-1">
            Step {stepNum} / {STEPS.length}
          </span>
        </div>
      </div>

      {/* Heading */}
      <div>
        <h1 className="text-2xl font-bold text-np-navy mb-1">Running Your Audit</h1>
        <p className="text-np-gray text-sm">
          {status?.business_name
            ? `Analysing ${status.business_name}`
            : "Analysing your Klaviyo account…"}
        </p>
      </div>

      {/* Linear progress bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <div
          className="h-2 rounded-full bg-np-navy"
          style={{ width: `${pct}%`, transition: "width 0.15s ease-out" }}
        />
      </div>

      {/* Step-by-step checklist */}
      <div className="card text-left space-y-2.5 py-5">
        {STEPS.map((s, i) => {
          const done   = serverPct > s.max;
          const active = serverPct >= s.min && serverPct <= s.max;
          return (
            <div
              key={i}
              className={`flex items-center gap-3 text-sm transition-all duration-300 ${
                done ? "opacity-40" : active ? "opacity-100" : "opacity-20"
              }`}
            >
              <span className="shrink-0 w-5 text-center">
                {done
                  ? <span className="text-green-500 font-bold text-base">✓</span>
                  : active
                    ? <span className="inline-block w-2.5 h-2.5 rounded-full bg-np-navy animate-pulse" />
                    : <span className="inline-block w-2.5 h-2.5 rounded-full border border-gray-300" />
                }
              </span>
              <span className={active ? "font-semibold text-np-navy" : "text-np-gray"}>
                {s.label}
              </span>
            </div>
          );
        })}
      </div>

      <p className="text-xs text-np-gray pb-4">
        Typical audits complete in 60–120 seconds depending on account size.
      </p>
    </div>
  );
}
