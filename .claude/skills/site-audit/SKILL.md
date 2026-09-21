---
name: site-audit
description: >
  Focused audit skill for this portfolio + blog. Use whenever the user asks to
  audit, review, check, or QA the site, a page, a post, or the build. Picks ONE
  target per run; grounds in docs/AUDIT_LEDGER.md before scoping and adds a
  ledger row after executing. Triggers on: "audit the site", "review this post",
  "check the build", "is the site any good", "what should I look at", or any
  QA/review request about this repo.
---

# Site Audit Skill

Adapted from the `project-audit` skill in `cc-data-project-template`. The shape
is the same — **one target, deep, with a written verdict** — but the failure
classes are different. A data pipeline fails by publishing a wrong number
silently. A personal site fails by being **unread, unreadable, or quietly
broken**: a dead link, a page nobody can finish, a claim that was true in 2022.

## Purpose

One **single, deep, actionable verdict** per run. Do not sweep. A shallow pass
over everything is what produces a list of nits and no decisions.

## The audit ecosystem

- **`docs/AUDIT_LEDGER.md`** — the coverage map: one row per *executed* run.
  **Read it FIRST when scoping; add a row when your audit executes.**
- **Findings** — a `docs/FINDINGS_<target>.md` for a big run, or the session
  handoff §2 for a small one. The ledger row points; it never duplicates.
- **`docs/DECISIONS.md`** — if the audit locks or reopens a decision, add a row.

## How to run an audit

### Step 1 — Ground before scoping (non-negotiable)

1. Read `docs/AUDIT_LEDGER.md` — all tables.
2. Cross-check the latest session summary. `TODO.md` lags executed work.
3. Ledger verdicts are **point-in-time**. Re-auditing after a relevant change is
   fair game — say so: "re-run, prior row YYYY-MM-DD, delta since: …".

### Step 2 — Pick ONE target

Named by the user, or the top of the ledger's ranked "Never audited" list. Say
which you picked and why before going deep.

### Step 3 — Choose the audit family

**(a) Content audit** — the default for anything a reader sees.

Build the target's **decision stack** top-down and evaluate in order. When a
level is unsound, everything beneath it is moot — don't fix the heading
hierarchy of a page that should not exist.

- **L0 — should this be on the site at all?** Who is it for, and what do they
  do after reading it? A portfolio entry whose honest answer is "it exists
  because I built the thing" is a candidate for deletion, not polish.
- **L1 — does the opening earn the next paragraph?** Most visitors read the
  first two sentences and the headings. If those don't carry the claim, the
  rest is decoration.
- **L2 — is it still true?** Dates, job descriptions, "currently", project
  status, links to services that have since shut down. ⚠️ **The site ages
  while nobody is reading it.** This is the single most common real finding.
- **L3 — is it readable?** One idea per paragraph, concrete over abstract,
  jargon defined on first use, and no sentence the author could not say out
  loud.
- **L4 — is the markup right?** Heading order, alt text, link text that means
  something out of context.

Per level: **SOUND / CONDITIONAL / UNSOUND**, the sharpest argument against
that level, and what evidence would change the verdict. Assume the author
believes their own page; the value of the run is the argument they did not make
against themselves.

**(b) Mechanical audit** — verdicts are **PASS / FAIL / WARN**. Checklists in
the appendix.

### Step 4 — Deliver verdicts

⚠️ **Every findings document MUST end with a `What this run got wrong` section,
and it may not be empty.** If you genuinely found no error in your own work,
you have not looked: re-read your sharpest claim and ask what would have to be
true for it to be wrong, then go check that. ⚠️ **A confident NEGATIVE — "no
page links to this", "nothing reads that file", "this never renders" — is the
highest-risk claim shape.** Verify a negative by finding the reader, not by
failing to find one.

```
## Audit: [Target]
**Verdict:** PASS / FAIL / WARN
**Finding:** [One paragraph. Quote the actual line. Don't hedge.]
**Fix (if needed):** [Concrete change; if PASS, what you confirmed and why.]
```

### Step 5 — Close the loop

1. Add a row to `docs/AUDIT_LEDGER.md`: date, target, instrument, output
   pointer, one-line verdict, outstanding items.
2. Write findings where they belong; the ledger row points.
3. Reconcile `TODO.md`; append to `docs/DECISIONS.md` if a decision moved.
4. Ship as a PR (`git pull` main first — ledger/TODO tails are append-conflict
   magnets).

## Escalation

A FAIL that makes the site **wrong in public** — a broken deploy, a dead
canonical URL, a draft that published, a factual claim that is false — is
blocking. Stop auditing other targets and fix it. An UNSOUND at L0 or L1 moots
the levels below: report it and stop descending.

---

## Appendix — mechanical checklists (family b)

### The build is what ships
Assert against `dist/`, never against source. "The listing filters drafts" and
"the draft is not on the internet" are different claims. `npm run build` first,
then look at the artifact.

### Links
Internal links resolve to a built page (a typo'd href is a 404 nothing catches).
External links still resolve — **link rot is the site's silent data drift**, and
the v1 site is the proof: Drive links and Omdena project pages from 2021 are
prime suspects. Check what a dead link was *for* before deleting it.

### Absolute URLs
`site` in `astro.config.mjs` decides the canonical tag, the sitemap and the feed.
If the repo is renamed, all three move and nothing fails loudly.
`tests/site-config.test.mjs` pins it; confirm the test still matches reality.

### Weight and speed
No JavaScript unless a page earns it (`tests/content.test.mjs` enforces this).
No webfonts. Images sized and in a modern format. Check the *largest* page, not
the home page — the home page is always the fast one.

### Accessibility
One `<h1>` per page, headings in order with none skipped, alt text on every
informational image (and empty `alt=""` on decorative ones), visible focus
rings, contrast that holds in **both** colour schemes — dark mode is where
contrast regressions hide.

### Metadata
Every page has a unique `<title>` and a non-empty description. The feed
validates. The sitemap lists what it should and omits drafts and 404.

### Content freshness
Anything with a date, a status, or the word "currently". Cross-check project
status against the actual repo: an "active" project whose last commit was two
years ago is a false claim, made by the site, in public.
