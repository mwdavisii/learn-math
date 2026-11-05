---
type: personal
title: Math Curriculum — Initial Build Plan
source: personal
---

# Math for ML Papers: Initial Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the curriculum scaffold, with root docs, Tier 0 written in full, and Tier 1–5 skeletons, as specified in `docs/superpowers/specs/2026-11-05-math-for-ml-curriculum-design.md`.

**Architecture:** Plain markdown files in tier folders, plus Jupyter notebooks. A structural validator (`tools/check_curriculum.py`) acts as the test suite: it enforces the session format, progress IDs, skeleton shape, the absence of placeholders and answer keys, and (with `--notebooks`) that every notebook executes cleanly. Every content task ends by running the validator.

**Tech Stack:** Markdown, Python 3.13, a venv at `.venv/` with numpy, matplotlib, sympy, jupyter, and nbformat.

## Global Constraints

- Root: the curriculum folder (written `math/` below). All paths are relative to it.
- **Not a git repo. There are no commit steps.** Do not run `git init`.
- Every markdown file outside `docs/` starts with this front matter (brain convention):
  ```
  ---
  type: personal
  title: <Title>
  source: personal
  ---
  ```
- Session files are named `NN-kebab-title.md` (two digits). Progress IDs are `<tier>.<n>A` / `<tier>.<n>B` per session half, and `<tier>.CP` for the checkpoint.
- Session format (exact headings): `## Half A — <title>` containing `### Read`, `### Key ideas`, `### Worked example`, then `## Half B — <title>` containing `### Problems`, `### Proof thread`, `### Done when`.
- Problems: 5–8 numbered items (`1.` at line start) per session; 1–2 contain 🐍.
- **No answer keys** in any file. Worked examples are fully solved, but problems are not.
- No `TODO`, `TBD`, or `FIXME` anywhere outside `docs/`.
- Notebook stack: numpy, matplotlib, sympy. No ML frameworks.
- Book section numbers are for *Book of Proof* 3rd ed., OpenStax *Calculus* Vol 1/2 (2016), and MML (2020 print/PDF). Each tier README tells the learner: "If a section number doesn't match your copy, find it by title."
- Small spec addition: `tools/` holds the validator. It's maintenance tooling, not learner content.

## File Map

| File | Responsibility |
|---|---|
| `tools/check_curriculum.py` | Structural validator (the test suite) |
| `requirements.txt` | Python deps |
| `README.md` | Goal, tier table, how to use, resources |
| `CLAUDE.md` | Tutor context and rules |
| `progress.md` | Checkboxes and the stuck-on list |
| `reference/notation.md` | Symbol cheat sheet |
| `notes/README.md` | Explains the notes folder |
| `tier-0-notation/README.md`, `01…08-*.md`, `checkpoint.md`, `notebooks/sessions.ipynb`, `notebooks/checkpoint.ipynb` | Tier 0, full |
| `tier-{1..5}-*/README.md` | Skeletons |

---

### Task 1: Environment + validator

**Files:**
- Create: `requirements.txt`, `tools/check_curriculum.py`

**Interfaces:**
- Produces: `.venv/bin/python tools/check_curriculum.py [--notebooks]`. Exits 0 when clean. Otherwise it exits 1 and prints one `FAIL: <msg>` line per problem. Every later task runs it.

- [ ] **Step 1: Write `requirements.txt`**

```
numpy>=2.0
matplotlib>=3.8
sympy>=1.13
jupyter>=1.0
nbformat>=5.9
nbconvert>=7.0
```

- [ ] **Step 2: Create venv and install**

