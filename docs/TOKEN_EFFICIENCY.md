# Token Efficiency

Practices for keeping context usage low. A living doc — add to it whenever a new
"don't read that raw" lesson comes up. Rough tokens ≈ bytes ÷ 4.

⚠️ **The lever is what the standing instructions require, not how files are
split.** Nobody reads the whole repo; a task touches a handful of files. What
every session pays unconditionally is the *loaded path* — `CLAUDE.md` +
`TODO.md` + the latest handoff. Measure that before optimizing anything else.

## Rules

1. **Never `Read` generated or vendored files.** `dist/`, `node_modules/`,
   `package-lock.json`, `.astro/`. `dist/` is the build output — read the source
   that produced it, or `grep` the output for the one string you need. A test
   that asserts against `dist/` does so with `grep`-shaped reads, never whole
   files.

2. **Never bulk-read `archive/v1-2022/`.** It is frozen 2022 markup kept as
   source material. When porting a project write-up, read the ONE `<article>`
   block you need — `sed -n` on the line range, not the file.

3. **Read only the latest session summary.** Keep the **3 most recent** at the
   top level; older ones live in `session-summary/archive/` so a
   `session-summary/*.md` glob doesn't reach them.
   `tests/loaded-path.test.mjs` enforces this.

4. **⚠️ MANY SMALL READS ARE THE EXPENSIVE PATTERN, not one big one.** Every
   tool result persists and is re-sent on every later turn, so 21 reads of
   30–60 lines cost far more than 4 large ones covering the same ground — and
   the overlap is paid twice. Decide what you need up front, then read it in a
   few large slices. Batch independent reads into one turn.

5. **Never let raw HTML, SVG or lockfile content into the transcript.** Pipe
   through `grep`/`sed`/`head` or print only the fields being asserted.
   `dist/index.html` is minified into ~4 unbroken lines — one `cat` is the whole
   page as a single wall of text.

6. **Batch slow runs.** A build plus a test run in one command beats two turns.

## Files to watch

- `session-summary/` — grows every `/handoff`; the archive policy bounds it.
- `TODO.md` — read first every session, so closed work must leave it
  (`python3 tools/todo_archive.py`).
- `docs/DECISIONS.md` — append-only; grep it rather than reading it whole.
- `src/content/` — will grow with every post. Read the one entry you're working
  on, not the directory.
