# Bright Data MCP — Tool Map & Credit Cost per Stage

Server name: **`brightdata`** → tools are exposed as `mcp__brightdata__<tool>`.
Configured via `npx -y @brightdata/mcp` with `PRO_MODE=true` (unlocks the GEO /
AI-query tools). Config: `.claude/settings.local.json` (key is NOT in shared
settings or committed — see `.gitignore`).

> ⚠️ **Verify names at runtime.** Bright Data updates its tool set. Before a run,
> if any tool below isn't present in-session, list the available
> `mcp__brightdata__*` tools and bind to the real ones. **Never call a guessed
> tool name.** The exact GEO tool names below are the ones to confirm first.

## Tiers (what costs what)

| Tier | What it is | Cost implication |
|------|-----------|------------------|
| **Base / free tier** | `search_engine`, `scrape_as_markdown`, `scrape_as_html`, `scrape_batch`, `search_engine_batch`, `discover` | Included in the free tier (rate-limited). Cheap/no per-call credits — use freely. |
| **GEO / Pro (credits)** | The LLM/AI-engine query tools that return how ChatGPT / Perplexity / Google AI Overview answer a query + their citations | **Burns account credits per call.** Use deliberately — batch target queries, don't re-run needlessly. Stage 2 & 4 are the credit-spending stages. |

## Which tool fires at each phase

| Phase | Tool(s) | Tier | Why |
|-------|---------|------|-----|
| **1 — Product intake** | `scrape_as_markdown` on the product URL | Free | Pull the page to extract the product profile (features, use cases, ICP, entities). |
| **2 — Category validation** | none (interactive — AskUserQuestion) | Free | Confirm which topic categories are in scope before spending. |
| **3 — Prompt discovery** | `search_engine` (params: `query`, `engine`=google/bing/yandex, `geo_location`=2-letter country) — call once per category seed (no batch variant in this build) | Free | Harvest live People Also Ask + related searches to ground the 15-20 candidate prompts in real demand. Optionally `discover` for relevance expansion. Ends at the credit checkpoint. |
| **4 — GEO diagnosis at scale** | `web_data_chatgpt_ai_insights` per approved prompt (sequentially) → dedupe cited URLs → `scrape_batch` | GEO = credits; scrape = free | Get each prompt's AI answer + cited URLs, then batch-scrape (**≤5 URLs per call**) the cited pages to read the citation pattern + page type. Perplexity/Grok optional, only on request (each is another paid call per prompt). |
| **5 — Opportunity matrix** | none (scores Phase-4 evidence; helper `score_opportunities.py`) | Free | Pure synthesis: rank prompts by capturability × relevance. |
| **Optional — Capture** | none (uses Phase 1–4 evidence) — optional `scrape_as_markdown` to re-pull a competitor | mostly none | Brief + draft for a chosen opportunity. |
| **Optional — Track** | Same GEO tools (`web_data_*_ai_insights`) as Phase 4 | GEO = credits | Re-run the AI-answer check to see if the user's page is now cited. |

## Confirmed in-session tool names  (verified via tools/list, PRO_MODE=true → 74 tools)

- **Base scrape/search (free tier):** `mcp__brightdata__search_engine`,
  `mcp__brightdata__scrape_as_markdown`, `mcp__brightdata__scrape_as_html`,
  `mcp__brightdata__scrape_batch` (**max 5 URLs**), `mcp__brightdata__extract`,
  `mcp__brightdata__discover`. (Note: no `search_engine_batch` in this build —
  loop `search_engine` per query.)
- **GEO / AI-engine tools (credits):**
  - `mcp__brightdata__web_data_chatgpt_ai_insights` — returns answer text **with
    clickable source URLs** → **primary citation-tracking engine** for GEO.
  - `mcp__brightdata__web_data_perplexity_ai_insights` — answer text, but observed
    to return **no source URLs** (prose only). Use to confirm which brands get
    named, not which page is cited.
  - `mcp__brightdata__web_data_grok_ai_insights` — observed to return **empty
    `[{}]`** on this account. Treat empty as "live data unavailable", don't invent.
  - **No Claude tool** and **no Google AI Overview tool** exist in this set.
  - **Call GEO tools sequentially** — parallel calls cause transient
    `HTTP 400: Customer is not active`; a sequential retry succeeds.
- **Other useful structured tools (credits):** `web_data_google_shopping`,
  `web_data_youtube_videos`, `web_data_reddit_posts`, etc. — not needed for the
  core GEO flow but available.
- Input shapes: `search_engine{query, engine?, geo_location?}` ·
  `scrape_batch{urls[≤5]}` · `web_data_*_ai_insights{prompt}`.

## Cost-safety rules
- Stage 1 and scraping are free — run them generously.
- Treat each GEO/AI-query call as a metered request: cap target queries (2–3),
  dedupe before scraping, and never loop a GEO call to "double-check."
- If a GEO call fails, report it (`⚠️ Live data unavailable`) — do **not**
  substitute training-data knowledge of who "usually" gets cited.
