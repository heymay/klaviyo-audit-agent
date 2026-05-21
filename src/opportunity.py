"""
Klaviyo Audit Katie — Opportunity Range Estimator
Produces account-specific conservative/moderate/optimistic revenue lift ranges
based on the account's current Klaviyo revenue, score, and top findings.

All estimates are directional ranges — never point forecasts.
The required disclaimer is injected automatically into every estimate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from .models import AuditResult, Recommendation

DISCLAIMER = (
    "*Revenue estimates are directional ranges only, based on industry benchmarks "
    "and comparable account improvements. They are not guarantees of results. "
    "Actual outcomes depend on implementation quality, market conditions, and "
    "account-specific factors. National Positions does not guarantee revenue outcomes.*"
)

# Monthly revenue range midpoints for when Klaviyo revenue is $0 / not configured
_RANGE_MIDPOINTS = {
    "Under $10,000/month":          5_000,
    "$10,000–$50,000/month":       30_000,
    "$50,000–$200,000/month":     125_000,
    "$200,000–$1,000,000/month":  600_000,
    "Over $1,000,000/month":    2_000_000,
}
_DEFAULT_EMAIL_SHARE = 0.15   # typical Klaviyo revenue as % of store revenue

# Impact multipliers per recommendation priority tier (applied to current Klaviyo revenue)
_LIFT_TABLE = {
    # (conservative_low, conservative_high, moderate_low, moderate_high, optimistic_low, optimistic_high)
    "Critical": (0.08, 0.15,  0.15, 0.30,  0.30, 0.60),
    "High":     (0.04, 0.08,  0.08, 0.15,  0.15, 0.30),
    "Medium":   (0.02, 0.04,  0.04, 0.08,  0.08, 0.15),
}


@dataclass
class OpportunityRange:
    conservative_low: float
    conservative_high: float
    moderate_low: float
    moderate_high: float
    optimistic_low: float
    optimistic_high: float
    baseline_revenue: float
    basis: str          # "klaviyo_revenue" | "monthly_revenue_estimate" | "no_data"
    disclaimer: str = DISCLAIMER

    def as_dict(self) -> dict:
        def fmt(v): return f"${v:,.0f}"
        return {
            "conservative": f"{fmt(self.conservative_low)}–{fmt(self.conservative_high)} / yr",
            "moderate":     f"{fmt(self.moderate_low)}–{fmt(self.moderate_high)} / yr",
            "optimistic":   f"{fmt(self.optimistic_low)}–{fmt(self.optimistic_high)} / yr",
            "basis": self.basis,
            "disclaimer": self.disclaimer,
        }


def estimate_opportunity(result: AuditResult) -> OpportunityRange:
    """
    Calculate annualised revenue lift ranges from the top recommendations.
    Uses current Klaviyo revenue as the baseline; falls back to monthly_revenue_range
    if Klaviyo revenue is $0 or attribution is not configured.
    """
    r = result.account.revenue
    monthly_range = result.account.monthly_revenue_range

    # Determine baseline annual Klaviyo revenue
    if r.revenue_attribution_configured and r.total_klaviyo_revenue > 0:
        baseline = r.total_klaviyo_revenue
        basis = "klaviyo_revenue"
    elif monthly_range and monthly_range in _RANGE_MIDPOINTS:
        monthly_store_rev = _RANGE_MIDPOINTS[monthly_range]
        baseline = monthly_store_rev * 12 * _DEFAULT_EMAIL_SHARE
        basis = "monthly_revenue_estimate"
    else:
        # No revenue data at all — use a minimal placeholder
        baseline = 50_000
        basis = "no_data"

    # Aggregate lift from top recommendations (cap at 5 to avoid stacking)
    top_recs = result.recommendations[:5]
    if not top_recs:
        # Strong account — small optimisation lift
        return OpportunityRange(
            conservative_low=baseline * 0.02,
            conservative_high=baseline * 0.05,
            moderate_low=baseline * 0.05,
            moderate_high=baseline * 0.10,
            optimistic_low=baseline * 0.10,
            optimistic_high=baseline * 0.20,
            baseline_revenue=baseline,
            basis=basis,
        )

    # Sum lift ranges from each rec, then dampen for stacking
    # (each successive rec contributes less — diminishing returns)
    cl = ch = ml = mh = ol = oh = 0.0
    for i, rec in enumerate(top_recs):
        multipliers = _LIFT_TABLE.get(rec.priority, _LIFT_TABLE["Medium"])
        dampen = 1.0 / (1 + i * 0.3)   # first rec = 100%, second = 77%, third = 62%...
        cl += baseline * multipliers[0] * dampen
        ch += baseline * multipliers[1] * dampen
        ml += baseline * multipliers[2] * dampen
        mh += baseline * multipliers[3] * dampen
        ol += baseline * multipliers[4] * dampen
        oh += baseline * multipliers[5] * dampen

    # Round to nearest $500 for readability
    def r500(v): return round(v / 500) * 500

    return OpportunityRange(
        conservative_low=r500(cl),
        conservative_high=r500(ch),
        moderate_low=r500(ml),
        moderate_high=r500(mh),
        optimistic_low=r500(ol),
        optimistic_high=r500(oh),
        baseline_revenue=baseline,
        basis=basis,
    )


def format_opportunity_section(opp: OpportunityRange) -> str:
    """Return a Markdown block for the opportunity section of the report."""
    d = opp.as_dict()
    basis_note = {
        "klaviyo_revenue": f"Based on current annual Klaviyo revenue of **${opp.baseline_revenue:,.0f}**.",
        "monthly_revenue_estimate": (
            f"Based on estimated annual Klaviyo revenue of **${opp.baseline_revenue:,.0f}** "
            f"(derived from monthly revenue range — actual Klaviyo revenue not provided)."
        ),
        "no_data": (
            "Revenue baseline not available — estimates use a conservative placeholder. "
            "Provide Klaviyo revenue data in manual_inputs.json for account-specific ranges."
        ),
    }.get(opp.basis, "")

    lines = [
        "| Scenario | Estimated Annual Revenue Lift |",
        "|---|---|",
        f"| Conservative | {d['conservative']} |",
        f"| Moderate | {d['moderate']} |",
        f"| Optimistic | {d['optimistic']} |",
        "",
        basis_note,
        "",
        d["disclaimer"],
    ]
    return "\n".join(lines)
