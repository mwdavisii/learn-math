#!/usr/bin/env python3
"""Structural checks for the math curriculum. Exit 1 on any failure.

Usage: .venv/bin/python tools/check_curriculum.py [--notebooks]
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CURRICULUM_ROOT") or Path(__file__).resolve().parent.parent)
TIERS = [
    "tier-0-notation",
    "tier-1-calculus",
    "tier-2-linear-algebra",
    "tier-3-multivariable",
    "tier-4-probability",
    "tier-5-proofs-and-papers",
]
ROOT_FILES = ["README.md", "progress.md", "CLAUDE.md", "requirements.txt",
              "reference/notation.md", "notes/README.md"]
HALF_A = ["### Read", "### Key ideas", "### Worked example"]
HALF_B = ["### Problems", "### Proof thread", "### Done when"]
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME)\b")
ANSWER_HEADING = re.compile(r"^#{1,6}[ \t]+.*\b(answers?|solutions?)\b", re.M | re.I)
ANSWER_BOLD = re.compile(r"^\*\*[^*]*\b(answers?|solutions?)\b[^*]*\*\*[ \t]*:?[ \t]*$", re.M | re.I)
FENCE_OPEN = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
PROGRESS_ID = re.compile(r"^- \[[ xX]\] (\d+)\.(\d+)[AB]\b", re.M)
SKIP_TOP = {"docs", ".venv"}
OPTIONAL_MD = {"README.md", "checkpoint.md"}
SESSION_RE = re.compile(r"^(\d\d)-[a-z0-9-]+\.md$")
NUMBERED = re.compile(r"^\d+\.\s", re.M)


def strip_fences(text: str) -> str:
    """Remove fenced code blocks (``` or ~~~, length >= 3) from markdown text."""
    out, fence = [], None
    for line in text.splitlines():
        m = FENCE_OPEN.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                continue
            out.append(line)
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) \
                and not line.strip().strip(fence[0]):
            fence = None
    return "\n".join(out)


def check_snake_cells(tier_dir: Path, ss: list[Path], errs: list[str]) -> None:
    """Every 🐍 problem i.n/k needs a '## i.n problem k' markdown cell in sessions.ipynb."""
    nb_path = tier_dir / "notebooks" / "sessions.ipynb"
    if not nb_path.is_file():
        return
    try:
        cells = json.loads(nb_path.read_text(encoding="utf-8")).get("cells", [])
    except ValueError as e:
        errs.append(f"{nb_path.relative_to(ROOT)}: invalid JSON ({e})")
        return
    titles = []
    for c in cells:
        if c.get("cell_type") == "markdown":
            src = c.get("source", "")
            src = "".join(src) if isinstance(src, list) else src
            titles.append(src.split("\n", 1)[0].strip())
    tier_i = TIERS.index(tier_dir.name) if tier_dir.name in TIERS else None
    for s in ss:
        n = int(SESSION_RE.match(s.name).group(1))
        t = s.read_text(encoding="utf-8")
        p0, p1 = heading(t, "### Problems"), heading(t, "### Proof thread")
        if not 0 <= p0 < p1:
            continue
        for ch in re.split(r"^(?=\d+\.\s)", t[p0:p1], flags=re.M):
            m = re.match(r"(\d+)\.\s", ch)
            if m and "🐍" in ch:
                k = m.group(1)
                tag = f"{tier_i}.{n}" if tier_i is not None else f"{tier_dir.name[5]}.{n}"
                if not any(re.match(rf"^## {re.escape(tag)} problem {k}\b", x) for x in titles):
                    errs.append(f"{s.relative_to(ROOT)}: 🐍 problem {k} has no "
                                f"'## {tag} problem {k}' markdown cell in {nb_path.relative_to(ROOT)}")


def sessions(tier_dir: Path) -> list[Path]:
    return sorted(p for p in tier_dir.glob("*.md") if SESSION_RE.match(p.name))


def heading(text: str, h: str) -> int:
    """Start offset of the whole-line heading `h`, or -1."""
    m = re.search(rf"^{re.escape(h)}\s*$", text, re.M)
    return m.start() if m else -1


def curriculum_md_files():
    """All .md files under ROOT, pruning docs/, .venv/ and dot-directories."""
    for entry in sorted(ROOT.iterdir()):
        if entry.name in SKIP_TOP or entry.name.startswith("."):
            continue
        if entry.is_file() and entry.suffix == ".md":
            yield entry
        elif entry.is_dir():
            for md in sorted(entry.rglob("*.md")):
                if not any(part.startswith(".") for part in md.relative_to(ROOT).parts):
                    yield md


def check_session(path: Path, errs: list[str]) -> None:
    t = path.read_text(encoding="utf-8")
    name = path.relative_to(ROOT)
    a, b = (m.start() if (m := re.search(rf"^{h}\b", t, re.M)) else -1
            for h in ("## Half A", "## Half B"))
    if a < 0 or b < 0 or a > b:
        errs.append(f"{name}: needs '## Half A' before '## Half B'")
        return
    last = -1
    for h in HALF_A + HALF_B:
        k = heading(t, h)
        if k < 0:
            errs.append(f"{name}: missing '{h}'")
            continue
        if k < last:
            errs.append(f"{name}: '{h}' out of order")
        if h in HALF_A and not a < k < b:
            errs.append(f"{name}: '{h}' must be inside Half A")
        if h in HALF_B and k < b:
            errs.append(f"{name}: '{h}' must be inside Half B")
        last = max(last, k)
    p0, p1 = heading(t, "### Problems"), heading(t, "### Proof thread")
    if 0 <= p0 < p1:
        probs = t[p0:p1]
        n = len(NUMBERED.findall(probs))
        if not 5 <= n <= 8:
            errs.append(f"{name}: {n} problems (need 5-8)")
        chunks = re.split(r"^(?=\d+\.\s)", probs, flags=re.M)
        snakes = sum("🐍" in c for c in chunks if NUMBERED.match(c))
        if not 1 <= snakes <= 2:
            errs.append(f"{name}: {snakes} 🐍 problems (need 1-2)")


def check_readme(tier_dir: Path, errs: list[str]) -> None:
    readme = tier_dir / "README.md"
    if not readme.is_file():
        errs.append(f"{tier_dir.name}: missing README.md")
        return
    t = readme.read_text(encoding="utf-8")
    s, c = heading(t, "## Sessions"), heading(t, "## Checkpoint")
    if s < 0 or c < 0:
        errs.append(f"{tier_dir.name}/README.md: needs '## Sessions' and '## Checkpoint'")
        return
    n = len(NUMBERED.findall(t[s:c] if s < c else t[s:]))
    if not 6 <= n <= 12:
        errs.append(f"{tier_dir.name}/README.md: {n} sessions listed (need 6-12)")


def main() -> int:
    errs: list[str] = []
    for f in ROOT_FILES:
        if not (ROOT / f).is_file():
            errs.append(f"missing {f}")
    progress = (ROOT / "progress.md").read_text(encoding="utf-8") if (ROOT / "progress.md").is_file() else ""

    for i, tier in enumerate(TIERS):
        d = ROOT / tier
        if not d.is_dir():
            errs.append(f"missing {tier}/")
            continue
        check_readme(d, errs)
        ss = sessions(d)
        for p in sorted(d.glob("*.md")):
            if p.name not in OPTIONAL_MD and not SESSION_RE.match(p.name):
                errs.append(f"{tier}/{p.name}: unrecognized md file name")
        nums = [int(SESSION_RE.match(p.name).group(1)) for p in ss]
        if nums != list(range(1, len(nums) + 1)):
            errs.append(f"{tier}: session numbers {nums} not consecutive from 01")
        if ss:
            if not 6 <= len(ss) <= 12:
                errs.append(f"{tier}: {len(ss)} session files (need 6-12)")
            for f in ["checkpoint.md", "notebooks/sessions.ipynb", "notebooks/checkpoint.ipynb"]:
                if not (d / f).is_file():
                    errs.append(f"{tier}: missing {f}")
        check_snake_cells(d, ss, errs)
        for s in ss:
            check_session(s, errs)
            n = int(SESSION_RE.match(s.name).group(1))
            for half in "AB":
                if not re.search(rf"^- \[[ xX]\] {i}\.{n}{half}\b", progress, re.M):
                    errs.append(f"progress.md: missing {i}.{n}{half}")
        if not re.search(rf"^- \[[ xX]\] {i}\.CP\b", progress, re.M):
            errs.append(f"progress.md: missing {i}.CP")

    for m in PROGRESS_ID.finditer(progress):
        i, n = int(m.group(1)), int(m.group(2))
        tier = TIERS[i] if i < len(TIERS) else None
        if tier is None or not any(
                int(SESSION_RE.match(p.name).group(1)) == n for p in sessions(ROOT / tier)):
            errs.append(f"progress.md: stale ID {m.group(0)[6:]} has no session file")

    for md in curriculum_md_files():
        rel = md.relative_to(ROOT)
        if rel.parts[0] == "notes" and rel.name != "README.md":
            continue  # the learner's own write-ups: no format rules
        t = md.read_text(encoding="utf-8")
        body = strip_fences(t)
        if ANSWER_HEADING.search(body) or ANSWER_BOLD.search(body):
            errs.append(f"{rel}: contains an answers/solutions heading")
        if PLACEHOLDER.search(t):
            errs.append(f"{rel}: placeholder text")
        if not t.startswith("---\ntype: personal\n"):
            errs.append(f"{rel}: missing front matter")

    if "--notebooks" in sys.argv:
        for nb in sorted(ROOT.glob("tier-*/notebooks/*.ipynb")):
            r = subprocess.run(
                [sys.executable, "-m", "nbconvert", "--to", "notebook",
                 "--execute", "--ExecutePreprocessor.timeout=120",
                 "--stdout", str(nb)],
                capture_output=True, text=True)
            if r.returncode != 0:
                errs.append(f"{nb.relative_to(ROOT)}: execution failed\n{r.stderr[-800:]}")

    for e in errs:
        print(f"FAIL: {e}")
    print("OK" if not errs else f"{len(errs)} failure(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
