"""DECISIONS.md log guard: a new row cites a test, a superseded row says so.

Two mechanical checks on ``docs/DECISIONS.md``:

  1. **A NEW ROW NAMES A TEST, OR SAYS IT CANNOT.** A row dated on or after
     ``CUTOFF`` must cite a test that exists — a ``x.test.mjs`` file under
     ``tests/`` or a ``check_x.py`` in ``scripts/`` — or carry the literal tag
     ``[unverifiable]``. Rows before ``CUTOFF``
     are grandfathered. On EVERY row, a cited test that does not exist fails: a
     citation that resolves to nothing is the class the source project kept
     re-learning.
     ⚠️ This checks that the row NAMES a test that EXISTS — not that the test
     tests the decision (a repaired pointer once led to a script verifying the
     opposite). The tag is self-applied and nothing audits it. What the gate
     buys is the question asked at write time: *can this decision be a test?*

  2. **A SUPERSEDED ROW IS MARKED WHERE IT STANDS.** A row that supersedes /
     retracts / reverses / reopens / amends an earlier row — "the 2026-07-23
     row", "the same-day … row", "the row above" — must have that earlier row
     marked: struck (``~~``, the header's form) or carrying
     ``SUPERSEDED 2026-07-28`` (or RETRACTED / REVERSED / REOPENED / AMENDED)
     naming the date of the row that did it. Left unguarded, the practice
     goes forward-only — the new row announces the supersession and the
     original is left clean, so a grep landing on the original gets no signal.

Exit codes: 0 ok; 6 a row fails either check (2 is argparse's).

Usage:
    python scripts/check_decisions_log.py
    python scripts/check_decisions_log.py --root /path/to/checkout
"""

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = "docs/DECISIONS.md"

EXIT_OK = 0
EXIT_FAIL = 6

# Rows dated from here on must cite a test or be tagged. In a repo started from
# the template every row is after it; keep the constant so an adopting repo with
# a pre-existing log can grandfather its history by moving the date.
CUTOFF = date(2026, 9, 21)  # this repo's rebuild; there is nothing before it
TAG = "[unverifiable]"

# `content.test.mjs` is this repo's citable form (node --test files); the
# pytest and profiling spellings stay recognised so a guard ported back into
# the data-project template keeps resolving.
TEST_ID = re.compile(
    r"\b([a-z0-9-]+\.test\.mjs|test_[a-z0-9_]+|verify-[a-z0-9-]+\.js|check_[a-z0-9_]+\.py)\b")
DATE = re.compile(r"\b(\d{4})-(\d{2})(?:-(\d{2}))?\b")

# A supersession announcement names its target as a ROW: "supersedes the
# 2026-07-23 row", "Amends 2026-08-07", "reverses the clause locked earlier the
# same day", "the 2026-08-12 row above is RETRACTED". Prose that merely mentions
# a date near the verb ("had already been retracted on 2026-08-11", a quoted
# date, "the owner reversed") is not one, and the first cut of this pattern caught
# four of those in 22 hits.
VERB = r"(?:supersed(?:es|ed|ing)|retract(?:s|ed)|revers(?:es|ed)|reopen(?:s|ed)|amend(?:s|ed))"
TARGET = r"(?:\d{4}-\d{2}-\d{2}|same[- ]day|(?:rows?|lines?|clauses?|decisions?)\s+above)"
ANNOUNCE = re.compile(
    rf"\b{VERB}\b(?:\s+\S+){{0,8}}?\s+(?:the\s+)?{TARGET}"
    rf"|(\d{{4}}-\d{{2}}-\d{{2}})\s+(?:rows?|lines?|clauses?|decisions?)\s+above[^|]{{0,40}}?\b{VERB}\b",
    re.I | re.S,
)
HAPPENED_ON = re.compile(rf"\b{VERB}\s+on\s+\d{{4}}-", re.I)  # when it happened, not what
MARK = r"(?:SUPERSEDED|RETRACTED|REVERSED|REOPENED|AMENDED|CLOSED)"
# The mark itself ("PARTLY AMENDED 2026-08-15 — see that row") names a LATER row
# and must not read as an announcement pointing backwards.
IS_MARK = re.compile(rf"^\W*(?:PARTLY\s+)?{MARK}\s+\d{{4}}-\d{{2}}-\d{{2}}")


@dataclass
class Row:
    lineno: int
    when: date | None
    text: str  # the Decision cell


