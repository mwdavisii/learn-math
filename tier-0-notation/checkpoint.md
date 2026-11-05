---
type: personal
title: "Tier 0 Checkpoint: Decode the Target Passage"
source: personal
---

# Tier 0 Checkpoint: Decode the Target Passage

## The passage

Source: Cloud et al., *Subliminal Learning* (2025), arXiv:2507.14805 — verify the citation when you start Tier 5.

> More formally, given student and teacher initializations θ⁰_S and θ⁰_T, and any differentiable loss function L_T : Θ → ℝ, we consider a teacher obtained via a single step of gradient descent on L_T. In our experiments, L_T is the empirical loss on some dataset D_T = {(x₁, y₁), …, (x_m, y_m)}. I.e., L_T(θ) = (1/m) Σᵢ₌₁ᵐ ℓ[f_θ(xᵢ), yᵢ] for some loss function ℓ. For some learning rate ε > 0, the teacher's parameters are θ^ε_T := θ⁰_T + εΔθ_T, where Δθ_T := −∇_θ L_T(θ⁰). Using this teacher, and given samples x ∼ D_S from the training distribution, we produce labels y^ε_x = f_{θ^ε_T}(x). We obtain the student via a single step of gradient descent on this data distribution with learning rate α > 0 and loss L_S(z, y) either softmax cross-entropy or squared error. The student's parameters are θ^ε_S := θ⁰_S + αΔθ^ε_S, where Δθ^ε_S := −∇_θ 𝔼_{x∼D_S}[L_S(f_{θ⁰}(x), y^ε_x)]. Then:
>
> **Theorem 1.** If θ⁰_S = θ⁰_T, then either Δθ^ε_S · Δθ_T = 0 for all ε > 0, or for sufficiently small ε > 0, L_T(θ^ε_S) < L_T(θ⁰_S).

## Tasks

1. Build a symbol table (use the format from 0.8, with a "Session learned" column) covering **every** symbol in the passage. For the parked symbols (∇, 𝔼, ·), write the tier where each is taught.
2. Give the type of f_θ, ℓ, L_T, D_T, and Δθ_T. For Δθ_T, say only "same kind of object as θ".
3. Write Theorem 1 as H ⇒ (A ∨ B), then as (H ∧ ¬A) ⇒ B, with B in ∃δ∀ε form.
4. In plain English, say what the theorem *claims* in 3 sentences, without computing anything.
5. Notebook: `notebooks/checkpoint.ipynb`.

## Pass when

- The table is complete with at most 2 lookups, and Claude has checked tasks 3 and 4.
- If not, add the shaky items to the Stuck list in progress.md and ask for a review session.
