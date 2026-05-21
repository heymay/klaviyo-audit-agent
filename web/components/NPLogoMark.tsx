/**
 * NPLogoMark — the National Positions 4×4 red-grid + navy-star mark.
 *
 * Grid spec (matching the NP brand mark):
 *   - 4 columns × 4 rows of red squares
 *   - outer padding: 5px, cell: 20px, gap: 6px  →  viewBox 108×108
 *   - Star cell: row 3 / col 2 (1-indexed)  =  row=2 / col=1 (0-indexed)
 *   - White fill behind star so it reads on any background
 */
interface Props {
  size?: number;
  className?: string;
  /** "color" = red squares on transparent (default); "white" = white squares on transparent */
  variant?: "color" | "white";
}

const OUTER = 3;
const CELL  = 22;
const GAP   = 4;
const STEP  = CELL + GAP;   // 26
const VB    = OUTER * 2 + CELL * 4 + GAP * 3;  // 106

// Star geometry — center of the star cell (row=2, col=1, 0-indexed)
const STAR_CX = OUTER + 1 * STEP + CELL / 2;
const STAR_CY = OUTER + 2 * STEP + CELL / 2;
const STAR_R  = CELL * 0.42;   // outer radius
const STAR_r  = STAR_R * 0.42; // inner radius

function buildStar(cx: number, cy: number, R: number, r: number): string {
  const pts: string[] = [];
  for (let i = 0; i < 5; i++) {
    const outerA = (i * 72 - 90) * (Math.PI / 180);
    const innerA = outerA + 36  * (Math.PI / 180);
    pts.push(`${(cx + R * Math.cos(outerA)).toFixed(3)},${(cy + R * Math.sin(outerA)).toFixed(3)}`);
    pts.push(`${(cx + r * Math.cos(innerA)).toFixed(3)},${(cy + r * Math.sin(innerA)).toFixed(3)}`);
  }
  return pts.join(" ");
}

const RED   = "#CC2229";
const NAVY  = "#1B2D50";
const STAR_CELL_ROW = 2;  // 0-indexed
const STAR_CELL_COL = 1;  // 0-indexed

export default function NPLogoMark({ size = 40, className = "", variant = "color" }: Props) {
  const starPoints = buildStar(STAR_CX, STAR_CY, STAR_R, STAR_r);
  const squareFill = variant === "white" ? "white" : RED;
  const starFill   = variant === "white" ? NAVY    : NAVY;
  const starBg     = variant === "white" ? "white" : "white";

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${VB} ${VB}`}
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-label="National Positions"
    >
      {/* 4×4 grid */}
      {Array.from({ length: 4 }, (_, row) =>
        Array.from({ length: 4 }, (_, col) => {
          const x = OUTER + col * STEP;
          const y = OUTER + row * STEP;
          const isStar = row === STAR_CELL_ROW && col === STAR_CELL_COL;
          return (
            <rect
              key={`${row}-${col}`}
              x={x}
              y={y}
              width={CELL}
              height={CELL}
              fill={isStar ? starBg : squareFill}
            />
          );
        })
      )}
      {/* Star centred in the star cell */}
      <polygon points={starPoints} fill={starFill} />
    </svg>
  );
}
