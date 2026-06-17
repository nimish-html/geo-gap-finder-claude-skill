---
name: geo-opportunity-finder
description: >
  Live-data GEO (Generative Engine Optimization) opportunity finder, powered by
  the Bright Data MCP. Give it your product and it runs deep research to find the
  AI-search prompts you can actually WIN — the prompts where ChatGPT cites nobody,
  cites something irrelevant, or cites a page you could easily beat. It profiles
  your product, validates which topics are in scope, discovers 15-20 real long-tail
  prompts people are searching, runs live GEO citation diagnosis on each, then
  ranks them into an opportunity matrix scored by how easy each one is to capture.

  Every prompt, citation, and score is grounded in something scraped live in this
  run. Nothing comes from training-data memory. Sources are always cited. Search
  volume and domain authority are labeled as PROXIES (no such metric exists in this
  data source) — never invented numbers.

  Trigger whenever the user wants to: find GEO / AI-search opportunities for their
  product, figure out "where can I rank in AI search", "which prompts should I
  target", "what AI-search gaps can my product fill", "where does ChatGPT cite
  nobody for my space", find winnable long-tail prompts, or do GEO competitor /
  citation gap analysis. Also trigger on "/geo-opportunity-finder <product url>",
  "find GEO opportunities for <product>", or "what AI prompts can <product> win".
  After an opportunity is chosen, can optionally produce the content brief + draft
  to capture it.
user-invocable: true
argument-hint: "<product URL or description> [--phase intake|categories|prompts|diagnose|matrix]"
allowed-tools: Bash, Read, Write, mcp__brightdata__search_engine, mcp__brightdata__scrape_as_markdown, mcp__brightdata__scrape_batch, mcp__brightdata__discover, mcp__brightdata__web_data_chatgpt_ai_insights, mcp__brightdata__web_data_perplexity_ai_insights, mcp__brightdata__web_data_grok_ai_insights
---

# GEO Opportunity Finder

A guided, multi-phase deep-research flow whose whole purpose is to find the
**AI-search prompts your product can actually win** — and prove each one is
winnable with **live data scraped right now** via the **Bright Data MCP** (server
name: `brightdata`). It exists to defeat the #1 objection to AI-generated SEO/GEO
advice — *"the AI just hallucinates"* — so the prime directive is non-negotiable:

> **NO-FABRICATION RULE.** Never state a prompt, ranking, competitor, citation,
> metric, or "best practice" unless it came from a live tool call in THIS run. If
> a live call fails or returns nothing, write **"⚠️ Live data unavailable for this
> step"** and stop that step. Do not fill the gap from memory. Do not invent search
> volumes, citation counts, domain-authority scores, or URLs. **Search volume and
> domain authority do not exist in this data source — treat any demand/authority
> read as a labeled PROXY** (People Also Ask / related presence; organic SERP rank
> + recognizability). Every output ends with a **Sources** section listing the
> exact URLs/queries it pulled.

## The big idea

Most SEO tools tell you how to rank for a keyword you already picked. This skill
answers the question that comes *first*: **which battles are even worth fighting?**
It scans many prompts about your product and ranks them by how easy they are to
capture in AI search. The opportunity matrix is the deliverable. Writing the
content to capture a chosen opportunity is an *optional* follow-on.

**An opportunity is a prompt where (your hypothesis, made measurable):**
- 🟢 **Nothing is cited** — the AI answers from memory; any solid page can become the source.
- 🟢 **Something irrelevant is cited** — the cited pages don't really answer the prompt.
- 🟡 **A recreatable page is cited** — a blog, listicle, product page, Q&A, or Reddit thread you could out-build.
- 🔴 (not an opportunity) **A hard-to-beat source is cited** — official docs, Wikipedia, standards bodies, gov, top-brand domains.
- ⚪ (defend, not capture) **Your own domain is already cited.**

## Prerequisites (check first)

