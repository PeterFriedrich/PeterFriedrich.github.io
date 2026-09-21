/**
 * Invariants on the BUILT SITE — asserted against `dist/`, not against source.
 *
 * ⚠️ The distinction is the whole point. "The listing filters drafts" and "the
 * draft is not on the internet" are different claims, and only the second one
 * matters. A source-level test passes over a build that leaked the file through
 * a route, a feed or a sitemap that forgot the filter. So these read the
 * artifact that actually gets uploaded.
 *
 * Requires `npm run build` first; skips (loudly) if dist/ is absent, so a bare
 * `npm test` on a fresh clone reports "not checked" rather than a false pass.
 */
import { test, skip } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, existsSync, statSync } from 'node:fs';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = join(REPO, 'dist');
const CONTENT = join(REPO, 'src', 'content');

const built = existsSync(DIST);

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

/** Every markdown entry marked `draft: true`, by slug. */
function draftSlugs() {
  const slugs = [];
  for (const kind of ['blog', 'projects']) {
    const dir = join(CONTENT, kind);
    if (!existsSync(dir)) continue;
    for (const f of readdirSync(dir)) {
      if (!/\.mdx?$/.test(f)) continue;
      const src = readFileSync(join(dir, f), 'utf8');
      const fm = src.split('---')[1] ?? '';
      if (/^draft:\s*true\s*$/m.test(fm)) {
        slugs.push({ kind, slug: f.replace(/\.mdx?$/, '') });
      }
    }
  }
  return slugs;
}

test('a draft never reaches dist', { skip: built ? false : 'run `npm run build` first' }, () => {
  const drafts = draftSlugs();
  const files = walk(DIST);
  const haystack = files
    .filter((f) => /\.(html|xml)$/.test(f))
    .map((f) => readFileSync(f, 'utf8'))
    .join('\n');

  for (const { kind, slug } of drafts) {
    const route = kind === 'blog' ? `/blog/${slug}` : `/projects/${slug}`;
    assert.ok(
      !files.some((f) => relative(DIST, f).includes(slug)),
      `draft "${slug}" has its own page in dist/ — it is published.`,
    );
    assert.ok(
      !haystack.includes(route),
      `draft "${slug}" is linked from a built page, feed or sitemap (${route}).`,
    );
  }
});

test('the feed and the sitemap exist and are non-empty', { skip: built ? false : 'run `npm run build` first' }, () => {
  for (const f of ['rss.xml', 'sitemap-index.xml', '404.html', 'robots.txt']) {
    const p = join(DIST, f);
    assert.ok(existsSync(p), `dist/${f} was not built`);
    assert.ok(statSync(p).size > 0, `dist/${f} is empty`);
  }
});

test('no page ships javascript', { skip: built ? false : 'run `npm run build` first' }, () => {
  // The site's one hard performance promise (README, docs/DECISIONS.md). An
  // integration or a stray client directive breaks it silently — the page still
  // renders, just slower for everyone. If a post ever genuinely needs an
  // interactive chart, change this test deliberately and write the row.
  const offenders = walk(DIST)
    .filter((f) => f.endsWith('.html'))
    .filter((f) => /<script(?![^>]*\btype=["']application\/ld\+json["'])/i.test(readFileSync(f, 'utf8')))
    .map((f) => relative(DIST, f));
  assert.deepEqual(
    offenders,
    [],
    `these pages carry a <script> tag: ${offenders.join(', ')}`,
  );
});

test('every built page has a canonical url and a description', { skip: built ? false : 'run `npm run build` first' }, () => {
  for (const f of walk(DIST).filter((p) => p.endsWith('.html'))) {
    const html = readFileSync(f, 'utf8');
    const where = relative(DIST, f);
    assert.match(html, /<link rel="canonical" href="https:\/\//, `${where}: no absolute canonical URL`);
    assert.match(html, /<meta name="description" content="[^"]+"/, `${where}: empty or missing description`);
  }
});
