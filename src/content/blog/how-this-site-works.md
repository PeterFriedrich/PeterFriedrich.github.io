---
title: "How this site works"
description: "The build, the content model, and what it costs to add a post — a colophon that doubles as the template for every post after it."
pubDate: 2026-09-21
tags: ["meta", "astro"]
draft: true
---

This file is a working example of a post. Copy it, change the frontmatter, write
below the `---`. Nothing else is required — no nav edit, no index entry, no
build config.

## Adding a post

```bash
npm run new:post "A title with spaces"   # writes src/content/blog/a-title-with-spaces.md
npm run dev                              # http://localhost:4321
```

The filename becomes the URL: `src/content/blog/a-title-with-spaces.md` serves at
`/blog/a-title-with-spaces`. Posts appear in the listing, the home page, the RSS
feed and the sitemap automatically, newest first.

## Frontmatter

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Used in `<title>`, the listing, and the feed |
| `description` | yes | Meta description and the listing blurb — one sentence |
| `pubDate` | yes | Sort key. `YYYY-MM-DD` |
| `updatedDate` | no | Shown next to the publish date when present |
| `tags` | no | Array of strings; displayed, not yet browsable |
| `draft` | no | `true` keeps it out of every production listing |

The schema in `src/content.config.ts` enforces this. A typo in a key name fails
the build rather than quietly rendering a post with no date.

## Drafts

A draft renders in `npm run dev` and is dropped from the production build —
listings, feed, sitemap, and its own page. `tests/content.test.mjs` fails the
build if a draft ever reaches `dist/`, because "it's filtered in the listing"
and "it is not on the internet" are different claims.

## Why it's fast

No JavaScript is shipped. No webfonts are loaded — the type is whatever the
reader's OS already has resident. Every page is HTML generated at build time and
served by GitHub Pages' CDN. Interactive charts are possible when a post needs
one, but they cost JS on that page only, not site-wide.

**Delete this post once you've written a real one** — or flip `draft` to `false`
if the colophon is worth keeping.
