---
type: personal
title: "0.3 Statements and If-Then"
source: personal
---

# 0.3 Statements and If-Then

*Why this matters for the target passage:* Theorem 1 has the shape "If H, then (A or B)", and you need to know exactly what that claims.

## Half A — Learn

### Read

*Book of Proof* §2.1 Statements, §2.2 And, Or, Not, §2.3 Conditional Statements, §2.4 Biconditional Statements, §2.5 Truth Tables for Statements, §2.6 Logical Equivalence (about 40 minutes). Truth tables are mechanical, so do the book's small examples by hand once. That is enough.

### Key ideas

- A **statement** is a sentence that is definitely true or definitely false. "x > 3" is not a statement until x is given a value or is quantified (session 4).
- The connectives: P ∧ Q (and), P ∨ Q (or), ¬P (not). Mathematical "or" is **inclusive**: P ∨ Q is true when P is true, when Q is true, or when both are. "Either A or B" means the same thing unless the author says "but not both".
- P ⇒ Q ("if P then Q") is false in exactly one case: P true and Q false. When P is false, the implication is true automatically ("vacuously").
- The **converse** of P ⇒ Q is Q ⇒ P, which is a different statement. The **contrapositive** ¬Q ⇒ ¬P is equivalent to the original, so they are true or false together.
- P ⇔ Q ("P if and only if Q") means P ⇒ Q and Q ⇒ P together. Two statements that always have the same truth value are called **equivalent**, written ≡.

### Worked example

**Claim:** P ⇒ Q ≡ ¬P ∨ Q.

Build a truth table with one row for each combination of truth values of P and Q (T = true, F = false).

| P | Q | P ⇒ Q | ¬P | ¬P ∨ Q |
|---|---|-------|----|--------|
| T | T | T     | F  | T      |
| T | F | F     | F  | F      |
| F | T | T     | T  | T      |
| F | F | T     | T  | T      |

How each entry was filled in:

- P ⇒ Q column: false only in row 2 (P true, Q false), true in the other three rows.
- ¬P column: the opposite of P in each row: F, F, T, T.
- ¬P ∨ Q column: true when ¬P is true or Q is true. Row 1: F or T gives T. Row 2: F or F gives F. Row 3: T or T gives T. Row 4: T or F gives T.

The P ⇒ Q column (T, F, T, T) and the ¬P ∨ Q column (T, F, T, T) match in every row, so P ⇒ Q ≡ ¬P ∨ Q.

**Theorem 1's skeleton.** Name the pieces of the theorem:

- H = "θ⁰_S = θ⁰_T" (the student and teacher start from the same initialization; the superscripts here are labels, not exponents — session 0.8 explains)
- A = "Δθ^ε_S · Δθ_T = 0 for all ε > 0" (the dot product is zero no matter what ε is)
- B = "for sufficiently small ε > 0, L_T(θ^ε_S) < L_T(θ⁰_S)" (for small ε the teacher loss of the student drops)

The theorem says H ⇒ (A ∨ B). You don't need to know what any of the symbols compute yet to see the logical shape.

## Half B — Practice

### Problems

1. Make the truth table for P ∧ ¬Q.
2. "If it rains, the ground is wet." Write the converse and the contrapositive. Which one is equivalent to the original?
3. Is "If 2 > 3, then 5 = 7" true? Explain.
4. Use a truth table to show (P ⇒ Q) ≡ (¬Q ⇒ ¬P).
5. Use a truth table to show (P ∨ Q) ≡ (¬P ⇒ Q). Explain in one sentence why this means you can prove "A or B" by assuming A is false and deducing B.
6. 🐍 Write `truth_table(expr)`, where `expr` is a Python function of `(P, Q)` returning a bool. It should print all 4 rows. Use it to check problems 4 and 5.

### Proof thread

Using problem 5, rewrite H ⇒ (A ∨ B) as (H ∧ ¬A) ⇒ B. Say in words what a proof of Theorem 1 would have to assume and what it would have to show. Hint: the step from H ⇒ (¬A ⇒ B) to (H ∧ ¬A) ⇒ B is itself an equivalence you can check with a three-variable truth table.

### Done when

You can turn any "either…or" claim into an if-then.
