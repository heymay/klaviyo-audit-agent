import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.AUDIT_API_URL ?? "http://localhost:8000";

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const res = await fetch(`${API_URL}/audits/${id}/report`, { cache: "no-store" });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[audit/report]", err);
    return NextResponse.json({ detail: "Could not reach the audit service." }, { status: 502 });
  }
}
