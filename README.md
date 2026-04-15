# 🍳 OvenOS POS

> **Full-featured TOAST-inspired restaurant POS system** — Built with React + FastAPI + Stripe + Dust AI by Tommy Nation.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Base44-orange?style=for-the-badge)](https://app.base44.com/apps/69bef60ef108d9139d50af30/editor/preview)
[![GitHub Issues](https://img.shields.io/github/issues/TommyNationPol1984/ovenos-pos?style=for-the-badge)](https://github.com/TommyNationPol1984/ovenos-pos/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## 🚀 What Is OvenOS?

OvenOS is a production-ready restaurant Point-of-Sale platform designed to compete directly with TOAST, Square for Restaurants, and Lightspeed — at a fraction of the cost. Built for real operator use with AI-powered demand forecasting, multi-platform delivery integration, and an intuitive tablet-first interface.

**Target Customers:** Full-service restaurants, bars, fast-casual, food trucks, ghost kitchens, hotel F&B.

---

## ✨ Core Features

| Module | Status |
|---|---|
| 🛒 POS — Cart, Modifiers, Tip, Payment | ✅ Live |
| 🍽️ Kitchen Display System (KDS) | ✅ Live |
| 📋 Menu Management | ✅ Live |
| 🗺️ Floor Plan (Drag & Drop) | ✅ Live |
| 📦 Inventory Control Tower | ✅ Live |
| 🛍️ Purchase Orders | ✅ Live |
| 📅 Reservations | ✅ Live |
| 💎 Loyalty & Gift Cards | ✅ Live |
| 👥 Employee Management & Payroll | ✅ Live |
| 📊 Analytics Dashboard | ✅ Live |
| 🤖 AI Insights (Dust API) | ✅ Live |
| 💳 Subscription Billing (Stripe) | ✅ Live |
| 🚗 Delivery Hub (DoorDash/Uber Eats) | 🟡 In Progress |
| 📱 Mobile Fast Order Mode | 🔨 Building |
| 🏢 Multi-Tenant / Multi-Location | ⬜ Phase 4 |
| 📲 React Native App | ⬜ Phase 5 |

---

## 🏗️ Tech Stack

**Frontend:** React + TypeScript + Tailwind CSS + shadcn/ui (via Base44)
**Backend:** FastAPI (Python 3.11) on Replit
**Database:** PostgreSQL via Supabase (11 tables, RLS-ready)
**Auth:** Supabase Auth + RBAC (admin/manager/server/cook/host roles)
**Payments:** Stripe Terminal + Stripe Billing + PayPal
**AI:** Dust API (demand forecasting, shift optimizer, menu mix analysis)
**Receipts:** ESC/POS thermal print + SendGrid email + Twilio SMS
**Deployment:** Docker Compose + GitHub Actions CI/CD

---

## 📂 Repository Structure

```
ovenos-pos/
├── frontend/                  # React + Tailwind (Base44 export)
│   ├── src/pages/             # All 18 pages
│   ├── src/components/        # Shared components
│   └── src/utils/             # formatCurrency, auth, dustClient.ts
├── backend/                   # FastAPI (Python 3.11)
│   ├── main.py                # Entry point, all routers
│   ├── dust_service.py        # Dust API integration
│   ├── receipt_service.py     # Print/email/SMS receipts
│   ├── void_comp_router.py    # Manager PIN, Stripe refund, audit
│   ├── delivery_webhooks.py   # DoorDash + Uber Eats HMAC-verified
│   ├── payroll_service.py     # Clock-in/out, tip pool, OT, CSV export
│   ├── analytics_router.py    # Daily/hourly/top-items/labor cost
│   ├── loyalty_service.py     # Tier engine, earn/redeem
│   └── eod_router.py          # EOD closeout, Z-report, PDF
├── database/                  # Supabase DDL
│   └── schema.sql             # All 11 tables in order
├── docker-compose.yml
├── .env.template
└── README.md
```

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/TommyNationPol1984/ovenos-pos.git
cd ovenos-pos

# 2. Configure environment
cp .env.template .env
# Fill in: SUPABASE_URL, SUPABASE_KEY, STRIPE_SECRET_KEY,
#          DUST_API_KEY, SENDGRID_API_KEY, TWILIO_ACCOUNT_SID

# 3. Run database migrations
# → Paste database/schema.sql into Supabase SQL Editor

# 4. Start backend
cd backend && pip install -r requirements.txt
uvicorn main:app --reload

# 5. Start frontend
cd frontend && npm install && npm run dev

# OR: Docker Compose
docker compose up -d
```

---

## 🤖 Dust AI Integration

OvenOS integrates with Dust.tt for three AI-powered features:

```python
# MCP Heartbeat — verified at startup
POST https://dust.tt/api/v1/w/{DUST_WORKSPACE_ID}/mcp/heartbeat

# Demand Forecast — predicts next 7 days covers by meal period
# Shift Optimizer — generates optimal schedule to minimize labor cost %
# Menu Mix Analysis — Stars/Plowhorses/Puzzles/Dogs per menu engineering
```

**Environment:** `DUST_API_KEY`, `DUST_WORKSPACE_ID`, `DUST_SPACE_ID`

---

## 💰 Pricing Tiers

| Plan | Price | Locations | Features |
|---|---|---|---|
| 🥄 Starter | $59/mo | 1 | Core POS + KDS + Inventory |
| 🍳 Professional | $149/mo | 1-3 | + AI Insights + Delivery Hub |
| 🏆 Enterprise | $349/mo | 4-15 | + Multi-tenant + Payroll |
| 🌐 Enterprise Plus | Custom | Unlimited | + White-label + API access |

---

## 📋 Issue Tracker

| # | Issue | Status |
|---|---|---|
| #1 | Master Build Tracker | 📌 Pinned |
| #3 | Phase 1: Core POS | ✅ Done |
| #4 | Phase 2: AI / Dust | ✅ Done |
| #5 | Phase 3: Delivery Integration | 🟡 In Progress |
| #6 | Phase 4: Multi-Tenant | ⬜ TODO |
| #2 | Phase 5: React Native | ⬜ TODO |
| #7 | Stripe Terminal Modal | 🔨 Building |
| #8 | Demo Mode Seeder | 🔨 Building |
| #9 | Mobile Fast Order Mode | 🔨 Building |
| #10 | Global UI Polish | 🔨 Building |
# OvenOS POS

Full-featured TOAST-inspired restaurant POS — React + FastAPI + Stripe + Dust AI by Tommy Nation.

## Live Demo
https://app.base44.com/apps/69bef60ef108d9139d50af30/editor/preview

## Features
- POS cart, modifiers, tip, Stripe Terminal payment
- Kitchen Display System (bump/recall/station routing)
- Menu management, inventory, purchase orders
- Floor plan (drag and drop), reservations
- Loyalty and gift cards (Bronze to Platinum)
- Employee management, payroll, tip pooling
- AI demand forecast + shift optimizer (Dust API)
- Delivery Hub: DoorDash, Uber Eats, Grubhub
- Analytics dashboard with Recharts
- Subscription billing (Starter $59 / Pro $149 / Enterprise $349)

## Stack
Frontend: React + Tailwind CSS + shadcn/ui (Base44)
Backend: FastAPI Python 3.11 (Replit)
Database: PostgreSQL via Supabase (11 tables)
Auth: Supabase Auth + RBAC
Payments: Stripe Terminal + Stripe Billing
AI: Dust.tt (workspace: tommynationpolitics)
Receipts: ESC/POS + SendGrid + Twilio

## Google Drive Docs
- Architecture: https://docs.google.com/document/d/1DNQ9Tllfc5LQDsYEMmtRUTy83dLk8ofrdvVl8cz69l0/edit
- Progress Tracker: https://docs.google.com/document/d/17FPU-LKeEg3xr6_y7xE1z1-naipEYLYAZyqqIeKqa_o/edit
- Database Schema: https://docs.google.com/document/d/1xoz_kTF1SkeL_5yp6uDderKkN_evVEuAwuVXQ76zoxc/edit
- Frontend Code: https://docs.google.com/document/d/1z99WmTXtC7RRT0QtAHeCGaNqB87AkLMf-pVDeeOP608/edit
- Backend Code: https://docs.google.com/document/d/1_f3pJ9om7YqqhgbIRxU5Mv7Yk6QJiUCcRhMywlv2aHw/edit
- DevOps/Docker: https://docs.google.com/document/d/1FDn09WC_LLH-OGg0NmoDtKa6dU6tpKX54lGxdGk7kk0/edit

## Issues
See https://github.com/TommyNationPol1984/ovenos-pos/issues for full roadmap and build status.

## License
MIT 2026 Tommy Nation| #12 | Database Schema DDL | 📖 Reference |

---

## 🔗 Google Drive Documentation

| Doc | Link |
|---|---|
| 📖 Architecture & README | [Open](https://docs.google.com/document/d/1DNQ9Tllfc5LQDsYEMmtRUTy83dLk8ofrdvVl8cz69l0/edit) |
| 📊 Progress Tracker & Roadmap | [Open](https://docs.google.com/document/d/17FPU-LKeEg3xr6_y7xE1z1-naipEYLYAZyqqIeKqa_o/edit) |
| 🗄️ Database Schema | [Open](https://docs.google.com/document/d/1xoz_kTF1SkeL_5yp6uDderKkN_evVEuAwuVXQ76zoxc/edit) |
| ⚛️ Frontend Codebase | [Open](https://docs.google.com/document/d/1z99WmTXtC7RRT0QtAHeCGaNqB87AkLMf-pVDeeOP608/edit) |
| 🐍 Backend Services | [Open](https://docs.google.com/document/d/1_f3pJ9om7YqqhgbIRxU5Mv7Yk6QJiUCcRhMywlv2aHw/edit) |
| 🐳 Environment, Docker & CI/CD | [Open](https://docs.google.com/document/d/1FDn09WC_LLH-OGg0NmoDtKa6dU6tpKX54lGxdGk7kk0/edit) |

---

## 📜 License

MIT License — Copyright 2026 Tommy Nation / TommyNationPol1984

---

*Built with NationPOSBuilder + TommyNexusAI · April 2026*OvenOS POS — Full-featured TOAST-inspired restaurant POS system by Tommy Nation. React + FastAPI + Stripe + Dust AI.
