---
type: personal
title: Notation Cheat Sheet
source: personal
---

# Notation Cheat Sheet

Each symbol: how to read it aloud, what it means, where it's taught. ⏳ = parked, taught later.

| Symbol | Read aloud | Meaning | Tier |
|---|---|---|---|
| `∈` | "in" / "is an element of" | membership | 0.1 |
| `∉` | "not in" | not an element of | 0.1 |
| `{x ∈ A : P(x)}` | "the set of x in A such that P" | set-builder notation | 0.1 |
| `ℕ ℤ ℚ ℝ` | naturals, integers, rationals, reals | the standard number systems | 0.1 |
| `ℝⁿ` | "R n" | n-tuples of reals | 0.1 |
| `A × B` | "A cross B" | Cartesian product: pairs (a, b) | 0.1 |
| `(a,b]`, `[a,b]` | "open-closed interval", "closed interval" | interval notation: round bracket excludes the endpoint, square bracket includes it | 0.1 |
| `\|A\|` | "size of A" | number of elements of a finite set A | 0.1 |
| `⊂`, `⊆` | "is a subset of" | `⊆` means every element of the left is in the right (equality allowed). `⊂` is used for the same idea or for a proper subset, depending on the author, as in ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ, so check the context | 0.1, 0.2 |
| `∅` | "the empty set" | the set with no elements | 0.2 |
| `∪ ∩ −` | union, intersection, difference | combining sets | 0.2 |
| `⋃ᵢ Aᵢ` | "union over i of A i" | indexed union | 0.2 |
| `⋂ᵢ Aᵢ` | "intersection over i of A i" | indexed intersection: elements in every Aᵢ | 0.2 |
| `Aᶜ`, `U − A` | "A complement" | everything in the universal set U that is not in A | 0.2 |
| `∧ ∨ ¬ ⇒ ⇔` | and, or, not, implies, iff | logical connectives | 0.3 |
| `≡` | "is logically equivalent to" | the two statements always have the same truth value | 0.3 |
| `∀ ∃` | for all, there exists | quantifiers | 0.4 |
| `f : A → B` | "f from A to B" | a function with domain A and codomain B | 0.5 |
| `x ↦ …` | "x maps to" | names a function by its rule, e.g. x ↦ x² | 0.5 |
| `Θ` | "capital theta" | the set of all parameter vectors | 0.5 |
| `g ∘ f` | "g after f" | composition: first f, then g | 0.5 |
| `f_θ` | "f sub theta" | a function chosen by parameters θ | 0.5 |
| `Σᵢ₌₁ᵐ` | "sum from i equals 1 to m" | sum | 0.6 |
| `ℓ` | "ell" | per-example loss | 0.6 |
| `ℓ[a, b]` | "ell of a, b" | square brackets here are ordinary function application, same as ℓ(a, b) | 0.6 |
| `eˣ, ln` | exp, natural log | exponential and its inverse | 0.7 |
| `softmax(z)` | "soft-max" | turns scores into probabilities: e^(zᵢ) / Σⱼ e^(zⱼ) | 0.7 |
| `−ln p_y` (cross-entropy) | "cross-entropy" | loss when the true class got probability p_y | 0.7 |
| `:=` | "is defined as" | definition, not a claim | 0.8 |
| `x ∼ D` | "x drawn from D" | x is a random sample from distribution D | 0.8 (details 4) |
| `θ⁰, θ^ε` | "theta zero", "theta epsilon" | superscript *labels*, not powers | 0.8 |
| `θ⁰` | "theta zero" | with no subscript: the shared initialization, as in θ⁰_S = θ⁰_T | 0.8 |
| `y^ε_x` | "y epsilon sub x" | the label for input x produced by the ε-teacher | 0.8 |
| `ε, α` | "epsilon", "alpha" | small positive numbers, step sizes | 0.8 |
| `Δ` | "delta" | change in; Δθ is a step/update to θ | 0.8 |
| `·` between vectors | "dot" | dot product ⏳ | 2 |
| `θᵀx` | "theta transpose x" | dot product written as a matrix product ⏳ | 2 |
| `∇_θ L` | "gradient of L with respect to theta" | vector of partial derivatives ⏳ | 3 |
| `𝔼_{x∼D}[·]` | "expectation over x drawn from D" | average over a distribution ⏳ | 4 |
