/**
 * Guards on the LOADED PATH — what every session is told to read before it works.
 *
 * Ported from the data-project template's `tests/test_loaded_path.py`. CLAUDE.md
 * names the files a session must open: itself, TODO.md, the latest handoff. The
 * handoff pile stays a small share of that only while the archive discipline
 * holds — "keep the 3 most recent at top level, archive older" is a rule with a
 * reader and no check unless this file exists, and a lapse is silent and
 * compounding: nobody notices the 4th file.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..');
const SUMMARIES = join(REPO, 'session-summary');

// CLAUDE.md, "Token efficiency": read only the latest, keep the 3 most recent.
const MAX_LIVE = 3;

const mdIn = (dir) =>
  existsSync(dir)
    ? readdirSync(dir)
        .filter((f) => f.endsWith('.md'))
        .sort()
    : [];

const live = () => mdIn(SUMMARIES);
const archived = () => mdIn(join(SUMMARIES, 'archive'));

test('at most three handoffs at session-summary/ top level', () => {
  const files = live();
  assert.ok(
    files.length <= MAX_LIVE,
    `${files.length} handoffs at session-summary/ top level, max ${MAX_LIVE} ` +
      `(CLAUDE.md). Move the oldest into session-summary/archive/ in this same ` +
      `PR — \`git mv session-summary/${files[0]} session-summary/archive/\`. ` +
      `Archiving is not deletion: the files stay, out of the loaded path.`,
  );
});

test('the live handoffs are the most recent ones', () => {
  // Not just three — the three NEWEST. Filenames are date-prefixed, so every
  // archived name must sort before every live one. Catches archiving the wrong
  // end, which passes the count test while leaving a stale file in the path a
  // session is told to read.
  const [l, a] = [live(), archived()];
  if (l.length === 0 || a.length === 0) return;
  assert.ok(
    a[a.length - 1] < l[0],
    `session-summary/archive/${a[a.length - 1]} is newer than the live ${l[0]} ` +
      `— the wrong end was archived. The top-level files must be the ` +
      `${MAX_LIVE} most recent.`,
  );
});

test('the handoff archive is never deleted from', () => {
  // A floor under the two tests above: both pass over a repo that DELETED its
  // history instead of moving it. A young repo (no archive yet) and a repo that
  // emptied its archive look identical on disk, so ask git. `-M` so a rename
  // (re-dating a file) is not read as a deletion. Fails open without git or
  // history — a shallow CI checkout sees nothing, which is why the workflow
  // checks out with fetch-depth: 0.
  let out;
  try {
    out = execFileSync(
      'git',
      ['log', '-M', '--diff-filter=D', '--name-only', '--format=', '--',
       'session-summary/archive/'],
      { cwd: REPO, encoding: 'utf8', timeout: 30_000 },
    );
  } catch {
    return; // not a git checkout, or no git: nothing to check
  }
  const deleted = out.split('\n').filter((l) => l.trim());
  assert.equal(
    deleted.length,
    0,
    `${deleted.length} file(s) were DELETED from session-summary/archive/ ` +
      `(e.g. ${deleted[0]}). The archive is append-only: it is the only copy of ` +
      `what earlier sessions did. Restore them.`,
  );
});
