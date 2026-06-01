"""
Klaviyo Audit Katie — FastAPI Backend
Runs the Python audit engine and stores results in Supabase.

Security rules enforced:
  - API key accepted in request body only — never URL params, never logged
  - All Klaviyo API calls are server-side
  - No PII stored beyond aggregate audit results
  - CORS locked to the Next.js origin

Run locally:
  cd klaviyo-audit-agent
  uvicorn api.main:app --reload --port 8000

Deploy (Railway):
  Set env vars: SUPABASE_URL, SUPABASE_SERVICE_KEY
  Start command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
"""
from __future__ import annotations

import json
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Add repo root to path so we can import src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import AccountData
from src.scorer import run_scoring
from src.rules import run_rules
from src.recommender import build_recommendations
from src.data_quality import detect_gaps, gaps_to_findings
from src.opportunity import estimate_opportunity
from src.serializer import audit_result_to_dict
from src.models import AuditResult

log = logging.getLogger("api")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

# ── Supabase client (optional — falls back to in-memory if not configured) ──

_supabase = None

def _get_supabase():
    global _supabase
    if _supabase is not None:
        return _supabase
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_SERVICE_KEY")
    if url and key:
        try:
            from supabase import create_client
            _supabase = create_client(url, key)
            log.info("Supabase client initialised.")
        except ImportError:
            log.warning("supabase-py not installed — results will not persist.")
        except Exception as e:
            log.warning(f"Supabase init failed ({e}) — falling back to in-memory store.")
    return _supabase


# In-memory fallback when Supabase is not configured
_in_memory: Dict[str, Dict] = {}


def _store(audit_id: str, data: Dict) -> None:
    sb = _get_supabase()
    if sb:
        sb.table("audits").upsert({"id": audit_id, **data}).execute()
    else:
        _in_memory[audit_id] = data


def _fetch(audit_id: str) -> Optional[Dict]:
    sb = _get_supabase()
    if sb:
        result = sb.table("audits").select("*").eq("id", audit_id).single().execute()
        return result.data if result.data else None
    return _in_memory.get(audit_id)


# ── FastAPI app ─────────────────────────────────────────────────────────────

ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://klaviyo-audit-agent.vercel.app",
).split(",")
# Also allow any vercel.app preview deployment
ALLOWED_ORIGIN_REGEX = r"https://.*\.vercel\.app"

