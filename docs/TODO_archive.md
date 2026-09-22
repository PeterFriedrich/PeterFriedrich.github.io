# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **Rename the repo to `PeterFriedrich.github.io`** — DONE 2026-09-21.
      The repo is `PeterFriedrich/PeterFriedrich.github.io` and
      `curl -sI https://peterfriedrich.github.io/` returns `HTTP/2 200`. `site`
      in `astro.config.mjs` and the absolute sitemap URL in `public/robots.txt`
      now match what is actually served. For ~4 minutes between the merge and
      the rename the site was live at `/main-portfolio/` with every internal
      link pointing at a root that was not ours — the failure `docs/DEPLOY.md`
      predicts, observed.

- [x] **Set Pages source to "GitHub Actions"** — DONE (already set before the
      first deploy). Confirmed by the fact that `actions/configure-pages` and
      `actions/deploy-pages` both succeeded on run #1; neither does when Pages
      is on "Deploy from a branch".
