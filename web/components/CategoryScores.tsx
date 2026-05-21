"use client";

import type { CategoryScore } from "@/types/audit";

interface Props {
  categories: CategoryScore[];
}

function scoreColor(score: number) {
  if (score >= 8) return "bg-green-500";
  if (score >= 6) return "bg-blue-500";
  if (score >= 4) return "bg-amber-500";
  if (score >= 2) return "bg-orange-500";
  return "bg-red-500";
}

function scoreLabel(score: number) {
  if (score >= 8) return "text-green-700";
  if (score >= 6) return "text-blue-700";
  if (score >= 4) return "text-amber-700";
  if (score >= 2) return "text-orange-700";
  return "text-red-700";
}

export default function CategoryScores({ categories }: Props) {
  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-np-navy mb-4">
        Score Breakdown
      </h2>
      <div className="space-y-4">
        {categories.map((cat) => (
          <div key={cat.name}>
            <div className="flex justify-between items-baseline mb-1">
              <span className="text-sm font-medium text-gray-700">
                {cat.name}
              </span>
              <div className="flex items-baseline gap-2">
                <span
                  className={`text-sm font-bold ${scoreLabel(cat.score)}`}
                >
                  {cat.score}/10
                </span>
                <span className="text-xs text-np-gray">
                  {cat.weight * 100}% weight
                </span>
              </div>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${scoreColor(cat.score)}`}
                style={{ width: `${cat.score * 10}%` }}
              />
            </div>
            {cat.justification && (
              <p className="text-xs text-np-gray mt-1">{cat.justification}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