app = FastAPI(title="Klaviyo Audit Katie API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


# ── Request / Response models ───────────────────────────────────────────────

class AuditRequest(BaseModel):
    # Business context
    business_name: str = Field(..., min_length=1, max_length=200)
    website: str = Field(..., min_length=1, max_length=500)
    ecommerce_platform: str = "Shopify"
    monthly_revenue_range: str = ""
    audit_period_days: int = 365

    # From the intake form
    sms_enabled: bool = False

    # Klaviyo connection — key is write-once, never echoed back
    klaviyo_api_key: str = Field(..., min_length=10)

    # Manual inputs (all optional — data quality warnings if omitted)
    manual_inputs: Dict[str, Any] = Field(default_factory=dict)


class AuditStatusResponse(BaseModel):
    audit_id: str
    status: str          # pending | running | complete | error
    composite_score: Optional[int] = None
    score_band: Optional[str] = None
    business_name: Optional[str] = None
    error: Optional[str] = None
    progress: Optional[int] = None       # 0–100
    current_step: Optional[str] = None  # human-readable step label


# ── Background audit runner ─────────────────────────────────────────────────

def _progress(audit_id: str, pct: int, step: str) -> None:
    """Write a progress update so the poller can surface it."""
    _store(audit_id, {"status": "running", "progress": pct, "current_step": step})
    log.info("Audit %s — %d%% — %s", audit_id, pct, step)


def _run_audit_background(audit_id: str, request_data: Dict) -> None:
    """Runs the full audit pipeline and stores result in Supabase."""
    try:
        _progress(audit_id, 2, "Connecting to Klaviyo…")

        api_key = request_data.pop("klaviyo_api_key")
        manual = request_data.get("manual_inputs", {})
        if "account_context" not in manual:
            manual["account_context"] = {}
        if "sms_enabled" in request_data:
            manual["account_context"]["sms_enabled"] = request_data["sms_enabled"]
        context = {
            "business_name": request_data["business_name"],
            "website": request_data["website"],
            "ecommerce_platform": request_data.get("ecommerce_platform", "Shopify"),
            "monthly_revenue_range": request_data.get("monthly_revenue_range", ""),
            "audit_period_label": f"Last {request_data.get('audit_period_days', 365)} days",
            "audit_period_days": request_data.get("audit_period_days", 365),
        }

        os.environ["KLAVIYO_API_KEY"] = api_key
        try:
            from src.klaviyo_client import KlaviyoClient
            from src.data_pull import pull_all
            from src.normalizer import normalize

            client = KlaviyoClient.from_env()

            _progress(audit_id, 8, "Validating API key & reading account info…")
            client.validate_connection()

            def _on_progress(pct: int, msg: str):
                _progress(audit_id, pct, msg)

            _progress(audit_id, 12, "Starting data pull…")
            raw = pull_all(client, website=context.get("website", ""), progress_cb=_on_progress)

            _progress(audit_id, 76, "Normalising account data…")
            acct = normalize(raw, manual, context)
        finally:
            os.environ.pop("KLAVIYO_API_KEY", None)

        _progress(audit_id, 78, "Scoring 10 audit categories…")
        category_scores, composite, band = run_scoring(acct)

        _progress(audit_id, 84, "Running 125+ decision rules…")
        gaps = detect_gaps(acct)
        gap_findings = gaps_to_findings(gaps)
        rule_findings = run_rules(acct)
        findings = rule_findings + gap_findings

        _progress(audit_id, 91, f"Evaluating {len(findings)} findings & building recommendations…")
        recommendations = build_recommendations(rule_findings)

        _progress(audit_id, 96, "Calculating revenue opportunity & finalising report…")

        result = AuditResult(
            account=acct,
            category_scores=category_scores,
            composite_score=composite,
            score_band=band,
            findings=findings,
            recommendations=recommendations,
            data_gaps=[g.description for g in gaps],
        )
        result._opportunity = estimate_opportunity(result)

        report_data = audit_result_to_dict(result)

        _store(audit_id, {
            "status": "complete",
            "business_name": acct.business_name,
            "website": acct.website,
            "composite_score": composite,
            "score_band": band,
            "report_data": json.dumps(report_data),
        })
        log.info("Audit %s complete — score %d (%s)", audit_id, composite, band)

    except Exception as e:
        log.error("Audit %s failed: %s", audit_id, e, exc_info=True)
        _store(audit_id, {
            "status": "error",
            "error_message": str(e)[:500],
        })


# ── Routes ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "klaviyo-audit-api"}


@app.post("/validate-key")
async def validate_key(request: Request):
    """
    Validate a Klaviyo private API key by hitting GET /api/accounts/.
    Returns: { valid: bool, account_name: str | None, error: str | None }
    """
    import httpx
    body = await request.json()
    key = (body.get("klaviyo_api_key") or "").strip()

    if not key:
        return JSONResponse({"valid": False, "error": "No API key provided."})

    # Basic format hint — Klaviyo private keys start with pk_
    if key.startswith("sb.") or key.startswith("sb_"):
        return JSONResponse({
            "valid": False,
            "error": "That looks like a Supabase key, not a Klaviyo key. "
                     "In Klaviyo go to Settings → API Keys and create a Private Key."
        })

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://a.klaviyo.com/api/accounts/",
                headers={
                    "Authorization": f"Klaviyo-API-Key {key}",
                    "revision": "2024-02-15",
                    "Accept": "application/json",
                },
            )
        if resp.status_code == 200:
            data = resp.json()
            name = (
                data.get("data", [{}])[0]
                    .get("attributes", {})
                    .get("contact_information", {})
                    .get("organization_name")
                or data.get("data", [{}])[0]
                    .get("attributes", {})
                    .get("public_api_key")
            )
            return JSONResponse({"valid": True, "account_name": name})
        elif resp.status_code == 401:
            return JSONResponse({"valid": False, "error": "Invalid API key — authentication failed (401)."})
        elif resp.status_code == 403:
            return JSONResponse({"valid": False, "error": "Key valid but missing read:accounts scope. Create a full read-only key."})
        else:
            return JSONResponse({"valid": False, "error": f"Klaviyo returned {resp.status_code}."})
    except Exception as e:
        log.error("validate-key error: %s", e)
        return JSONResponse({"valid": False, "error": "Could not reach Klaviyo API. Check your connection."}, status_code=502)


