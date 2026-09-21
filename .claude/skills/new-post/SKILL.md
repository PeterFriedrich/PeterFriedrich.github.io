---
name: new-post
description: >
  Draft, edit, and publish a blog post or project entry on this site. Use when
  the user wants to write, draft, start, or publish a post, article, write-up,
  or project entry — "write a post about X", "add a project entry for Y",
  "publish the draft", "turn these notes into a post".
---

# Writing on this site

The bottleneck on a personal blog is never the tooling; it is the blank page and
the half-finished draft. This skill exists to keep the mechanical parts out of
the way, not to write in the owner's voice — **it does not.**

## Scaffold

```bash
npm run new:post "A title with spaces"      # -> src/content/blog/a-title-with-spaces.md
npm run new:project "Project name"          # -> src/content/projects/project-name.md
```

Both land with `draft: true` and refuse to overwrite an existing file. The
filename is the URL; changing it later breaks any link anyone has shared, so get
the slug right at the start.

## The rules that matter

1. **`description` is required.** One sentence. It is the meta description, the
   listing blurb, and the RSS summary — the three places a reader decides
   whether to click. The build fails without it, on purpose.
2. **A draft is invisible in production.** `draft: true` renders in
   `npm run dev` and is dropped from every listing, the feed, the sitemap and
   its own page. `tests/content.test.mjs` fails the build if one leaks.
3. **Publishing is one flag.** `draft: false`, commit, merge to `main`. There is
   no other step.
4. **Never invent facts about the owner's work.** Dates, employers, model
   metrics, what a project did or achieved — if it is not in the repo, in the
   archived v1 site, or in what the user just told you, ask. A plausible
   invention on a portfolio is a lie told in public under their name.

## Drafting with the user

- Ask what the post is *for* before drafting: an argument, a walkthrough, or a
  record. The three have different shapes and mixing them is why drafts stall.
- Write the strongest version of the point in two sentences first, and check it
  with the user. If those two sentences are not interesting, the post is not
  either, and no amount of drafting fixes that.
- Prefer the specific: the actual number, the actual error message, the thing
  that broke. Generalities are what makes technical writing unreadable.
- **A post that ends with what it got wrong is worth more than one that does
  not.** It is also the section only the author can write.

## Before it ships

```bash
npm run build && npm test
```

`npm test` asserts against `dist/` — the draft check, the no-JavaScript
promise, canonical URLs and descriptions on every page. A post that needs
client-side JavaScript (an interactive chart) breaks the no-JS test **by
design**: that is a decision, so write the `docs/DECISIONS.md` row rather than
loosening the test quietly.
