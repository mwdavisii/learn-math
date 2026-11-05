---
type: personal
title: "0.4 Quantifiers and Negation"
source: personal
---

# 0.4 Quantifiers and Negation

*Why this matters for the target passage:* "for all ε > 0" and "for sufficiently small ε > 0" are quantifier statements, and you need to be able to unpack and negate them.

## Half A — Learn

### Read

*Book of Proof* §2.7 Quantifiers, §2.9 Translating English to Symbolic Logic, §2.10 Negating Statements (about 30 minutes). This is the densest session in the tier, so take it slowly and say each symbolic statement aloud.

### Key ideas

- ∀ means "for all" and ∃ means "there exists". Together with a variable and a set, they turn an open sentence like "x + 1 > x" into a statement: ∀x ∈ ℝ, x + 1 > x.
- **Order matters.** "Everyone has someone they trust" is ∀p ∃q Trusts(p, q). "There is someone everyone trusts" is ∃q ∀p Trusts(p, q). Same words, different claims: the first can be true while the second is false.
- **Negation swaps the quantifier and negates the inside.** ¬(∀x P(x)) ≡ ∃x ¬P(x), and ¬(∃x P(x)) ≡ ∀x ¬P(x). The negation of an implication is ¬(P ⇒ Q) ≡ P ∧ ¬Q (from session 3: P ⇒ Q is ¬P ∨ Q).
- "For all ε > 0" means ∀ε ∈ (0, ∞).
- "For sufficiently small ε > 0, P(ε)" means: ∃δ > 0 such that ∀ε ∈ (0, δ), P(ε). In words: there is some window (0, δ) so that P holds everywhere inside the window. You may need the window to be tiny, but it must exist.

### Worked example

**Translate.** Take the statement "for sufficiently small ε > 0, L(θ^ε) < L(θ⁰)" (the superscripts here are labels, not exponents — session 0.8 explains). Following the key idea above, it becomes

∃δ > 0 ∀ε (0 < ε < δ ⇒ L(θ^ε) < L(θ⁰)).

**Negate, one step at a time.** Write P(ε) for "L(θ^ε) < L(θ⁰)", so the statement is ∃δ > 0 ∀ε (0 < ε < δ ⇒ P(ε)).

1. Negating the outer ∃δ > 0 turns it into ∀δ > 0, and we now negate what follows: ∀δ > 0 ¬[∀ε (0 < ε < δ ⇒ P(ε))].
2. Negating the ∀ε turns it into ∃ε, and we negate what follows: ∀δ > 0 ∃ε ¬(0 < ε < δ ⇒ P(ε)).
3. Negate the implication using ¬(X ⇒ Y) ≡ X ∧ ¬Y: ∀δ > 0 ∃ε (0 < ε < δ ∧ ¬P(ε)).
4. The negation of "L(θ^ε) < L(θ⁰)" is "L(θ^ε) ≥ L(θ⁰)", so the final result is

∀δ > 0 ∃ε (0 < ε < δ ∧ L(θ^ε) ≥ L(θ⁰)).

**Read it in English.** "However small a window (0, δ) you pick, some ε inside it fails." This is the opposite of "for sufficiently small ε the loss drops". It says no window of safe ε values exists.

## Half B — Practice

### Problems

1. Translate into symbols: "every real number is less than some integer."
2. Swap the quantifier order in problem 1, then translate back into English. Is it still true?
3. Negate ∀x ∈ ℝ, x² ≥ 0. Is the negation true?
4. Negate ∃δ > 0 ∀ε ∈ (0,δ), ε² < ε. Which is true, the original or the negation?
5. Let g(ε) be the dot product in Theorem 1 (a number depending on ε). Write "g(ε) = 0 for all ε > 0" in symbols, and also write its negation.
6. Is "for sufficiently small ε > 0, ε < 0.001" true? Give a δ that works.
7. 🐍 Let f(ε) = ε − 10ε². By sampling ε values in Python, estimate how small ε must be for f(ε) > 0. Then find the exact δ with algebra.

### Proof thread

Explain in your own words why, when proving "∃δ ∀ε…", *you* get to choose δ, but then you must handle *every* ε in (0,δ). Use problem 7 as the example.

### Done when

You can translate and negate quantified statements, especially "for sufficiently small ε."
