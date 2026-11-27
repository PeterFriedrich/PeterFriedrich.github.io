# Session State & Handoff: owner actions listed, content sources mapped

## 0. Session Metadata
- **Model:** Opus 5.5 (`claude-opus-5-5`), one model throughout, no mid-session switch
- **Effort:** `high` (from `$CLAUDE_EFFORT`, checked not recalled)
- **Date / session #:** 2026-11-26 → 2026-11-27, S5 of this repo. One
  markdown-only change (PR #16); the rest was cross-session messages and
  read-only checks.

⚠️ **This file doesn't replace the earlier handoffs.** The 2026-10-14 handoff
still owns the Google Docs pipeline plan (§2–§4 there). The 2026-11-18 handoff
still owns the "private repo reads the published project list" thread. The
backlog is in `TODO.md`.

## 1. Goal
- Project: Peter Friedrich's portfolio + blog, a static Astro site on GitHub
  Pages. It has shipped no real content yet: the live site is empty (TODO.md
  "Deploy").
- This session:
  - answered `server`'s request for every by-hand action pending on the owner;
  - recorded that action in TODO.md in `server`'s format;
  - started on the question of where portfolio content comes from.

## 2. Current State
### ✅ Completed
- **Replied to `server`** (it collects pending by-hand actions across the box).
  This repo has one: the Drive-folder share. Decisions were mentioned in one
  line only, as `server` asked.
- **PR #16, merged** (merge commit `e952904`; confirmed with
  `git merge-base --is-ancestor`). It adds `### Waiting on the owner` at the top
  of `## Open work` in `TODO.md`, with one item in `server`'s required format:
  `- [ ] **Owner runs:** \`<action>\` — why · confirm: \`<check>\` · urgency · since YYYY-MM-DD`.
  - The item is the Drive-folder share. Confirm check: `gdocs.py` can list the
    folder. Since 2026-10-14.
  - **The service account's email is deliberately left out.** The repo is
    PUBLIC. The line points to `client_email` in
    `~/.config/server-ops/gdocs-sa.json` instead. That key file was never
    opened.
  - The export cron is `server`'s to install, so it stays an ordinary Content
    item, not an "Owner runs" line.
  - Self-merged under the core rule: markdown only, outside published paths, no
    synced file, CI green.
- **Convention (relayed by `server`, not confirmed by the owner in this
  session):** each repo keeps its own by-hand actions in its `TODO.md` under
  `### Waiting on the owner`, and `server` reads them across the box. Add new
  owner actions there, in that format.

### ⚠️ In Progress
- **Content source inventory: proposed, not started.** The owner said "we
  actually need to list out all the source stuff". The proposal is one row per
  project: what it is, its dates, whether the repo is public, whether it's worth
  an entry, and the claims the owner must confirm. **We stopped on an unanswered
  question:** where does the inventory live? It names private repos, so it
  can't go in this public repo. The options offered were the private `job-search`
  repo (another session's repo, so ask that session) or a private file on the
  server outside any repo.

### ❌ Blocking Issues
- The live site is still empty. Every Content item needs facts confirmed by the
  owner (CLAUDE.md: never invent facts).
- The Google Docs pipeline is blocked on the Drive-folder share and the other
  owner decisions (2026-10-14 handoff §4).

## 3. Technical Learnings
- **GitHub access:** `gh repo list PeterFriedrich --limit 100` returns all 68
  repos, public and private (checked 2026-11-27).
  - About 25 were pushed in 2026, mostly the box's projects.
  - About 40 are older (2017–2025). A few match v1 write-ups:
    `machine-sound-prediction` matches "machine reliability from sound". Other
    old repos could become entries: `StatsCan-PUMF-Analysis`,
    `housing-edmonton`, `biochar_data`, `camvid_deploy`, `algo_viz`. That list
    comes from repo names only; none were opened.
- **LinkedIn:** scraping is out (terms of service and active blocking), and
  there's no API that returns your own full profile. The route is the owner's
  own data export: `Positions.csv`, `Education.csv`, `Skills.csv`,
  `Profile.csv`. This is from the 2026-10-14 notes, which say "from model
  knowledge, not re-verified", and it is still unverified. The export must be
  stored privately, never in this repo.
- **Google Drive:** the claude.ai Drive connector works from this session
  (2026-10-14 handoff §3).
- **Permissions gotcha:** a Bash call that chained `gh auth status` with other
  commands was denied. Split into separate calls, `gh repo list` alone worked.
- The `todo_archive.py` tool has no `--help`. Running it with any arguments runs
  it for real (here it said "nothing closed to move").

## 4. Next Steps (prioritized)
1. **Ask the owner where the source inventory lives**, unless they've already
   answered: `job-search`, or a private file outside any repo. If it's
   `job-search`, message that session first. Then build the inventory from
   `gh repo list`, each repo's README and commit dates, and `archive/v1-2022/`.
   Drive and the LinkedIn export come in when available.
2. From the inventory, the owner picks the first entry. Draft it with
   `draft: true` and list every claim for confirmation. That entry closes
   "The live site is currently EMPTY".
3. Still waiting on the owner:
   - the Drive-folder share (the "Owner runs" line in TODO.md);
   - the sitemap-as-published-signal row in `docs/DECISIONS.md` (2026-11-18
     handoff §4);
   - the content-repo name and approval of the export cron (2026-10-14
     handoff §4).

## 5. Restoration Procedure
- `npm ci && npm run build && npm test`; `npm run guards`.
  `git config core.hooksPath .githooks` on a fresh clone.
- State not in this repo: unchanged from `docs/DEPLOY.md`. This session changed
  no Pages, DNS or repo settings.
