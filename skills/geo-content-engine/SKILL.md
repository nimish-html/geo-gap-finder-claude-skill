---
name: geo-content-engine
description: >
  Live-data SEO + GEO (Generative Engine Optimization) content research engine,
  powered by the Bright Data MCP. Pulls REAL Google SERPs, People Also Ask,
  related searches, and the actual answers + citations that ChatGPT, Perplexity,
  and Google AI Overviews return today — then reverse-engineers why specific
  pages get cited and turns that evidence into a content brief and draft.

  Every recommendation is grounded in something just scraped. Nothing comes from
  training-data memory. Sources are always cited.

  Trigger whenever the user mentions: SEO, GEO, AI search visibility, getting
  cited by ChatGPT / Perplexity / Google AI Overviews / AI search, keyword or
  SERP research, "what's ranking for X", content briefs, "why isn't my site
  showing up in AI answers", competitor citation analysis, or tracking AI
  citations over time. Also trigger on "/geo-content-engine", "research GEO for
  <topic>", "build me a content brief for <topic>", or "reverse-engineer AI
  citations for <query>".
user-invocable: true
argument-hint: "<topic or query> [--stage 1|2|3|4]"
allowed-tools: Bash, Read, Write, mcp__brightdata__search_engine, mcp__brightdata__scrape_as_markdown, mcp__brightdata__scrape_batch, mcp__brightdata__discover, mcp__brightdata__web_data_chatgpt_ai_insights, mcp__brightdata__web_data_perplexity_ai_insights, mcp__brightdata__web_data_grok_ai_insights
---

# GEO Content Engine

A 4-stage research pipeline that grounds **every** SEO + GEO recommendation in
**live data scraped right now** via the **Bright Data MCP** (server name:
`brightdata`). It exists to defeat the #1 objection to AI-generated SEO advice —
*"the AI just hallucinates"* — so the prime directive is non-negotiable:

> **NO-FABRICATION RULE.** Never state a keyword, ranking, competitor, citation,
> metric, or "best practice" unless it came from a live tool call in THIS run.
> If a live call fails or returns nothing, write **"⚠️ Live data unavailable for
> this step"** and stop that step. Do not fill the gap from memory. Do not invent
> search volumes, citation counts, or URLs. Every output ends with a **Sources**
> section listing the exact URLs/queries it pulled.

## Prerequisites (check first)

1. The `brightdata` MCP server must be connected. Confirm `mcp__brightdata__*`
   tools are available in this session. If they are **not**, tell the user:
   *"The Bright Data MCP isn't loaded in this session. Config lives in
   `.claude/settings.local.json`; reconnect/restart Claude Code, then re-run."*
   Do not attempt the stages without it.
2. Before the first run, skim `references/tool-map.md` to use the **real** tool
   names + know which tier (free vs. credits) each call burns. If a tool name in
   that file doesn't exist in-session, list the actual `mcp__brightdata__*` tools
   and use those — never guess a tool name.

## How to invoke

- **Whole pipeline:** "research GEO for `<topic>`" → run Stage 1 → 2 → 3 (Stage 4
  is on-demand later).
