---
type: personal
title: "Tier 5: Proofs and Papers"
source: personal
---

# Tier 5: Proofs and Papers

## Goal

Read and reconstruct proofs, ending with Theorem 1.

**Status**: Skeleton. Sessions are written when you're ~2 sessions from finishing the previous tier.

## Reading

- Hammack, *Book of Proof* (3rd ed.): ch. 4–7 and ch. 13.
- The target paper (see Finish line below).

If a section number doesn't match your copy, find it by title.

## Finish line

> More formally, given student and teacher initializations θ⁰_S and θ⁰_T, and any differentiable loss function L_T : Θ → ℝ, we consider a teacher obtained via a single step of gradient descent on L_T. In our experiments, L_T is the empirical loss on some dataset D_T = {(x₁, y₁), …, (x_m, y_m)}. I.e., L_T(θ) = (1/m) Σᵢ₌₁ᵐ ℓ[f_θ(xᵢ), yᵢ] for some loss function ℓ. For some learning rate ε > 0, the teacher's parameters are θ^ε_T := θ⁰_T + εΔθ_T, where Δθ_T := −∇_θ L_T(θ⁰). Using this teacher, and given samples x ∼ D_S from the training distribution, we produce labels y^ε_x = f_{θ^ε_T}(x). We obtain the student via a single step of gradient descent on this data distribution with learning rate α > 0 and loss L_S(z, y) either softmax cross-entropy or squared error. The student's parameters are θ^ε_S := θ⁰_S + αΔθ^ε_S, where Δθ^ε_S := −∇_θ 𝔼_{x∼D_S}[L_S(f_{θ⁰}(x), y^ε_x)]. Then:
>
> **Theorem 1.** If θ⁰_S = θ⁰_T, then either Δθ^ε_S · Δθ_T = 0 for all ε > 0, or for sufficiently small ε > 0, L_T(θ^ε_S) < L_T(θ⁰_S).

Source: Cloud et al., *Subliminal Learning* (2025), arXiv:2507.14805 (verify the citation).

## Sessions

1. Direct proof — BoP ch. 4
2. Contrapositive proof — BoP ch. 5
3. Proof by contradiction — BoP ch. 6
4. Proving non-conditional statements: either/or and cases — BoP ch. 7
5. ε-arguments in calculus — BoP ch. 13
6. First-order arguments: "for sufficiently small ε" via Taylor — session notes (builds on Tier 1's checkpoint)
7. Reading a paper's setup section — target paper, setup/theory section
8. Theorem 1 walkthrough — target paper, theorem and its proof (appendix)

## Checkpoint

Read the passage cold, explain every symbol, and write the proof of Theorem 1 in your own words (first-order Taylor expansion of L_T around θ⁰, plus the sign of Δθ_S · Δθ_T).

Pass: proof checked by Claude.
