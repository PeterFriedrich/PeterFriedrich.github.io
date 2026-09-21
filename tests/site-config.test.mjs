/**
 * The two config values that are wrong SILENTLY.
 *
 * `site` and `base` decide every absolute URL the build emits — canonical tags,
 * the sitemap, the feed. Get them wrong and the build still succeeds, the pages
 * still render locally, and the live site quietly advertises URLs that 404.
 * Nothing else in the repo notices, which is exactly why this is pinned.
 *
 * If the repo is renamed away from `PeterFriedrich.github.io` (a user site, served
 * at the root), the site moves to a subpath and BOTH values have to change
 * together. This test is the thing that says so out loud.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..');
const config = readFileSync(join(REPO, 'astro.config.mjs'), 'utf8');

test('site is the user-site root and base is unset', () => {
  assert.match(
    config,
    /site:\s*'https:\/\/peterfriedrich\.github\.io'/,
    "astro.config.mjs `site` must be the deployed origin — see docs/DECISIONS.md",
  );
  assert.ok(
    !/^\s*base:/m.test(config),
    'a `base` is set while `site` is the user-site root: one of the two is wrong. ' +
      'A user site (repo named PeterFriedrich.github.io) serves at `/` and needs no base; ' +
      'a project repo serves at `/<repo>/` and needs both.',
  );
});

test('robots.txt points at the sitemap that is actually built', () => {
  const robots = readFileSync(join(REPO, 'public', 'robots.txt'), 'utf8');
  const site = config.match(/site:\s*'([^']+)'/)?.[1];
  assert.ok(site, 'could not read `site` out of astro.config.mjs');
  assert.ok(
    robots.includes(`${site}/sitemap-index.xml`),
    `public/robots.txt advertises a sitemap URL that does not match \`site\` (${site}). ` +
      'A stale absolute URL here is invisible until a crawler follows it.',
  );
});
