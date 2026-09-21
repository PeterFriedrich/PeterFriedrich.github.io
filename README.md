# peterfriedrich.github.io

Portfolio and blog. Static [Astro](https://astro.build) site, built by GitHub
Actions, served by GitHub Pages.

**Live:** https://peterfriedrich.github.io/ *(after the repo rename — see
`docs/DEPLOY.md`)*

## Quick start

```bash
npm ci
git config core.hooksPath .githooks   # hooks are NOT cloned; see below
npm run dev                           # http://localhost:4321
```

| Command | What it does |
|---|---|
| `npm run dev` | Dev server, drafts visible |
| `npm run build` | Static build into `dist/` |
| `npm test` | Invariants asserted against `dist/` — **build first** |
| `npm run new:post "Title"` | Scaffold a post with valid frontmatter |
| `npm run new:project "Name"` | Scaffold a project entry |
| `npm run guards` | Doc-citation and decisions-log checks |

## Writing

One markdown file per post in `src/content/blog/`. The filename is the URL. A
new post needs no nav edit, no index entry, no config change — it appears in the
listing, the home page, the feed and the sitemap automatically.

`draft: true` renders locally and is dropped from the production build. Publishing
is that one flag. Full contract: `docs/CONTENT.md`.

## What this site deliberately does not do

- **Ship JavaScript.** Not a byte, site-wide — enforced by
  `tests/content.test.mjs`. An interactive chart in one post is possible and is
  a `docs/DECISIONS.md` row, not a quiet test edit.
- **Load webfonts.** System font stack only.
- **Run analytics, comments, or a newsletter.** Each is a third-party script.

The result is a ~2.5 KB home page with one stylesheet and no render-blocking
requests.

## Layout

```
src/
  content/          blog/ and projects/ — markdown, schema-checked
  content.config.ts the frontmatter contract
  lib/content.ts    the ONLY place drafts are filtered
  layouts/          page shells
  components/       head, header, footer, listings
  pages/            routes; [...id].astro generate from collections
  styles/global.css the whole stylesheet
docs/               decisions, deploy, content model, ledgers
scripts/            guards (check_*.py) and the handoff hook
tools/              maintenance (todo_archive.py, new-post.mjs)
tests/              node --test invariants, asserted against dist/
session-summary/    session handoffs; archive/ holds all but the newest 3
archive/v1-2022/    the hand-written site this replaced. Never built.
```

## Working on this with Claude Code

The workflow apparatus is ported from
[`cc-data-project-template`](https://github.com/PeterFriedrich/cc-data-project-template),
where each piece was earned by a failure it now prevents. The theme: **a working
guard on a channel nobody reads is not a guard.**

| Piece | What it prevents |
|---|---|
| `CLAUDE.md` | Sessions that start without the rules — including "never invent facts about the owner's work" |
| `/handoff` skill + `scripts/handoff_gap.py` (SessionStart/End hooks) | Context wiped without a written record. The hook **names the unrecorded commits** and is silent when nothing is owed |
| `/site-audit` skill + `docs/AUDIT_LEDGER.md` | Audits that sweep broadly, re-run what already ran, or never record a verdict |
| `/new-post` skill | A draft that stalls on mechanics, and invented biography |
| `.githooks/pre-push` | Pushing to a branch whose PR already merged (work reaches origin, never `main`) |
| `tests/loaded-path.test.mjs` | The handoff pile growing into every session's mandatory reading |
| `tests/content.test.mjs` | A draft that publishes; JavaScript that creeps in; a page with no canonical URL |
| `tests/site-config.test.mjs` | `site`/`base` silently wrong after a repo rename — green build, 404 URLs |
| `scripts/check_decisions_log.py` | A decision recorded with no guard; a superseded row left looking current |
| `scripts/check_doc_citations.py` | A doc citation that rots in place (line numbers banned, `§N` verified) |
| `tools/todo_archive.py` | Closed work accumulating in the file read first every session |
| `.github/workflows/ci.yml` | A merge gate that is offline, secret-free, and therefore never ignored for flaking |

The two Python tools stayed Python rather than being rewritten for a
single Node toolchain: they carry bug fixes earned by real failures, and
rewriting them would re-run those failures for tidiness. They are stdlib-only —
nothing to install. Reasoning in `docs/DECISIONS.md`.

**Not ported:** the retrieval-logging hook and `tools/retrieval_report.py`
(overkill at this size), and the template's dataset ledgers, which have no
subject here. Tracked in `TODO.md`.

⚠️ **Hooks are not cloned.** `git config core.hooksPath .githooks` after every
fresh clone, or the pre-push guard is off.