@app.post("/audits", status_code=202)
async def start_audit(body: AuditRequest, background_tasks: BackgroundTasks):
    """
    Start a new audit. Returns immediately with audit_id.
    The audit runs asynchronously — poll GET /audits/{id} for status.
    """
    audit_id = str(uuid.uuid4())

    # Store initial record
    _store(audit_id, {
        "status": "pending",
        "business_name": body.business_name,
        "website": body.website,
    })

    # Pass request data as a plain dict — API key leaves body.klaviyo_api_key
    # and is cleared from env immediately after use in the background task
    request_dict = body.model_dump()

    background_tasks.add_task(_run_audit_background, audit_id, request_dict)

    log.info("Audit %s queued for %s", audit_id, body.business_name)
    return {"audit_id": audit_id, "status": "pending"}


@app.get("/audits/{audit_id}", response_model=AuditStatusResponse)
def get_audit_status(audit_id: str):
    """Poll this endpoint to check audit progress and retrieve results."""
    record = _fetch(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit not found.")

    status = record.get("status", "pending")
    response: Dict[str, Any] = {
        "audit_id": audit_id,
        "status": status,
        "business_name": record.get("business_name"),
        "progress": record.get("progress", 0 if status == "pending" else None),
        "current_step": record.get("current_step"),
    }

    if status == "complete":
        response["composite_score"] = record.get("composite_score")
        response["score_band"] = record.get("score_band")
        response["progress"] = 100

    if status == "error":
        response["error"] = record.get("error_message", "Unknown error")

    return response


@app.get("/audits/{audit_id}/report")
def get_audit_report(audit_id: str):
    """Returns the full structured report JSON for a completed audit."""
    record = _fetch(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit not found.")
    if record.get("status") != "complete":
        raise HTTPException(status_code=425, detail="Audit is not yet complete.")

    report_data = record.get("report_data")
    if isinstance(report_data, str):
        report_data = json.loads(report_data)
    return JSONResponse(content=report_data)


# ── Mock audit endpoint (dev/demo only) ────────────────────────────────────

@app.post("/audits/mock/{account_type}", status_code=202)
async def start_mock_audit(account_type: str, background_tasks: BackgroundTasks):
    """
    Run a mock audit using one of the bundled mock accounts.
    account_type: critical | average | strong
    For development and demo purposes only — not for production.
    """
    valid = {"critical", "average", "strong"}
    if account_type not in valid:
        raise HTTPException(status_code=400, detail=f"account_type must be one of: {valid}")

    audit_id = str(uuid.uuid4())
    _store(audit_id, {"status": "pending", "business_name": f"Demo ({account_type})"})

    def _run_mock(aid: str, atype: str):
        try:
            _store(aid, {"status": "running"})
            mock_path = Path(__file__).parent.parent / "mock_data" / f"account_{atype}.json"
            with open(mock_path) as f:
                import json as _json
                data = _json.load(f)

            acct = AccountData.from_dict(data)
            category_scores, composite, band = run_scoring(acct)
            gaps = detect_gaps(acct)
            gap_findings = gaps_to_findings(gaps)
            rule_findings = run_rules(acct)
            findings = rule_findings + gap_findings
            recommendations = build_recommendations(rule_findings)

            result = AuditResult(
                account=acct,
                category_scores=category_scores,
                composite_score=composite,
                score_band=band,
                findings=findings,
                recommendations=recommendations,
                data_gaps=[g.description for g in gaps],
            )
            result._opportunity = estimate_opportunity(result)
            report_data = audit_result_to_dict(result)

            _store(aid, {
                "status": "complete",
                "business_name": acct.business_name,
                "website": acct.website,
                "composite_score": composite,
                "score_band": band,
                "report_data": json.dumps(report_data),
            })
        except Exception as e:
            log.error("Mock audit %s failed: %s", aid, e, exc_info=True)
            _store(aid, {"status": "error", "error_message": str(e)[:500]})

    background_tasks.add_task(_run_mock, audit_id, account_type)
    return {"audit_id": audit_id, "status": "pending"}
