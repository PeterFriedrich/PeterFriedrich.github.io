"""Doc-citation guard: fail loud when a citation stops resolving.

Comments cite docs as their authority — ``spec.md §5``, ``methods.md "Fire
lens"``. Nothing re-reads them, so a citation can rot in place while the code
still runs and every test still passes (two sweeps in the project this template
came from found exactly that).

THIS GUARD COVERS EXACTLY ONE OF THE THREE FAILURE CLASSES — the mechanical one:

  1. **The pointer stops resolving** — the doc is gone, the section number does
     not exist, or the citation names a LINE NUMBER and the doc has since grown
     (one such citation drifted ~240 lines in two months). THIS IS WHAT THE
     GUARD CHECKS, and it is fully decidable.
  2. **The same figure lives in 2+ places and they drift apart.** Not checkable
     here; the fix is to stop duplicating the figure.
  3. **The prose no longer supports the claim** — "19 rows" that are 19
     *accounts*. Requires judgement. That is what a periodic sweep is for.

⚠️ **LINE-NUMBER CITATIONS ARE BANNED OUTRIGHT**, not validated. A line number is
correct only until the doc is edited, and it fails SILENTLY and PLAUSIBLY — it
lands on some other real content rather than erroring. Cite ``§N`` or a section
title instead.

⚠️ **BOTH SPELLINGS, and the second one is the one that matters.** The first cut
of this guard required the literal word "line", so it caught "DATA.md line ~308"
and missed "DATA.md:207" — which is the form the terminal renders as a clickable
link, so it is what anyone actually types. Two such citations sat unflagged in
``TODO.md`` from the day this guard shipped until 2026-08-09, both pointing at a
line that had since become the *correction* of the claim citing it: plausible,
wrong, silent, exactly as the ban predicts. A guard that bans only the wordy
spelling of a mistake bans the spelling nobody uses. ``#L207`` (GitHub's) is
banned too; a bare ``#anchor`` is a real fragment and stays legal.

History files are deliberately NOT scanned: ``session-summary/`` is frozen by
definition, and ``TODO_archive.md`` / ``AUDIT_LEDGER.md`` are append-only records
that *quote* the banned form in order to document it. A citation wrapped in
quotes is likewise treated as a mention, not a use.

Outcomes (exit codes; 2 is argparse's):
  0  ok    — every citation resolves (quoted-title misses warn only).
  5  drift — a citation names a missing doc, an absent section, or a line number.

Usage:
    python scripts/check_doc_citations.py
    python scripts/check_doc_citations.py --log-level DEBUG
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent

EXIT_OK = 0
EXIT_DRIFT = 5

# Where citations are LIVE — code plus the docs that are still edited.
SCAN_DIRS = ("src", "scripts", "tools", "docs", "tests", ".github")
SCAN_FILES = ("TODO.md", "CLAUDE.md", "README.md", "CONTRIBUTING.md")
SCAN_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".astro", ".html", ".md", ".yml", ".yaml"}

# Append-only history + generated files + vendored trees. See the module docstring:
# these RECORD citations rather than making them, so a banned form inside them is
# documentation of a fixed bug, not a live pointer.
EXCLUDE_PARTS = (
    "node_modules", "dist", ".astro", "_site", ".venv", ".git", "session-summary",
    # The archived v1 site: frozen by definition, and its `style_test.css`-era
    # markup is not a live pointer at anything.
    "archive/",
    # PUBLISHED PROSE IS NOT AN INTERNAL POINTER. A post may legitimately write
    # "src/index.js:40" when the subject of the post IS that line of someone
    # else's code; the ban exists for citations this repo has to keep resolving.
    "src/content",
    # Verbatim third-party documents (docs/external/). Their evidentiary value IS
    # that they are unedited -- an outside author's citations are theirs, not ours
    # to fix, and rewriting one to satisfy this guard would destroy the thing it is
    # kept for. NOTE this excludes them from SCANNING only: project_docs() still
    # lists them, so OUR citations TO such a file resolve.
    "docs/external",
)
EXCLUDE_NAMES = ("TODO_archive.md", "AUDIT_LEDGER.md", "CODEMAP.md")

# A bare basename this short collides with ordinary prose and data vocabulary
# (`UI`, `API`), so citations to a doc this short must spell out the .md.
MIN_BARE_NAME = 5

# A handoff cited as a findings record. The tree is never scanned, but a
# citation INTO it is live like any other, and the archive move breaks it (6 of
# 8 such citations were dead when this check was added, and nothing had noticed).
HANDOFF = re.compile(r"\b(session-summary/[\w./-]+\.md)\b")


def project_docs(root: Path) -> dict[str, Path]:
    """Every markdown doc a citation could legitimately name."""
    found = (list(root.glob("*.md")) + list(root.glob("docs/*.md"))
             # Not scanned (EXCLUDE_PARTS) but nameable: a citation TO a verbatim
             # external document must resolve like any other.
             + list(root.glob("docs/external/*.md")))
    return {p.name: p for p in found}


def doc_sections(path: Path) -> set[str]:
    """Section numbers a ``§N`` citation may resolve to, from the doc's headings.

    Handles ``## 5. Zoning``, ``### 0.1 The defect map`` and ``## 6b. Round 2``
    alike: the number is whatever leads the heading text.
    """
    out: set[str] = set()
    for line in path.read_text(errors="ignore").splitlines():
        m = re.match(r"^#{1,6}\s+(?:\*\*)?§?\s*(\d+[a-z]?(?:\.\d+)*)", line)
        if m:
            out.add(m.group(1).rstrip("."))
    return out


def scan_paths(root: Path) -> list[Path]:
    """The files whose citations are live and therefore checkable."""
    paths: list[Path] = []
    for d in SCAN_DIRS:
        paths.extend(p for p in (root / d).rglob("*") if p.is_file() and p.suffix in SCAN_SUFFIXES)
    paths.extend(root / f for f in SCAN_FILES if (root / f).is_file())
    return sorted(
        p for p in paths
        if p.name not in EXCLUDE_NAMES
        and not any(part in p.as_posix() for part in EXCLUDE_PARTS)
    )


def _citation_pattern(doc_names: list[str]) -> re.Pattern[str]:
    """Match a doc name, with ``.md`` optional only when the name is unambiguous."""
    alts = []
    for name in sorted(doc_names, key=len, reverse=True):
        stem = re.escape(name[:-3])
        alts.append(rf"{stem}\.md" if len(name[:-3]) < MIN_BARE_NAME else rf"{stem}(?:\.md)?")
    return re.compile(rf"\b({'|'.join(alts)})\b([^\n]{{0,40}})")


def _is_mention(line: str, start: int) -> bool:
    """True when the citation sits inside quotes — being discussed, not used."""
    before = line[:start]
    return before.count('"') % 2 == 1


def check_citations(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Check every live citation. Returns ``(failures, warnings)``."""
    docs = project_docs(root)
    sections = {name: doc_sections(p) for name, p in docs.items()}
    bodies = {name: p.read_text(errors="ignore").lower() for name, p in docs.items()}
    pattern = _citation_pattern(list(docs))

    # A cited .md that does not exist at all. Restricted to the scanned (non-vendored)
    # tree, so third-party filenames in bundled JS cannot reach this.
    any_md = re.compile(r"\b([A-Za-z][\w.-]*\.md)\b")

    failures: list[str] = []
    warnings: list[str] = []

    for path in scan_paths(root):
        rel = path.relative_to(root)
        for lineno, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            where = f"{rel}:{lineno}"

            for m in any_md.finditer(line):
                name = m.group(1)
                if name not in docs and (root / name).name not in docs and "/" not in name:
                    if name.isupper() or name[0].isupper():
                        warnings.append(f"{where}  cites {name}, which does not exist")

            for m in HANDOFF.finditer(line):
                if _is_mention(line, m.start()) or (root / m.group(1)).is_file():
                    continue
                failures.append(
                    f"{where}  cites {m.group(1)}, which does not exist — archived? "
                    f"the file may now be under session-summary/archive/"
                )

            for m in pattern.finditer(line):
                if _is_mention(line, m.start()):
                    continue
                name = m.group(1) if m.group(1).endswith(".md") else m.group(1) + ".md"
                if name not in docs:
                    continue
                tail = m.group(2)

                # Both spellings of the banned form. The `:NNN` one was MISSED
                # until 2026-08-09 and it is the one people actually type: the
                # terminal renders `file.md:207` as a clickable link, so it is the
                # path of least resistance, and two live citations had been sitting
                # in TODO.md unflagged. A guard that bans only the wordy spelling
                # of a mistake bans the spelling nobody uses. `#LNNN` is GitHub's;
                # a bare `#anchor` is a real fragment and stays legal.
                if (re.match(r"[^0-9]{0,12}lines?\s*~?\d+", tail)
                        or re.match(r"(?::|#L)\s*\d+", tail)):
                    failures.append(
                        f"{where}  cites {name} by LINE NUMBER — banned, it drifts "
                        f"silently as the doc grows. Cite §N or a section title."
                    )
                    continue

                # NOT "phase N": a phase is a project milestone, not a heading, and
                # ARCHITECTURE.md's "Phase 2 notes" resolved against §2 only by luck.
                sec = re.match(r"\s*(?:§|sections?\s+)\s*(\d+[a-z]?(?:\.\d+)*)", tail, re.I)
                if sec:
                    num = sec.group(1).rstrip(".")
                    avail = sections.get(name, set())
                    if num not in avail and not any(s.startswith(num + ".") for s in avail):
                        failures.append(
                            f"{where}  cites {name} §{num}, which has no such section "
                            f"(has: {', '.join(sorted(avail)) or 'no numbered sections'})"
                        )
                    continue

                title = re.match(r'[`\s]*"([^"]{2,60})"', tail)
                if title and title.group(1).lower() not in bodies.get(name, ""):
                    warnings.append(
                        f'{where}  cites {name} "{title.group(1)}", which does not '
                        f"appear in that doc"
                    )

    return failures, warnings


def _write_github_output(**kv: object) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=args.log_level, format="%(levelname)s %(message)s")

    failures, warnings = check_citations(args.root)

    for w in warnings:
        logger.warning("%s", w)

    if failures:
        logger.error(
            "DOC-CITATION DRIFT — %d citation(s) no longer resolve:\n  %s",
            len(failures), "\n  ".join(failures),
        )
        _write_github_output(result="drift", failures=len(failures))
        return EXIT_DRIFT

    logger.info(
        "Doc-citation guard OK: every live citation resolves (%d quoted-title warning(s)).",
        len(warnings),
    )
    _write_github_output(result="ok", failures=0)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
