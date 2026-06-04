export type ScoreBand = "Elite" | "Strong" | "Average" | "Weak" | "Critical";
export type Severity = "Critical" | "High" | "Medium" | "Low";
export type Impact = "High" | "Medium" | "Low";
export type Timeline = "Immediate" | "30 days" | "60 days" | "90 days";

export interface CategoryScore {
  name: string;
  score: number;
  weight: number;
  weighted_points: number;
  justification: string;
  penalties: string[];
  bonuses: string[];
}

export interface Finding {
  rule_id: string;
  severity: Severity;
  category: string;
  description: string;
  business_impact: string;
  recommended_action: string;
  priority: string;
  score_impact: string;
  confidence: string;
}

export interface Recommendation {
  rec_id: string;
  source_rules: string[];
  issue: string;
  why_it_matters: string;
  expected_impact: Impact;
  complexity: string;
  priority: string;
  owner: string;
  timeline: Timeline;
  confidence: string;
  opportunity_note: string;
  next_step: string;
  priority_score: number;
}

export interface OpportunityRange {
  conservative: string;
  moderate: string;
  optimistic: string;
  basis: string;
  disclaimer: string;
}

export interface ProfileMetrics {
  total_profiles: number;
  emailable_profiles: number;
  sms_consented_profiles: number;
  suppressed_profiles: number;
  suppression_rate: number;
  engaged_30_day: number;
  engaged_90_day: number;
  engaged_30_pct: number;
  engaged_90_pct: number;
  dormant_profiles: number;
  dormant_rate: number;
}

export interface CampaignMetrics {
  total_sent: number;
  email_campaigns: number;
  sms_campaigns: number;
  campaigns_per_week: number;
  avg_open_rate: number;
  avg_click_rate: number;
  avg_unsubscribe_rate: number;
  avg_spam_complaint_rate: number;
  avg_hard_bounce_rate: number;
  pct_to_engaged_segments: number;
  longest_gap_days: number;
  open_rate_trend: string;
}

export interface DeliverabilityData {
  hard_bounce_rate: number;
  soft_bounce_rate: number;
  spam_complaint_rate: number;
  avg_unsubscribe_rate: number;
  has_spf: boolean;
  has_dkim: boolean;
  has_dmarc: boolean;
  has_branded_sending_domain: boolean;
  open_rate_trend: string;
}

export interface FlowSummary {
  name: string;
  status: string;
  flow_type: string | null;
  email_count: number;
  sms_count: number;
  revenue: number;
  has_incentive: boolean;
  first_message_delay_minutes: number;
  last_updated_days_ago: number;
}

export interface FormSummary {
  name: string;
  form_type: string;
  status: string;
  opt_in_rate: number;
  mobile_opt_in_rate: number;
  collects_sms: boolean;
  has_incentive: boolean;
  views: number;
  submits: number;
}

export interface SegmentationData {
  has_engaged_30_segment: boolean;
  has_engaged_90_segment: boolean;
  has_vip_segment: boolean;
  has_purchaser_segment: boolean;
  has_sunset_segment: boolean;
  pct_campaigns_to_engaged: number;
  list_count?: number;
  segment_count?: number;
}

export interface RevenueData {
  total_klaviyo_revenue: number;
  campaign_revenue: number;
  flow_revenue: number;
  flow_revenue_pct: number;
  revenue_attribution_configured: boolean;
  benchmark_overall: string;
}

export interface AuditReport {
  account: {
    business_name: string;
    website: string;
    klaviyo_account_name: string;
    audit_period_label: string;
    ecommerce_platform: string;
    monthly_revenue_range: string;
    sms_enabled: boolean;
  };
  composite_score: number;
  score_band: ScoreBand;
  category_scores: CategoryScore[];
  findings: Finding[];
  recommendations: Recommendation[];
  opportunity: OpportunityRange | null;
  data_gaps: string[];
  profile_metrics: ProfileMetrics;
  campaign_metrics: CampaignMetrics;
  deliverability: DeliverabilityData;
  revenue: RevenueData;
  flows: FlowSummary[];
  forms: FormSummary[];
  segmentation: SegmentationData;
  billing: { plan_tier: string; plan_profile_limit: number };
}

export interface AuditStatus {
  audit_id: string;
  status: "pending" | "running" | "complete" | "error";
  composite_score?: number;
  score_band?: ScoreBand;
  business_name?: string;
  error?: string;
  progress?: number;       // 0–100
  current_step?: string;
}
