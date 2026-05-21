# Deployment Guide — Klaviyo Audit Katie

## Architecture

```
Browser → Vercel (Next.js) → Railway (FastAPI) → Supabase (Postgres)
```

---

## 1. Supabase (Database)

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run the contents of `supabase/schema.sql`
3. Note your:
   - Project URL: `https://xxxx.supabase.co`
   - `anon` public key (for Next.js)
   - `service_role` secret key (for FastAPI — never expose client-side)

---

## 2. Railway (FastAPI Backend)

1. Install Railway CLI: `npm i -g @railway/cli` then `railway login`
2. From the project root:
   ```bash
   railway init
   railway up
   ```
3. Set environment variables in Railway dashboard:
   ```
   SUPABASE_URL=https://xxxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   ```
4. Note your Railway public URL (e.g. `https://katie-api.railway.app`)

The `nixpacks.toml` handles install + start automatically.

---

## 3. Vercel (Next.js Frontend)

1. Push the repo to GitHub
2. Import the project in [vercel.com](https://vercel.com) — set **Root Directory** to `web/`
3. Set environment variables:
   ```
   AUDIT_API_URL=https://katie-api.railway.app
   NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
   ```
4. Deploy — Vercel auto-detects Next.js

---

## 4. Local Development

```bash
# Terminal 1 — FastAPI backend
cd klaviyo-audit-agent
pip install -r api/requirements.txt
uvicorn api.main:app --reload --port 8000

# Terminal 2 — Next.js frontend
cd web
cp .env.local.example .env.local   # fill in values
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Without Supabase (in-memory mode)
Leave `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` unset.  
The FastAPI backend falls back to an in-memory dict — audits are lost on restart, perfect for local testing.

---

## 5. Environment Variable Reference

| Variable | Where | Required | Description |
|---|---|---|---|
| `SUPABASE_URL` | Railway | No* | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Railway | No* | Service role key for writes |
| `AUDIT_API_URL` | Vercel | Yes | Railway backend URL |
| `NEXT_PUBLIC_SUPABASE_URL` | Vercel | No* | Supabase URL for browser client |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Vercel | No* | Supabase anon key for browser |
| `NEXT_PUBLIC_APP_URL` | Vercel | No | Canonical app URL |

*Falls back to in-memory / degraded mode if not set.
