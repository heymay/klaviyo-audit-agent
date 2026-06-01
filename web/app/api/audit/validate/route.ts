import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.AUDIT_API_URL ?? "http://localhost:8000";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const res = await fetch(`${API_URL}/validate-key`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    console.error("[validate-key]", err);
    return NextResponse.json(
      { valid: false, error: "Could not reach the audit service." },
      { status: 502 }
    );
  }
}
