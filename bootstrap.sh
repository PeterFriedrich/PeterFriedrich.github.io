#!/usr/bin/env bash
# One-time setup after a fresh clone. Idempotent.
set -euo pipefail
cd "$(dirname "$0")"

# Hooks are not cloned. Without this the pre-push guard is OFF, and it is the
# guard that stops work being stranded on a branch whose PR already merged.
git config core.hooksPath .githooks
echo "core.hooksPath -> .githooks"

npm ci
npm run build
npm test

# The doc guards are stdlib-only python3; if there is no python3 on PATH the
# repo still works, the merge gate just carries checks you cannot run locally.
if command -v python3 >/dev/null 2>&1; then
  python3 scripts/check_doc_citations.py
  python3 scripts/check_decisions_log.py
else
  echo "no python3 on PATH — skipping doc guards (CI still runs them)"
fi

cat <<'EOF'

Ready. Next:
  npm run dev                      http://localhost:4321
  npm run new:post "A title"       scaffold a post

Not done by this script, because neither lives in the repo (docs/DEPLOY.md):
  1. Rename the repo to PeterFriedrich.github.io
  2. Settings -> Pages -> Source -> GitHub Actions
EOF
