# Session State & Handoff — site is live; what is left is content

## 0. Session Metadata
- **Model:** Opus 5 (`claude-opus-5`) — one model throughout, no mid-session switch
- **Effort:** `high` (from `$CLAUDE_EFFORT`, checked not recalled)
- **Date / session #:** 2026-09-22 (session ran across the UTC midnight from
  2026-09-21), S2 of the rebuild

⚠️ **This file is written to stand alone.** An earlier handoff in
`session-summary/` covers the build of the Astro site in more detail and will be
archived as it ages out; nothing below depends on reading it.

## 1. Goal

**The project:** Peter Friedrich's portfolio and blog. Static Astro site, built
by GitHub Actions, served by GitHub Pages at `https://peterfriedrich.github.io`.
Deliberately not an app: no JavaScript reaches the reader, no webfonts, no
analytics, no CMS. Content is markdown in `src/content/`.

**This session** rebuilt the repo from scratch (the v1 hand-written HTML site is
archived, not deleted), ported the workflow apparatus from
`PeterFriedrich/cc-data-project-template`, shipped it in two PRs, and got the
site live at the user-site root.

## 2. Current State

### ✅ Completed

- **The site is LIVE and correct** at `https://peterfriedrich.github.io/` —
  owner confirmed `curl -sI` → `HTTP/2 200`.
- **PR #9** (the rebuild) and **PR #10** (backlog reconciliation) both merged.
  `origin/main` is at `b537d2e`.
- **Two Pages deploys, both green.** Run #1 at 21:03Z on the #9 merge, run #2 at
  00:01Z on the #10 merge. Both ran build → 9 tests → upload → deploy.
- **Repo renamed** to `PeterFriedrich/PeterFriedrich.github.io`; Pages source is
  "GitHub Actions". Both were the blocking non-repo settings and both are done.
- Workflow apparatus in place: `/handoff`, `/site-audit`, `/new-post` skills;
  `scripts/handoff_gap.py` on SessionStart/SessionEnd; `.githooks/pre-push`;
  `tools/todo_archive.py`; two doc guards; `ci.yml` (merge gate) and
  `deploy.yml` (publish gate).

### ⚠️ In Progress

Nothing is mid-edit. The working tree is clean and the branch sits on merged
`main`. One thing is *done in the repo but visibly wrong in the world*:

- **⚠️ THE LIVE SITE IS EMPTY.** It deployed with both seeded content entries
  still `draft: true`, so `https://peterfriedrich.github.io/` shows "No projects
  written up yet" and "Nothing published yet" — where the v1 site listed five
  projects. This is the single most important open item and it is the top entry
  in `TODO.md`. The source material is intact in `archive/v1-2022/index.html`.

### ❌ Blocking Issues

None technical. The content work is blocked on **owner input, not on code**:
project facts cannot be invented (see §3), and the v1 write-ups' external links
cannot be checked from this VM (see §3).

## 3. Technical Learnings

### Environment quirks that will bite a fresh session

- **⚠️ THIS VM CANNOT REACH `peterfriedrich.github.io`.** The egress proxy
  answers `403` to `CONNECT` (`connect_rejected` in
  `curl -sS "$HTTPS_PROXY/__agentproxy/status"`). **A failed request from inside
  this container is NOT evidence the site is down.** Every claim about the live
  site in this file came from the GitHub deployment record or from the owner
  running curl themselves. The same applies to the 2021 Google Drive and Omdena
  links in the v1 write-ups: they cannot be verified here, and must not be
  recorded as dead based on a request made from this VM.
- **The GitHub API in this session only accepts the OLD repo name.** The session
  scope is `peterfriedrich/main-portfolio`; passing
  `PeterFriedrich.github.io` to the github MCP tools returns
  `Access denied: repository ... is not configured for this session`. Use
  `repo: "main-portfolio"` — GitHub resolves the rename server-side and returns
  URLs under the new name. `git push` works the same way, via redirect.
