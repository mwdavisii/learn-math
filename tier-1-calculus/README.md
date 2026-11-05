---
type: personal
title: "Tier 1: Single-Variable Calculus"
source: personal
---

# Tier 1: Single-Variable Calculus

## Goal

Derivatives as rates and slopes, the chain rule, and linear/Taylor approximation, which is the 1-D core of gradient descent.

**Status**: Skeleton. Sessions are written when you're ~2 sessions from finishing the previous tier.

## Reading

- OpenStax *Calculus* Vol 1 (2016), with Vol 2 for Taylor polynomials.
- 3Blue1Brown, *Essence of Calculus* (video series, cited by video title).

If a section number doesn't match your copy, find it by title.

## Sessions

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

## Checkpoint

Read MML §7.1 "Optimization Using Gradient Descent" through a 1-D lens. In a notebook, run 1-D gradient descent on L(θ) from 0.6 and compare it with sympy's exact minimizer. Prove that if L′(θ⁰) ≠ 0, then for sufficiently small ε, L(θ⁰ − εL′(θ⁰)) < L(θ⁰) (the 1-D shadow of Theorem 1).

Pass: proof checked by Claude.