Run: `cd math && python -m venv .venv && .venv/bin/pip install -q -r requirements.txt && .venv/bin/python -c "import numpy, matplotlib, sympy, nbformat; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Write `tools/check_curriculum.py`**

```python
#!/usr/bin/env python3
"""Structural checks for the math curriculum. Exit 1 on any failure.

Usage: .venv/bin/python tools/check_curriculum.py [--notebooks]
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIERS = [
    "tier-0-notation",
    "tier-1-calculus",
    "tier-2-linear-algebra",
    "tier-3-multivariable",
    "tier-4-probability",
    "tier-5-proofs-and-papers",
]
FULL_TIERS = {"tier-0-notation"}
ROOT_FILES = ["README.md", "progress.md", "CLAUDE.md", "requirements.txt",
              "reference/notation.md", "notes/README.md"]
HALF_A = ["### Read", "### Key ideas", "### Worked example"]
HALF_B = ["### Problems", "### Proof thread", "### Done when"]
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME)\b")
ANSWER_HEADING = re.compile(r"^#+\s*(answers?|solutions?)\b", re.M | re.I)
SESSION_RE = re.compile(r"^(\d\d)-[a-z0-9-]+\.md$")
NUMBERED = re.compile(r"^\d+\.\s", re.M)


def sessions(tier_dir: Path) -> list[Path]:
    return sorted(p for p in tier_dir.glob("*.md") if SESSION_RE.match(p.name))


def check_session(path: Path, errs: list[str]) -> None:
    t = path.read_text()
    name = path.relative_to(ROOT)
    a, b = t.find("## Half A"), t.find("## Half B")
    if a < 0 or b < 0 or a > b:
        errs.append(f"{name}: needs '## Half A' before '## Half B'")
        return
    last = -1
    for h in HALF_A + HALF_B:
        k = t.find(h)
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
    p0, p1 = t.find("### Problems"), t.find("### Proof thread")
    if 0 <= p0 < p1:
        probs = t[p0:p1]
        n = len(NUMBERED.findall(probs))
        if not 5 <= n <= 8:
            errs.append(f"{name}: {n} problems (need 5-8)")
        snakes = sum("🐍" in line for line in probs.splitlines()
                     if NUMBERED.match(line))
        if not 1 <= snakes <= 2:
            errs.append(f"{name}: {snakes} 🐍 problems (need 1-2)")
    if ANSWER_HEADING.search(t):
        errs.append(f"{name}: contains an answers/solutions heading")


def check_readme(tier_dir: Path, errs: list[str]) -> None:
    readme = tier_dir / "README.md"
    if not readme.is_file():
        errs.append(f"{tier_dir.name}: missing README.md")
        return
    t = readme.read_text()
    s, c = t.find("## Sessions"), t.find("## Checkpoint")
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
    progress = (ROOT / "progress.md").read_text() if (ROOT / "progress.md").is_file() else ""

    for i, tier in enumerate(TIERS):
        d = ROOT / tier
        if not d.is_dir():
            errs.append(f"missing {tier}/")
            continue
        check_readme(d, errs)
        ss = sessions(d)
        if tier in FULL_TIERS:
            if not 6 <= len(ss) <= 12:
                errs.append(f"{tier}: {len(ss)} session files (need 6-12)")
            for f in ["checkpoint.md", "notebooks/sessions.ipynb", "notebooks/checkpoint.ipynb"]:
                if not (d / f).is_file():
                    errs.append(f"{tier}: missing {f}")
        for s in ss:
            check_session(s, errs)
            n = int(SESSION_RE.match(s.name).group(1))
            for half in "AB":
                if not re.search(rf"\b{i}\.{n}{half}\b", progress):
                    errs.append(f"progress.md: missing {i}.{n}{half}")
        if not re.search(rf"\b{i}\.CP\b", progress):
            errs.append(f"progress.md: missing {i}.CP")

    for md in ROOT.rglob("*.md"):
        rel = md.relative_to(ROOT)
        if rel.parts[0] in {"docs", ".venv"}:
            continue
        t = md.read_text()
        if PLACEHOLDER.search(t):
            errs.append(f"{rel}: placeholder text")
        if not t.startswith("---\ntype: personal\n"):
            errs.append(f"{rel}: missing front matter")

    if "--notebooks" in sys.argv:
        for nb in sorted(ROOT.glob("tier-*/notebooks/*.ipynb")):
            r = subprocess.run(
                [sys.executable, "-m", "nbconvert", "--to", "notebook",
                 "--execute", "--stdout", str(nb)],
                capture_output=True, text=True)
            if r.returncode != 0:
                errs.append(f"{nb.relative_to(ROOT)}: execution failed\n{r.stderr[-800:]}")

    for e in errs:
        print(f"FAIL: {e}")
    print("OK" if not errs else f"{len(errs)} failure(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run validator, verify it fails for the right reasons**

Run: `cd math && .venv/bin/python tools/check_curriculum.py`
Expected: exit 1, with `FAIL: missing README.md`, `FAIL: missing tier-0-notation/`, etc. No Python traceback.

- [ ] **Step 5: Self-test the session checker with a bad fixture**

Run:
```bash
cd math && mkdir -p tier-0-notation && cat > tier-0-notation/99-bad-fixture.md <<'EOF'
---
type: personal
title: bad
source: personal
---
## Half B — x
### Problems
1. one
## Answers
EOF
.venv/bin/python tools/check_curriculum.py | grep 99-bad; rm tier-0-notation/99-bad-fixture.md
```
Expected: lines including `needs '## Half A' before '## Half B'`. Then change the fixture so it has both halves with all six headings and one problem, rerun, and expect `1 problems (need 5-8)`, `0 🐍 problems`, and `answers/solutions heading`. Delete the fixture afterward.

---

### Task 2: Root documents

**Files:**
- Create: `README.md`, `CLAUDE.md`, `progress.md`, `reference/notation.md`, `notes/README.md`

**Interfaces:**
- Consumes: the validator from Task 1.
- Produces: progress IDs `0.1A … 0.8B`, `0.CP`, and `1.CP … 5.CP` that later tasks rely on. Tier 1–5 session IDs get added to `progress.md` when those tiers are fleshed out, not now.

- [ ] **Step 1: Write `README.md`**

Front matter, title `Math for ML Papers`. Sections:
- **Goal:** one paragraph. Go from high-school precalc to reading ML papers with theorems. Finish line: the Theorem 1 passage (quote it as in the spec). Topology comes later; this builds its foundation.
- **How to use this:** about two sittings a week, each about 45 minutes, and each sitting is one *half* (A or B) of a session. Do the reading, then the problems on paper, then the 🐍 problems in the tier notebook. Check work with Claude ("check 0.3 problem 4", then paste or photo your work). Tick `progress.md`. A tier ends with its checkpoint, and if the checkpoint feels shaky, ask Claude for a review session. Say "where was I?" to resume.
- **Tiers:** the 6-row table from the spec (Tier / Topic / Backbone / Checkpoint), each tier name linking to its folder.
- **Setup:** `python -m venv .venv && .venv/bin/pip install -r requirements.txt`, then `.venv/bin/jupyter lab`.
- **Resources:** the four links from the spec, plus the 3Blue1Brown channel `https://www.youtube.com/@3blue1brown`.

- [ ] **Step 2: Write `CLAUDE.md`**

Front matter, title `Math Tutor Context`. Content, in this exact order:

```markdown
# Math Tutor Context

## Learner
Learner background lives in `CLAUDE.local.md` (git-ignored, loaded automatically by Claude Code).
Read it before tutoring. If it is missing, ask the learner about their background and pace.

## Goal
Read ML papers including theorem proofs. Finish line: the Theorem 1 passage in
tier-5-proofs-and-papers/README.md. Later goal (not this curriculum): topology.

## Teaching rules
- **Hints before answers.** Smallest useful nudge first. Full solution only when asked.
- **Checking work:** find the *first* wrong step, say why, stop. Don't rewrite their solution.
- **Never** put answer keys in files.
- **Resume:** on "where was I?", read progress.md; report last completed half and the next one,
  plus anything on the Stuck list.
- **Notation:** whenever a session introduces a symbol, make sure it's in reference/notation.md.
- **Tone:** adult learner, not remedial. Connect to the ML goal where natural; don't force it.

## Authoring rules
- Tier 0 is written. Tiers 1–5 are skeletons (README only).
- When the learner is ~2 sessions from the end of a tier, write the next tier's session files
  in full, using the format below, adjusted by the Stuck list. Add their IDs to progress.md.
- Session format: front matter; `## Half A — <title>` with `### Read`, `### Key ideas`,
  `### Worked example`; `## Half B — <title>` with `### Problems` (5–8, 1–2 marked 🐍),
  `### Proof thread`, `### Done when`.
- Add 🐍 starter cells to that tier's notebooks/sessions.ipynb.
- Run `.venv/bin/python tools/check_curriculum.py --notebooks` after any authoring.
- If a checkpoint goes badly, write a review session `NN-review-<topic>.md` before moving on.
```

- [ ] **Step 3: Write `progress.md`**

Front matter, title `Progress`. Content:

```markdown
# Progress

Tick a box and write the date when you finish each half. `A` = read + worked example,
`B` = problems + proof thread.

## Tier 0: Notation & functions
- [ ] 0.1A Sets, number systems, ℝⁿ — date:
- [ ] 0.1B — date:
- [ ] 0.2A Subsets, operations, indexed sets — date:
- [ ] 0.2B — date:
- [ ] 0.3A Statements and if-then — date:
- [ ] 0.3B — date:
- [ ] 0.4A Quantifiers and negation — date:
- [ ] 0.4B — date:
- [ ] 0.5A Functions as maps — date:
- [ ] 0.5B — date:
- [ ] 0.6A Σ notation and averages — date:
- [ ] 0.6B — date:
- [ ] 0.7A Exponentials and logarithms — date:
- [ ] 0.7B — date:
- [ ] 0.8A Reading mathematical writing — date:
- [ ] 0.8B — date:
- [ ] 0.CP Checkpoint: decode the target passage — date:

## Tier 1: Single-variable calculus
Sessions added when this tier is written.
- [ ] 1.CP Checkpoint: 1-D gradient descent — date:

## Tier 2: Linear algebra
- [ ] 2.CP Checkpoint: linear model as θᵀx — date:

## Tier 3: Multivariable calculus
- [ ] 3.CP Checkpoint: backprop by hand — date:

## Tier 4: Probability
- [ ] 4.CP Checkpoint: empirical risk — date:

## Tier 5: Proofs & papers
- [ ] 5.CP Checkpoint: Theorem 1 — date:

## Stuck on / revisit
(Add a line whenever something didn't click: `- 0.4 negating nested quantifiers`.)
```

- [ ] **Step 4: Write `reference/notation.md`**

Front matter, title `Notation Cheat Sheet`. One intro line: "Each symbol: how to read it aloud, what it means, where it's taught. ⏳ = parked, taught later." Then a table with columns `Symbol | Read aloud | Meaning | Tier`, with these rows:

`∈` "in / is an element of" (0.1); `{x ∈ A : P(x)}` "the set of x in A such that P" (0.1); `ℕ ℤ ℚ ℝ` naturals, integers, rationals, reals (0.1); `ℝⁿ` "R n": n-tuples of reals (0.1); `A × B` Cartesian product (0.1); `⊆` subset (0.2); `∪ ∩ −` union, intersection, difference (0.2); `⋃ᵢ Aᵢ` indexed union (0.2); `∧ ∨ ¬ ⇒ ⇔` and, or, not, implies, iff (0.3); `∀ ∃` for all, there exists (0.4); `f : A → B` "f from A to B" (0.5); `g ∘ f` "g after f" (0.5); `f_θ` "f sub theta": a function chosen by parameters θ (0.5); `Σᵢ₌₁ᵐ` sum (0.6); `eˣ, ln` exp, natural log (0.7); `:=` "is defined as" (0.8); `x ∼ D` "x drawn from D" (0.8, details 4); `θ⁰, θᵋ` superscript *labels*, not powers (0.8); `ε, α` small positive numbers, step sizes (0.8); `·` between vectors: dot product ⏳ (2); `∇_θ L` gradient of L w.r.t. θ ⏳ (3); `𝔼_{x∼D}[·]` expectation ⏳ (4); `ℓ` per-example loss (0.6).

- [ ] **Step 5: Write `notes/README.md`**

Front matter, title `Notes`. Content: "Your own write-ups, photos/scans of paper work, and 'aha' notes. Suggested naming: `0.4-quantifiers.md`, `0.4-problems.jpg`. Claude can read images you put here when checking work."

- [ ] **Step 6: Run validator**

Run: `cd math && .venv/bin/python tools/check_curriculum.py`
Expected: no `missing README.md`/`CLAUDE.md`/`progress.md`/`reference`/`notes` failures, and no front-matter failures for these files. Tier failures are still expected.

---

### Task 3: Tier 0 README + sessions 01–04 (sets & logic)

**Files:**
- Create: `tier-0-notation/README.md`, `tier-0-notation/01-sets-and-rn.md`, `02-set-operations-and-indexing.md`, `03-statements-and-if-then.md`, `04-quantifiers-and-negation.md`

**Interfaces:**
- Consumes: progress IDs 0.1–0.4 (Task 2), validator.
- Produces: the 🐍 problem list for 0.1–0.4. Task 5 builds one notebook section per 🐍 problem, titled `0.N problem K`.

**Writing guidance for every session file:** follow the Global Constraints session format. Expand each item below into readable prose. Key ideas should be 3–5 bullets. The worked example is fully worked, with every step shown. Problems are written exactly as given (wording can be polished, not the substance). The Read block lists exact sections and an estimated time. Half headings: `## Half A — Learn` and `## Half B — Practice`. Each file opens with a one-line "Why this matters for the target passage" sentence under the title.

- [ ] **Step 1: Write `tier-0-notation/README.md`**

Front matter, title `Tier 0: Notation & Functions`. Sections:
- **Goal:** read mathematical notation fluently, enough to decode every symbol in the target passage, even before you know what ∇ or 𝔼 compute.
- **Reading:** *Book of Proof* ch. 1, 2, and 12 (selected sections), OpenStax Calc Vol 1 §1.5 and §5.1 (sigma subsection only). Include the edition note.
- **Notebook:** `notebooks/sessions.ipynb` (🐍 problems), `notebooks/checkpoint.ipynb`.
- `## Sessions`, a numbered list of 8 linking to files: 1 Sets, number systems, ℝⁿ · 2 Subsets, set operations, indexed sets · 3 Statements and if-then · 4 Quantifiers and negation · 5 Functions as maps · 6 Σ notation and averages · 7 Exponentials and logarithms · 8 Reading mathematical writing
- `## Checkpoint`: link to `checkpoint.md`, plus one line: "Decode every symbol in the target passage and restate Theorem 1 in logical form."

- [ ] **Step 2: Write `01-sets-and-rn.md`** (title: `0.1 Sets, Number Systems, and ℝⁿ`)

Why: θ ∈ ℝⁿ and D = {…} are sets. *Read:* BoP §1.1 Introduction to Sets, §1.2 The Cartesian Product, §1.9 Sets That Are Number Systems (~25 min).
*Key ideas:* a set is a collection, with `∈`/`∉`; set-builder `{x ∈ ℝ : x > 0}`; ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ and interval notation `(0,1]`; A × B is the set of ordered pairs; ℝⁿ is n-tuples (x₁,…,xₙ), so a model's parameters θ ∈ ℝⁿ are just n numbers in a list.
*Worked example:* (a) L = {(x,y) ∈ ℝ² : y = 2x + 1}. Describe it in words (the line with slope 2 and intercept 1) and test membership: (1,3) ∈ L since 3 = 2·1+1, and (2,4) ∉ L since 4 ≠ 5. (b) {0,1} × {a,b,c}: list all 6 pairs and note 2·3 = 6.
*Problems:*
1. Write in set-builder notation: the positive even integers.
2. True or false, with a reason: −3 ∈ ℕ; √2 ∈ ℚ; π ∈ ℝ; 0.5 ∈ ℤ.
3. List every element of {0,1}² and of {0,1}³. How many elements does {0,1}ⁿ have?
4. Write {x ∈ ℝ : x² < 4} in interval notation.
5. A model has 3 weights and 1 bias. In what set does its parameter vector θ live? Write one example θ.
6. 🐍 Use Python `set`s and `itertools.product` to build {0,1}³. Check its size, then write a function `size(n)` that returns |{0,1}ⁿ| for n = 1…10.
*Proof thread:* For finite sets, |A × B| = |A|·|B|. In 2–3 sentences, explain why. (Hint: picture a table with a row for each element of A and a column for each element of B.)
*Done when:* you can read "θ ∈ ℝⁿ" and "{x ∈ ℝ : x > 0}" aloud in plain English, and problems 1–5 have been checked.

- [ ] **Step 3: Write `02-set-operations-and-indexing.md`** (title: `0.2 Subsets, Set Operations, and Indexed Sets`)

Why: datasets are indexed collections, and index notation returns in Σ. *Read:* BoP §1.3 Subsets, §1.5 Union, Intersection, Difference, §1.6 Complement, §1.8 Indexed Sets (~30 min).
*Key ideas:* A ⊆ B means every element of A is in B; ∪, ∩, and A − B; complement relative to a universal set U; an indexed family A₁,…,Aₙ, with ⋃ᵢ₌₁ⁿ Aᵢ and ⋂ᵢ₌₁ⁿ Aᵢ; a dataset D = {(x₁,y₁),…,(x_m,y_m)} is indexed by i = 1…m.
*Worked example:* (a) A = {1,2,3,4} and B = {3,4,5}: A∪B = {1,2,3,4,5}, A∩B = {3,4}, A−B = {1,2}, B−A = {5}. (b) Aᵢ = [0, 1/i] for i = 1,2,3: the union is [0,1] (they're nested and A₁ is the largest), and the intersection is [0, 1/3].
*Problems:*
1. Is ∅ ⊆ A for every set A? Explain in one sentence.
2. A = [0,2], B = (1,3). Find A∪B, A∩B, A−B.
3. Aᵢ = {i, i+1}. Find ⋃ᵢ₌₁⁴ Aᵢ and ⋂ᵢ₌₁⁴ Aᵢ.
4. Aᵢ = (−1/i, 1/i) for i ∈ ℕ. What is ⋂ᵢ₌₁^∞ Aᵢ? Justify it. (This is your first "as small as you like" argument.)
5. The dataset {(1,2),(2,4),(3,7)} is written D = {(x₁,y₁),…,(x_m,y_m)}. What are m, x₂, and y₃?
6. 🐍 With U = set(range(10)), A = {0,2,4,6}, B = {4,5,6,7}, check De Morgan's law U − (A ∪ B) = (U − A) ∩ (U − B) in Python. Then try a few random A, B.
*Proof thread:* Show A ∩ B ⊆ A by starting with "Let x ∈ A ∩ B. Then…". This "take an arbitrary element" move is the basic step in set proofs.
*Done when:* you can compute indexed unions and intersections and name dataset pieces by index.

- [ ] **Step 4: Write `03-statements-and-if-then.md`** (title: `0.3 Statements and If-Then`)

Why: Theorem 1 has the shape "If H, then (A or B)". *Read:* BoP §2.1 Logic and Sentences, §2.2 And, Or, Not, §2.3 Conditional Statements, §2.4 Biconditional Statements, §2.5 Truth Tables for Statements (~30 min).
*Key ideas:* a statement is true or false; ∧, ∨ (inclusive), ¬; P ⇒ Q is false only when P is true and Q is false; the converse Q ⇒ P is a different statement, while the contrapositive ¬Q ⇒ ¬P is equivalent; mathematicians' "either A or B" is inclusive unless they say otherwise.
*Worked example:* full truth tables for P ⇒ Q and for ¬P ∨ Q, showing the columns match, so P ⇒ Q ≡ ¬P ∨ Q. Then write Theorem 1's skeleton: H = "θ⁰_S = θ⁰_T", A = "the dot product is 0 for all ε > 0", B = "for small ε the teacher loss drops". The theorem says H ⇒ (A ∨ B).
*Problems:*
1. Make the truth table for P ∧ ¬Q.
2. "If it rains, the ground is wet." Write the converse and the contrapositive. Which one is equivalent to the original?
3. Is "If 2 > 3, then 5 = 7" true? Explain.
4. Use a truth table to show (P ⇒ Q) ≡ (¬Q ⇒ ¬P).
5. Use a truth table to show (P ∨ Q) ≡ (¬P ⇒ Q). Explain in one sentence why this means you can prove "A or B" by assuming A is false and deducing B.
6. 🐍 Write `truth_table(expr)`, where `expr` is a Python function of `(P, Q)` returning a bool. It should print all 4 rows. Use it to check problems 4 and 5.
*Proof thread:* Using problem 5, rewrite H ⇒ (A ∨ B) as (H ∧ ¬A) ⇒ B. Say in words what a proof of Theorem 1 would have to assume and what it would have to show.
*Done when:* you can turn any "either…or" claim into an if-then.

- [ ] **Step 5: Write `04-quantifiers-and-negation.md`** (title: `0.4 Quantifiers and Negation`)

Why: "for all ε > 0" and "for sufficiently small ε > 0" are quantifier statements. *Read:* BoP §2.7 Quantifiers, §2.9 Translating English to Symbolic Logic, §2.10 Negating Statements (~30 min).
*Key ideas:* ∀ and ∃; the order of quantifiers matters; negation swaps ∀ ↔ ∃ and negates the inside; "for all ε > 0" means ∀ε ∈ (0,∞); "for sufficiently small ε > 0, P(ε)" means ∃δ > 0 such that ∀ε ∈ (0,δ), P(ε).
*Worked example:* translate "for sufficiently small ε > 0, L(θᵋ) < L(θ⁰)" into ∃δ>0 ∀ε (0<ε<δ ⇒ L(θᵋ) < L(θ⁰)). Negate it step by step: ∀δ>0 ∃ε (0<ε<δ ∧ L(θᵋ) ≥ L(θ⁰)). Then read the negation in English: "however small a window you pick, some ε inside it fails."
*Problems:*
1. Translate into symbols: "every real number is less than some integer."
2. Swap the quantifier order in problem 1, then translate back into English. Is it still true?
3. Negate ∀x ∈ ℝ, x² ≥ 0. Is the negation true?
4. Negate ∃δ > 0 ∀ε ∈ (0,δ), ε² < ε. Which is true, the original or the negation?
5. Let g(ε) be the dot product in Theorem 1 (a number depending on ε). Write "g(ε) = 0 for all ε > 0" in symbols, and also write its negation.
6. Is "for sufficiently small ε > 0, ε < 0.001" true? Give a δ that works.
7. 🐍 Let f(ε) = ε − 10ε². By sampling ε values in Python, estimate how small ε must be for f(ε) > 0. Then find the exact δ with algebra.
*Proof thread:* Explain in your own words why, when proving "∃δ ∀ε…", *you* get to choose δ, but then you must handle *every* ε in (0,δ). Use problem 7 as the example.
*Done when:* you can translate and negate quantified statements, especially "for sufficiently small ε."

- [ ] **Step 6: Run validator**

Run: `cd math && .venv/bin/python tools/check_curriculum.py | grep -E "tier-0|0\.[1-4]"`
Expected: no failures mentioning files 01–04 or the Tier 0 README. Failures saying `4 session files (need 6-12)` and missing checkpoint/notebooks are expected until Task 5.

---

### Task 4: Tier 0 sessions 05–08 (functions, Σ, exp/log, reading)

**Files:**
- Create: `tier-0-notation/05-functions-as-maps.md`, `06-sigma-and-averages.md`, `07-exp-and-log.md`, `08-reading-math-writing.md`

**Interfaces:**
- Consumes: the same writing guidance as Task 3.
- Produces: 🐍 problems for 0.5–0.8 (used by Task 5). Session 08's symbol-table format (`Symbol | Read aloud | Type/meaning | Tier learned`) is reused by the checkpoint.

- [ ] **Step 1: Write `05-functions-as-maps.md`** (title: `0.5 Functions as Maps`)

Why: L_T : Θ → ℝ, f_θ, and ℓ are all functions with types. *Read:* BoP §12.1 Functions, §12.4 Composition (skim §12.2 Injective and Surjective) (~30 min).
*Key ideas:* f : A → B has a domain, a codomain, and a rule, with exactly one output per input; functions can take vectors, as in f : ℝⁿ → ℝ; composition (g∘f)(x) = g(f(x)); a parameterized family f_θ gives a different function for each θ; a loss L : Θ → ℝ takes **parameters** and returns a number, with the data held fixed inside it.
*Worked example:* f_θ(x) = θ₁x + θ₂ with θ = (θ₁,θ₂) ∈ ℝ². Then f_(2,1)(3) = 7. Define L(θ) = (f_θ(1) − 3)². L((2,1)) = (3−3)² = 0 and L((1,2)) = (3−3)² = 0, so two different θ both give zero loss on one data point. Types: f_θ : ℝ → ℝ, L : ℝ² → ℝ.
*Problems:*
1. Which of these define functions ℝ → ℝ: x ↦ x², x ↦ ±√x, x ↦ 1/x? For each one that fails, fix it by changing the domain or the rule.
2. f(x) = x + 1, g(x) = x². Compute (g∘f)(2) and (f∘g)(2). Does order matter?
3. f : ℝ² → ℝ, f(x,y) = x² + y². Compute f(1,2), and describe the set {(x,y) : f(x,y) = 1}.
4. f_θ(x) = θx. Compute f₃(2) and f₋₁(2). What set is θ in, and what is the type of f_θ?
5. With f_θ(x) = θx and data {(1,2),(2,4)}, let L(θ) = ½[(f_θ(1)−2)² + (f_θ(2)−4)²]. Compute L(0), L(1), L(2). Which θ is best?
6. In the target passage, write the type (A → B) of f_θ, ℓ, and L_T. You may leave Θ, the inputs, and the outputs as named sets.
7. 🐍 Implement `f(theta, x)` and `L(theta)` from problem 5 and plot L(θ) for θ ∈ [−1, 4] with matplotlib.
*Proof thread:* Show that composition is associative, h∘(g∘f) = (h∘g)∘f, by evaluating both sides at an arbitrary x.
*Done when:* you can state the domain and codomain of every function in the target passage.

- [ ] **Step 2: Write `06-sigma-and-averages.md`** (title: `0.6 Σ Notation and Averages`)

Why: L_T(θ) = (1/m) Σᵢ₌₁ᵐ ℓ[f_θ(xᵢ), yᵢ]. *Read:* OpenStax Calculus Vol 1 §5.1, only the "Sigma (Summation) Notation" subsection and its rules (~15 min), plus the key ideas here.
*Key ideas:* Σᵢ₌₁ᵐ aᵢ, where the index i is a dummy variable; linearity Σ(c·aᵢ + bᵢ) = cΣaᵢ + Σbᵢ; an average is (1/m)Σ; xᵢ and yᵢ share the index i, so they're the i-th pair; empirical loss is the *average per-example loss over the dataset*.
*Worked example:* data {(1,2),(2,4),(3,7)}, f_θ(x) = 2x, ℓ(z,y) = (z−y)². The terms are (2−2)² = 0, (4−4)² = 0, (6−7)² = 1. L = (1/3)(0+0+1) = 1/3.
*Problems:*
1. Compute Σᵢ₌₁⁴ i² and Σₖ₌₀³ 2ᵏ.
2. Show Σᵢ₌₁ᵐ (3aᵢ + 2) = 3Σᵢ₌₁ᵐ aᵢ + 2m.
3. Write 1 + 3 + 5 + … + 19 in Σ notation.
4. Is Σᵢ aᵢbᵢ = (Σᵢ aᵢ)(Σᵢ bᵢ) in general? Test it with m = 2.
5. For the worked-example data and f_θ(x) = θx, write L(θ) = (1/3)Σ(θxᵢ − yᵢ)² as an explicit polynomial in θ.
6. If every data point is duplicated (each appears twice), what happens to m, to the sum, and to L? Explain.
7. 🐍 Compute L(θ) from problem 5 in two ways: a Python loop, and numpy `np.mean((theta*x - y)**2)`. Confirm they agree, then grid-search θ ∈ [0, 4] for the minimizer.
*Proof thread:* Prove problem 2 by writing the sum out term by term and regrouping. Justify each `=`.
*Done when:* you can read L_T(θ) = (1/m)Σℓ[f_θ(xᵢ), yᵢ] aloud and compute it for a small dataset by hand.

- [ ] **Step 3: Write `07-exp-and-log.md`** (title: `0.7 Exponentials and Logarithms`)

Why: the target paper's loss options include softmax cross-entropy, which is built from eˣ and ln. *Read:* OpenStax Calculus Vol 1 §1.5 Exponential and Logarithmic Functions (~30 min).
*Key ideas:* eˣ > 0 and is increasing; ln is the inverse of eˣ; ln(ab) = ln a + ln b and ln(aᵏ) = k ln a; ln 1 = 0, and ln x < 0 for 0 < x < 1; softmax pᵢ = e^{zᵢ} / Σⱼ e^{zⱼ} turns any scores into positive numbers summing to 1; cross-entropy −ln p_y is small when the correct class gets high probability and large when it gets low probability.
*Worked example:* z = (2, 1, 0). e² ≈ 7.389, e¹ ≈ 2.718, e⁰ = 1, and the sum ≈ 11.107, so p ≈ (0.665, 0.245, 0.090). If the true class is 1, the loss is −ln 0.665 ≈ 0.408. If the true class is 3, the loss is −ln 0.090 ≈ 2.408.
*Problems:*
1. Simplify ln(e³), e^{ln 5}, and ln(1/e²).
2. Solve e^{2x} = 7 for x.
3. Derive ln(a/b) = ln a − ln b from the product rule for logs.
4. Compute softmax(0,0,0) and softmax(1,1,1). Then show that adding the same constant c to every zᵢ never changes the softmax.
5. Compute −ln p for p ∈ {0.9, 0.5, 0.1, 0.01} and describe the pattern.
6. 🐍 Implement `softmax(z)` in numpy and check that it sums to 1. Show that the naive version overflows on z = (1000, 1001), then fix it by subtracting max(z) first (that's why problem 4 matters).
*Proof thread:* Write out the algebra for problem 4's shift invariance: e^{z+c} = e^z·e^c, then factor and cancel. Justify each step.
*Done when:* you can compute softmax and cross-entropy for a 3-class example by hand.

- [ ] **Step 4: Write `08-reading-math-writing.md`** (title: `0.8 Reading Mathematical Writing`)

Why: this session turns the passage from noise into a list of known and parked symbols. *Read:* no book. Read this file's key ideas, then read the target passage (quoted in full in this file) slowly, twice (~25 min).
*Key ideas:* `:=` means "defined as"; superscripts are often **labels** (θ⁰ is the initial value, θᵋ is the value that depends on ε), not powers; subscripts are either names (θ_S student, θ_T teacher) or indices (xᵢ); the Greek roster is θ (parameters), ε and α (small positive step sizes), ℓ (per-example loss), Δ ("change in"); `x ∼ D` means x is drawn from D; unknown symbols (∇, 𝔼, ·) get *named and parked* with the tier where they're taught.
*Worked example:* annotate the passage's first sentence as a table with columns `Symbol | Read aloud | Type/meaning | Tier learned`. Rows: θ⁰_S ("theta-zero sub S", the student's initial parameters, an element of Θ, tier 0), θ⁰_T, L_T (a function Θ → ℝ, tier 0.5), Θ (the set of all parameter vectors, think ℝⁿ, tier 0.1), ℝ.
*Problems:*
1. In θᵋ_T := θ⁰_T + εΔθ_T, which superscripts are labels and which (if any) are exponents? How can you tell?
2. Say "x ∼ D_S" in a plain-English sentence.
3. "For some learning rate ε > 0" versus "for all ε > 0" later on: in each phrase, is ε fixed or ranging over values?
4. Rewrite θᵋ_S := θ⁰_S + αΔθᵋ_S entirely in words.
5. Given θ⁰ = (1, 2), Δθ = (−0.5, 0.25), and ε = 0.1, compute θᵋ = θ⁰ + εΔθ component by component.
6. 🐍 Do problem 5 with numpy arrays. Then loop over ε ∈ {0.01, 0.1, 0.5, 1}, plot the points θᵋ in the plane, and describe the shape they make.
*Proof thread:* State Theorem 1's hypothesis and its two possible conclusions in your own words. Which conclusion uses "for sufficiently small ε"? Write that one in ∃δ∀ε form (from 0.4).
*Done when:* you can say what kind of thing every symbol in the passage is, even before knowing what ∇ computes.

Quote the full target passage (as in the spec) in a blockquote at the top of the Read block.

- [ ] **Step 5: Run validator**

Run: `cd math && .venv/bin/python tools/check_curriculum.py | grep -E "0[5-8]-|session files"`
Expected: no output (no failures for 05–08 and the session count is 8).

---

### Task 5: Tier 0 notebooks + checkpoint

**Files:**
- Create: `tier-0-notation/checkpoint.md`, `tier-0-notation/notebooks/sessions.ipynb`, `tier-0-notation/notebooks/checkpoint.ipynb`
- Temp: `<scratchpad>/build_tier0_nb.py` (not kept in the curriculum, so a rebuild can never clobber learner work)

**Interfaces:**
- Consumes: the 🐍 problems from Tasks 3–4: 0.1 #6, 0.2 #6, 0.3 #6, 0.4 #7, 0.5 #7, 0.6 #7, 0.7 #6, 0.8 #6.
- Produces: notebooks that execute cleanly, with starter code only and no solutions.

- [ ] **Step 1: Write `checkpoint.md`**

Front matter, title `Tier 0 Checkpoint: Decode the Target Passage`. Sections:
- **The passage:** the full target passage in a blockquote, with its source given as "Cloud et al., *Subliminal Learning* (2025), arXiv:2507.14805 — verify the citation when you start Tier 5."
- **Tasks:**
  1. Build a symbol table (format from 0.8) covering **every** symbol in the passage. For parked symbols (∇, 𝔼, ·), write the tier where they're taught.
  2. Give the type of f_θ, ℓ, L_T, D_T, and Δθ_T (for Δθ_T, say only "same kind of object as θ").
  3. Write Theorem 1 as H ⇒ (A ∨ B), then as (H ∧ ¬A) ⇒ B, with B in ∃δ∀ε form.
  4. In plain English, say what the theorem *claims* in 3 sentences, without computing anything.
  5. Notebook: `notebooks/checkpoint.ipynb`.
- **Pass when:** the table is complete with at most 2 lookups, and Claude has checked tasks 3 and 4. If not, add the shaky items to the Stuck list and ask for a review session.

- [ ] **Step 2: Write the notebook builder to the scratchpad and run it**

```python
# build_tier0_nb.py: usage: .venv/bin/python build_tier0_nb.py <math-root>
import sys
from pathlib import Path
import nbformat as nbf

root = Path(sys.argv[1]) / "tier-0-notation" / "notebooks"
root.mkdir(parents=True, exist_ok=True)
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

def write(name, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    path = root / name
    if path.exists():
        sys.exit(f"refusing to overwrite {path}")
    nbf.write(nb, path)

write("sessions.ipynb", [
    md("# Tier 0 — 🐍 problems\nOne section per 🐍 problem. Do the paper problems first. Starter code runs as-is; replace the `...` parts."),
    code("import itertools\nimport numpy as np\nimport matplotlib.pyplot as plt"),
    md("## 0.1 problem 6 — {0,1}ⁿ"),
    code("cube = set(itertools.product([0, 1], repeat=3))\nprint(len(cube))\n\ndef size(n):\n    ...  # return the number of elements of {0,1}^n\n\nprint([size(n) for n in range(1, 11)])"),
    md("## 0.2 problem 6 — De Morgan"),
    code("U = set(range(10))\nA = {0, 2, 4, 6}\nB = {4, 5, 6, 7}\nlhs = ...  # U − (A ∪ B)\nrhs = ...  # (U − A) ∩ (U − B)\nprint(lhs, rhs, lhs == rhs)"),
    md("## 0.3 problem 6 — truth tables"),
    code("def truth_table(expr):\n    for P in (True, False):\n        for Q in (True, False):\n            print(P, Q, expr(P, Q))\n\nimplies = lambda a, b: (not a) or b\ntruth_table(lambda P, Q: implies(P, Q))\n# now check problems 4 and 5"),
    md("## 0.4 problem 7 — how small is sufficiently small?"),
    code("f = lambda eps: eps - 10 * eps**2\nfor eps in [1, 0.5, 0.2, 0.1, 0.05, 0.01]:\n    print(eps, f(eps), f(eps) > 0)\n# narrow it down, then find δ exactly on paper"),
    md("## 0.5 problem 7 — plot a loss"),
    code("def f(theta, x):\n    return theta * x\n\ndef L(theta):\n    ...  # ½[(f(θ,1)−2)² + (f(θ,2)−4)²]\n\nthetas = np.linspace(-1, 4, 200)\n# plt.plot(thetas, [L(t) for t in thetas]); plt.xlabel('θ'); plt.ylabel('L(θ)')"),
    md("## 0.6 problem 7 — loop vs. numpy"),
    code("x = np.array([1.0, 2.0, 3.0])\ny = np.array([2.0, 4.0, 7.0])\n\ndef L_loop(theta):\n    ...\n\ndef L_np(theta):\n    ...  # one line with np.mean"),
    md("## 0.7 problem 6 — softmax"),
    code("def softmax(z):\n    z = np.asarray(z, dtype=float)\n    ...  # naive first, then the stable version\n"),
    md("## 0.8 problem 6 — θᵋ = θ⁰ + εΔθ"),
    code("theta0 = np.array([1.0, 2.0])\ndelta = np.array([-0.5, 0.25])\nfor eps in [0.01, 0.1, 0.5, 1]:\n    ...  # compute and collect θᵋ, then plot the points"),
])

write("checkpoint.ipynb", [
    md("# Tier 0 checkpoint — the passage in code (no calculus yet)\n"
       "Toy setup: f_θ(x) = θ·x with θ a single number, squared-error ℓ. "
       "You are *given* a direction Δθ; in Tier 3 you'll learn it's −∇L."),
    code("import numpy as np\n\nx = np.array([1.0, 2.0, 3.0])\ny = np.array([2.0, 4.0, 7.0])\nm = len(x)\n\ndef f(theta, x):\n    return theta * x\n\ndef ell(z, y):\n    return (z - y) ** 2"),
    md("**1.** Write `L_T(theta)` = (1/m) Σ ℓ[f_θ(xᵢ), yᵢ]."),
    code("def L_T(theta):\n    ...\n"),
    md("**2.** θ⁰ = 1.0 and Δθ = +1.0 (given). Compute θᵋ = θ⁰ + εΔθ and L_T(θᵋ) for ε in [0.01, 0.1, 0.5, 1, 2, 3]. "
       "For which ε does the loss go down? Up? Connect this to 'for sufficiently small ε'."),
    code("theta0, delta = 1.0, 1.0\nfor eps in [0.01, 0.1, 0.5, 1, 2, 3]:\n    ...\n"),
    md("**3.** Repeat with Δθ = −1.0. What changes, and why might *direction* matter?"),
    code(""),
])
print("ok")
```

Run: `cd math && .venv/bin/python <scratchpad>/build_tier0_nb.py "$PWD"`
Expected: `ok`, and two `.ipynb` files exist.

- [ ] **Step 3: Run the full validator with notebooks**

Run: `cd math && .venv/bin/python tools/check_curriculum.py --notebooks | grep -E "tier-0|0\."`
Expected: no output. Notebooks must execute: the starter stubs return `None` and the prints run. If `print([size(n) ...])` causes trouble, that's fine because it prints `[None, …]`. Any traceback means a stub is invalid, so fix the stub, not the check.

---

### Task 6: Tier 1–5 skeletons

**Files:**
- Create: `tier-1-calculus/README.md`, `tier-2-linear-algebra/README.md`, `tier-3-multivariable/README.md`, `tier-4-probability/README.md`, `tier-5-proofs-and-papers/README.md`

**Interfaces:**
- Consumes: validator `check_readme` (`## Sessions` with 6–12 numbered items, then `## Checkpoint`).
- Produces: the session titles that become `NN-*.md` files when each tier is authored (per CLAUDE.md).

Each README has: front matter; title `Tier N: <Topic>`; **Goal** (1–2 sentences); **Status** line: "Skeleton. Sessions are written when you're ~2 sessions from finishing the previous tier."; **Reading** with the edition note; `## Sessions` as a numbered list in the form `Title — reading`; `## Checkpoint` (excerpt pointer + task + pass criterion). Use exactly this content:

- [ ] **Step 1: `tier-1-calculus/README.md`**

Goal: derivatives as rates and slopes, the chain rule, and linear/Taylor approximation, which is the 1-D core of gradient descent. Reading: OpenStax Calculus Vol 1 (Vol 2 for Taylor), plus 3Blue1Brown *Essence of Calculus* (by video title).
Sessions:
1. Functions and graphs refresher — OpenStax §1.1–1.3
2. Limits, intuitively — §2.1–2.2; 3B1B "Limits, L'Hôpital's rule, and epsilon delta definitions"
3. Limit laws and continuity — §2.3–2.4
4. The derivative — §3.1–3.2; 3B1B "The essence of calculus", "The paradox of the derivative"
5. Differentiation rules — §3.3; 3B1B "Derivative formulas through geometry"
6. The chain rule — §3.6; 3B1B "Visualizing the chain rule and product rule"
7. Derivatives of exp and log — §3.9; 3B1B "What's so special about Euler's number e?"
8. Linear approximation — §4.2
9. Maxima, minima, optimization — §4.3, §4.7
10. Taylor polynomials — Vol 2 §6.3; 3B1B "Taylor series"
11. Integrals as accumulation (light) — §5.1–5.3; 3B1B "Integration and the fundamental theorem of calculus"
Checkpoint: read MML §7.1 "Optimization Using Gradient Descent" through a 1-D lens. In a notebook, run 1-D gradient descent on L(θ) from 0.6 and compare it with sympy's exact minimizer. Prove that if L′(θ⁰) ≠ 0, then for sufficiently small ε, L(θ⁰ − εL′(θ⁰)) < L(θ⁰) (the 1-D shadow of Theorem 1). Pass: proof checked by Claude.

- [ ] **Step 2: `tier-2-linear-algebra/README.md`**

Goal: vectors, dot products, and matrices as linear maps, enough to read θ ∈ ℝⁿ, θᵀx, and Δθ_S · Δθ_T. Reading: 3Blue1Brown *Essence of Linear Algebra* + MML ch. 2–3.
Sessions:
1. Vectors — 3B1B "Vectors, what even are they?"
2. Linear combinations and span — 3B1B "Linear combinations, span, and basis vectors"; MML §2.5
3. Matrices as linear transformations — 3B1B "Linear transformations and matrices"; MML §2.7
4. Matrix multiplication as composition — 3B1B "Matrix multiplication as composition"; MML §2.2
5. Systems of linear equations — MML §2.1, §2.3
6. Dot products and norms — 3B1B "Dot products and duality"; MML §3.1–3.2
7. Angles, orthogonality, projections — MML §3.3–3.4, §3.8
8. Basis and rank — MML §2.6; 3B1B "Change of basis"
Checkpoint: MML §9.1–9.2 (the linear regression problem setup). Annotate every symbol and implement f(x) = θᵀx for a small dataset in numpy. Explain what Δθ_S · Δθ_T = 0 means geometrically. Pass: annotation and explanation checked by Claude.

- [ ] **Step 3: `tier-3-multivariable/README.md`**

Goal: partial derivatives, gradients, and the multivariate chain rule, enough to read ∇_θ L and backprop. Reading: MML ch. 5 and §7.1, plus 3Blue1Brown *Neural Networks* (backprop videos).
Sessions:
1. Partial derivatives — MML §5.2
2. The gradient as a vector — MML §5.2
3. Directional derivatives and steepest descent — MML §5.2 + session notes
4. Gradients of vector-valued functions (Jacobians) — MML §5.3
5. The multivariate chain rule — MML §5.2.2
6. Backpropagation — MML §5.6; 3B1B "What is backpropagation really doing?", "Backpropagation calculus"
7. Linearization and multivariate Taylor — MML §5.8
8. Gradient descent in ℝⁿ — MML §7.1
Checkpoint: MML §5.6. By hand, compute the gradient of a 2-input, 2-hidden-unit, 1-output network's squared-error loss, then verify it in numpy with finite differences. Pass: gradients agree to 1e-6 and the hand derivation is checked by Claude.

- [ ] **Step 4: `tier-4-probability/README.md`**

Goal: distributions, expectation, and empirical averages, enough to read x ∼ D, 𝔼_{x∼D}[·], and cross-entropy as a loss. Reading: MML ch. 6 and ch. 8.
Sessions:
1. Probability spaces and random variables — MML §6.1
2. Discrete and continuous distributions — MML §6.2
3. Sum rule, product rule, Bayes — MML §6.3
4. Expectation and variance — MML §6.4
5. Sampling and empirical averages (law of large numbers) — MML §6.4 + session notes and simulation
6. The Gaussian — MML §6.5
7. Losses as likelihoods: squared error and cross-entropy — MML §8.3
8. Empirical risk minimization — MML §8.2
Checkpoint: MML §8.2. Explain the difference between the expected loss 𝔼_{x∼D}[ℓ] and the empirical loss (1/m)Σℓ, and show by simulation that the empirical loss approaches the expected loss as m grows. Pass: explanation checked by Claude.

- [ ] **Step 5: `tier-5-proofs-and-papers/README.md`**

Goal: read and reconstruct proofs, ending with Theorem 1. Reading: *Book of Proof* ch. 4–7 and 13, plus the target paper. Include the full target passage in a blockquote under **Finish line**, citing Cloud et al., *Subliminal Learning* (2025), arXiv:2507.14805 (verify).
Sessions:
1. Direct proof — BoP ch. 4
2. Contrapositive proof — BoP ch. 5
3. Proof by contradiction — BoP ch. 6
4. Proving non-conditional statements: either/or and cases — BoP ch. 7
5. ε-arguments in calculus — BoP ch. 13
6. First-order arguments: "for sufficiently small ε" via Taylor — session notes (builds on Tier 1's checkpoint)
7. Reading a paper's setup section — target paper, setup/theory section
8. Theorem 1 walkthrough — target paper, theorem and its proof (appendix)
Checkpoint: read the passage cold, explain every symbol, and write the proof of Theorem 1 in your own words (first-order Taylor expansion of L_T around θ⁰, plus the sign of Δθ_S · Δθ_T). Pass: proof checked by Claude.

- [ ] **Step 6: Run the full validator**

Run: `cd math && .venv/bin/python tools/check_curriculum.py --notebooks`
Expected: `OK`, exit 0.

---

### Task 7: Final verification

- [ ] **Step 1:** Run `cd math && .venv/bin/python tools/check_curriculum.py --notebooks; echo exit=$?`. Expected: `OK` and `exit=0`.
- [ ] **Step 2:** Run `cd math && find . -path ./.venv -prune -o -type f -print | sort` and confirm the tree matches the File Map (plus `docs/`).
- [ ] **Step 3:** Read `tier-0-notation/01-sets-and-rn.md` and `08-reading-math-writing.md` end to end as the learner would. Check that each worked example's arithmetic is correct (e.g. the softmax in 0.7: recompute it in the venv). Fix any errors found.
- [ ] **Step 4:** Update the memory file `learner-background.md` so it notes the curriculum is built and that Tier 0 is the starting point.