1. The `brightdata` MCP server must be connected. Confirm `mcp__brightdata__*`
   tools are available. If **not**, tell the user: *"The Bright Data MCP isn't
   loaded. Copy `.mcp.json.example` → `.mcp.json`, paste your API token (raw, not
   `${VAR}`), restart Claude Code, then re-run."* Do not attempt the phases without it.
2. Skim `references/tool-map.md` for the **real** tool names + which tier (free vs.
   credits) each call burns. If a tool name there isn't present in-session, list
   the actual `mcp__brightdata__*` tools and use those — never guess a tool name.
3. Read `references/opportunity-scoring.md` — it holds the scoring rubric and the
   opportunity-type taxonomy used in Phase 5.

## How to invoke

- **Whole flow:** "find GEO opportunities for `<product URL>`" → runs Phase 1 → 5,
  pausing for input at Phase 2 and at the Phase 3 credit checkpoint.
- **A single phase:** pass `--phase` or just ask ("just profile my product",
  "regenerate the prompt list", "score the opportunities from the diagnosis").
- Each phase reads any prior phase's saved Markdown from
  `opportunity-research/<product-slug>/` if present, else runs what it needs.

## Output location

Write all artifacts as clean Markdown a non-technical founder can read, under the
user's current directory:

```
opportunity-research/<product-slug>/
├── 01-product-profile.md
├── 02-validated-categories.md
├── 03-candidate-prompts.md
├── 04-geo-diagnosis.md
└── 05-opportunity-matrix.md      ← the hero deliverable
```

Announce the file path after writing each one.

---

## PHASE 1 — Product Intake

**Goal:** understand the product well enough to judge prompt relevance later.

1. Take the user's product URL + one-sentence description. Scrape the page with
   **`mcp__brightdata__scrape_as_markdown`** (free).
2. Extract a **product profile**: what it does (1-2 lines), core features, primary
   use cases, ICP / buyer, the category it competes in, any competitors named on
   the page, and the key entities/specs/numbers it owns.
3. Write `01-product-profile.md` and show it back. Ask the user to correct anything
   wrong before continuing — a bad profile poisons every later relevance score.

**Output ends with Sources:** the URL scraped.

---

## PHASE 2 — Category Validation  *(interactive)*

**Goal:** prune the search space so paid calls aren't wasted on off-target prompts.

1. From the profile, derive 4-8 candidate **topic categories / angles** the product
   could plausibly be the answer for (e.g. for a payments-address tool: address
   validation, sanctions screening, ISO 20022 structured address, STP rates,
   payment data quality).
2. Use **AskUserQuestion** (multiSelect) to let the user confirm which categories
   are in scope and cut the irrelevant ones. Let them add categories you missed.
3. Write `02-validated-categories.md` listing the kept categories (and what was cut).

---

## PHASE 3 — Prompt Discovery  *(free; ends at the credit checkpoint)*

**Goal:** a list of ~15-20 **real** long-tail prompts, grounded in live search data.

1. For each validated category, draft candidate prompts across families: question
   forms, "best X for Y", "X vs Y", alternatives-to, "how do I…", integration/spec
   questions.
2. **Ground them in reality** — do NOT ship hallucinated prompts. For category
   seeds, fire **`mcp__brightdata__search_engine`** (`engine: "google"`,
   optional `geo_location`) and harvest the live **People Also Ask** + **related
   searches**. Keep/expand prompts that map to real surfaced queries; this is also
   where genuine long-tail demand shows up. Pipe collected SERP JSON through the
   helper if useful:
   ```bash
   python3 scripts/cluster_serp.py < serp.json
   ```
3. Pre-rank candidates by relevance to the Phase 1 profile, dedupe, and trim to
   ~15-20. Tag each with its source category and whether it came from PAA/related
   (real) vs. constructed-but-plausible.
4. Write `03-candidate-prompts.md` and **STOP. Show the list to the user and ask
   them to cut/approve.** The next phase spends Bright Data credits (one paid call
   per prompt) — do not proceed until the user approves the final set.

**Output ends with Sources:** every SERP query run + PAA/related pulled.

---

## PHASE 4 — GEO Diagnosis at scale  *(credits — only after approval)*

