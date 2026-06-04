"""
Klaviyo Audit Katie — Data Models
Normalized internal data model for audit engine.
All Klaviyo API responses are mapped to these structures before scoring.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ProfileMetrics:
    total_profiles: int = 0
    emailable_profiles: int = 0
    sms_consented_profiles: int = 0
    suppressed_profiles: int = 0
    engaged_30_day: int = 0
    engaged_60_day: int = 0
    engaged_90_day: int = 0
    engaged_180_day: int = 0

    @property
    def sms_consent_rate(self) -> float:
        if self.emailable_profiles == 0:
            return 0.0
        return self.sms_consented_profiles / self.emailable_profiles

    @property
    def suppression_rate(self) -> float:
        if self.total_profiles == 0:
            return 0.0
        return self.suppressed_profiles / self.total_profiles

    @property
    def engaged_30_pct(self) -> float:
        if self.emailable_profiles == 0:
            return 0.0
        return self.engaged_30_day / self.emailable_profiles

    @property
    def engaged_90_pct(self) -> float:
        if self.emailable_profiles == 0:
            return 0.0
        return self.engaged_90_day / self.emailable_profiles

    @property
    def dormant_profiles(self) -> int:
        return max(0, self.emailable_profiles - self.engaged_180_day)

    @property
    def dormant_rate(self) -> float:
        if self.emailable_profiles == 0:
            return 0.0
        return self.dormant_profiles / self.emailable_profiles

    @classmethod
    def from_dict(cls, d: dict) -> ProfileMetrics:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class FlowMessage:
    channel: str = "email"          # email | sms
    position: int = 1
    delay_minutes: int = 0          # minutes from trigger (position 1) or prior message
    has_discount: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> FlowMessage:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# Canonical names used for core flow type detection
CORE_FLOW_PATTERNS = {
    "welcome":           ["welcome", "new subscriber", "welcome series", "onboard", "getting started"],
    "abandoned_cart":    ["abandoned cart", "cart abandonment", "checkout abandonment", "abandon checkout", "recover cart"],
    "added_to_cart":     ["added to cart", "browse + cart", "add to cart"],
    "browse_abandonment":["browse abandonment", "viewed product", "product viewed", "browse abandon"],
    "post_purchase":     ["post-purchase", "post purchase", "thank you", "after purchase", "order thank", "order confirm", "receipt"],
    "winback":           ["winback", "win back", "re-engagement", "reengagement", "we miss you", "lapsed", "come back"],
    "vip":               ["vip", "loyalty", "top customer", "signature club", "member"],
}


@dataclass
class FlowData:
    flow_id: str = ""
    name: str = ""
    status: str = "Live"            # Live | Draft | Manual | Archived
    trigger_type: str = ""
    messages: List[FlowMessage] = field(default_factory=list)
    revenue: float = 0.0
    conversion_rate: float = 0.0
    last_updated_days_ago: int = 0

    @property
    def email_messages(self) -> List[FlowMessage]:
        return [m for m in self.messages if m.channel == "email"]

    @property
    def sms_messages(self) -> List[FlowMessage]:
        return [m for m in self.messages if m.channel == "sms"]

    @property
    def email_count(self) -> int:
        return len(self.email_messages)

    @property
    def sms_count(self) -> int:
        return len(self.sms_messages)

    @property
    def first_message_delay_minutes(self) -> int:
        msgs = sorted(self.messages, key=lambda m: m.position)
        return msgs[0].delay_minutes if msgs else 0

    @property
    def has_incentive(self) -> bool:
        return any(m.has_discount for m in self.messages)

    @property
    def flow_type(self) -> Optional[str]:
        name_lower = self.name.lower()
        for ftype, patterns in CORE_FLOW_PATTERNS.items():
            if any(p in name_lower for p in patterns):
                return ftype
        return None

    @property
    def is_live(self) -> bool:
        return self.status == "Live"

    @classmethod
    def from_dict(cls, d: dict) -> FlowData:
        messages = [FlowMessage.from_dict(m) for m in d.get("messages", [])]
        return cls(
            flow_id=d.get("flow_id", ""),
            name=d.get("name", ""),
            status=d.get("status", "Live"),
            trigger_type=d.get("trigger_type", ""),
            messages=messages,
            revenue=d.get("revenue", 0.0),
            conversion_rate=d.get("conversion_rate", 0.0),
            last_updated_days_ago=d.get("last_updated_days_ago", 0),
        )


@dataclass
class CampaignData:
    total_sent: int = 0
    email_campaigns: int = 0
    sms_campaigns: int = 0
    avg_open_rate: float = 0.0          # 0.0–1.0
    avg_click_rate: float = 0.0
    avg_unsubscribe_rate: float = 0.0
    avg_spam_complaint_rate: float = 0.0
    avg_hard_bounce_rate: float = 0.0
    pct_to_engaged_segments: float = 0.0  # 0.0–1.0
    total_revenue: float = 0.0
    weeks_in_period: int = 52
    longest_gap_days: int = 0
    open_rate_trend: str = "flat"         # improving | flat | declining

    @property
    def campaigns_per_week(self) -> float:
        if self.weeks_in_period == 0:
            return 0.0
        return self.total_sent / self.weeks_in_period

    @classmethod
    def from_dict(cls, d: dict) -> CampaignData:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class FormData:
    form_id: str = ""
    name: str = ""
    form_type: str = "popup"           # popup | flyout | embed | fullpage
    status: str = "Published"
    views: int = 0
    submits: int = 0
    mobile_views: int = 0
    mobile_submits: int = 0
    collects_sms: bool = False
    has_incentive: bool = False

    @property
    def opt_in_rate(self) -> float:
        if self.views == 0:
            return 0.0
        return self.submits / self.views

    @property
    def mobile_opt_in_rate(self) -> float:
        if self.mobile_views == 0:
            return 0.0
        return self.mobile_submits / self.mobile_views

    @classmethod
    def from_dict(cls, d: dict) -> FormData:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class DeliverabilityData:
    hard_bounce_rate: float = 0.0
    soft_bounce_rate: float = 0.0
    spam_complaint_rate: float = 0.0
    avg_unsubscribe_rate: float = 0.0
    has_spf: bool = False
    has_dkim: bool = False
    has_dmarc: bool = False
    has_branded_sending_domain: bool = False
    open_rate_trend: str = "flat"       # improving | flat | declining

    @classmethod
    def from_dict(cls, d: dict) -> DeliverabilityData:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class BenchmarkData:
    open_rate_rating: str = "average"       # poor | below_average | average | good | excellent
    click_rate_rating: str = "average"
    conversion_rate_rating: str = "average"
    flow_revenue_rating: str = "average"
    list_growth_rating: str = "average"

    @property
    def overall_rating(self) -> str:
        ratings = [
            self.open_rate_rating, self.click_rate_rating,
            self.conversion_rate_rating, self.flow_revenue_rating,
        ]
        score_map = {"poor": 1, "below_average": 2, "average": 3, "good": 4, "excellent": 5}
        avg = sum(score_map.get(r, 3) for r in ratings) / len(ratings)
        if avg >= 4.5:
            return "excellent"
        elif avg >= 3.5:
            return "good"
        elif avg >= 2.5:
            return "average"
        elif avg >= 1.5:
            return "below_average"
        return "poor"

    @classmethod
    def from_dict(cls, d: dict) -> BenchmarkData:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class RevenueData:
    total_klaviyo_revenue: float = 0.0
    campaign_revenue: float = 0.0
    flow_revenue: float = 0.0
    revenue_attribution_configured: bool = True
    benchmarks: BenchmarkData = field(default_factory=BenchmarkData)

    @property
    def flow_revenue_pct(self) -> float:
        if self.total_klaviyo_revenue == 0:
            return 0.0
        return self.flow_revenue / self.total_klaviyo_revenue

    @property
    def campaign_revenue_pct(self) -> float:
        if self.total_klaviyo_revenue == 0:
            return 0.0
        return self.campaign_revenue / self.total_klaviyo_revenue

    @classmethod
    def from_dict(cls, d: dict) -> RevenueData:
        benchmarks = BenchmarkData.from_dict(d.get("benchmarks", {}))
        return cls(
            total_klaviyo_revenue=d.get("total_klaviyo_revenue", 0.0),
            campaign_revenue=d.get("campaign_revenue", 0.0),
            flow_revenue=d.get("flow_revenue", 0.0),
            revenue_attribution_configured=d.get("revenue_attribution_configured", True),
            benchmarks=benchmarks,
        )


@dataclass
class BillingData:
    plan_tier: str = "Unknown"
    plan_profile_limit: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> BillingData:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class SegmentationData:
    has_engaged_30_segment: bool = False
    has_engaged_90_segment: bool = False
    has_vip_segment: bool = False
    has_purchaser_segment: bool = False
    has_sunset_segment: bool = False
    pct_campaigns_to_engaged: float = 0.0   # 0.0–1.0

    @classmethod
    def from_dict(cls, d: dict) -> SegmentationData:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class AccountData:
    # Identity
    business_name: str = ""
    website: str = ""
    klaviyo_account_name: str = ""
    audit_period_label: str = "Last 12 months"
    audit_period_days: int = 365
    ecommerce_platform: str = "Shopify"
    monthly_revenue_range: str = ""

    # Core data objects
    sms_enabled: bool = False
    profiles: ProfileMetrics = field(default_factory=ProfileMetrics)
    flows: List[FlowData] = field(default_factory=list)
    campaigns: CampaignData = field(default_factory=CampaignData)
    forms: List[FormData] = field(default_factory=list)
    list_count: int = 0
    segment_count: int = 0
    deliverability: DeliverabilityData = field(default_factory=DeliverabilityData)
    revenue: RevenueData = field(default_factory=RevenueData)
    billing: BillingData = field(default_factory=BillingData)
    segmentation: SegmentationData = field(default_factory=SegmentationData)
    ecommerce_events_configured: bool = True

    # Helpers
    @property
    def live_flows(self) -> List[FlowData]:
        # Include Manual — Klaviyo uses "Manual" for metric-triggered active flows
        return [f for f in self.flows if f.status in ("Live", "Manual")]

    def get_flow(self, flow_type: str) -> Optional[FlowData]:
        for f in self.live_flows:
            if f.flow_type == flow_type:
                return f
        return None

    @property
    def active_forms(self) -> List[FormData]:
        return [f for f in self.forms if f.status == "Published"]

    @property
    def primary_form(self) -> Optional[FormData]:
        published = self.active_forms
        if not published:
            return None
        return max(published, key=lambda f: f.views)

    @classmethod
    def from_dict(cls, d: dict) -> AccountData:
        return cls(
            business_name=d.get("business_name", ""),
            website=d.get("website", ""),
            klaviyo_account_name=d.get("klaviyo_account_name", ""),
            audit_period_label=d.get("audit_period_label", "Last 12 months"),
            audit_period_days=d.get("audit_period_days", 365),
            ecommerce_platform=d.get("ecommerce_platform", "Shopify"),
            monthly_revenue_range=d.get("monthly_revenue_range", ""),
            sms_enabled=d.get("sms_enabled", False),
            profiles=ProfileMetrics.from_dict(d.get("profiles", {})),
            flows=[FlowData.from_dict(f) for f in d.get("flows", [])],
            campaigns=CampaignData.from_dict(d.get("campaigns", {})),
            forms=[FormData.from_dict(f) for f in d.get("forms", [])],
            deliverability=DeliverabilityData.from_dict(d.get("deliverability", {})),
            revenue=RevenueData.from_dict(d.get("revenue", {})),
            billing=BillingData.from_dict(d.get("billing", {})),
            segmentation=SegmentationData.from_dict(d.get("segmentation", {})),
            ecommerce_events_configured=d.get("ecommerce_events_configured", True),
        )


@dataclass
class CategoryScore:
    name: str
    score: int          # 1–10
    weight: float       # 0.0–1.0
    justification: str
    penalties_applied: List[str] = field(default_factory=list)
    bonuses_applied: List[str] = field(default_factory=list)

    @property
    def weighted_points(self) -> float:
        return (self.score / 10) * self.weight * 100


@dataclass
class Finding:
    rule_id: str
    severity: str           # Critical | High | Medium | Low
    category: str
    description: str
    business_impact: str
    recommended_action: str
    priority: str
    score_impact: str = ""
    confidence: str = "Confirmed"

    @property
    def severity_rank(self) -> int:
        return {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}.get(self.severity, 0)


@dataclass
class Recommendation:
    rec_id: str
    source_rules: List[str]
    issue: str
    why_it_matters: str
    expected_impact: str    # High | Medium | Low
    complexity: str         # Easy | Moderate | Complex
    priority: str           # Critical | High | Medium | Low
    owner: str              # NP | Client | Shared
    timeline: str           # Immediate | 30 days | 60 days | 90 days
    confidence: str
    opportunity_note: str
    next_step: str
    priority_score: int = 0


@dataclass
class AuditResult:
    account: AccountData
    category_scores: List[CategoryScore]
    composite_score: int
    score_band: str
    findings: List[Finding]
    recommendations: List[Recommendation]
    data_gaps: List[str] = field(default_factory=list)   # human-readable gap descriptions

    @property
    def critical_findings(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == "Critical"]

    @property
    def high_findings(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == "High"]

    @property
    def top_wins(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == "Positive"][:5]

    @property
    def data_quality_findings(self) -> List[Finding]:
        return [f for f in self.findings if f.category == "Data Quality"]

    @property
    def scoreable_findings(self) -> List[Finding]:
        """Findings excluding data quality notices — used for Section 6 Top Issues."""
        return [f for f in self.findings if f.category != "Data Quality"]