- **A single stage:** pass `--stage N`, or just ask ("just do the SERP research
  for `<topic>`", "reverse-engineer who ChatGPT cites for `<query>`", "write the
  brief", "re-check my citations").
- Each stage is self-contained: it reads any prior stage's saved Markdown from
  `geo-research/<topic-slug>/` if present, otherwise runs what it needs itself.

## Output location

Write all artifacts as clean Markdown a non-technical business owner can read,
under the user's current directory:

```
geo-research/<topic-slug>/
├── stage1-intent-map.md
├── stage2-geo-diagnosis.md
├── stage3-brief.md
├── stage3-draft.md
└── stage4-tracking-<date>.md
```

Announce the file path after writing each one.

---

## STAGE 1 — Demand & SERP Research

**Goal:** a grounded map of what's actually searched and ranking *today*.

1. From the seed topic, derive 3–6 query variants (the seed, question forms,
   commercial modifiers like "best/vs/pricing"). State the list you chose.
2. For each variant fire **`mcp__brightdata__search_engine`** (`query`,
   `engine: "google"`, optional `geo_location` 2-letter country). Call it once
   per query (this build has no batch variant). Capture from the live SERP:
   organic results (title + URL + snippet), **People Also Ask**, **related
   searches**, and any AI Overview block present.
3. Cluster everything into intent groups. Pipe the collected results through the
   helper:
   ```bash
   python3 scripts/cluster_serp.py < serp.json
   ```
   (or cluster inline if the script errors — it's only a convenience). Groups:
   informational / commercial-investigation / transactional / navigational.
4. Write `stage1-intent-map.md`: a table of clusters → representative queries →
   who currently ranks (real URLs) → the user-facing question each answers.
   Flag which queries are the strongest GEO targets (question-shaped, answer-led).

**Output ends with Sources:** every SERP query run + result URLs referenced.

---

## STAGE 2 — GEO Reverse-Engineering  *(the hero)*

**Goal:** diagnose *why* specific competitors get cited in AI search for a query,
and what the user is missing.

1. Pick 2–3 target queries (from Stage 1, or ask the user). For each, call the
   Bright Data **GEO tools** that query an AI engine directly, passing the query
   as `prompt`:
   - `mcp__brightdata__web_data_chatgpt_ai_insights` — returns answer text **plus
     explicit citations** (best for "who gets cited").
   - `mcp__brightdata__web_data_perplexity_ai_insights` — answer + inline sources.
   - `mcp__brightdata__web_data_grok_ai_insights` — answer text (markdown).
   Run at least the ChatGPT one; add Perplexity/Grok for cross-engine coverage.
   For **Google AI Overview**, there is no dedicated tool — capture the AI
   Overview block from the `search_engine` result if one is present, else say so.
   There is **no Claude tool** in the Bright Data set. Capture: the answer text
   and the **cited source URLs** from each engine.
   - **Fire these GEO calls one at a time (sequentially).** Parallel calls trigger
     transient `HTTP 400: Customer is not active` — a sequential retry succeeds.
   - **Engine behavior (observed):** ChatGPT returns answers **with clickable
     source URLs** → use it as the primary citation-tracking engine. Perplexity
     returns prose but often **no source URLs** → use it to confirm *which brands*
     get named, not *which page*. Grok may return empty `[{}]` → if so, mark
     "⚠️ Live data unavailable for Grok" and move on; never invent its answer.
2. Collect the cited URLs across queries (dedupe). Scrape them with
   **`mcp__brightdata__scrape_batch`** as Markdown — **max 5 URLs per call**, so
   batch in groups of 5 if there are more.
3. For each cited page, extract the **citation pattern** using the checklist in
   `references/geo-citation-patterns.md`: content structure (headings/answer
   placement), schema/markup, entity coverage, format (lists/tables/FAQ), depth,
   freshness/date signals, source authority.
4. Write `stage2-geo-diagnosis.md`: per target query, a table of *cited page →
   what it does that earns the citation*; then a synthesis of the **common
   pattern**; then a **"what yours is missing"** gap list (only if the user gave
   their URL — scrape it and compare; otherwise say comparison needs their URL).

**Output ends with Sources:** the AI queries run + every cited URL scraped.

---

## STAGE 3 — Content Creation

**Goal:** a brief + draft optimized for classic ranking AND AI citability, every
element traceable to Stage 1–2 evidence.

1. Build an evidence bundle (target query, cited competitors + their winning
   patterns, the entities/subtopics they all cover, schema types observed,
   PAA questions to answer verbatim).
2. Generate the brief with `templates/content-brief.md` as the skeleton:
   ```bash
   python3 scripts/format_brief.py evidence.json
   ```
   or fill the template inline. The brief must include: target query + intent,
   recommended title/H1, H2/H3 outline mapped to PAA + entities, a "direct
   answer" block (≤ 60 words, citation-extractable) for the head query,
   FAQ/schema (FAQPage/Article/HowTo as the evidence supports), entity checklist,
   and internal-link/source notes. Each recommendation cites which scraped
   competitor/PAA it came from.
3. Draft the article to that brief: clear H2/H3s, a direct answer up top under
   each question, lists/tables where the cited winners used them, factual and
   skimmable. Mark any spot needing a real stat the user must supply as
   `[NEEDS SOURCE: …]` — never invent the number.

**Output:** `stage3-brief.md` and `stage3-draft.md`, each ending with the Stage
1–2 Sources it was built from.

---

## STAGE 4 — Tracking *(optional kicker)*

**Goal:** see whether the user's own page starts getting cited.

1. Re-run Stage 2's GEO check on the same target queries.
2. Compare against the prior `stage2-geo-diagnosis.md` / last tracking file:
   is the user's domain now cited? did competitors change? Output a simple
   before/after table (date, query, was-cited?, position in answer, notable new
   competitors).
3. Write `stage4-tracking-<date>.md`. Keep it skimmable: "✅ now cited" /
   "❌ still not cited, here's the nearest gap from Stage 2".

**Output ends with Sources:** the AI queries re-run on this date.

---

## Style for all outputs
- Plain language, short sentences, tables over walls of text.
- Lead with the takeaway, then the evidence.
- Always close with **Sources** (real URLs + the live queries used). If a section
  has no live source, it doesn't belong in the output.
