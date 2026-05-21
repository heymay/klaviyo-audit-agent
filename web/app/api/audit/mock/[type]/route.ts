import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.AUDIT_API_URL ?? "http://localhost:8000";

export async function POST(
  _req: NextRequest,
  { params }: { params: Promise<{ type: string }> }
) {
  try {
    const { type } = await params;
    const res = await fetch(`${API_URL}/audits/mock/${type}`, { method: "POST" });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[audit/mock]", err);
    return NextResponse.json(
      { detail: "Could not reach the audit service. Please try again." },
      { status: 502 }
    );
  }
}
