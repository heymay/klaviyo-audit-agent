import type { AuditStatus, AuditReport } from "@/types/audit";

const BASE = "/api/audit";

export async function startAudit(payload: {
  klaviyo_api_key: string;
  business_name: string;
  website: string;
  ecommerce_platform: string;
  monthly_revenue_range: string;
  sms_enabled: boolean;
}): Promise<{ audit_id: string }> {
  const res = await fetch(`${BASE}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? "Failed to start audit");
  }
  return res.json();
}

export async function pollStatus(auditId: string): Promise<AuditStatus> {
  const res = await fetch(`${BASE}/${auditId}`);
  if (!res.ok) throw new Error("Failed to fetch status");
  return res.json();
}

export async function fetchReport(auditId: string): Promise<AuditReport> {
  const res = await fetch(`${BASE}/${auditId}/report`);
  if (!res.ok) throw new Error("Failed to fetch report");
  return res.json();
}

export async function startMockAudit(
  accountType: "critical" | "average" | "strong"
): Promise<{ audit_id: string }> {
  const res = await fetch(`${BASE}/mock/${accountType}`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to start mock audit");
  return res.json();
}
