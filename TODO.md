# TODO

The source of truth for what's left. Read first every session; update in place.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce
the symptom before acting on it.

## Open work

### Blocking the first deploy

- [ ] **Rename the repo to `PeterFriedrich.github.io`** — GitHub Settings →
      General → Repository name. Until this happens the site serves at
      `/main-portfolio/` and every absolute URL the build emits is wrong.
      `tests/site-config.test.mjs` pins `site` to the user-site root; it will
      keep passing while the live URLs 404, because a test cannot see the repo's
      name. Done when `https://peterfriedrich.github.io/` serves the new site.
- [ ] **Set Pages source to "GitHub Actions"** — Settings → Pages → Build and
      deployment → Source. On the default "Deploy from a branch", `deploy.yml`
      goes green and publishes nothing. See `docs/DEPLOY.md`.
- [ ] **Publish at least one real project entry before merging to `main`** —
      the seeded entries are `draft: true`, so a deploy today replaces the v1
      site with an empty one. Either port a project (below) or accept the empty
      launch deliberately.

### Content

- [ ] **Port the five v1 project write-ups** from `archive/v1-2022/index.html`,
      one entry each, checking every claim and link before it goes live:
      Omdena/DriQ Health IoT monitoring, Omdena/Azolla soil organic carbon,
      machine reliability from sound, AMII solar power capstone, UAIS skin
      cancer webapp. ⚠️ Several link to Google Drive and Omdena pages from
      2021 — **verify each still resolves**; link rot is the likely finding.
- [ ] **Add entries for the recent work** that post-dates v1:
      `edmonton-tax-viz`, `alberta-regional-viz`, `noise-complaint-map`,
      `cc-data-project-template`. These are the strongest portfolio pieces and
      none of them are on the site.
- [ ] **Rewrite `src/pages/about.astro` in your own voice** — the current text
      is stitched from the v1 About section and is deliberately thin.
- [ ] **Write the first real post, or delete `how-this-site-works.md`** — it is
      a draft template masquerading as a colophon. Decide which it is.

### Site

- [ ] **Decide on tag pages** — tags are displayed but not browsable. Either
      build `/tags/[tag]` or stop rendering them as if they were links.
- [ ] **Add an OG image** — link previews are currently text-only. A single
      static image is enough; per-post generated images are not worth the build
      complexity yet.
- [ ] **Check contrast in dark mode** against WCAG AA, specifically
      `--fg-muted` on `--bg` and `--accent` on `--bg`. Untested, asserted by
      eye only.

### Workflow apparatus

- [ ] **Extract `.claude/` into a plugin** once a workflow fix has to be
      hand-copied between this repo and `cc-data-project-template` a second
      time. The `/handoff` skill, `handoff_gap.py`, `.githooks/pre-push` and
      `todo_archive.py` now exist in two places and will drift.
- [ ] **Decide whether `tools/retrieval_report.py` is worth porting** — the
      Read/Grep/Glob logging hook was deliberately left out of
      `.claude/settings.json` as overkill for a repo this size. Revisit if
      context pressure ever becomes real here.

## Done