**Goal:** for each approved prompt, capture what AI search cites today and why.

1. For each approved prompt, fire **`mcp__brightdata__web_data_chatgpt_ai_insights`**
   (`prompt`) **one at a time (sequentially)** — parallel calls trigger transient
   `HTTP 400: Customer is not active`; a sequential retry succeeds. ChatGPT is the
   default engine because it's the only one returning explicit cited URLs.
   Perplexity (prose, usually no URLs) and Grok (often empty `[{}]`) are optional
   cross-checks — only add them if the user asks, since each is another paid call
   per prompt. If a call returns empty, mark "⚠️ Live data unavailable" — never invent.
2. Capture per prompt: the answer text + the **cited source URLs**. Dedupe cited
   URLs across all prompts, then scrape them with **`mcp__brightdata__scrape_batch`**
   as Markdown (**≤5 URLs per call** — batch in groups of 5).
3. For each cited page, read the **citation pattern** via
   `references/geo-citation-patterns.md` and note its **page type** (blog / listicle
   / product page / docs / Wikipedia / standards body / Reddit / etc.) and a
   recognizability/authority read (proxy).
4. Write `04-geo-diagnosis.md`: per prompt → who's cited, page types, whether the
   citations actually answer the prompt, and whether the user's own domain appears.

**Output ends with Sources:** every AI prompt run + every cited URL scraped.

---

## PHASE 5 — Opportunity Matrix  *(free — the deliverable)*

**Goal:** rank the prompts into a clear "go capture these" list.

1. Score every prompt on two axes using `references/opportunity-scoring.md`:
   - **Capturability** (from what's cited): 🟢 nothing cited → 🟢 irrelevant cited →
     🟡 recreatable page cited → 🔴 hard-to-beat cited → ⚪ you're already cited.
   - **Relevance**: how well the product (Phase 1 profile) actually answers the prompt.
   The helper turns the Phase-4 evidence JSON into a ranked matrix:
   ```bash
   python3 scripts/score_opportunities.py < diagnosis.json
   ```
   (or score inline if it errors — it only organizes scraped evidence, never invents).
2. Classify each prompt's **opportunity type** and the **recommended capture move**
   (new blog post / product page / comparison page / FAQ / schema add).
3. Write `05-opportunity-matrix.md`: a ranked table —
   `prompt → capturability → relevance → who's cited now → opportunity type →
   capture move`. Lead with the **top-right quadrant** (easy *and* relevant) as the
   priority targets. Label demand/authority reads as proxies.

**Output ends with Sources:** the diagnosis + SERP evidence each score rests on.

---

## OPTIONAL — Capture a chosen opportunity

If the user picks an opportunity row, generate the content to capture it (this is
the old content-engine, now a follow-on, not the core):

1. Build an evidence bundle from Phases 1-4 for the chosen prompt (cited competitors
   + their winning patterns, shared entities, PAA to answer verbatim, schema seen).
2. Fill `templates/content-brief.md` (helper: `python3 scripts/format_brief.py
   evidence.json`) → a brief with target prompt + intent, title/H1, H2/H3 outline
   mapped to PAA + entities, a ≤60-word extractable direct-answer block,
   FAQ/schema recommendations, entity checklist, internal-link notes — each item
   citing the scraped competitor/PAA it came from.
3. Draft the article to that brief: direct answer up top under each question,
   lists/tables where the cited winners used them, skimmable. Mark any spot needing
   a real stat the user must supply as `[NEEDS SOURCE: …]` — never invent a number.

Save as `capture-brief.md` / `capture-draft.md`, each ending with its Sources.

---

## OPTIONAL — Track

Re-run Phase 4 on the captured prompts later to see if the user's page is now
cited. Output a before/after table (date, prompt, was-cited?, notable changes).
Save as `tracking-<date>.md`.

---

## Style for all outputs
- Plain language, short sentences, tables over walls of text.
- Lead with the takeaway (the winnable prompts), then the evidence.
- Always close with **Sources** (real URLs + the live queries used). If a section
  has no live source, it doesn't belong in the output.
