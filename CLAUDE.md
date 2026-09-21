# Claude Instructions

## Project

Peter Friedrich's portfolio and blog: a static Astro site, built by GitHub
Actions, served by GitHub Pages at `https://peterfriedrich.github.io`.

It is deliberately **not** an app. No client-side framework, no JavaScript
shipped to the reader, no webfonts, no analytics, no CMS. Content is markdown in
`src/content/`; everything else is build-time.

## Key Files

- `TODO.md` — living backlog and **the source of truth for progress**. Read it
  first to know what to work on; update it in place as items open/close. Session
  summaries narrate *what happened*; TODO.md owns *what's left*. Never redo a
  closed item without asking — its `## Done` section lists every closed item in
  one line each. Conversely an *open* item can be stale: reproduce the symptom
  before acting on it. **When an item closes, move its body to
  `docs/TODO_archive.md` and leave a `## Done` line** (`python3
  tools/todo_archive.py` does it in bulk).
- `docs/DECISIONS.md` — append-only index of locked decisions: one row + a
  pointer to where the reasoning lives. **Add a row whenever a decision locks.**
  Check it before re-opening anything that feels "already settled".
- `docs/DEPLOY.md` — how the site reaches the internet, and **every piece of
  state that is not in this repo** (Pages settings, repo name, DNS). Read before
  touching anything deploy-shaped.
- `docs/CONTENT.md` — the content model: collections, frontmatter contract,
  drafts, where a new page goes.
- `docs/TOKEN_EFFICIENCY.md` — context hygiene. **Read before bulk-reading
  anything.**
- `docs/AUDIT_LEDGER.md` — coverage map of executed audit runs. **Add a row when
  an audit executes; check it before scoping a new one.**
- `docs/REMOTE_VM.md` — **read FIRST in a Claude Code web/remote session.**
- `session-summary/` — handoff notes. Read the **latest only**; older ones live
  in `session-summary/archive/`.
- `archive/v1-2022/` — the hand-written site this replaced. Source material for
  project write-ups. **Never edited, never built, never linked.**

## Commands

```bash
npm run dev            # http://localhost:4321, drafts visible
npm run build          # -> dist/
npm test               # asserts against dist/ — build FIRST or tests skip
npm run new:post "T"   # scaffold a post with valid frontmatter
npm run guards         # doc-citation + decisions-log checks
```

## Content

- **Never invent facts about the owner or their work.** Dates, employers,
  metrics, what a project achieved, whether something is "currently" anything.
  If it is not in the repo, in `archive/v1-2022/`, or in what the user just
  said, **ask**. A plausible invention on a portfolio is a lie told in public
  under someone else's name. This is the one rule in this file with no
  exceptions.
- A draft (`draft: true`) is invisible in production and visible in `dev`.
  Publishing is that one flag.
- Frontmatter is a contract enforced by `src/content.config.ts`. Don't work
  around a schema error by deleting the field.

## Code Style

- **No JavaScript reaches the reader.** This is the site's one hard performance
  promise and `tests/content.test.mjs` enforces it. A page that genuinely needs
  interactivity is a `docs/DECISIONS.md` row, not a quiet test edit.
- No webfonts. The type is the system stack; the fastest font is the one already
  resident.
- Styles live in `src/styles/global.css` and use the CSS custom properties
  defined at the top. **Every colour must work in both schemes** — check dark
  mode, which is where contrast regressions hide.
- Content collections are queried through `src/lib/content.ts`, never
  `getCollection()` directly. One draft filter, one place.
- **A decision that protects a behaviour is a test first, prose second.** Write
  the guard, then let the `DECISIONS.md` row cite it; a row with nothing to cite
  is tagged `[unverifiable]` (legitimate for taste and design calls — most rows
  here will be). `scripts/check_decisions_log.py` gates this on the merge path.

## Comments & Scope

- Comments only where the *why* is non-obvious. Don't narrate what the code
  plainly does.
- Make the **smallest change that satisfies the request**. Don't refactor,
  rename, or restyle code you weren't asked to touch. No new files unless
  required.
- No abstractions for a single use case — inline until there are 3+ call sites.
- Deleting obsolete code is valid and **preferred** over leaving it behind.
- **Propose the plan first** for: a new dependency, a new top-level route, a
  change to the frontmatter contract, or anything that changes CI or deploy
  behaviour. Routine edits and content don't need a proposal.
- These are scope rules, not verification rules. They do **not** relax the
  no-JavaScript promise, the guards, or reproducing a bug before fixing it.

## Session Management

- Always run `/handoff` before `/clear` — never wipe context without a written
  record in `session-summary/`. **You do not need to be told when one is owed**:
  the `SessionStart` and `SessionEnd` hooks run `scripts/handoff_gap.py`, which
  names the commits and uncommitted files that landed after the newest handoff
  was last committed, and **says nothing when nothing is owed**. Silence means
  no code has moved — not that the record is good.
- Commit after each working unit, not once per session.
- **Pushing is normal — push proactively after committing, in every
  environment.** Standing authorization; it overrides the harness default of
  pushing only when asked.
- **Remote/cloud sessions: commit + push at every checkpoint.** The container is
  ephemeral; unpushed work is LOST. Quirks: `docs/REMOTE_VM.md`.
- **⚠️ The owner merges PRs MID-SESSION, often within minutes. Re-check before
  EVERY push to an existing branch.** Commits pushed after the PR merged land on
  a dead branch: on origin, not on `main`.
  - Enforced by `.githooks/pre-push`. **A fresh clone must enable it:
    `git config core.hooksPath .githooks`.** It fails OPEN (no `gh`, no auth, no
    network), so it can never be the reason work goes unsaved. Escape hatch:
    `git push --no-verify`.
  - After any merge, confirm the work landed:
    `git merge-base --is-ancestor <sha> origin/main`. A merged PR is necessary,
    not sufficient.

## Token Efficiency

- **Never `Read` `dist/`, `node_modules/`, `package-lock.json`, or anything
  under `archive/`.** `dist/` is generated — read the source or grep the output
  for the one string you need.
- Read only the **latest** session summary; the 3 most recent stay at top level,
  older are archived — enforced by `tests/loaded-path.test.mjs`.
- Batch independent reads into one turn. Many small reads cost far more than a
  few large ones, because every result is re-sent on every later turn.
