# geo-opportunity-finder

A Claude Code skill that finds the **AI-search prompts your product can actually win** — then proves it with live data. Powered by the Bright Data MCP.

Most SEO tools tell you how to rank for a keyword you already picked. This one answers the question that comes *first*: **which battles are even worth fighting?** Give it your product and it scans 15-20 real prompts people search, checks who ChatGPT cites for each one, and ranks them by how easy each is to capture — the prompts where ChatGPT cites nobody, cites something irrelevant, or cites a page you could easily out-build.

Every prompt, citation, and score is grounded in something scraped live. No hallucinated metrics. No training-data guesses. Every output cites its source.

> Built and demoed live in [this YouTube video](#). Install it yourself in under 5 minutes below.

---

## What it does — 5 phases

| Phase | What happens | Spends credits? |
|-------|--------------|:--:|
| **1 — Product Intake** | Drop a URL + one sentence. It scrapes your page and builds a product profile (features, use cases, ICP, the entities you own). | No |
| **2 — Category Validation** | It proposes the topic angles your product could win, and asks you to confirm which are in scope. | No |
| **3 — Prompt Discovery** | Generates ~15-20 real long-tail prompts, grounded in live People Also Ask + related searches. **Shows you the list to approve before spending anything.** | No |
| **4 — GEO Diagnosis** | For each approved prompt, asks ChatGPT directly, captures who it cites, scrapes those pages, and reads *why* they got cited. | **Yes** |
| **5 — Opportunity Matrix** | Ranks every prompt by **capturability × relevance** and tells you which to go after first, with the exact capture move. | No |

**Then, optionally:** pick a winning prompt and it writes the content brief + draft to capture it, or re-runs the check later to track whether your page starts getting cited.

### What counts as an opportunity

| Citation situation | Opportunity |
|---|---|
| 🟢 ChatGPT cites **nobody** (answers from memory) | Highest — any solid page can become *the* source |
| 🟢 Cites something **irrelevant** | High — out-answer it on the exact intent |
| 🟡 Cites a **recreatable** page (blog, listicle, product page, Q&A, Reddit) | Medium — build a better version |
| 🔴 Cites **docs / Wikipedia / standards / top brands** | Low — long authority game |
| ⚪ Cites **your own** domain | Defend, don't capture |

---

## Prerequisites

- **Claude Code** (CLI) — [install guide](https://docs.anthropic.com/en/docs/claude-code)
- **Node.js 18+** (`node --version`) — runs the Bright Data MCP via `npx`
- **A Bright Data account** with an API token and **PRO_MODE enabled** (the GEO / AI-Insights tools are a paid add-on)
  - Sign up at [brightdata.com](https://brightdata.com)
  - Get your token from the dashboard → Account → API Token
  - Make sure your plan includes the **Web Data / AI Insights** product group (this enables the ChatGPT citation tool)

---

## Installation (5 steps)

### 1. Clone the repo

```bash
git clone https://github.com/nimish-html/geo-gap-finder-claude-skill.git
cd geo-gap-finder-claude-skill
```

### 2. Configure Bright Data MCP

```bash
cp .mcp.json.example .mcp.json
```

Open `.mcp.json` and replace `YOUR_BRIGHTDATA_API_TOKEN_HERE` with your real token:

```json
{
  "mcpServers": {
    "brightdata": {
      "command": "npx",
      "args": ["-y", "@brightdata/mcp"],
      "env": {
        "API_TOKEN": "paste-your-token-here",
        "PRO_MODE": "true"
      }
    }
  }
}
```

> **Important:** Paste the raw token directly. Claude Code does **not** expand `${ENV_VAR}` syntax inside `.mcp.json` — if you use that form the server gets the literal string and returns HTTP 401.

`.mcp.json` is gitignored, so your token never gets committed.

### 3. Restart Claude Code

MCP servers load at startup. After saving `.mcp.json`, fully quit and reopen Claude Code so the `brightdata` tools appear.

### 4. Install the skill

Inside Claude Code:

```
/plugin marketplace add nimish-html/geo-gap-finder-claude-skill
```

Then **Browse and install plugins** → **geo-gap-finder-claude-skill** → **geo-opportunity-finder** → **Install now**.

Or symlink it directly:

```bash
ln -s "$(pwd)/skills/geo-opportunity-finder" ~/.claude/skills/geo-opportunity-finder
```

### 5. Run it

```
/geo-opportunity-finder https://yourproduct.com
```

Or just describe it:

```
Find GEO opportunities for my product — https://yourproduct.com, it's an X for Y
```

---

## Usage

```
/geo-opportunity-finder <product URL or description> [--phase intake|categories|prompts|diagnose|matrix]
```

- **No `--phase`** → runs the whole flow, pausing for your input at Phase 2 and at the credit checkpoint in Phase 3.
- **`--phase prompts`** → just (re)generate the candidate prompt list (free).
- **`--phase diagnose`** → run the GEO citation check on an approved prompt list (costs credits).
- **`--phase matrix`** → score and rank from an existing diagnosis.

All outputs save as Markdown under `opportunity-research/<product-slug>/` in your current directory. The hero file is `05-opportunity-matrix.md`.

---

## Cost & credit notes

| Tool | Tier | Cost |
|------|------|------|
| `scrape_as_markdown` (your page) | Free | No credits |
| `search_engine` (PAA / related) | Free | No credits |
| `scrape_batch` (cited pages) | Free | No credits |
| `web_data_chatgpt_ai_insights` | Pro | **One paid call per prompt** |

Phases 1-3 and 5 are free. Only Phase 4 spends credits — one ChatGPT call per approved prompt. The skill always shows you the prompt list and waits for approval before spending, so you control the bill.

---

## Honest limitations

This Bright Data account has **no keyword search-volume tool and no domain-authority metric**. So:
- "Demand" is a **proxy** — whether a query shows up in People Also Ask / related searches, not an absolute monthly volume.
- "Authority" of cited domains is a **proxy** — recognizability + organic SERP rank, not a real DA score.

The skill labels these as proxies in every output and never invents a number. If you want true volume/DA, bolt on a paid tool like Ahrefs or Semrush separately.

## Known quirks (from live testing)

- **ChatGPT** returns answers with explicit cited URLs — it's the primary (default) engine.
- **Perplexity** returns prose but often no source URLs — optional, use to see *which brands* get named.
- **Grok** returns empty `[{}]` on most accounts — the skill marks it "live data unavailable" and moves on.
- **Fire GEO calls sequentially.** Parallel calls trigger `HTTP 400: Customer is not active`. The skill does this automatically.

---

## File structure

```
geo-gap-finder-claude-skill/
├── skills/
│   └── geo-opportunity-finder/
│       ├── SKILL.md                     # the 5-phase opportunity-finder workflow
│       ├── references/
│       │   ├── opportunity-scoring.md   # capturability × relevance rubric
│       │   ├── geo-citation-patterns.md # why a page gets cited by AI engines
│       │   └── tool-map.md              # which Bright Data tool per phase + tiers
│       ├── scripts/
│       │   ├── cluster_serp.py          # SERP → intent clusters (stdlib, no pip)
│       │   ├── score_opportunities.py   # diagnosis → ranked opportunity matrix
│       │   └── format_brief.py          # evidence → content brief (capture step)
│       └── templates/
│           └── content-brief.md
├── .mcp.json.example                    # safe config template (copy → .mcp.json)
├── .gitignore                           # keeps your API token out of git
└── README.md
```

---

## License

MIT — use it, fork it, build on it.
