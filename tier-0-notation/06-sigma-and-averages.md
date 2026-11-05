---
type: personal
title: "0.6 Σ Notation and Averages"
source: personal
---

# 0.6 Σ Notation and Averages

*Why this matters for the target passage:* the empirical loss L_T(θ) = (1/m) Σᵢ₌₁ᵐ ℓ[f_θ(xᵢ), yᵢ] is a Σ-average, and you need to read it as a loop over the dataset.

## Half A — Learn

### Read

OpenStax *Calculus* Vol. 1 §5.1, only the "Sigma (Summation) Notation" subsection and its rules (about 15 minutes), plus the key ideas below. Σ is a `for` loop that accumulates a total, so you already know the idea. The reading is for the notation and the algebra rules.

### Key ideas

- **Σᵢ₌₁ᵐ aᵢ** means a₁ + a₂ + … + aₘ. The index i is a **dummy variable**: it exists only inside the sum, like a loop variable, and renaming it changes nothing. Σⱼ₌₁³ j and Σₖ₌₁³ k are the same number.
- **Linearity.** Sums split over addition and let constants out: Σ(c·aᵢ + bᵢ) = c·Σaᵢ + Σbᵢ. This is the main algebra tool for sums.
- An **average** of m numbers is (1/m)·Σ of them. It is the sum divided by how many things you summed.
- In a dataset of pairs, xᵢ and yᵢ **share the index i**: they are the i-th input and its i-th label, a matched pair. A sum like Σ ℓ[f_θ(xᵢ), yᵢ] walks down the dataset one pair at a time.
- So the **empirical loss** is the *average per-example loss over the dataset*: compute the loss on each example, add them up, and divide by m.

### Worked example

Dataset {(1,2), (2,4), (3,7)}, so m = 3, with model f_θ(x) = θx at θ = 2 (so f_θ(x) = 2x) and per-example loss ℓ(z, y) = (z − y)².

**Step 1: model outputs.** f_θ(1) = 2, f_θ(2) = 4, f_θ(3) = 6.

**Step 2: per-example losses**, pairing each output with its own label.

- i = 1: ℓ(2, 2) = (2 − 2)² = 0
- i = 2: ℓ(4, 4) = (4 − 4)² = 0
- i = 3: ℓ(6, 7) = (6 − 7)² = 1

**Step 3: average.** L = (1/3)(0 + 0 + 1) = 1/3.

The one example the model misses by 1 accounts for the whole loss, and dividing by m = 3 spreads it over the dataset.

## Half B — Practice

### Problems

1. Compute Σᵢ₌₁⁴ i² and Σₖ₌₀³ 2ᵏ.
2. Show Σᵢ₌₁ᵐ (3aᵢ + 2) = 3Σᵢ₌₁ᵐ aᵢ + 2m.
3. Write 1 + 3 + 5 + … + 19 in Σ notation.
4. Is Σᵢ aᵢbᵢ = (Σᵢ aᵢ)(Σᵢ bᵢ) in general? Test it with m = 2.
5. For the worked-example data and f_θ(x) = θx, write L(θ) = (1/3)Σ(θxᵢ − yᵢ)² as an explicit polynomial in θ.
6. If every data point is duplicated (each appears twice), what happens to m, to the sum, and to L? Explain.
7. 🐍 Compute L(θ) from problem 5 in two ways: a Python loop, and numpy `np.mean((theta*x - y)**2)`. Confirm they agree, then grid-search θ ∈ [0, 4] for the minimizer.

### Proof thread

Prove problem 2 by writing the sum out term by term and regrouping. Justify each `=`.

### Done when

You can read L_T(θ) = (1/m) Σℓ[f_θ(xᵢ), yᵢ] aloud and compute it for a small dataset by hand.
