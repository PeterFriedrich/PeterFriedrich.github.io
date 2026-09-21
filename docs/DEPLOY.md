# Deploy — how this site reaches the internet

⚠️ **Read this before changing anything deploy-shaped.** Most of what makes the
deploy work is **not in this repo**: it is settings in the GitHub UI. Nothing in
git can see them, no test can assert them, and when one is wrong the workflow
still goes green.

## The path

```
push to main → .github/workflows/deploy.yml
             → npm ci → npm run build → npm test → upload dist/ as a Pages artifact
             → actions/deploy-pages publishes it
             → https://peterfriedrich.github.io/
```

`ci.yml` runs the same checks on every PR. `deploy.yml` re-runs them rather than
trusting CI's green tick on the same commit — see `docs/DECISIONS.md`.

## State that is NOT in this repo

| What | Where | Wrong looks like |
|---|---|---|
| **Repo name** must be `PeterFriedrich.github.io` | Settings → General | Site serves at `/main-portfolio/`; every canonical URL, sitemap entry and feed link 404s. The build is still green. |
| **Pages source** must be **GitHub Actions** | Settings → Pages → Build and deployment | `deploy.yml` succeeds and publishes NOTHING. The live site stays whatever the branch had. This is the failure that looks most like success. |
| **Custom domain** (if ever added) | Settings → Pages + a `CNAME` file in `public/` | Both are required. Setting one without the other reverts on the next deploy. |
| **`site` in `astro.config.mjs`** must match the URL actually served | in this repo | Silently wrong absolute URLs everywhere. `tests/site-config.test.mjs` pins the value, but **it cannot see the repo's name** — the test passes while the site is wrong. |

## If the repo is ever renamed back to a project repo

Two changes, together, or the site breaks in a way nothing catches:

1. `astro.config.mjs`: `site: 'https://peterfriedrich.github.io'` **and**
   `base: '/<repo-name>'`.
2. `tests/site-config.test.mjs`: update both assertions — it currently fails any
   build that sets a `base`, which is what tells you this list exists.

Also update `public/robots.txt`, whose sitemap URL is absolute.

## Checking a deploy actually landed

A green workflow is necessary, not sufficient. After a merge:

```bash
curl -sI https://peterfriedrich.github.io/ | head -1        # 200?
curl -s  https://peterfriedrich.github.io/ | grep -o '<title>[^<]*'
curl -s  https://peterfriedrich.github.io/sitemap-0.xml | head -c 300
```

If the workflow is green and the content is stale, the Pages source setting is
the first thing to check.
