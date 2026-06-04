import { notFound } from "next/navigation";
import type { Metadata } from "next";
import Image from "next/image";
import ProgressPoller from "@/components/ProgressPoller";
import ScoreGauge from "@/components/ScoreGauge";
import CategoryScores from "@/components/CategoryScores";
import FindingsList from "@/components/FindingsList";
import ActionPlan from "@/components/ActionPlan";
import NPCta from "@/components/NPCta";
import PrintButton from "@/components/PrintButton";
import type { AuditReport, AuditStatus } from "@/types/audit";

const API_URL = process.env.AUDIT_API_URL ?? "http://localhost:8000";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const status = await getStatus(id).catch(() => null);
  const name = status?.business_name ?? "Klaviyo Audit";
  const score = status?.composite_score;
  const band = status?.score_band;
  const title = score
    ? `${name} — ${score}/100 ${band} | Klaviyo Audit`
    : `${name} | Klaviyo Audit`;
  return {
    title,
    description: `Klaviyo account audit for ${name}. Scored by National Positions' AI audit engine across deliverability, flows, campaigns, SMS, and segmentation.`,
  };
}

async function getStatus(id: string): Promise<AuditStatus | null> {
  try {
    const res = await fetch(`${API_URL}/audits/${id}`, { cache: "no-store" });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

async function getReport(id: string): Promise<AuditReport | null> {
  try {
    const res = await fetch(`${API_URL}/audits/${id}/report`, {
      cache: "no-store",
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

function fmt(n: number, decimals = 1) {
  return n.toFixed(decimals);
}

function pct(n: number) {
  return `${fmt(n * 100)}%`;
}

export default async function ReportPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const status = await getStatus(id);

  if (!status) notFound();

  if (status.status === "pending" || status.status === "running") {
    return <ProgressPoller auditId={id} />;
  }

  if (status.status === "error") {
    return (
      <div className="max-w-xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="text-5xl">⚠️</div>
        <h1 className="text-2xl font-bold text-np-navy">Audit Failed</h1>
        <p className="text-np-gray">{status.error ?? "Unknown error"}</p>
        <a href="/" className="btn-primary inline-block mt-2">
          Try Again
        </a>
      </div>
    );
  }

  const report = await getReport(id);
  if (!report) notFound();

  const { account, composite_score, score_band, category_scores, findings, recommendations, opportunity, profile_metrics, campaign_metrics, deliverability, segmentation, flows } = report;

  const critical = findings.filter((f) => f.severity === "Critical");
  const high = findings.filter((f) => f.severity === "High");

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10 space-y-8">

      {/* Print-only header with NP logo */}
      <div className="print-header hidden items-center justify-between border-b border-gray-200 pb-4 mb-2">
        <Image src="/logo.png" alt="National Positions" width={160} height={48} className="object-contain" />
        <div className="text-right text-xs text-gray-500">
          <div>Klaviyo Account Audit</div>
          <div>{new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}</div>
        </div>
      </div>

      {/* Print button */}
      <div className="flex justify-end print-hide">
        <PrintButton />
      </div>

      {/* Header */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-6 items-center sm:items-start">
          <ScoreGauge score={composite_score} band={score_band} />
          <div className="flex-1 text-center sm:text-left">
            <h1 className="text-2xl font-bold text-np-navy mb-1">
              {account.business_name}
            </h1>
            <p className="text-np-gray text-sm mb-4">
              {account.website} &middot; {account.ecommerce_platform} &middot;{" "}
              {account.audit_period_label}
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {[
                {
                  label: "Critical Issues",
                  value: critical.length,
                  cls: critical.length > 0 ? "text-red-600" : "text-green-600",
                },
                {
                  label: "High Issues",
                  value: high.length,
                  cls: high.length > 0 ? "text-orange-600" : "text-green-600",
                },
                {
                  label: "Total Findings",
                  value: findings.length,
                  cls: "text-np-navy",
                },
                {
                  label: "Recommendations",
                  value: recommendations.length,
                  cls: "text-np-navy",
                },
                {
                  label: "SMS Enabled",
                  value: account.sms_enabled ? "Yes" : "No",
                  cls: account.sms_enabled ? "text-green-600" : "text-red-600",
                },
                {
                  label: "Revenue Range",
                  value: account.monthly_revenue_range,
                  cls: "text-np-navy",
                },
              ].map(({ label, value, cls }) => (
                <div
                  key={label}
                  className="bg-np-light rounded-lg p-3 text-center"
                >
                  <div className={`text-lg font-bold ${cls}`}>{value}</div>
                  <div className="text-xs text-np-gray">{label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Opportunity */}
      {opportunity && (
        <div className="bg-green-50 border border-green-200 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-green-800 uppercase tracking-wide mb-2">
            Estimated Annual Revenue Opportunity
          </h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            {[
              { label: "Conservative", val: opportunity.conservative },
              { label: "Moderate", val: opportunity.moderate },
              { label: "Optimistic", val: opportunity.optimistic },
            ].map(({ label, val }) => (
              <div key={label}>
                <div className="text-xl font-bold text-green-700">{val}</div>
                <div className="text-xs text-green-600">{label}</div>
              </div>
            ))}
          </div>
          <p className="text-xs text-green-700 mt-3 text-center">
            {opportunity.disclaimer}
          </p>
        </div>
      )}

      {/* Score Breakdown */}
      <CategoryScores categories={category_scores} />

      {/* Key Metrics */}
      <div className="card">
        <h2 className="text-lg font-semibold text-np-navy mb-4">
          Key Account Metrics
        </h2>
        <div className="grid sm:grid-cols-2 gap-6">
          {/* Account Structure — data confirmed via API */}
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">
              Account Structure
            </h3>
            <div className="space-y-1 text-sm">
              {[
                ["Total Profiles", profile_metrics.total_profiles > 0 ? `${profile_metrics.total_profiles.toLocaleString()}+` : "—"],
                ["Email Lists", (segmentation.list_count ?? 0) > 0 ? (segmentation.list_count ?? 0).toLocaleString() : "—"],
                ["Segments", (segmentation.segment_count ?? 0) > 0 ? (segmentation.segment_count ?? 0).toLocaleString() : "—"],
                ["Live Flows", flows.filter(f => f.status === "Live" || f.status === "Manual").length.toLocaleString()],
                ["Total Flows", flows.length.toLocaleString()],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between">
                  <span className="text-np-gray">{k}</span>
                  <span className="font-medium">{v}</span>
                </div>
              ))}
            </div>
          </div>
          {/* Campaign Performance — data confirmed via API */}
          <div>
            <h3 className="text-sm font-semibold text-gray-600 mb-2">
              Campaign Performance
            </h3>
            <div className="space-y-1 text-sm">
              {[
                ["Campaigns Sent (12mo)", campaign_metrics.total_sent.toLocaleString()],
                ["Email Campaigns", campaign_metrics.email_campaigns.toLocaleString()],
                ["SMS Campaigns", campaign_metrics.sms_campaigns.toLocaleString()],
                ["Sends / Week", fmt(campaign_metrics.campaigns_per_week)],
                ["Engaged-Segment Rate", pct(campaign_metrics.pct_to_engaged_segments)],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between">
                  <span className="text-np-gray">{k}</span>
                  <span className="font-medium">{v}</span>
                </div>
              ))}
            </div>
            <div className="mt-3 flex gap-2 flex-wrap">
              {/* Only show SPF and DMARC — confirmed via live DNS lookup */}
              {[
                ["SPF", deliverability.has_spf],
                ["DMARC", deliverability.has_dmarc],
              ].map(([label, ok]) => (
                <span
                  key={label as string}
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    ok
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {ok ? "✓" : "✗"} {label}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Findings */}
      {findings.length > 0 ? (
        <FindingsList findings={findings} />
      ) : (
        <div className="card text-center py-10">
          <div className="text-4xl mb-3">✅</div>
          <h2 className="text-lg font-semibold text-np-navy">No findings — great work!</h2>
          <p className="text-np-gray text-sm mt-1">
            No issues triggered across 125+ audit rules. This account is well-configured.
          </p>
        </div>
      )}

      {/* Action Plan */}
      {recommendations.length > 0 && <ActionPlan recommendations={recommendations} />}

      {/* CTA */}
      <NPCta />
    </div>
  );
}