def parse_rows(md: str) -> list[Row]:
    """Table rows of the decisions log. Splits on unescaped ``|`` only: a row
    carrying a pipe inside inline code is scattered by a naive split."""
    rows: list[Row] = []
    for lineno, line in enumerate(md.splitlines(), 1):
        if not line.startswith("|") or re.match(r"^\|\s*-{3,}", line):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) < 2 or cells[0].lower() == "when":
            continue
        m = DATE.match(cells[0])
        when = None
        if m and m.group(3):
            when = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        rows.append(Row(lineno, when, cells[1]))
    return rows


def known_tests(root: Path) -> set[str]:
    """Every name a DECISIONS row may legitimately cite as its guard.

    This repo's tests are `node --test` files, so the citable unit is the test
    FILE — `content.test.mjs`. A row is free to name the individual case after
    it ("`content.test.mjs` — a draft never reaches dist"); only the filename is
    checked, because only the filename can be checked mechanically. Python
    `test_*.py` stays recognised so a guard ported back into the data-project
    template keeps working.
    """
    names: set[str] = set()
    names.update(p.name for p in (root / "tests").glob("*.test.mjs"))
    for p in (root / "tests").glob("test_*.py"):
        names.add(p.name)
        names.update(re.findall(r"^\s*def (test_[a-z0-9_]+)", p.read_text(errors="ignore"), re.M))
    names.update(p.name for p in (root / "scripts").glob("check_*.py"))
    return names


def check_test_ids(rows: list[Row], tests: set[str]) -> list[str]:
    failures: list[str] = []
    for r in rows:
        cited = set(TEST_ID.findall(r.text))
        # `test_x.py` cites a file; `test_x` a function. Both resolve by name.
        dangling = sorted(c for c in cited if c not in tests and c + ".py" not in tests)
        for c in dangling:
            failures.append(f"{DECISIONS}:{r.lineno}  cites `{c}`, which does not exist")
        if r.when and r.when >= CUTOFF and not (cited - set(dangling)) and TAG not in r.text:
            failures.append(
                f"{DECISIONS}:{r.lineno}  row dated {r.when} names no test — cite one "
                f"(x.test.mjs / check_x.py) or tag it {TAG}"
            )
    return failures


def _targets(rows: list[Row], i: int, window: str) -> tuple[list[Row], str]:
    """The earlier rows an announcement points at, and how it named them."""
    me = rows[i]
    m = DATE.search(window)
    if m and m.group(3):
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if me.when is None or d < me.when:
            return [r for r in rows[:i] if r.when == d], str(d)
        # A same-day date names siblings; a later one is a forward mark, not a target.
        if d == me.when:
            return [r for r in rows[:i] if r.when == d], "same-day"
        return [], "later"
    if re.search(r"same[- ]day", window, re.I):
        return [r for r in rows[:i] if r.when == me.when], "same-day"
    return rows[i - 1:i], "the row above"


def _marked(target: Row, by: date | None) -> bool:
    if "~~" in target.text:
        return True
    if by is None:
        return re.search(MARK, target.text) is not None
    return re.search(rf"{MARK}[^|]{{0,60}}?{by.isoformat()}", target.text) is not None


def check_back_annotation(rows: list[Row]) -> list[str]:
    failures: list[str] = []
    for i, r in enumerate(rows):
        if "~~" in r.text:
            continue  # a struck original announcing its own successor — that IS the mark
        for m in ANNOUNCE.finditer(r.text):
            window = m.group(0)
            if HAPPENED_ON.search(window) or IS_MARK.match(window):
                continue
            targets, named = _targets(rows, i, window)
            if not targets:
                if named not in ("the row above", "later"):
                    failures.append(
                        f"{DECISIONS}:{r.lineno}  announces a supersession of {named}, "
                        f"and no earlier row carries that date"
                    )
                continue
            if any(_marked(t, r.when) for t in targets):
                continue
            where = ", ".join(f"L{t.lineno}" for t in targets)
            stamp = r.when.isoformat() if r.when else "<date>"
            failures.append(
                f"{DECISIONS}:{r.lineno}  supersedes {named} ({where}) but none of those "
                f"rows is marked — strike it (~~) or add `SUPERSEDED {stamp}` in place"
            )
            break  # one failure per announcing row is enough to read
    return failures


def check(root: Path = ROOT) -> list[str]:
    md = (root / DECISIONS).read_text(errors="ignore")
    rows = parse_rows(md)
    return check_test_ids(rows, known_tests(root)) + check_back_annotation(rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", type=Path, default=ROOT)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    failures = check(args.root)
    for f in failures:
        print(f"FAIL  {f}")
    if failures:
        print(f"\n{len(failures)} failure(s) in {DECISIONS}")
        return EXIT_FAIL
    print(f"OK  {DECISIONS}: every new row names a test or says it cannot; every "
          f"superseded row is marked where it stands")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
