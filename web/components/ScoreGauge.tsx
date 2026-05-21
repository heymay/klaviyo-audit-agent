"use client";

import type { ScoreBand } from "@/types/audit";

const BAND_COLORS: Record<ScoreBand, string> = {
  Elite: "#16a34a",
  Strong: "#2563eb",
  Average: "#d97706",
  Weak: "#ea580c",
  Critical: "#dc2626",
};

const BAND_BG: Record<ScoreBand, string> = {
  Elite: "bg-green-50 text-green-800 border-green-200",
  Strong: "bg-blue-50 text-blue-800 border-blue-200",
  Average: "bg-amber-50 text-amber-800 border-amber-200",
  Weak: "bg-orange-50 text-orange-800 border-orange-200",
  Critical: "bg-red-50 text-red-800 border-red-200",
};

interface Props {
  score: number;
  band: ScoreBand;
}

export default function ScoreGauge({ score, band }: Props) {
  const r = 80;
  const cx = 100;
  const cy = 100;
  const startAngle = -210;
  const endAngle = 30;
  const totalDeg = endAngle - startAngle; // 240°
  const scoreDeg = (score / 100) * totalDeg;

  function polarToXY(deg: number) {
    const rad = ((deg - 90) * Math.PI) / 180;
    return {
      x: cx + r * Math.cos(rad),
      y: cy + r * Math.sin(rad),
    };
  }

  const start = polarToXY(startAngle);
  const trackEnd = polarToXY(endAngle);
  const fillEnd = polarToXY(startAngle + scoreDeg);
  const largeArcTrack = totalDeg > 180 ? 1 : 0;
  const largeArcFill = scoreDeg > 180 ? 1 : 0;

  const color = BAND_COLORS[band];

  return (
    <div className="flex flex-col items-center gap-3">
      <svg viewBox="0 0 200 160" className="w-52 h-44">
        {/* track */}
        <path
          d={`M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArcTrack} 1 ${trackEnd.x} ${trackEnd.y}`}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="14"
          strokeLinecap="round"
        />
        {/* fill */}
        {score > 0 && (
          <path
            d={`M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArcFill} 1 ${fillEnd.x} ${fillEnd.y}`}
            fill="none"
            stroke={color}
            strokeWidth="14"
            strokeLinecap="round"
          />
        )}
        {/* score label */}
        <text
          x="100"
          y="104"
          textAnchor="middle"
          fontSize="36"
          fontWeight="700"
          fill={color}
          fontFamily="Inter, system-ui, sans-serif"
        >
          {score}
        </text>
        <text
          x="100"
          y="122"
          textAnchor="middle"
          fontSize="11"
          fill="#8C8C8C"
          fontFamily="Inter, system-ui, sans-serif"
        >
          out of 100
        </text>
      </svg>
      <span
        className={`border text-sm font-semibold px-4 py-1.5 rounded-full ${BAND_BG[band]}`}
      >
        {band}
      </span>
    </div>
  );
}
