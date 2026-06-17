#!/usr/bin/env python3
"""
score_opportunities.py — turn Phase-4 GEO diagnosis into a ranked opportunity matrix.

Stdlib only. CONVENIENCE for Phase 5: if it errors, score inline instead. It does
NOT invent data — it only organizes evidence already gathered in Phase 4 and
applies the rubric in references/opportunity-scoring.md.

Input (stdin or file arg): JSON list of per-prompt diagnosis objects:

[
  {
    "prompt": "best iso 20022 address resolution tool",
    "category": "ISO 20022 structured address",
    "relevance": 5,                       # 1-5, how well the product answers it
    "user_cited": false,                  # is the user's own domain already cited?
    "citations": [                        # what ChatGPT cited (empty list = nothing)
      {"url": "https://...", "page_type": "blog", "answers_prompt": true}
    ]
  },
  ...
]

page_type ∈ {none, blog, listicle, product, qa, reddit, forum, aggregator,
             mid_publication, niche_site, docs, wikipedia, standards, gov, brand}

Output: a ranked Markdown opportunity matrix to stdout.

Usage:
  python3 score_opportunities.py < diagnosis.json
  python3 score_opportunities.py diagnosis.json
"""

import json
import sys

# page_type -> (capturability score, label) when that's the strongest citation.
RECREATABLE = {"blog", "listicle", "product", "qa", "reddit", "forum", "aggregator"}
CONTESTED = {"mid_publication", "niche_site"}
LOCKED = {"docs", "wikipedia", "standards", "gov", "brand"}

CAP_LABEL = {
    5: "🟢 Wide open (nothing cited)",
    4: "🟢 Weak (irrelevant cited)",
    3: "🟡 Recreatable page cited",
    2: "🟠 Contested (mid-authority)",
    1: "🔴 Locked (hard to beat)",
    0: "⚪ Owned (you're cited)",
}

MOVE = {
    5: "Publish a focused, extractable answer page (H2 = the question, ≤60-word answer up top) + FAQ + schema.",
    4: "Publish a page that directly out-answers the tangential pages on this exact intent.",
    3: "Build a deeper, better-structured version of the cited page type (blog / comparison / FAQ).",
    2: "Invest in a high-quality page plus some topical authority to displace mid-tier content.",
    1: "Long game — build topical authority around it; not a quick capture.",
    0: "Defend: add schema, tighten internal linking, expand entity coverage on the cited page.",
}


def capturability(item):
    """Return (score 0-5, reason) from the citation situation."""
    if item.get("user_cited"):
        return 0, "user's own domain already cited"
    cites = item.get("citations") or []
    if not cites:
        return 5, "no sources cited — engine answered from memory"
    # If none of the citations actually answer the prompt -> weak/irrelevant.
    if all(not c.get("answers_prompt", True) for c in cites):
        return 4, "cited pages are irrelevant / don't answer the prompt"
    types = {(c.get("page_type") or "").lower() for c in cites}
    # Best (easiest) tier wins, but a single locked source raises the floor only
    # if everything cited is locked.
    if types & RECREATABLE and not (types & LOCKED):
        return 3, "recreatable page types cited (" + ", ".join(sorted(types & RECREATABLE)) + ")"
    if types & CONTESTED and not (types & LOCKED):
        return 2, "mid-authority pages cited"
    if types & LOCKED:
        return 1, "hard-to-beat sources cited (" + ", ".join(sorted(types & LOCKED)) + ")"
    # Unknown page types: treat as recreatable-ish but flag.
    return 3, "page type not determinable from scrape — treat as recreatable, verify"


def opp_type(score):
    return CAP_LABEL.get(score, "?")


def fmt_citations(item):
    cites = item.get("citations") or []
    if not cites:
        return "_none cited_"
    parts = []
    for c in cites:
        pt = c.get("page_type", "?")
        flag = "" if c.get("answers_prompt", True) else " ⚠️off-topic"
        parts.append(f"{c.get('url','?')} ({pt}{flag})")
    return "<br>".join(parts)


def load_input():
    raw = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    if not raw.strip():
        sys.exit("No input. Pipe Phase-4 diagnosis JSON in or pass a file path.")
    data = json.loads(raw)
    return data if isinstance(data, list) else [data]


def main():
    items = load_input()
    rows = []
    for it in items:
        cap, reason = capturability(it)
        rel = int(it.get("relevance", 0) or 0)
        # Owned (cap 0) sorts to the bottom of the capture list (defend, not capture).
        priority = (cap if cap > 0 else -1) + rel
        rows.append((priority, cap, reason, rel, it))

    rows.sort(key=lambda r: r[0], reverse=True)

    out = ["# Phase 5 — GEO Opportunity Matrix\n"]
    out.append("_Ranked by capturability + relevance. Demand/authority reads are "
               "PROXIES (no volume/DA metric exists in the data source). Every row "
               "traces to a live Phase-4 citation check._\n")
    out.append("| # | Prompt | Capturability | Relevance | Who's cited now | Opportunity / move |")
    out.append("|---|---|---|---|---|---|")
    for i, (_prio, cap, reason, rel, it) in enumerate(rows, 1):
        out.append(
            f"| {i} | {it.get('prompt','?')} | {opp_type(cap)} — {reason} "
            f"| {rel}/5 | {fmt_citations(it)} | {MOVE.get(cap,'?')} |"
        )
    out.append("")

    # "Start here" callout: top priority rows that are capturable (cap>=3) and relevant (rel>=4).
    starts = [r for r in rows if r[1] >= 3 and r[3] >= 4][:3]
    if starts:
        out.append("## ★ Start here\n")
        for _prio, cap, reason, rel, it in starts:
            out.append(f"- **{it.get('prompt','?')}** — {opp_type(cap)}, relevance {rel}/5. "
                       f"{MOVE.get(cap,'')}")
        out.append("")
    else:
        out.append("## ★ Start here\n\n_No prompt scored both easy-to-capture and "
                   "highly relevant. Review the matrix for the best trade-offs._\n")

    out.append("> Generated by score_opportunities.py from live Phase-4 evidence only.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
