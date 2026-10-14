# Session State & Handoff — template sync done; Google Docs content pipeline proposed

## 0. Session Metadata
- **Model:** Opus 5.5 (`claude-opus-5-5`) — one model throughout, no mid-session switch
- **Effort:** `high` (from `$CLAUDE_EFFORT`, checked not recalled)
- **Date / session #:** work on 2026-10-03, handoff written 2026-10-14 (same
  long-lived tmux session `portfolio`, idle in between). S3 of this repo.

⚠️ **This file stands alone.** The 2026-09-22 handoff still owns the content
backlog (§4 there is unchanged and still correct); this one records what
changed around it.

## 1. Goal

**The project:** Peter Friedrich's portfolio + blog, a static Astro site on
GitHub Pages at `https://peterfriedrich.github.io`. No JS to the reader, no
webfonts, no analytics.

**This session:** (a) ask the `template` and `server` sessions which apparatus
files this hand-ported repo lacks, and pull them; (b) decide how the site
should host one-off data-analysis reports (convert notebooks or not);
(c) LinkedIn as a data source; (d) the owner's new direction: **Google Docs as
the source of truth for portfolio content**, backed up to a private git repo.

## 2. Current State

### ✅ Completed

- **PR #13 merged** 2026-10-03T03:01Z as `7b99183`; verified on trunk with
  `git merge-base --is-ancestor`; deploy run on `7b99183` succeeded.
  - `.claude/skills/steward/SKILL.md` — ported from
    `~/cc-data-project-template`, `origin/master` → `origin/main`, pytest →
    `npm run build && npm test`, `npm run guards`.
  - `package.json` `guards` script now runs
    `PY=$(command -v python3.12 || command -v python3)`. Both guard scripts
    use `dict[str, Path]` annotations and crashed on the server's system
    python3 (3.6.8) with `TypeError: 'type' object is not subscriptable`.
    CI behaviour unchanged (no python3.12 there → falls back to python3).
- **`git config core.hooksPath .githooks` set** in `~/PeterFriedrich.github.io`
  (was unset; server had it open in server-ops since 2026-09-28, now closed).
- **Node 22 on the server.** `server` installed it system-wide (nodejs:22 dnf
  module) with owner approval: `/usr/bin/node` v22.23.2, npm 10.9.8. Before
  that, v20.20.2 could not build Astro 7.3 (`>=22.12.0` required). Verified
  here afterwards: `npm run build` → 5 pages; `npm test` → 9/9 pass;
  `npm run guards` OK.
- **Template's verdict (recorded so nobody re-asks):**
  - **Keep porting by hand — do NOT connect copier.** The template renders the
    data skeleton with no way to turn it off; every shared file here is a
    deliberate adaptation, so updates would be piles of 3-way conflicts.
  - **No stale files.** Diffs in `handoff_gap.py`, `pre-push`,
    `check_doc_citations.py`, `check_decisions_log.py` are intentional
    adaptations. `tools/todo_archive.py` is byte-identical.
  - **Skip (data/copier-only):** `data/**`, `docs/DATA_ISSUES.md`,
    `requirements*.txt`, `tests.yml`, `test_loaded_path.py`, `project-audit`
    skill, `copier.yml`, `*.jinja`, `template_drift.py`, `docs/COPIER.md`,
    `docs/FINDINGS_harvest.md`.
  - **Offered, deliberately not taken:** the `.venv → python3.12 → python3`
    fallback in `.claude/settings.json` hooks (not needed: `handoff_gap.py`
    runs fine on 3.6, exit 0); `docs/WEB_CACHE_BUSTING.md` (Astro
    fingerprints bundled assets; only matters once changing files are served
    from `public/`); the read-log hook + `tools/retrieval_report.py`;
    `make_brief.py`/`CLAUDE_WEB.md`.
  - **Offered, awaiting owner:** a CLAUDE.md "Session Management" line to run
    `gh issue list --state open` at session start. Not added.

### ⚠️ In Progress — the Google Docs pipeline (proposed, nothing built)

Owner decided: **Google Docs = source of truth for written content** (About,
project write-ups, profile facts), backed up in a **private git repo**.
Proposal given to the owner, not yet approved:

1. Owner makes **one Drive folder** for portfolio writing and shares it with
   the server's **service account** as Viewer (new docs then covered with no
   per-doc sharing). The SA email: ask `server`.
2. A **private content repo** (name not chosen) receives daily Markdown
   exports via `~/server-ops/gdocs/gdocs.py backup <doc> <dir>`, from a script
   that commits there. **Not** server-ops' own `backup.sh` — server said
   portfolio content does not belong in server-ops.
3. **The site keeps building from markdown committed in THIS repo**, pulled
   from the exports when something is published. No Google credentials in
   GitHub Actions (server recommends this over a GitHub secret).

**Blocked on the owner for:** the Drive folder (created + shared with the SA),
the content repo name (or go-ahead to create it), and approval of a second
daily cron (`server` installs crons; the auto-mode classifier refuses to).

