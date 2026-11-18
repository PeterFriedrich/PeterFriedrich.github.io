# Session State & Handoff — a private repo reads the published project list

## 0. Session Metadata
- **Model:** Opus 5.5 (`claude-opus-5-5`) — one model throughout, no mid-session switch
- **Effort:** `medium` (from `$CLAUDE_EFFORT`, checked not recalled)
- **Date / session #:** 2026-11-15 → 2026-11-18, S4 of this repo. No code
  changed; this session was read-only plus one cross-session exchange.

⚠️ **This file stands alone, but does not replace the 2026-10-14 handoff.**
That one still owns the Google Docs pipeline plan (§2–§4 there) and is
unchanged. The content backlog lives in `TODO.md`.

## 1. Goal

**The project:** Peter Friedrich's portfolio + blog, a static Astro site on
GitHub Pages at `https://peterfriedrich.github.io`. No JS to the reader, no
webfonts, no analytics.

**This session:** resume from the 2026-10-14 handoff, then answer another
session on the server that wants to read this site's published project list
(the owner wants the portfolio kept in step with work that lives in a private
repo).

## 2. Current State

### ✅ Completed

- Verified the 2026-10-14 handoff commit `632f8d2` is on `origin/main`
  (PR #14 merged). That branch is dead; this handoff is on
  `claude/handoff-2026-11-18`, cut from `origin/main`.
- **Answered a private repo's questions on reading the published list.** The
  agreement, as recorded on both sides:
  - **"Published" = present in the deployed sitemap**
    (`https://peterfriedrich.github.io/sitemap-index.xml` → `sitemap-0.xml`).
    It is built after the single draft filter in `src/lib/content.ts`, and
    `tests/content.test.mjs` asserts no draft reaches `dist/`.
  - **Metadata comes from frontmatter in the local clone**
    (`src/content/projects/*.md`, `src/content/blog/*.md`). Missing `draft`
    means false. The reader does not re-implement the draft rule.
  - Trailing slashes are normalised (`trailingSlash: 'ignore'`; RSS links
    `/blog/<slug>/`). RSS is blog-only, so it is not a project source.
  - No proof link is guessed before a page is live. Slugs are permanent once
    published, but none are published yet.
  - `example-project.md` and `how-this-site-works.md` are placeholders and are
    never cited.
  - **`TODO.md` stays the only write-up backlog.** The other repo keeps no
    ranking of its own. It will hand the owner a list of claims with no public
    proof, and the owner ranks this repo's Content items through this session.
  - A build-time `projects.json` was offered as a possibility only. It is a
    new public route, so it needs an owner-approved plan (CLAUDE.md) and is
    **not** agreed.
  - Writing portfolio prose from the other repo's claims still requires the
    owner to confirm each fact (CLAUDE.md's no-invented-facts rule).
- ⚠️ **Privacy constraint from that exchange:** the other repo is private and
  holds personal details. Nothing from it goes into this public repo, commits
  or PR text. Refer to it only as "a private repo reads the published project
  list". This file follows that.

### ⚠️ In Progress

- **Offered, awaiting the owner:** a `docs/DECISIONS.md` row recording "the
  deployed sitemap is the published signal for outside readers"
  (`[unverifiable]`, worded per the privacy constraint above). Not added.

### ❌ Blocking Issues

None technical. The site is still EMPTY. Confirmed 2026-11-15: both entries
are `draft: true`, and the live sitemap lists only the index pages. Content is
blocked on owner input (no invented facts).

## 3. Technical Learnings

- `src/pages/rss.xml.js` emits **blog posts only**, via `publishedPosts()`.
  Projects are in the sitemap but not in the feed.
- `astro.config.mjs`: `site: 'https://peterfriedrich.github.io'`,
  `trailingSlash: 'ignore'`, `@astrojs/sitemap` integration.
- `TODO.md` "### Content" has **no ranked order**: 5 v1 ports (DriQ Health,
  Azolla SOC, machine reliability from sound, AMII solar capstone, UAIS skin
  cancer) and 4 newer projects (`edmonton-tax-viz`, `alberta-regional-viz`,
  `noise-complaint-map`, `cc-data-project-template`).
- Report notebooks published by other repos' Pages sites sit under this
  hostname (e.g. `/edmonton-tax-viz/notebooks/...`) but are **not** in this
  site's sitemap. Check them by HTTP status, not via the sitemap.

## 4. Next Steps (prioritized)

1. Ask the owner: add the sitemap-as-published-signal row to
   `docs/DECISIONS.md`? If yes, add it with `[unverifiable]` and run
   `npm run guards`.
2. When the owner ranks the Content items (fed by the list of claims with no
   public proof), reorder `TODO.md` "### Content" to match.
3. Still open from 2026-10-14 §4: the Google Docs pipeline (blocked on the
   Drive folder, content-repo name and cron approval), the content backlog,
   the `gh issue list --state open` CLAUDE.md line, then tag pages, an OG
   image and the dark-mode contrast check.

## 5. Restoration Procedure

```bash
cd ~/PeterFriedrich.github.io
npm ci                                 # Node >= 22.12 required (server: 22.23.2)
git config core.hooksPath .githooks    # already set in this clone
npm run build && npm test              # build FIRST or content tests skip
npm run guards                         # uses python3.12 if present
```

**Not in this repo:** repo name / Pages source / DNS (`docs/DEPLOY.md`); the
server's Node 22 install; the service-account key and `gdocs.py`
(server-ops); the other repo's copy of the agreement in §2.