- **`git remote get-url origin` reads `.../main-portfolio` and that is fine.**
  It was explicitly set to the new name at one point and came back as the old
  one, most likely re-injected by the environment's git config handling. Pushes
  succeed either way. Not worth fighting.
- **`gh` is not installed here**, so `.githooks/pre-push` exits early and guards
  nothing in this environment. It still must be enabled in any fresh clone:
  `git config core.hooksPath .githooks`.

### Things that were verified rather than assumed

- **The draft-leak test was tautological in its first form.** Flipping
  `draft: true` → `false` in the markdown changes both the assertion's input and
  its subject, so it passes either way. The real check is to break the *filter*
  in `src/lib/content.ts` (make `visible` return `true`) while leaving the
  frontmatter alone; the test then fails with
  `draft "how-this-site-works" has its own page in dist/`. **Re-validate this
  way if that test is ever changed.**
- **`node --test tests/` does not work** on Node 22.22 — it resolves `tests` as
  a module and dies with `MODULE_NOT_FOUND`. The working form, and what
  `npm test` runs, is `node --test 'tests/*.test.mjs'`.
- **Astro is at 7.3.3**, well past the 5.x API in the model's training. The
  content API was read off the installed package, not recalled:
  `src/content.config.ts` (not `src/content/config.ts`), `glob()` from
  `astro/loaders`, `render(entry)` from `astro:content` (**not**
  `entry.render()`), and `entry.id` as the slug (**not** `entry.slug`).
- **Action SHAs were resolved with `git ls-remote`, not recalled.**
  `actions/checkout` is at v7. Both workflows pin by commit SHA with a version
  comment; re-resolve the same way when bumping.
- **Pages source was confirmed indirectly**: `actions/configure-pages` and
  `actions/deploy-pages` both succeeding means the source is "GitHub Actions".
  Neither succeeds on "Deploy from a branch".

### The incident worth remembering

For roughly four minutes between the #9 merge and the rename, **the site was
live and broken**: served at `/main-portfolio/` but built for the root, so every
internal link pointed at a root that was not ours. `docs/DEPLOY.md` predicted
exactly this — the repo name is deploy configuration that lives outside the
repo, cannot be tested, and fails silently. It is now an observed incident, not
a hypothetical. `tests/site-config.test.mjs` pins `site`/`base` together but
**cannot see the repo's name**, so it stayed green throughout.

### Important file locations

| What | Where |
|---|---|
| The only place drafts are filtered | `src/lib/content.ts` |
| Frontmatter contract | `src/content.config.ts` |
| Whole stylesheet | `src/styles/global.css` |
| Deploy state that is NOT in git | `docs/DEPLOY.md` |
| Why anything is the way it is (7 rows) | `docs/DECISIONS.md` |
| Content model, drafts, where a page goes | `docs/CONTENT.md` |
| v1 source material (never edited, never built) | `archive/v1-2022/` |
| Backlog, source of truth | `TODO.md` |

## 4. Next Steps (prioritized)

1. **Get something on the live site.** Read ONE `<article>` block out of
   `archive/v1-2022/index.html` with `sed -n` (do not read the whole file), then
   `npm run new:project "<name>"` and write the entry. The five v1 projects:
   Omdena/DriQ Health IoT nursing-home monitoring, Omdena/Azolla soil organic
   carbon, machine reliability from sound, AMII solar power capstone, UAIS skin
   cancer webapp.
   ⚠️ **Ask the owner to confirm every factual claim and to check each 2021
   Drive/Omdena link.** `CLAUDE.md` forbids inventing facts about the owner's
   work, without exception, and the links cannot be checked from here.
2. **Add entries for the newer repos** that post-date v1 and are currently
   absent from the site: `edmonton-tax-viz`, `alberta-regional-viz`,
   `noise-complaint-map`, `cc-data-project-template`. These are the strongest
   portfolio pieces.
3. **Rewrite `src/pages/about.astro`** in the owner's voice — it is stitched
   from the v1 About section and is deliberately thin. Needs the owner.
