---
type: personal
title: "0.5 Functions as Maps"
source: personal
---

# 0.5 Functions as Maps

*Why this matters for the target passage:* L_T : Θ → ℝ, f_θ, and ℓ are all functions with types, and reading the passage means knowing what goes into each one and what comes out.

## Half A — Learn

### Read

*Book of Proof* §12.1 Functions and §12.4 Composition (about 30 minutes). Skim §12.2 Injective and Surjective: you don't need the vocabulary yet, but it is worth seeing once. You have used functions for years, so read for the *type* viewpoint: every function comes with a stated domain and codomain, and papers lean on that heavily.

### Key ideas

- A function f : A → B has three parts: a **domain** A (the inputs allowed), a **codomain** B (the set the outputs live in), and a **rule** that assigns to each input exactly one output. "Exactly one" is the whole definition: no input may be left without an output, and no input may get two. Think of it as a Python function with type hints, `def f(a: A) -> B`.
- Inputs can be vectors. A function f : ℝⁿ → ℝ takes a list of n reals and returns one real, for example f(x₁, x₂) = x₁ + 3x₂ is a function ℝ² → ℝ.
- **Composition** chains functions: (g∘f)(x) = g(f(x)). Read it right to left, since f acts first. It only makes sense when the codomain of f fits inside the domain of g.
- A **parameterized family** f_θ is really one function for each choice of θ. The subscript is a setting, not an input. Change θ and you get a different function of x. In code, this is a function that takes `theta` first and `x` second.
- Two kinds of loss. A **per-example loss** ℓ compares one prediction with its label and returns a number: how wrong that one prediction is. The **training objective** L is built from ℓ with the dataset held fixed inside its definition, so *L* takes the *parameters* as input and returns a single number. L is a function of θ, not of the data.

### Worked example

Let θ = (θ₁, θ₂) ∈ ℝ² and define f_θ(x) = θ₁x + θ₂. For each fixed θ this is a line, so f_θ : ℝ → ℝ.

**Evaluate.** Take θ = (2, 1) and x = 3. Then f_(2,1)(3) = 2·3 + 1 = 7.

**Build a loss.** Suppose our whole dataset is the single pair (x, y) = (1, 3). Define

L(θ) = (f_θ(1) − 3)².

The input of L is θ, and the data (1, 3) is baked into the formula. Its type is L : ℝ² → ℝ.

**Two different parameters, same loss.**

- L((2, 1)) = (f_(2,1)(1) − 3)² = (2·1 + 1 − 3)² = (3 − 3)² = 0.
- L((1, 2)) = (f_(1,2)(1) − 3)² = (1·1 + 2 − 3)² = (3 − 3)² = 0.

So two different θ both give zero loss on one data point. That is worth remembering: a loss can have many parameter settings that do equally well, because one data point cannot tell the lines apart.

## Half B — Practice

### Problems

1. Which of these define functions ℝ → ℝ: x ↦ x², x ↦ ±√x, x ↦ 1/x? (Read x ↦ x² as "x maps to x²": it names a function by its rule, like `lambda x: x**2`.) For each one that fails, fix it by changing the domain or the rule.
2. Let f(x) = x + 1 and g(x) = x². Compute (g∘f)(2) and (f∘g)(2). Does order matter?
3. Let f : ℝ² → ℝ be given by f(x,y) = x² + y². Compute f(1,2), and describe the set {(x,y) : f(x,y) = 1}.
4. Let f_θ(x) = θx. Compute f₃(2) and f₋₁(2). What set is θ in, and what is the type of f_θ?
5. With f_θ(x) = θx and data {(1,2),(2,4)}, let L(θ) = ½[(f_θ(1)−2)² + (f_θ(2)−4)²]. Compute L(0), L(1), and L(2). Which θ is best?
6. In the target passage (quoted in full in session 0.8), write the type (A → B) of f_θ, ℓ, and L_T. You may leave Θ, the inputs, and the outputs as named sets.
7. 🐍 Implement `f(theta, x)` and `L(theta)` from problem 5, and plot L(θ) for θ ∈ [−1, 4] with matplotlib.

### Proof thread

Show that composition is associative, h∘(g∘f) = (h∘g)∘f, by evaluating both sides at an arbitrary x.

### Done when

You can state the domain and codomain of every function in the target passage.
