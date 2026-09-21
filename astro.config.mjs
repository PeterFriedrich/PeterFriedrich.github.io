// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// ⚠️ `site` must match where the build is actually served, or every absolute
// URL the build generates (canonical link, sitemap, RSS <link>) points somewhere
// that does not exist — and nothing fails loudly when it is wrong.
//
// This assumes the repo is named `PeterFriedrich.github.io`, which serves at the
// USER-SITE ROOT. If the repo is ever renamed back to a project repo, the site
// moves to `https://peterfriedrich.github.io/<repo>/` and `base` must be set to
// `/<repo>` alongside it — see docs/DECISIONS.md. `tests/site-config.test.mjs`
// pins the two together so they cannot drift apart silently.
export default defineConfig({
  site: 'https://peterfriedrich.github.io',
  trailingSlash: 'ignore',
  integrations: [mdx(), sitemap()],
  markdown: {
    shikiConfig: {
      // Two themes, switched by CSS media query — no client JS, no flash.
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: true,
    },
  },
  build: {
    // One stylesheet inlined per page beats a blocking request for a site this
    // small; above this size it is cheaper to let the browser cache a file.
    inlineStylesheets: 'auto',
  },
});
