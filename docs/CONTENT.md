# Content model

Two collections, both markdown, both defined and schema-checked in
`src/content.config.ts`. A typo in a frontmatter key fails the build rather than
quietly rendering a page with a missing date.

## Where things go

| What | Path | URL |
|---|---|---|
| Blog post | `src/content/blog/<slug>.md` | `/blog/<slug>` |
| Project entry | `src/content/projects/<slug>.md` | `/projects/<slug>` |
| Standalone page | `src/pages/<name>.astro` | `/<name>` |

The filename **is** the URL. Renaming a file after publishing breaks every link
anyone has shared; pick the slug carefully the first time.

```bash
npm run new:post "A title with spaces"     # scaffolds valid frontmatter
npm run new:project "Project name"
```

## Frontmatter

**Blog** — `title`, `description`, `pubDate` required; `updatedDate`, `tags`,
`draft` optional.

**Projects** — `title`, `description`, `year` required; `period`, `status`
(`active` / `complete` / `archived` / `paused`), `tags`, `repo`, `url`,
`featured`, `order`, `draft` optional.

`description` is required on both and is not decoration: it is the meta
description, the listing blurb, and the RSS summary — the three places a reader
decides whether to click.

## Drafts

`draft: true` renders in `npm run dev` and is dropped from the production build:
listings, home page, RSS, sitemap, and its own page. Publishing is that one flag.

⚠️ **Every list of entries goes through `src/lib/content.ts`**, never
`getCollection()` directly. One filter, one place — three separate filters is
three chances to publish something early. `tests/content.test.mjs` asserts
against `dist/` rather than source, because "the listing filters drafts" and
"the draft is not on the internet" are different claims.

## Ordering

Posts sort by `pubDate`, newest first. Projects sort by `order` then `year`
descending; the home page shows those with `featured: true`.

## What the site does not do

- **Tags are displayed, not browsable.** There are no `/tags/<tag>` pages yet.
  Tracked in `TODO.md` — either build them or stop styling tags like links.
- **No comments, no analytics, no newsletter.** Each is a third-party script,
  and the site ships no JavaScript.
- **No draft preview URLs.** A draft is local-only until the flag flips.
