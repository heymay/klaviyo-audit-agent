"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { startAudit, startMockAudit } from "@/lib/api";

const REVENUE_RANGES = [
  "Under $50K/mo",
  "$50K–$150K/mo",
  "$150K–$500K/mo",
  "$500K–$1M/mo",
  "Over $1M/mo",
];

const PLATFORMS = [
  "Shopify",
  "Shopify Plus",
  "WooCommerce",
  "BigCommerce",
  "Magento",
  "Other",
];

export default function AuditForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [keyStatus, setKeyStatus] = useState<"idle" | "checking" | "valid" | "invalid">("idle");
  const [keyMessage, setKeyMessage] = useState("");

  const [form, setForm] = useState({
    klaviyo_api_key: "",
    business_name: "",
    website: "",
    ecommerce_platform: "Shopify",
    monthly_revenue_range: "$50K–$150K/mo",
    sms_enabled: true,
  });

  function set(field: string, value: string | boolean) {
    setForm((prev) => ({ ...prev, [field]: value }));
    if (field === "klaviyo_api_key") {
      setKeyStatus("idle");
      setKeyMessage("");
    }
  }

  async function checkKey() {
    if (!form.klaviyo_api_key.trim()) return;
    setKeyStatus("checking");
    setKeyMessage("");
    try {
      const res = await fetch("/api/audit/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ klaviyo_api_key: form.klaviyo_api_key }),
      });
      const data = await res.json();
      if (data.valid) {
        setKeyStatus("valid");
        setKeyMessage(data.account_name ? `Connected: ${data.account_name}` : "Key is valid ✓");
      } else {
        setKeyStatus("invalid");
        setKeyMessage(data.error ?? "Invalid API key.");
      }
    } catch {
      setKeyStatus("invalid");
      setKeyMessage("Could not validate key — check your connection.");
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (!form.klaviyo_api_key.trim()) {
      setError("Klaviyo API key is required.");
      return;
    }
    setLoading(true);
    try {
      const { audit_id } = await startAudit(form);
      router.push(`/report/${audit_id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
      setLoading(false);
    }
  }

  async function handleDemo(type: "critical" | "average" | "strong") {
    setLoading(true);
    setError("");
    try {
      const { audit_id } = await startMockAudit(type);
      router.push(`/report/${audit_id}`);
    } catch {
      setError("Failed to start demo audit.");
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <form onSubmit={handleSubmit} className="card space-y-5">
        <div className="grid sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Business Name
            </label>
            <input
              type="text"
              required
              placeholder="Acme Store"
              value={form.business_name}
              onChange={(e) => set("business_name", e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-np-navy"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Website URL
            </label>
            <input
              type="url"
              required
              placeholder="https://acmestore.com"
              value={form.website}
              onChange={(e) => set("website", e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-np-navy"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Klaviyo Private API Key
            <span className="ml-1 text-xs text-np-gray font-normal">
              (read-only scope — never stored)
            </span>
          </label>
          <div className="relative">
            <input
              type={showKey ? "text" : "password"}
              required
              placeholder="pk_xxxxxxxxxxxxxxxxxxxxxxxx"
              value={form.klaviyo_api_key}
              onChange={(e) => set("klaviyo_api_key", e.target.value)}
              className={`w-full border rounded-lg px-3 py-2 pr-20 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-np-navy ${
                keyStatus === "valid" ? "border-green-400 bg-green-50" :
                keyStatus === "invalid" ? "border-red-400 bg-red-50" :
                "border-gray-300"
              }`}
            />
            <button
              type="button"
              onClick={() => setShowKey((v) => !v)}
              className="absolute right-3 top-2 text-xs text-np-gray hover:text-gray-700"
            >
              {showKey ? "Hide" : "Show"}
            </button>
          </div>

          {/* Check key button + status */}
          <div className="flex items-center gap-3 mt-1.5">
            <button
              type="button"
              onClick={checkKey}
              disabled={!form.klaviyo_api_key.trim() || keyStatus === "checking"}
              className="text-xs px-3 py-1.5 rounded-lg border border-np-navy text-np-navy hover:bg-np-navy hover:text-white transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {keyStatus === "checking" ? "Checking…" : "Check Key"}
            </button>
            {keyMessage && (
              <span className={`text-xs font-medium ${keyStatus === "valid" ? "text-green-600" : "text-red-600"}`}>
                {keyStatus === "valid" ? "✓ " : "✗ "}{keyMessage}
              </span>
            )}
            {!keyMessage && (
              <span className="text-xs text-np-gray">
                Settings → API Keys in Klaviyo. Create a read-only key.
              </span>
            )}
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Ecommerce Platform
            </label>
            <select
              value={form.ecommerce_platform}
              onChange={(e) => set("ecommerce_platform", e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-np-navy"
            >
              {PLATFORMS.map((p) => (
                <option key={p}>{p}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Monthly Revenue Range
            </label>
            <select
              value={form.monthly_revenue_range}
              onChange={(e) => set("monthly_revenue_range", e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-np-navy"
            >
              {REVENUE_RANGES.map((r) => (
                <option key={r}>{r}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            role="switch"
            aria-checked={form.sms_enabled}
            onClick={() => set("sms_enabled", !form.sms_enabled)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-np-navy ${
              form.sms_enabled ? "bg-np-navy" : "bg-gray-300"
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                form.sms_enabled ? "translate-x-6" : "translate-x-1"
              }`}
            />
          </button>
          <span className="text-sm font-medium text-gray-700">
            SMS is enabled in our Klaviyo account
          </span>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full text-center"
        >
          {loading ? "Starting audit…" : "Run My Klaviyo Audit →"}
        </button>
      </form>

      <div>
        <p className="text-center text-sm text-np-gray mb-3">
          Or try a demo account:
        </p>
        <div className="grid grid-cols-3 gap-3">
          {(["critical", "average", "strong"] as const).map((type) => (
            <button
              key={type}
              onClick={() => handleDemo(type)}
              disabled={loading}
              className="border border-gray-300 rounded-lg py-2 px-3 text-sm hover:bg-white hover:shadow-sm transition-all disabled:opacity-50 capitalize text-center"
            >
              {type === "critical" && "🔴 "}
              {type === "average" && "🟡 "}
              {type === "strong" && "🟢 "}
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
