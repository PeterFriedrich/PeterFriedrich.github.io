#!/usr/bin/env node
/**
 * Scaffold a post or a project entry with valid frontmatter.
 *
 * The point is not saving keystrokes — it is that the frontmatter contract in
 * src/content.config.ts is satisfied on the first try. A hand-written file with
 * a missing `description` fails the build with a zod error, which is a fine
 * guard and a lousy way to start writing.
 *
 *   node tools/new-post.mjs blog "Why the join dropped 4% of rows"
 *   node tools/new-post.mjs project "Edmonton tax visualizer"
 */
import { writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const [kind, ...titleParts] = process.argv.slice(2);
const title = titleParts.join(' ').trim();

if (!['blog', 'project'].includes(kind) || !title) {
  console.error('usage: node tools/new-post.mjs <blog|project> "Title"');
  process.exit(2);
}

const slug = title
  .toLowerCase()
  .normalize('NFKD')
  .replace(/[̀-ͯ]/g, '')
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-|-$/g, '');

if (!slug) {
  console.error(`"${title}" has no characters usable in a URL slug.`);
  process.exit(1);
}

const today = new Date().toISOString().slice(0, 10);
const dir = join('src', 'content', kind === 'blog' ? 'blog' : 'projects');
const path = join(dir, `${slug}.md`);

// Never clobber a draft in progress — losing an unfinished post to a
// re-run of a scaffolding command is not a recoverable mistake.
if (existsSync(path)) {
  console.error(`${path} already exists — refusing to overwrite it.`);
  process.exit(1);
}

const escaped = title.replace(/"/g, '\\"');

const body =
  kind === 'blog'
    ? `---
title: "${escaped}"
description: ""
pubDate: ${today}
tags: []
draft: true
---

`
    : `---
title: "${escaped}"
description: ""
year: ${today.slice(0, 4)}
status: "complete"
tags: []
featured: false
order: 100
draft: true
---

## What it does

## How it works

## What it gets wrong

`;

mkdirSync(dir, { recursive: true });
writeFileSync(path, body, 'utf8');
console.log(`${path}

Next: fill in \`description\` (it is required — the build fails without it),
then write. Flip \`draft: false\` when it should be public.`);
