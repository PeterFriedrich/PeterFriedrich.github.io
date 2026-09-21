# Decisions Index

Append-only. **One ROW per locked decision** — when, what, why (including what
was rejected), and a pointer to where the argument lives in full. When a
decision locks, add a row; when one is superseded, strike it (`~~...~~`) or mark
it `SUPERSEDED <date>` in place and add the successor — don't delete history.

**What a row owes you:**

1. ⚠️ **EVERY ROW CARRIES A POINTER** — to a doc, a test, or a file whose
   comment header holds the argument. Code moves; the reasoning has to live
   somewhere prose can hold it. `scripts/check_doc_citations.py` checks that
   every doc pointer resolves.
2. **The row is a self-contained summary** and may paraphrase the argument.
3. **The pointer is the authority.** When a row and its target disagree, the
   target wins and the row gets fixed.
4. **A row names the test that protects it, or carries `[unverifiable]`.**
   `scripts/check_decisions_log.py` enforces this on the merge gate.
   ⚠️ On a site, **most rows are legitimately `[unverifiable]`** — taste,
   voice, and layout have nothing to assert. The tag is not an admission of
   sloppiness here; it is the honest answer for a design call. Reserve real
   test citations for decisions that protect a *behaviour*: what gets
   published, what URLs resolve, what ships to the reader.

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-09-21 | **Astro, not Jekyll / Eleventy / hand-written HTML.** Chosen for: zero JS shipped by default, markdown posts with a schema-checked frontmatter contract, built-in RSS + sitemap + image optimization, and an escape hatch for an interactive chart in a single post without making the whole site a JS app. Jekyll was rejected for the Ruby toolchain and slower iteration; hand-written HTML for not surviving post five. `[unverifiable]` — a stack choice has nothing to assert. | `README.md`, `CONTRIBUTING.md` |
| 2026-09-21 | **No JavaScript is shipped to the reader, site-wide.** The site's one hard performance promise. A page that genuinely needs interactivity supersedes this row rather than editing the test quietly. Protected by `content.test.mjs` — "no page ships javascript". | `docs/CONTENT.md`, `src/styles/global.css` header |
| 2026-09-21 | **No webfonts; system font stack only.** The fastest font is the one already resident. A webfont costs a render-blocking request on the critical path for a typographic preference. `[unverifiable]` | `src/styles/global.css` header |
| 2026-09-21 | **The site is a USER site at the root (`peterfriedrich.github.io`), not a project site at `/main-portfolio/`.** Cleaner URLs, no `base` to thread through every link, and a custom domain can be pointed at it later without moving anything. Requires the repo to be renamed — until then the live URLs are wrong. Protected by `site-config.test.mjs` — "site is the user-site root and base is unset". | `docs/DEPLOY.md` |
| 2026-09-21 | **Workflow apparatus is ported from `cc-data-project-template` rather than reinvented, and its two Python tools stay Python.** `handoff_gap.py` and `todo_archive.py` carry bug fixes earned by real failures (the archive-overwrite bug, the orphaned-child-item bug, the 3.6-compatibility bug); rewriting them in Node to keep one toolchain would re-run those failures for the sake of tidiness. They are stdlib-only, so there is nothing to install. `[unverifiable]` | `README.md`, `docs/TOKEN_EFFICIENCY.md` |
| 2026-09-21 | **Drafts are filtered in exactly one place (`src/lib/content.ts`), and the guard asserts against `dist/`, not source.** Three separate filters — listing, feed, sitemap — is three chances to publish something early, and a source-level test passes over a build that leaked. Protected by `content.test.mjs` — "a draft never reaches dist". | `docs/CONTENT.md` |
| 2026-09-21 | **The merge gate and the publish gate are separate workflows that both run the full check set.** `deploy.yml` rebuilds and re-tests rather than trusting that `ci.yml` was green on the same commit: "another workflow passed" is a proxy for "what I am about to publish is sound", not the thing itself. `[unverifiable]` | `.github/workflows/deploy.yml` header |
