---
type: personal
title: "0.7 Exponentials and Logarithms"
source: personal
---

# 0.7 Exponentials and Logarithms

*Why this matters for the target passage:* the target paper's loss options include softmax cross-entropy, which is built from eˣ and ln, and it is one of the two student losses L_S (softmax cross-entropy or squared error) that the passage allows.

## Half A — Learn

### Read

OpenStax *Calculus* Vol. 1 §1.5 Exponential and Logarithmic Functions (about 30 minutes). You met logs in precalc, so read to refresh the rules and to get comfortable with the number e ≈ 2.718 and the natural log ln.

### Key ideas

- **eˣ is always positive and always increasing.** It never touches zero and never turns around. That makes it a handy way to force any real number into a positive one.
- **ln is the inverse of eˣ**: ln(eˣ) = x and e^(ln x) = x for x > 0. Its domain is only the positive reals.
- **Log rules.** ln(ab) = ln a + ln b and ln(aᵏ) = k·ln a. For instance ln 6 = ln 2 + ln 3, because 6 = 2·3. Logs turn products into sums, which is why they show up in likelihoods and losses.
- **Signs of ln.** ln 1 = 0, and ln x < 0 for 0 < x < 1. So for a probability p, the quantity −ln p is never negative.
- **Softmax** turns any list of real scores z = (z₁, …, zₖ) into probabilities: pᵢ = e^(zᵢ) / Σⱼ e^(zⱼ). Each e^(zᵢ) is positive, and dividing by the total makes the pᵢ add up to 1. Bigger scores get bigger probabilities.
- **Cross-entropy loss** for a true class y is −ln p_y. It is small when the correct class gets a high probability and large when it gets a low probability.

### Worked example

Scores z = (2, 1, 0) for three classes.

**Step 1: exponentiate.** e² ≈ 7.389, e¹ ≈ 2.718, e⁰ = 1.

**Step 2: sum.** 7.389 + 2.718 + 1 ≈ 11.107.

**Step 3: divide.** p ≈ (7.389/11.107, 2.718/11.107, 1/11.107) ≈ (0.665, 0.245, 0.090). These add to 1.000, as they must.

**Cross-entropy.**

- If the true class is 1, the loss is −ln 0.665 ≈ 0.408. The model gave the right class the largest probability, so the loss is small.
- If the true class is 3, the loss is −ln 0.090 ≈ 2.408. The model gave the right class a small probability, so the loss is large.

Same model output, two different losses: the loss depends on which class turned out to be correct.

## Half B — Practice

### Problems

1. Simplify ln(e³), e^(ln 5), and ln(1/e²).
2. Solve e^(2x) = 7 for x.
3. Derive ln(a/b) = ln a − ln b from the product rule for logs.
4. Compute softmax(0,0,0) and softmax(1,1,1). Then show that adding the same constant c to every zᵢ never changes the softmax.
5. Compute −ln p for p ∈ {0.9, 0.5, 0.1, 0.01} and describe the pattern.
6. 🐍 Implement `softmax(z)` in numpy and check that it sums to 1. Show that the naive version overflows on z = (1000, 1001), then fix it by subtracting max(z) first (that's why problem 4 matters).

### Proof thread

Write out the algebra for problem 4's shift invariance: e^(z+c) = e^z·e^c, then factor and cancel. Justify each step.

### Done when

You can compute softmax and cross-entropy for a 3-class example by hand.