### ❌ Blocking Issues

None technical. Content work is still blocked on owner input (no invented
facts — CLAUDE.md's one exceptionless rule).

## 3. Technical Learnings

- **Reports: link, don't convert.** `edmonton-tax-viz` already publishes its
  evidence notebooks (jupytext `.py` → nbconvert HTML) to its own project
  Pages site **under this hostname**, e.g.
  `https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/roll-year-metadata.html`
  (list: `~/edmonton-tax-viz-report/docs/EVIDENCE_NOTEBOOKS.md`). Project
  sites share the user-site domain, so the portfolio should link to them from
  project entries. Converting notebooks here is a poor fit: Astro has no
  official notebook support (roadmap discussion #579 declined it); nbconvert
  HTML with Plotly ships JS, breaking the no-JS rule. For a one-off analysis
  with no repo of its own: export to markdown + static images, publish as a
  normal post. No server/template convention for notebook publishing exists;
  a cross-repo one would belong to `template`.
- **LinkedIn has no usable API for your own profile** (Sign in with LinkedIn =
  name/photo/email only; profile API partner-only; DMA portability API is
  EU/EEA/CH only; scraping violates ToS). Route: one-off data export
  (Settings → Data privacy → Get a copy of your data → `Positions.csv`,
  `Education.csv`, `Skills.csv`, `Profile.csv`) to seed About/dates; then the
  site (now: Google Docs) is the source of truth. From model knowledge, not
  re-verified.
- **Two Google routes exist:**
  - The **claude.ai Google Drive connector** (`mcp__claude_ai_Google_Drive__*`)
    works in this session — `list_recent_files` returned the owner's files
    (metadata only read). Session-bound, so it cannot run unattended.
  - The **server's service account**: `~/server-ops/gdocs/gdocs.py` (venv
    `~/server-ops/gdocs/.venv`, key `~/.config/server-ops/gdocs-sa.json`,
    GCP project 866501688259). Read-only `md`/`backup`/`outline`/`text` may be
    called from this session without asking server. Reaches only docs shared
    with the SA. Docs: `~/server-ops/gdocs/README.md`.
- **Drive Markdown-export quirks** (from server, hit 2026-09-30): escapes
  `\_ \+ \#`, two trailing spaces on list items, `* ` bullets → normalise
  before Astro. **Untested:** images, tables, links, headings below `###`.
  Run one sample doc through before fixing the format.
- **Taking Docs as source of truth contradicts written rules** — `CLAUDE.md`
  ("Content is markdown in `src/content/`") and `docs/CONTENT.md`. Needs a
  `docs/DECISIONS.md` row + edits to both once the shape is settled.
- **Server facts:** disk ~86% full (≈5 GB free) — avoid big caches; dev port
  4321 is free (4330, 8080, 8501, 8765, 44321 taken); box reachable over
  Tailscale for previewing a dev server from another device
  (`server-ops/networking/tailscale.md`). Playwright chromium is in
  `~/.cache/ms-playwright`.
- **`gh` works on this server** (logged in as PeterFriedrich), so
  `.githooks/pre-push` is live here — unlike the cloud VM in the 2026-09-22
  handoff, whose environment warnings (can't reach the site, no `gh`, old
  repo name) apply to that VM only.

## 4. Next Steps (prioritized)

1. **When the owner supplies the Drive folder + content repo name:** ask
   `server` for the SA email if the owner needs it; export ONE sample doc with
   `~/server-ops/gdocs/.venv/bin/python ~/server-ops/gdocs/gdocs.py md <doc-id>`
   and check headings, links, images, tables before designing the
   normaliser. Then write the backup script in the content repo, ask `server`
   to install the cron (owner-approved), add the DECISIONS row and update
   `CLAUDE.md` + `docs/CONTENT.md`.
2. **Content backlog, unchanged** — 2026-09-22 handoff §4 / `TODO.md`: the
   live site is still EMPTY (both entries `draft: true`). Port the five v1
   write-ups; add newer projects (link to the live report pages rather than
   converting notebooks); rewrite About (seed from a LinkedIn export if the
   owner provides one); decide `how-this-site-works.md`.
3. **Owner decision pending:** add the `gh issue list --state open`
   session-start line to `CLAUDE.md`?
4. Smaller, unblocked: tag pages, OG image, dark-mode contrast check.

## 5. Restoration Procedure

```bash
cd ~/PeterFriedrich.github.io
npm ci                                 # Node >= 22.12 required (server: 22.23.2)
git config core.hooksPath .githooks    # already set in this clone
npm run build && npm test              # build FIRST or content tests skip
npm run guards                         # uses python3.12 if present
```

**Not in this repo:** repo name / Pages source / DNS (`docs/DEPLOY.md`); the
server's Node 22 install and the server-ops record of it; the service-account
key and `gdocs.py` (server-ops); the Drive folder and content repo once they
exist.
