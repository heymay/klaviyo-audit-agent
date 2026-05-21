"use client";

import type { Recommendation, Timeline } from "@/types/audit";

interface Props {
  recommendations: Recommendation[];
}

const TIMELINE_ORDER: Record<Timeline, number> = {
  Immediate: 0,
  "30 days": 1,
  "60 days": 2,
  "90 days": 3,
};

const TIMELINE_BADGE: Record<Timeline, string> = {
  Immediate: "bg-red-100 text-red-700",
  "30 days": "bg-orange-100 text-orange-700",
  "60 days": "bg-amber-100 text-amber-700",
  "90 days": "bg-blue-100 text-blue-700",
};

const IMPACT_COLOR: Record<string, string> = {
  High: "text-green-700 font-semibold",
  Medium: "text-amber-700 font-semibold",
  Low: "text-gray-500",
};

export default function ActionPlan({ recommendations }: Props) {
  const sorted = [...recommendations].sort(
    (a, b) => TIMELINE_ORDER[a.timeline] - TIMELINE_ORDER[b.timeline]
  );

  const buckets: Record<Timeline, Recommendation[]> = {
    Immediate: [],
    "30 days": [],
    "60 days": [],
    "90 days": [],
  };
  for (const rec of sorted) {
    buckets[rec.timeline].push(rec);
  }

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-np-navy mb-1">
        30 / 60 / 90 Day Action Plan
      </h2>
      <p className="text-sm text-np-gray mb-5">
        {recommendations.length} prioritized recommendations
      </p>
      <div className="space-y-6">
        {(["Immediate", "30 days", "60 days", "90 days"] as Timeline[]).map(
          (bucket) => {
            const recs = buckets[bucket];
            if (!recs.length) return null;
            return (
              <div key={bucket}>
                <div className="flex items-center gap-2 mb-3">
                  <span
                    className={`text-xs font-semibold px-2.5 py-1 rounded-full ${TIMELINE_BADGE[bucket]}`}
                  >
                    {bucket}
                  </span>
                  <span className="text-xs text-np-gray">
                    {recs.length} action{recs.length > 1 ? "s" : ""}
                  </span>
                </div>
                <div className="space-y-3">
                  {recs.map((rec) => (
                    <div
                      key={rec.rec_id}
                      className="border border-gray-100 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <p className="text-sm font-medium text-gray-800">
                          {rec.issue}
                        </p>
                        <span
                          className={`text-xs shrink-0 ${IMPACT_COLOR[rec.expected_impact] ?? "text-gray-500"}`}
                        >
                          {rec.expected_impact} impact
                        </span>
                      </div>
                      {rec.why_it_matters && (
                        <p className="text-xs text-np-gray mt-1">
                          {rec.why_it_matters}
                        </p>
                      )}
                      {rec.next_step && (
                        <div className="mt-2 pt-2 border-t border-gray-50">
                          <p className="text-xs text-gray-700">
                            <span className="font-medium">Next step: </span>
                            {rec.next_step}
                          </p>
                        </div>
                      )}
                      <div className="flex gap-3 mt-2 flex-wrap">
                        <span className="text-xs text-np-gray">
                          Complexity: {rec.complexity}
                        </span>
                        {rec.owner && (
                          <span className="text-xs text-np-gray">
                            Owner: {rec.owner}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          }
        )}
      </div>
    </div>
  );
}
