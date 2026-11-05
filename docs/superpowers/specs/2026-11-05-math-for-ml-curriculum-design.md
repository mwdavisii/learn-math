---
type: personal
title: Math for ML Papers — Curriculum Design
source: personal
---

# Math for ML Papers: Curriculum Design

**Date:** 2026-11-05
**Status:** Approved in brainstorming, pending spec review

## Goal

Get from "high-school precalc, strong Algebra I/II, rusty on calculus" to reading
ML research papers, including following their theorems and proofs. The finish
line is this passage, taken from a paper on teacher/student distillation:

> Given student and teacher initializations θ⁰_S and θ⁰_T, and any differentiable
> loss L_T : Θ → ℝ … θ^ε_T := θ⁰_T + εΔθ_T, where Δθ_T := −∇_θ L_T(θ⁰) …
> **Theorem 1.** If θ⁰_S = θ⁰_T, then either Δθ^ε_S · Δθ_T = 0 for all ε > 0, or
> for sufficiently small ε > 0, L_T(θ^ε_S) < L_T(θ⁰_S).

"Done" means the learner can read the full passage, explain each symbol, and
follow (and reconstruct) the proof of Theorem 1.

**Later (out of scope here):** topology and pure math. This curriculum
deliberately builds the shared foundation (calculus, linear algebra, proof
reading) that a later topology track needs.

## Constraints

- **Pacing:** sized for 2–3 hours/week in short sittings that may be interrupted.
  Expected duration is about 12–18 months.
- **Assumed background:** solid high-school algebra (through Algebra II/precalc);
  comfortable programming in Python; no prior numpy or scientific stack needed.
- **Style:** hybrid. A free textbook is the backbone. The folder holds session
  guides, problems, notebooks, and checkpoints, and Claude acts as tutor.

## Approach: tier ladder plus paper checkpoints

Tiers are done strictly in order. Each tier ends with a **checkpoint**: a real
ML excerpt that uses only the math learned so far. The learner reads and
annotates it, and a notebook reproduces it. Proof reading runs as a thread
through every tier instead of being saved for the end.

| Tier | Topic | Backbone | Checkpoint |
|---|---|---|---|
| 0 | Notation and functions: functions as maps (f : A → B), sets → ℝⁿ, Σ and indices, exp/log, reading definitions | *Book of Proof* (Hammack) ch. 1–2 | Decode the notation in the target passage (symbols only, not the meaning yet) |
| 1 | Single-variable calculus: limits, derivatives, chain rule, Taylor approximation, a little integration | OpenStax *Calculus* Vol 1 + 3Blue1Brown *Essence of Calculus* | 1-D gradient descent, by hand and in numpy |
| 2 | Linear algebra: vectors, dot products, matrices, linear maps | 3Blue1Brown *Essence of Linear Algebra* + *Mathematics for Machine Learning* (MML) ch. 2–3 | A linear model f_θ(x) = θ·x and its parameters as a vector |
| 3 | Multivariable calculus: partials, gradients, multivariate chain rule, first-order Taylor in ℝⁿ | MML ch. 5 | Backprop by hand for a tiny network, checked in numpy |
| 4 | Probability: distributions, expectation 𝔼_{x∼D}, empirical averages, squared error, softmax cross-entropy | MML ch. 6 | Empirical loss L(θ) = (1/m) Σ ℓ(f_θ(xᵢ), yᵢ) vs. expected loss |
| 5 | Reading theorems and proofs: "either/or," "for sufficiently small ε," first-order arguments | *Book of Proof* + the target paper | Full read of the target passage and proof of Theorem 1 |

All backbone resources are free:
- OpenStax *Calculus*: https://openstax.org/details/books/calculus-volume-1
- Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*: https://mml-book.github.io
- Hammack, *Book of Proof*: https://richardhammack.github.io/BookOfProof/
- 3Blue1Brown series on YouTube

## Folder layout

```
math/
├── README.md            # goal, tier table, how to use, resource links
├── progress.md          # checkbox per session half + checkpoint, dated
├── CLAUDE.md            # tutor context and teaching rules
├── requirements.txt     # numpy, matplotlib, jupyter (sympy added in Tier 1)
├── tier-0-notation/
│   ├── README.md        # tier goals, reading list, session list
│   ├── 01-<topic>.md … NN-<topic>.md
│   ├── checkpoint.md
│   └── notebooks/
├── tier-1-calculus/
├── tier-2-linear-algebra/
├── tier-3-multivariable/
├── tier-4-probability/
├── tier-5-proofs-and-papers/
├── notes/               # learner's own write-ups and scans
├── reference/
│   └── notation.md      # running symbol → meaning cheat sheet, extended each tier
└── docs/superpowers/specs/
```

Each tier has 6–12 sessions, which works out to 1–2 months per tier.

## Session format

Each session file is sized for 60–90 minutes and split into two halves,
**A** and **B**, of about 45 minutes each, so one interruption costs half a
session at most. Every session file contains:

1. **Read:** exact book sections or video, about 20–30 minutes
2. **Key ideas:** 3–5 bullets for fast review after a break
3. **Worked example:** one, fully written out
4. **Problems:** 5–8, graded easy to hard, done with pencil and paper first.
   1–2 are marked 🐍 to verify or visualize in a notebook.
5. **Proof thread:** one small "why does this step follow?" item
6. **Done when:** a concrete exit criterion

Answers are **not** included in session files. The learner checks with
Claude, so they aren't tempted to peek.

## Checkpoints

`checkpoint.md` in each tier contains the excerpt, the source, a list of
annotation questions ("what is the type of each symbol?", "what does this
line claim?"), and a notebook task. The checkpoint is the tier's acceptance
test. If it isn't comfortable, add 1–2 review sessions targeting the weak
spots before starting the next tier.

## Tutor behavior (`CLAUDE.md`)

`CLAUDE.md` records the learner's background and goal, plus these rules:
- **Hints before answers.** Give the smallest useful nudge first. Show full
  solutions only on request.
- **Checking work:** find the *first* wrong step and say why. Don't rewrite
  the learner's solution.
- **Resuming:** for "where was I?", read `progress.md` and summarize the last
  completed half-session and what comes next.
- **Just-in-time authoring:** Tier 0 is written in full up front. Tiers 1–5
  start as skeletons: a tier README with session titles, reading assignments,
  and the checkpoint excerpt. Each tier's sessions are written in full when the
  learner is about two sessions from reaching it, adjusted using the
  "stuck on" list.
- **Notation sheet:** add each new symbol to `reference/notation.md` when it is
  introduced.

## Progress tracking (`progress.md`)

- One checkbox per session half (e.g. `0.3A`, `0.3B`) and per checkpoint,
  with the completion date.
- A **Stuck on / revisit** list. Items get a deliberate review session
  rather than being left behind.

## Notebooks

- Stack: numpy and matplotlib, with sympy from Tier 1 for checking
  derivatives. No ML frameworks.
- One notebook per checkpoint plus the 🐍 problems, kept in the tier's
  `notebooks/` folder.

## Initial build scope

The first implementation produces:
- Root `README.md`, `progress.md`, `CLAUDE.md`, `requirements.txt`,
  `reference/notation.md`, and an empty `notes/`
- Tier 0 written in full: README, all sessions, checkpoint, notebook
- Tier 1–5 skeletons: README with session titles, readings, and checkpoint
  excerpt

## Out of scope

Spaced-repetition flashcards, a topology track, automated grading, and
answer keys in files.