4. **Decide on `src/content/blog/how-this-site-works.md`** — publish it as a
   colophon or delete it. It is currently a draft template pretending to be a
   post.
5. **Smaller, not blocked on anyone:** tag pages (`/tags/[tag]` — tags render as
   if browsable and are not), an OG image for link previews, and a dark-mode
   contrast check against WCAG AA for `--fg-muted` and `--accent`.
6. **Extract `.claude/` into a plugin.** `/handoff`, `handoff_gap.py`,
   `pre-push` and `todo_archive.py` now exist in both this repo and
   `cc-data-project-template` and will drift. The template's own README names
   this moment as the trigger.

## 5. Restoration Procedure

```bash
npm ci
git config core.hooksPath .githooks   # hooks are NOT cloned
npm run build && npm test             # build FIRST or the content tests skip
npm run guards                        # doc citations + decisions log
npm run dev                           # http://localhost:4321, drafts visible
```

`npm test` asserts against `dist/`, so a bare `npm test` on a fresh clone
reports skips rather than passes. CI runs build-then-test for this reason.

**Not reproducible from the repo, and not discoverable by reading code:**

- The repo name (`PeterFriedrich.github.io`) — it is the hostname, and it is
  what makes this a user site served at `/` instead of a project site served at
  `/<repo>/`.
- The Pages source setting ("GitHub Actions").
- Any future custom domain, which needs both a DNS record and a `CNAME` file in
  `public/`.

All three are documented in `docs/DEPLOY.md`. Nothing else about the deploy
lives outside the repo.

---

## Update — 01:10Z, after this file's own PR merged

**Metadata for this section:** Opus 5 (`claude-opus-5`), effort `high` (checked,
not recalled), same continuous session.

⚠️ **Small delta on purpose.** Nothing above changed. No code, no content, no
site change landed between the two writings — the site is still live and still
empty. This section exists so the next session is not left wondering whether
something happened in the gap. It did not.

### What actually happened

- **PR #11 (this file) merged** at 00:06Z. `origin/main` is now `eed9e7a`.
  Verified it reached the trunk, not just origin:
  `git merge-base --is-ancestor 9fd76ef origin/main` → true.
- **Deploy run #3 went green** at 00:07Z on the #11 merge. Three deploy runs
  now, all successful. The published site is byte-identical to run #2's — a
  handoff file changes nothing the build reads.
- **The scheduled check-in for PR #11 fired at 01:06Z**, found the PR already
  merged, and stopped per its own instruction. `list_triggers` returns empty:
  **no routines are pending for this repo.** Nothing is waiting to wake this
  session.

### One more environment gotcha, found by tripping over it

**After a PR merges, resetting the local branch onto `main` makes the stop hook
report "unpushed commits" that are not unpushed work.**

`git checkout -B <branch> origin/main` leaves the *remote* feature branch behind
at its old tip, so the local branch looks N commits ahead of its upstream — and
`~/.claude/stop-hook-git-check.sh` reports exactly that. It is not a warning
about lost work.

**Check which it is before reacting:**

```bash
git rev-list --count origin/main..HEAD   # 0 => nothing at risk; it is all on main
git branch -r --contains HEAD            # lists origin/main => already merged
```

If the count is `0`, the "unpushed" commit is the merge commit that is already
on `main`. Pushing is safe and silences the hook (it just fast-forwards the
stale branch); **do not open a PR for it** — there is nothing to review.
`.githooks/pre-push` agrees: it computes the same `origin/main..HEAD` count and
exits 0 when it is zero, treating the push as inert.

### State at the end of this section

| | |
|---|---|
| `origin/main` | `eed9e7a` |
| Local branch | `claude/portfolio-blog-repo-setup-k850v9`, in sync with its remote, 0 ahead of `main` |
| Working tree | Clean; `scripts/handoff_gap.py` silent |
| Handoffs at top level | 2 (limit is 3, enforced by `tests/loaded-path.test.mjs`) |
| Pending routines | None |
| Site | Live, empty, unchanged |

**§4's next steps are unchanged and still correct.** Start there.
