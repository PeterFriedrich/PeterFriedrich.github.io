# Working on this site

## The loop

```bash
npm run dev                    # write
npm run build && npm test      # check what actually ships
git commit && git push
```

Merging to `main` deploys. There is no other publish step.

## Rules that are not negotiable

1. **Never invent facts about the owner or their work.** Dates, employers,
   metrics, what a project did, whether something is "currently" anything. If
   it is not in the repo, in `archive/v1-2022/`, or in what the owner just
   said — ask. A plausible invention on a portfolio is a lie told in public
   under someone's name.
2. **No JavaScript reaches the reader.** `tests/content.test.mjs` enforces it. A
   page that genuinely needs interactivity is a `docs/DECISIONS.md` row.
3. **Test against `dist/`, not source.** "The listing filters drafts" and "the
   draft is not on the internet" are different claims.
4. **A decision that protects a behaviour is a test first, prose second.** Write
   the guard, then cite it in `docs/DECISIONS.md`. Design and taste calls are
   tagged `[unverifiable]` — most rows here legitimately are.

## Where a change goes

| Change | Where |
|---|---|
| A post or project entry | `src/content/` — nothing else |
| A new top-level page | `src/pages/<name>.astro` + `NAV` in `src/consts.ts` |
| Styling | `src/styles/global.css` — check **both** colour schemes |
| A frontmatter field | `src/content.config.ts` + `docs/CONTENT.md` + the scaffolder |
| Anything deploy-shaped | Read `docs/DEPLOY.md` first |

## Before you open a PR

- `npm run build && npm test` — the build must come first or the content tests
  skip themselves.
- `npm run guards` — doc citations and the decisions log.
- If a decision locked, add the `docs/DECISIONS.md` row in the same PR.
- If a TODO item closed, tick it and run `python3 tools/todo_archive.py`.

CI runs all of this on every PR. It is offline and secret-free, so it cannot go
red for a reason unrelated to the change.

## Conventions

- Smallest change that satisfies the request. No drive-by refactors.
- Comments explain *why*, not *what*.
- Deleting obsolete code is preferred over leaving it behind.
- Query collections through `src/lib/content.ts`, never `getCollection()`.
