<img src="./assets/avatar.png" align="right" width="88" alt="Gabriel Moura" />

# Gabriel Moura

**Software Engineer · Full Stack**

I build and run SaaS products end to end in TypeScript: React and Next.js on the front, Node.js and PostgreSQL on the back, and the parts in between that keep a product running after launch — auth, billing, background jobs, tests, CI and monitoring. Based in Brazil (UTC−3), working remotely.

## What I build

- **SaaS platforms** — multi-tenant data models, workspaces, roles and row-level security
- **APIs** — REST APIs in Node.js (Fastify), validated with Zod, backed by PostgreSQL
- **Real-time features** — Socket.IO and Redis for live state, BullMQ for background work
- **AI integrations** — LLM workflows with OpenAI and Anthropic models, LangGraph orchestration, RAG with pgvector
- **Automation** — queues, scheduled tasks and third-party integrations (payments, tax invoicing, email, file storage)

## Tech stack

| Area | Tools |
|---|---|
| Languages | TypeScript, JavaScript, SQL |
| Frontend | React, Next.js, Tailwind CSS, Zustand, TanStack Query, Framer Motion |
| Backend | Node.js, Fastify, REST APIs, Socket.IO, BullMQ, Zod |
| Data | PostgreSQL, Prisma, Supabase (Auth, RLS, Edge Functions), Redis, pgvector |
| AI | OpenAI API, Anthropic API, LangGraph / LangChain, Vercel AI SDK |
| Auth & billing | Clerk, Supabase Auth, Stripe |
| Testing | Vitest, Playwright, Testing Library |
| Infra & ops | Docker, GitHub Actions, Prometheus, Grafana, Sentry, Railway, Oracle Cloud |

## Featured project — CRN

**Live:** [appcrn.com.br](https://www.appcrn.com.br) (site in Portuguese) · built and run solo

A multi-tenant ERP for brick-and-mortar retailers in Brazil: point of sale, inventory, finance and tax invoicing in one product. Paying customers since late 2023; merchants run about **BRL 2M (~US$380K) in sales and 4,000–8,000 tax invoices a month** through it.

- Replaced the separate tax-invoicing and management systems store owners used with a single product
- Redesigned the hardest areas — tax rules, tax calculation, margin calculation — so owners can run them without specialist help, which cut support requests
- Brought onboarding plus data import down from ~3 hours to ~45 minutes per customer
- React, TypeScript, Supabase/PostgreSQL with row-level security and Edge Functions, plus a Dockerized invoice service on Oracle Cloud that talks directly to Brazil's tax authority (SEFAZ); Vitest, Playwright and GitHub Actions CI

## Featured project — AgentOffice

**Live:** [useagentoffice.com](https://useagentoffice.com) (early access, Portuguese-language market)

**The problem:** using AI at work still means re-explaining your company in every chat, stitching together outputs by hand and having no record of what the model did or where it got its facts.

**What I built:** a SaaS where a team of AI agents researches, writes and analyzes using the company's own context. Documents, Notion and Google Drive form a shared "Company Brain"; agents hand work to each other, a virtual office shows in real time what each one is doing, and nothing is published (for example, to LinkedIn) without human approval. Each workspace's data is isolated, and every task and day has a credit cap.

**Architecture**

```
Next.js (React) ──REST──▶ Fastify API ──▶ PostgreSQL + pgvector (Prisma)
       ▲                       │
       └──── Socket.IO ◀───────┤──▶ Redis ──▶ BullMQ workers
                               │              (task execution, file analysis, RAG indexing)
                               └──▶ LLM providers (OpenAI, Anthropic) via LangGraph
```

- **AI:** multi-agent orchestration with LangGraph across OpenAI and Anthropic models; RAG over files, Notion and Google Drive with pgvector; per-agent memory of user preferences
- **Real-time:** agent state and task events pushed over Socket.IO, with an output guard on what reaches the client
- **Billing:** Stripe subscriptions plus credit packs, per-task and daily credit caps, usage tracked per agent and model; webhook handling covered by tests
- **Auth:** Clerk, synced to the app's users and workspaces through webhooks
- **Quality:** GitHub Actions runs lint, type checks, Vitest suites and builds against a real Postgres/pgvector service; Playwright covers the main web flows
- **Observability:** Prometheus metrics (including BullMQ queue metrics), Grafana dashboards, Sentry

The source is private.

## Other projects

- **[Mini CRM SDR](https://github.com/GabrielMMoura/mini-crm-sdr-ai)** — CRM for sales development teams: Kanban pipeline with per-stage rules, outreach campaigns and AI-generated messages. Supabase with row-level security per workspace; each user's OpenAI key is encrypted (AES-GCM) inside an Edge Function and never returned to the browser. [Live demo](https://mini-crm-sdr-ai-vercel.vercel.app)

## Engineering focus

- Data models first: get tenancy, permissions and constraints right in the database
- API design that is hard to misuse — typed contracts and validation at the boundary
- Authentication and authorization, including row-level security
- Tests around money, permissions and anything async
- Performance where it matters: queues for slow work, caching for repeated work
- Code that the next person (often me, six months later) can change safely

## Contact

[LinkedIn — in/gabrielmouram](https://www.linkedin.com/in/gabrielmouram)
