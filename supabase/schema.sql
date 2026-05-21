-- Klaviyo Audit Katie — Supabase Schema
-- Run this in the Supabase SQL editor to set up the database.

-- ── Audits table ──────────────────────────────────────────────────────────
create table if not exists audits (
  id              uuid primary key default gen_random_uuid(),
  created_at      timestamptz not null default now(),
  status          text not null default 'pending'
                    check (status in ('pending', 'running', 'complete', 'error')),
  business_name   text,
  website         text,
  composite_score int,
  score_band      text,
  report_data     jsonb,          -- full serialized AuditResult
  error_message   text
);

-- Index for polling queries
create index if not exists audits_status_idx on audits (status);
create index if not exists audits_created_at_idx on audits (created_at desc);

-- ── Leads table ───────────────────────────────────────────────────────────
create table if not exists leads (
  id               uuid primary key default gen_random_uuid(),
  created_at       timestamptz not null default now(),
  audit_id         uuid references audits (id) on delete set null,
  first_name       text,
  last_name        text,
  email            text not null,
  company          text,
  website          text,
  revenue_range    text,
  platform         text,
  biggest_challenge text,
  lead_score       int,
  lead_tier        text,          -- Hot | Warm | Nurture | Low
  cta_clicked      boolean default false,
  calendly_booked  boolean default false,
  notes            text
);

create index if not exists leads_audit_id_idx on leads (audit_id);
create index if not exists leads_lead_tier_idx on leads (lead_tier);
create index if not exists leads_created_at_idx on leads (created_at desc);

-- ── Row Level Security ────────────────────────────────────────────────────
-- Reports are readable by anyone with the audit_id (UUID is the secret)
alter table audits enable row level security;

create policy "audits_select_by_id"
  on audits for select
  using (true);   -- UUID acts as the secret; no auth required to view

-- Inserts and updates only via service key (server-side FastAPI)
create policy "audits_insert_service_only"
  on audits for insert
  with check (auth.role() = 'service_role');

create policy "audits_update_service_only"
  on audits for update
  using (auth.role() = 'service_role');

-- Leads: NP internal only (requires auth)
alter table leads enable row level security;

create policy "leads_np_only"
  on leads for all
  using (auth.role() = 'service_role');

-- ── Helper view ───────────────────────────────────────────────────────────
-- Quick overview for NP team dashboard
create or replace view audit_summary as
select
  a.id,
  a.created_at,
  a.status,
  a.business_name,
  a.website,
  a.composite_score,
  a.score_band,
  l.email,
  l.lead_tier,
  l.lead_score
from audits a
left join leads l on l.audit_id = a.id
order by a.created_at desc;
