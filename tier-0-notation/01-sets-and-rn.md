---
type: personal
title: "0.1 Sets, Number Systems, and ℝⁿ"
source: personal
---

# 0.1 Sets, Number Systems, and ℝⁿ

*Why this matters for the target passage:* θ ∈ ℝⁿ and D = {…} are sets, and the passage cannot be read until those two pieces of notation feel natural.

## Half A — Learn

### Read

*Book of Proof* §1.1 Introduction to Sets, §1.2 The Cartesian Product, §1.9 Sets That Are Number Systems (about 25 minutes). You already know the basics of sets, so read for the notation: how mathematicians write membership, how they describe a set by a rule, and how they build bigger sets from smaller ones.

### Key ideas

- A **set** is a collection of things, with no order and no repeats. We write x ∈ A for "x is an element of A" and x ∉ A for "x is not an element of A". For a finite set, |A| is the number of elements in A.
- **Set-builder notation** describes a set by a rule. {x ∈ ℝ : x > 0} reads "the set of all real numbers x such that x is greater than 0". The colon (or a vertical bar) means "such that".
- The number systems nest: ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ (naturals, integers, rationals, reals). **Interval notation** is shorthand for sets of reals: (0,1] means {x ∈ ℝ : 0 < x ≤ 1}, where a round bracket excludes the endpoint and a square bracket includes it.
- The **Cartesian product** A × B is the set of all ordered pairs (a, b) with a ∈ A and b ∈ B. Order matters: (1,2) and (2,1) are different pairs.
- ℝⁿ is the set of n-tuples (x₁, …, xₙ) of real numbers. So when a paper says a model's parameters satisfy θ ∈ ℝⁿ, it means θ is just a list of n real numbers, much like a Python list of n floats.

### Worked example

**(a)** Let L = {(x, y) ∈ ℝ² : y = 2x + 1}.

*In words:* L is the set of all points in the plane whose y-coordinate equals twice the x-coordinate plus one. That is the line with slope 2 and y-intercept 1.

*Membership tests.* To test whether a point is in L, substitute and check the rule.

- Is (1, 3) ∈ L? Here x = 1 and y = 3. Compute 2x + 1 = 2·1 + 1 = 3. Since y = 3, the rule holds, so (1, 3) ∈ L.
- Is (2, 4) ∈ L? Here x = 2 and y = 4. Compute 2x + 1 = 2·2 + 1 = 5. Since 4 ≠ 5, the rule fails, so (2, 4) ∉ L.

**(b)** List {0, 1} × {a, b, c}.

Take each element of {0, 1} in turn and pair it with each element of {a, b, c}:

- with 0: (0, a), (0, b), (0, c)
- with 1: (1, a), (1, b), (1, c)

So {0, 1} × {a, b, c} = {(0,a), (0,b), (0,c), (1,a), (1,b), (1,c)}. That is 6 pairs, and 2·3 = 6: two choices for the first slot times three choices for the second.

## Half B — Practice

### Problems

1. Write in set-builder notation: the positive even integers.
2. True or false, with a reason: −3 ∈ ℕ; √2 ∈ ℚ; π ∈ ℝ; 0.5 ∈ ℤ.
3. List every element of {0,1}² and of {0,1}³. How many elements does {0,1}ⁿ have?
4. Write {x ∈ ℝ : x² < 4} in interval notation.
5. A model has 3 weights and 1 bias. In what set does its parameter vector θ live? Write one example θ.
6. 🐍 Use Python `set`s and `itertools.product` to build {0,1}³. Check its size, then write a function `size(n)` that returns |{0,1}ⁿ| for n = 1…10.

### Proof thread

For finite sets, |A × B| = |A|·|B|. In 2–3 sentences, explain why. (Hint: picture a table with a row for each element of A and a column for each element of B.)

### Done when

You can read "θ ∈ ℝⁿ" and "{x ∈ ℝ : x > 0}" aloud in plain English, and problems 1–5 have been checked.
