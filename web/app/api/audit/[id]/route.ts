import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.AUDIT_API_URL ?? "http://localhost:8000";

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const res = await fetch(`${API_URL}/audits/${id}`);
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
