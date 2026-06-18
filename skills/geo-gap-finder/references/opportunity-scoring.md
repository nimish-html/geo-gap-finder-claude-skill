# Opportunity Scoring Rubric (Phase 5)

How to turn the Phase-4 GEO diagnosis into a ranked, defensible opportunity matrix.
Score only from what was actually scraped — if a signal can't be observed, say
"not determinable from scrape", never guess.

## The two axes

Every prompt is scored on two independent axes, then placed in a quadrant.

### Axis 1 — Capturability (how easy to win the citation)

Read what ChatGPT cited for the prompt and assign the highest-matching tier:

| Score | Citation situation observed | Why it's that score |
|------:|-----------------------------|---------------------|
| **5 — 🟢 Wide open** | **No sources cited** — the engine answered from memory | Nothing to displace. A single well-structured, extractable page can become *the* cited source. |
| **4 — 🟢 Weak** | Cited pages are **irrelevant / tangential** — they don't actually answer the prompt | The bar is low; a focused page that directly answers wins. |
| **3 — 🟡 Recreatable** | Cited pages are **page types you can out-build**: blog post, listicle, product/marketing page, Q&A, Reddit/forum, thin aggregator | You can publish a deeper, better-structured version of the same thing. |
| **2 — 🟠 Contested** | Cited pages are **decent mid-authority** content (established niche sites, mid-tier publications) | Winnable but needs real quality + some authority. |
| **1 — 🔴 Locked** | Cited pages are **hard-to-beat**: official docs, Wikipedia, standards bodies, government, top-brand domains | Displacing these is a long authority play, not a quick capture. |
| **— ⚪ Owned** | **The user's own domain is already cited** | Not an opportunity to capture — a position to *defend* / extend. Flag separately. |

Page-type read comes from the scraped page (Phase 4) + `geo-citation-patterns.md`.
Authority is a **PROXY** — judge by recognizability + the page's organic SERP rank
(if seen in Phase 3). There is **no domain-authority metric** in this data source;
say so.

### Axis 2 — Relevance (does the product deserve to be the answer)

Score how well the Phase-1 product profile actually answers the prompt:

| Score | Meaning |
|------:|---------|
| **5** | Bullseye — the product is squarely the right answer; its features/use-cases map directly. |
| **3** | Adjacent — the product is a plausible answer for part of the prompt. |
| **1** | Stretch — only loosely related; capturing it wouldn't drive qualified traffic. |

A prompt that's easy to capture but irrelevant is a trap — high Capturability ×
low Relevance = skip it.

## The quadrant (how to rank)

```
              Relevance →
            low            high
        ┌──────────────┬──────────────┐
  easy  │  trap / skip │  ★ PRIORITY  │   ← top-right = capture first
        │  (ignore)    │  (easy+worth)│
 Captu- ├──────────────┼──────────────┤
 rabil  │  ignore      │  long game   │
  hard  │              │  (worth, but │
        │              │   authority) │
        └──────────────┴──────────────┘
```

Rank order = **Capturability + Relevance** (both high first). Surface the
top-right "★ PRIORITY" prompts at the top of the matrix; list "long game" prompts
(relevant but locked) as strategic bets; drop low-relevance prompts.

## Opportunity type → recommended capture move

Translate each priority prompt into a concrete action:

| Opportunity type (capturability reason) | Recommended capture move |
|-----------------------------------------|--------------------------|
| Wide open (nothing cited) | Publish a focused, extractable answer page (clear H2 = the question, ≤60-word direct answer up top) + FAQ + schema. |
| Irrelevant cited | Same, but explicitly out-answer the tangential pages on the exact intent. |
| Recreatable blog/listicle cited | Build a deeper, better-structured blog post / comparison page that out-covers it. |
| Recreatable product page cited | Sharpen/launch your own product or landing page targeting the prompt's intent. |
| Recreatable Q&A/Reddit cited | Publish an authoritative FAQ/answer page; the engine is currently leaning on UGC. |
| Locked (docs/Wikipedia/standards) | Long game — build topical authority around it; don't expect a quick win. |
| Owned (you're cited) | Defend: add schema, tighten internal linking to the canonical page, expand entity coverage. |

## What the matrix must contain (Phase 5 output)

A ranked table, priority first:

`# · prompt · capturability (score + label) · relevance (score) · who's cited now (URLs + page type) · opportunity type · recommended capture move`

Then a short **"Start here"** callout naming the top 2-3 prompts and why.

> Every row must trace to a Phase-4 cited URL (or "no citation observed") and a
> Phase-3 SERP/PAA source. Label all demand/authority reads as proxies. No invented
> volumes, scores, or URLs.
