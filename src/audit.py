"""
Klaviyo Audit Katie — CLI Entry Point

Mock mode (Phase 2):
  python3 -m src.audit mock_data/account_critical.json

Live mode (Phase 3):
  export KLAVIYO_API_KEY=pk_xxxxxxxxxxxx
  python3 -m src.audit --live --manual manual_inputs.json --context context.json

Options:
  --output <dir>     Report output directory (default: reports/)
  --live             Pull data from Klaviyo API instead of a JSON file
  --manual <file>    Path to filled-in manual_inputs.json (required for --live)
  --context <file>   Path to context.json with business name, website, platform
  --verbose          Enable debug logging
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from .models import AccountData, AuditResult
from .scorer import run_scoring
from .rules import run_rules
from .recommender import build_recommendations
from .reporter import generate_report
from .data_quality import detect_gaps, gaps_to_findings
from .opportunity import estimate_opportunity


# ── core audit pipeline ────────────────────────────────────────────────────

def _run_pipeline(acct: AccountData, output_dir: str, stem: str):
    category_scores, composite, band = run_scoring(acct)

    # Data quality — detect suspicious zeros before running rules
    gaps = detect_gaps(acct)
    gap_findings = gaps_to_findings(gaps)
    gap_descriptions = [g.description for g in gaps]

    rule_findings = run_rules(acct)
    findings = rule_findings + gap_findings   # DQ findings appended after scored findings

    recommendations = build_recommendations(rule_findings)  # only score real findings

    result = AuditResult(
        account=acct,
        category_scores=category_scores,
        composite_score=composite,
        score_band=band,
        findings=findings,
        recommendations=recommendations,
        data_gaps=gap_descriptions,
    )

    # Attach opportunity estimate to result for reporter
    result._opportunity = estimate_opportunity(result)

    report_md = generate_report(result)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(output_dir) / f"{stem}_report.md"
    out_path.write_text(report_md)

    return result, str(out_path)


# ── mock mode ──────────────────────────────────────────────────────────────

def run_mock_audit(json_path: str, output_dir: str = "reports"):
    with open(json_path) as f:
        data = json.load(f)
    acct = AccountData.from_dict(data)
    stem = Path(json_path).stem
    return _run_pipeline(acct, output_dir, stem)


# ── live mode ──────────────────────────────────────────────────────────────

def run_live_audit(manual_path: str, context_path: str, output_dir: str = "reports"):
    from .klaviyo_client import KlaviyoClient, KlaviyoAuthError
    from .data_pull import pull_all
    from .normalizer import normalize

    # Load manual inputs
    if not os.path.exists(manual_path):
        print(f"Error: manual inputs file not found: {manual_path}")
        print("Copy manual_inputs_template.json → manual_inputs.json and fill it in.")
        sys.exit(1)
    with open(manual_path) as f:
        manual = json.load(f)

    # Load context (business name, website, platform, etc.)
    context = {}
    if context_path and os.path.exists(context_path):
        with open(context_path) as f:
            context = json.load(f)
    elif context_path:
        print(f"Warning: context file not found ({context_path}) — using defaults.")

    # Connect to Klaviyo
    print("\nKlaviyo Audit Katie — Live Mode")
    print("=" * 50)
    try:
        client = KlaviyoClient.from_env()
    except KlaviyoAuthError as e:
        print(f"\nAuth error: {e}")
        sys.exit(1)

    print("Pulling data from Klaviyo API...")
    raw = pull_all(client)

    # Normalize raw + manual → AccountData
    acct = normalize(raw, manual, context)

    # Use account name as report stem
    stem = (acct.business_name or acct.klaviyo_account_name or "live_account").lower()
    stem = "".join(c if c.isalnum() else "_" for c in stem).strip("_")

    return _run_pipeline(acct, output_dir, stem)


# ── output ─────────────────────────────────────────────────────────────────

def _print_summary(result: AuditResult, out_path: str) -> None:
    acct = result.account
    print(f"\n{'='*60}")
    print(f"  Klaviyo Audit Katie — {acct.business_name or acct.klaviyo_account_name}")
    print(f"{'='*60}")
    print(f"  Composite Score : {result.composite_score}/100 — {result.score_band}")
    print()
    print("  Category Scores:")
    for cs in result.category_scores:
        bar = "█" * cs.score + "░" * (10 - cs.score)
        print(f"    {cs.name:<35} {bar}  {cs.score}/10")
    print()
    crit = len(result.critical_findings)
    high = len(result.high_findings)
    print(f"  Findings       : {len(result.findings)} total ({crit} Critical, {high} High)")
    print(f"  Recommendations: {len(result.recommendations)}")
    if result.recommendations:
        print()
        print("  Top 3 recommendations:")
        for i, r in enumerate(result.recommendations[:3], 1):
            print(f"    {i}. [{r.priority}] {r.issue[:65]}")
    print()
    print(f"  Report saved → {out_path}")
    print(f"{'='*60}\n")


# ── CLI ────────────────────────────────────────────────────────────────────

def _arg(flag: str, default: str = "") -> str:
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return default


def main() -> None:
    if "--verbose" in sys.argv:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    live_mode = "--live" in sys.argv
    output_dir = _arg("--output", "reports")

    if live_mode:
        manual_path = _arg("--manual", "manual_inputs.json")
        context_path = _arg("--context", "context.json")
        result, out_path = run_live_audit(manual_path, context_path, output_dir)
        _print_summary(result, out_path)

    else:
        # Mock/JSON mode
        positional = [a for a in sys.argv[1:] if not a.startswith("--")]
        if not positional:
            print(__doc__)
            sys.exit(1)

        json_path = positional[0]
        if not os.path.exists(json_path):
            print(f"Error: file not found: {json_path}")
            sys.exit(1)

        result, out_path = run_mock_audit(json_path, output_dir)
        _print_summary(result, out_path)


if __name__ == "__main__":
    main()
