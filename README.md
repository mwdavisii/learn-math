---
type: personal
title: Math for ML Papers
source: personal
---

# Math for ML Papers

## Goal

Go from high-school precalc to reading ML papers, including their theorems and proofs. The finish line is this passage, from a paper on teacher/student distillation:

> Given student and teacher initializations θ⁰_S and θ⁰_T, and any differentiable
> loss L_T : Θ → ℝ … θ^ε_T := θ⁰_T + εΔθ_T, where Δθ_T := −∇_θ L_T(θ⁰) …
> **Theorem 1.** If θ⁰_S = θ⁰_T, then either Δθ^ε_S · Δθ_T = 0 for all ε > 0, or
> for sufficiently small ε > 0, L_T(θ^ε_S) < L_T(θ⁰_S).

"Done" means you can read the full passage, explain each symbol, and follow (and reconstruct) the proof of Theorem 1. Topology comes later; this curriculum builds its foundation (calculus, linear algebra, proof reading).

## How to use this

- Plan on about two sittings a week, each about 45 minutes. Each sitting is one *half* (A or B) of a session.
- Do the reading, then the problems on paper, then the 🐍 problems in the tier notebook.
- Check your work with Claude: say "check 0.3 problem 4", then paste or photo your work.
- Tick `progress.md` when you finish a half.
- A tier ends with its checkpoint. If the checkpoint feels shaky, ask Claude for a review session.
- Say "where was I?" to resume.

## Tiers

| Tier | Topic | Backbone | Checkpoint |
|---|---|---|---|
| [0](tier-0-notation/) | Notation and functions: functions as maps (f : A → B), sets → ℝⁿ, Σ and indices, exp/log, reading definitions | *Book of Proof* ch. 1, 2, 12 + OpenStax §1.5, §5.1 | Decode the notation in the target passage (symbols only, not the meaning yet) |
| [1](tier-1-calculus/) | Single-variable calculus: limits, derivatives, chain rule, Taylor approximation, a little integration | OpenStax *Calculus* Vol 1 + 3Blue1Brown *Essence of Calculus* | 1-D gradient descent, by hand and in numpy |
| [2](tier-2-linear-algebra/) | Linear algebra: vectors, dot products, matrices, linear maps | 3Blue1Brown *Essence of Linear Algebra* + *Mathematics for Machine Learning* (MML) ch. 2–3 | A linear model f_θ(x) = θᵀx and its parameters as a vector |
| [3](tier-3-multivariable/) | Multivariable calculus: partials, gradients, multivariate chain rule, first-order Taylor in ℝⁿ | MML ch. 5 | Backprop by hand for a tiny network, checked in numpy |
| [4](tier-4-probability/) | Probability: distributions, expectation 𝔼_{x∼D}, empirical averages, squared error, softmax cross-entropy | MML ch. 6 | Empirical loss L(θ) = (1/m) Σ ℓ(f_θ(xᵢ), yᵢ) vs. expected loss |
| [5](tier-5-proofs-and-papers/) | Reading theorems and proofs: "either/or," "for sufficiently small ε," first-order arguments | *Book of Proof* + the target paper | Full read of the target passage and proof of Theorem 1 |

## Setup

```
/usr/bin/python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Then run `.venv/bin/jupyter lab`.

Note: on this machine, create the venv with the system Python (`/usr/bin/python3`); the Nix python breaks numpy. Elsewhere, `python -m venv .venv` is fine.

## Resources

All free:
- OpenStax *Calculus*: https://openstax.org/details/books/calculus-volume-1
- Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*: https://mml-book.github.io
- Hammack, *Book of Proof*: https://richardhammack.github.io/BookOfProof/
- 3Blue1Brown series on YouTube: https://www.youtube.com/@3blue1brown
