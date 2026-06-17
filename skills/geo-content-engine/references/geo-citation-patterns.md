# What Makes Content Get Cited in AI Search (extraction checklist)

Use this when analyzing each page an AI engine cited (Stage 2) and when shaping
the brief/draft (Stage 3). For every cited page, score it against these signals —
based only on what you actually scraped, not assumptions.

## 1. Answer extractability (the biggest lever)
- [ ] Is there a **direct, self-contained answer** to the query within the first
      screen? (≤ ~60 words, no "it depends" preamble.)
- [ ] Does a heading **restate the question** the way a user/LLM phrases it?
- [ ] Can a single paragraph or list item be lifted out and still make sense
      with no surrounding context? (LLMs quote extractable chunks.)

## 2. Structure & format
- [ ] Clear heading hierarchy (H1 → H2 → H3) that maps to sub-questions.
- [ ] **Lists, tables, or steps** where the answer is comparative or procedural
      (AI engines favor these for "best X", "X vs Y", "how to X").
- [ ] A visible **FAQ** section answering related/PAA questions verbatim.
- [ ] Short paragraphs, descriptive subheads, scannable.

## 3. Structured data / markup
- [ ] Schema present? Note type: `Article`, `FAQPage`, `HowTo`, `Product`,
      `Review`, `Organization`. (Check the scraped HTML/markdown for JSON-LD or
      obvious schema cues.)
- [ ] Clear authorship / publisher / organization signals.

## 4. Entity & topic coverage
- [ ] Which **entities** (named tools, people, concepts, specs, numbers) does the
      page cover that the others also cover? The intersection = the entity set
      the topic "requires" to be considered complete.
- [ ] Does it cover sub-topics the query implies but the user's page omits?
- [ ] Specific, concrete facts/figures (cited) vs. vague generalities.

## 5. Freshness & trust
- [ ] Visible **publish/updated date**; recent?
- [ ] Outbound citations to primary/authoritative sources.
- [ ] Domain authority cue (well-known publisher, official docs, recognized brand).
- [ ] First-hand signals: original data, examples, screenshots.

## Synthesis output (what to write in Stage 2)
For each target query produce:
1. **Per-page row:** `cited URL → top 2–3 signals above that earn the citation`.
2. **Common pattern:** the signals shared by *most* cited pages (this is the
   formula to replicate).
3. **Gap list (if user URL provided):** signals present in winners but missing on
   the user's scraped page → these become Stage 3 brief requirements.

> Only list a signal if you observed it in the scraped content. If you couldn't
> determine one (e.g. schema not visible in markdown), say "not determinable from
> scrape" rather than guessing.
