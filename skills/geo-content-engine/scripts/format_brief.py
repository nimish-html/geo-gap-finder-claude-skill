#!/usr/bin/env python3
"""
format_brief.py — assemble a Stage 3 content brief from a JSON evidence bundle.

Stdlib only. CONVENIENCE for Stage 3: if it errors, fill templates/content-brief.md
inline instead. It only formats evidence already gathered in Stages 1-2 — it does
not generate or invent any data.

Input: JSON file (arg or stdin) shaped like:
{
  "topic": "best CRM for small business",
  "target_query": "best crm for small business",
  "intent": "Commercial investigation",
  "recommended_title": "...",
  "direct_answer": "...",                       # <=60 words, extractable
  "outline": [{"h2": "...", "h3": ["...", "..."], "source": "url/PAA"}],
  "paa_questions": ["how much does a crm cost?", ...],
  "entities": ["pipeline", "contact management", ...],
  "schema_types": ["FAQPage", "Article"],
  "competitor_patterns": [{"url": "...", "wins_because": "..."}],
  "gaps": ["no FAQ section", "missing pricing table"],
  "sources": ["https://...", "search: best crm for small business"]
}

Usage:
  python3 format_brief.py evidence.json
  python3 format_brief.py < evidence.json
"""

import json
import sys


def load():
    raw = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    if not raw.strip():
        sys.exit("No input. Pass evidence.json or pipe it in.")
    return json.loads(raw)


def bullets(items, empty="_(none recorded)_"):
    items = items or []
    return "\n".join(f"- {i}" for i in items) if items else empty


def main():
    d = load()
    t = d.get

    md = []
    md.append(f"# Content Brief — {t('topic', t('target_query', 'Untitled'))}\n")
    md.append(f"**Target query:** {t('target_query', '—')}  ")
    md.append(f"**Search intent:** {t('intent', '—')}\n")

    md.append("## Recommended title / H1")
    md.append(f"{t('recommended_title', '_[fill from evidence]_')}\n")

    md.append("## Direct answer block (place at top — must be extractable, ≤60 words)")
    md.append(f"> {t('direct_answer', '_[write the lift-out answer to the head query]_')}\n")

    md.append("## Outline (H2/H3 mapped to evidence)")
    outline = t("outline") or []
    if outline:
        for sec in outline:
            src = f"  _(source: {sec['source']})_" if sec.get("source") else ""
            md.append(f"### {sec.get('h2','(section)')}{src}")
            for h3 in sec.get("h3", []) or []:
                md.append(f"- {h3}")
            md.append("")
    else:
        md.append("_[no outline supplied]_\n")

    md.append("## FAQ — answer these People Also Ask questions verbatim")
    md.append(bullets(t("paa_questions")))
    md.append("")

    md.append("## Entity / topic coverage checklist (competitors all cover these)")
    md.append(bullets(t("entities")))
    md.append("")

    md.append("## Schema to implement")
    md.append(bullets(t("schema_types"), "_(none observed in cited pages)_"))
    md.append("")

    md.append("## Why competitors get cited (replicate this)")
    cps = t("competitor_patterns") or []
    if cps:
        md.append("| Cited page | Wins because |")
        md.append("|---|---|")
        for c in cps:
            md.append(f"| {c.get('url','—')} | {c.get('wins_because','—')} |")
    else:
        md.append("_[no competitor patterns supplied]_")
    md.append("")

    md.append("## Gaps on the user's current page (close these)")
    md.append(bullets(t("gaps"), "_(no user page compared — supply URL to diff)_"))
    md.append("")

    md.append("## Sources (live data this brief is built on)")
    md.append(bullets(t("sources"), "⚠️ No sources recorded — do not ship."))
    md.append("")

    print("\n".join(md))


if __name__ == "__main__":
    main()
