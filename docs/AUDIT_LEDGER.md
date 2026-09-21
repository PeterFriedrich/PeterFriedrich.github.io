# AUDIT LEDGER — what has been audited, when, and what came back

One row per **executed audit run**. This is the coverage map the audit docs
don't give individually: briefs are reusable *instruments*, findings docs record
*one run's output*, and the `project-audit` skill deliberately picks ONE target
per session — so nothing else says what has and hasn't been looked at. This does.

Rules: add a row when an audit **executes** (not when a brief is written); every
row carries a **pointer to the findings doc**; verdicts are **point-in-time** — a
row says the target was audited *as of that date*, not that it's still clean
after later changes. Not part of any session's mandatory reading — open it to
scope an audit or to check what has already been covered. Audits are framed
top-down, fundamental decisions first.

## Executed audits

| Date | Target / scope | Instrument | Output | Verdict (one line) | Outstanding |
|------|----------------|------------|--------|--------------------|-------------|

## Queued — briefed, not yet run

## Never audited (candidates, roughly ranked)

- The five v1 project write-ups, once ported — every claim and every link
- External link health across the whole site (link rot is the standing risk)
- Dark-mode contrast against WCAG AA
- The About page: does it say anything only this author could say?
- Page weight on the heaviest page, not the home page
- The deploy path end to end: does a merge to `main` actually change the site?
