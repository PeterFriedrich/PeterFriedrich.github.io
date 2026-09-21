# Remote VM sessions (Claude Code on the web) — read FIRST in one of these

A remote session is recognizable by: the repo cloned at `/home/user/<repo>`, no
local editor, and a session-specific branch name like `claude/<something>`.

## The rules that differ from local sessions

- **Push proactively at every checkpoint** — see CLAUDE.md "Session
  Management". The container is ephemeral; unpushed work is lost when it idles
  out. Never wait to be told to push.
- **Work on the session's designated branch** (the harness names it). The
  handoff commit goes on the branch too; the merge carries it over.

## Network policy

Outbound HTTPS goes through an allowlist proxy. `registry.npmjs.org`, `pypi.org`
and GitHub are allowed, so `npm ci` works. **Most of the rest of the web is
blocked**, which matters here for one thing specifically:

- ⚠️ **You cannot check whether an external link still resolves.** The v1
  project write-ups link to Google Drive and Omdena pages from 2021, and link
  rot is the most likely finding when they are ported. A `curl` failure from
  inside this VM is the proxy, not evidence the link is dead — **do not record
  a link as broken based on a request made from here.** Flag it for checking
  from a normal network instead.
- Diagnose: `curl -sS "$HTTPS_PROXY/__agentproxy/status"` — a
  `connect_rejected` entry means policy denial, not a transient failure. Don't
  retry, don't disable TLS, don't unset `HTTPS_PROXY`.
- The fix is the owner's: claude.ai/code → this environment's settings →
  network access → add the hosts. Applies to NEW sessions.

## Environment setup (fresh container)

```bash
npm ci
git config core.hooksPath .githooks   # ⚠️ HOOKS ARE NOT CLONED — see below
npm run build && npm test
```

⚠️ **`core.hooksPath` matters MOST here.** `.githooks/pre-push` blocks a push to
a branch whose PR is already merged. Git does not clone hooks, so in a fresh
container it is **OFF until you set it** — and this is exactly the environment
where a stranded commit is unrecoverable. The hook **fails open**, so it can
never be the reason work goes unsaved. It is a backstop, not a substitute for
`git merge-base --is-ancestor <sha> origin/main` after any merge.

Note that `gh` is not installed in this environment, so the hook exits early and
guards nothing here. GitHub operations go through the MCP tools instead.
