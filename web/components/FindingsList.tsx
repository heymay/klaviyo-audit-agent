"use client";

import type { Finding, Severity } from "@/types/audit";

interface Props {
  findings: Finding[];
}

const BADGE: Record<Severity, string> = {
  Critical: "badge-critical",
  High: "badge-high",
  Medium: "badge-medium",
  Low: "badge-low",
};

const ORDER: Record<Severity, number> = {
  Critical: 0,
  High: 1,
  Medium: 2,
  Low: 3,
};

export default function FindingsList({ findings }: Props) {
  const sorted = [...findings].sort(
    (a, b) => ORDER[a.severity] - ORDER[b.severity]
  );

  const critical = sorted.filter((f) => f.severity === "Critical");
  const rest = sorted.filter((f) => f.severity !== "Critical");

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-np-navy mb-4">
        Findings ({findings.length})
      </h2>
      <div className="space-y-3">
        {[...critical, ...rest].map((f) => (
          <div
            key={f.rule_id}
            className="border border-gray-100 rounded-lg p-4 hover:shadow-sm transition-shadow"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <span className={BADGE[f.severity]}>{f.severity}</span>
                  <span className="text-xs text-np-gray">{f.category}</span>
                </div>
                <p className="text-sm font-medium text-gray-800">
                  {f.description}
                </p>
                {f.business_impact && (
                  <p className="text-xs text-np-gray mt-1">
                    {f.business_impact}
                  </p>
                )}
              </div>
              <span className="text-xs text-np-gray shrink-0 font-mono">
                {f.rule_id}
              </span>
            </div>
            {f.recommended_action && (
              <div className="mt-3 pt-3 border-t border-gray-50">
                <p className="text-xs font-medium text-gray-600">
                  Recommended Action
                </p>
                <p className="text-xs text-gray-700 mt-0.5">
                  {f.recommended_action}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
