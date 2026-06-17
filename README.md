# geo-content-engine

A Claude Code skill that does **live SEO + GEO (Generative Engine Optimization) research** — powered by the Bright Data MCP. Every ranking, citation, and recommendation is grounded in data scraped in real time. No hallucinated metrics. No training-data guesses. Every output cites its source URL.

> This skill was built and demoed live in [this YouTube video](#). Follow the steps below to install it yourself in under 5 minutes.

---

## What it does

Runs a 4-stage research pipeline on any topic or keyword:

| Stage | What it produces |
|-------|-----------------|
| **1 — SERP Research** | Live Google results, People Also Ask, related searches → intent-cluster map |
| **2 — GEO Diagnosis** | Queries ChatGPT + Perplexity directly, captures which pages they cite and *why* — then diffs against your own page |
| **3 — Content Brief & Draft** | Brief + full draft optimized for classic ranking AND AI citation, every recommendation traceable to Stage 1–2 evidence |
| **4 — Tracking** | Re-runs the GEO check on demand to measure whether your page starts getting cited |

---

## Prerequisites

- **Claude Code** (CLI) — [install guide](https://docs.anthropic.com/en/docs/claude-code)
- **Node.js 18+** (`node --version` to check) — needed to run the Bright Data MCP via `npx`
- **A Bright Data account** with an API token and **PRO_MODE enabled** (the GEO / AI-query tools are a paid add-on)
  - Sign up at [brightdata.com](https://brightdata.com)
  - Get your API token from the Bright Data dashboard → Account → API Token
  - Make sure your plan includes the **Web Data / AI Insights** product group (this enables the ChatGPT/Perplexity query tools)

---

## Installation (5 steps)

### 1. Clone the repo

```bash
git clone https://github.com/nimish-html/full-geo-claude-skill.git
cd full-geo-claude-skill
```

### 2. Configure Bright Data MCP

Copy the example config and fill in your token:

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

> **Important:** Paste the raw token directly. Claude Code does **not** expand `${ENV_VAR}` syntax inside `.mcp.json` — if you use that form the server will get the literal string and return HTTP 401.

`.mcp.json` is already in `.gitignore` so your token will never be committed.

### 3. Restart Claude Code

MCP servers load at startup. After saving `.mcp.json`, fully restart Claude Code (quit and reopen) so the `brightdata` tools appear in-session.

### 4. Install the skill via Claude Code plugin

Inside Claude Code, run:

```
/plugin marketplace add nimish-html/full-geo-claude-skill
```

Then:
1. Select **Browse and install plugins**
2. Select **full-geo-claude-skill**
3. Select **geo-content-engine**
4. Select **Install now**

Or install directly from the Claude Code terminal:

```bash
ln -s "$(pwd)/skills/geo-content-engine" ~/.claude/skills/geo-content-engine
```

### 5. Run it

```
/geo-content-engine best CRM for small business
```

Or just describe what you want and Claude will pick it up:

```
Research GEO for "best project management tool for agencies"
```

```
Run stage 2 only for "iso 20022 address resolution" — my page is https://example.com/page
```

---

## Usage

```
/geo-content-engine <topic or keyword> [--stage 1|2|3|4]
```

- **No `--stage` flag** → runs Stage 1 → 2 → 3 in sequence
- **`--stage 1`** → SERP research only (free, no credits)
- **`--stage 2`** → GEO citation diagnosis (costs Bright Data credits)
- **`--stage 3`** → Content brief + draft from existing Stage 1–2 output
- **`--stage 4`** → Re-run GEO check to track citation progress

All outputs are saved as Markdown under `geo-research/<topic-slug>/` in your current directory.

---

## Cost & credit notes

| Tool | Tier | Cost |
|------|------|------|
| `search_engine` (Google SERP) | Free | No credits |
| `scrape_as_markdown` / `scrape_batch` | Free | No credits |
| `web_data_chatgpt_ai_insights` | Pro | Burns credits per call |
| `web_data_perplexity_ai_insights` | Pro | Burns credits per call |
| `web_data_grok_ai_insights` | Pro | Burns credits per call |

Stage 1 and scraping are free-tier — run them as much as you like. Each GEO call (Stage 2 & 4) costs credits; the skill caps at 2–3 queries per run.

---

## Known quirks (from live testing)

- **Grok** returns empty `[{}]` on most accounts — the skill marks this as "live data unavailable" and moves on. Not a bug in the skill.
- **Perplexity** returns prose answers but often no clickable source URLs. Use it to see *which brands get named*, not *which page is cited*.
- **ChatGPT** returns answers with explicit cited URLs — it's the primary citation-tracking engine.
- **Fire GEO calls one at a time.** Parallel calls trigger `HTTP 400: Customer is not active`. The skill does this automatically; don't modify it to run them in parallel.
- **Claude and Google AI Overview** have no dedicated Bright Data tools. The skill captures any AI Overview block that appears in the `search_engine` result.

---

## File structure

```
full-geo-claude-skill/
├── skills/
│   └── geo-content-engine/
│       ├── SKILL.md                    # skill instructions + 4-stage workflow
│       ├── references/
│       │   ├── tool-map.md             # which Bright Data tool per stage + credit tiers
│       │   └── geo-citation-patterns.md # what makes content get cited by AI engines
│       ├── scripts/
│       │   ├── cluster_serp.py         # SERP → intent clusters (stdlib Python, no pip)
│       │   └── format_brief.py         # evidence → content brief (stdlib Python, no pip)
│       └── templates/
│           └── content-brief.md        # brief skeleton
├── .mcp.json.example                   # safe config template (copy → .mcp.json)
├── .gitignore                          # keeps your API token out of git
└── README.md
```

---

## License

MIT — use it, fork it, build on it.
