---
type: personal
title: "0.8 Reading Mathematical Writing"
source: personal
---

# 0.8 Reading Mathematical Writing

*Why this matters for the target passage:* this session turns the passage from noise into a list of known and parked symbols, so that nothing in it is just a squiggle anymore.

## Half A — Learn

### Read

No book this time. Read the key ideas below, then read the target passage slowly, twice (about 25 minutes). On the first pass, just let your eyes move over it and circle every symbol you cannot yet name. On the second, say each symbol aloud.

> More formally, given student and teacher initializations θ⁰_S and θ⁰_T, and any differentiable loss function L_T : Θ → ℝ, we consider a teacher obtained via a single step of gradient descent on L_T. In our experiments, L_T is the empirical loss on some dataset D_T = {(x₁, y₁), …, (x_m, y_m)}. I.e., L_T(θ) = (1/m) Σᵢ₌₁ᵐ ℓ[f_θ(xᵢ), yᵢ] for some loss function ℓ. For some learning rate ε > 0, the teacher's parameters are θ^ε_T := θ⁰_T + εΔθ_T, where Δθ_T := −∇_θ L_T(θ⁰). Using this teacher, and given samples x ∼ D_S from the training distribution, we produce labels y^ε_x = f_{θ^ε_T}(x). We obtain the student via a single step of gradient descent on this data distribution with learning rate α > 0 and loss L_S(z, y) either softmax cross-entropy or squared error. The student's parameters are θ^ε_S := θ⁰_S + αΔθ^ε_S, where Δθ^ε_S := −∇_θ 𝔼_{x∼D_S}[L_S(f_{θ⁰}(x), y^ε_x)]. Then:
>
> **Theorem 1.** If θ⁰_S = θ⁰_T, then either Δθ^ε_S · Δθ_T = 0 for all ε > 0, or for sufficiently small ε > 0, L_T(θ^ε_S) < L_T(θ⁰_S).

### Key ideas

- **`:=` means "is defined as".** In θ^ε_T := θ⁰_T + εΔθ_T, the author is introducing a name, not asserting a fact you must check. It is like an assignment statement, `theta_eps_T = ...`.
- **Superscripts are often labels, not powers.** In ML papers, a superscript on a parameter or variable is usually a label — an index or a name — not an exponent; you tell by context. For example, x⁽ⁱ⁾ means "the i-th example" and W⁽ᵏ⁾ means "the weights of layer k". They are names, like `x[i]` or `weights[layer]` in code. A superscript on a letter that is clearly a vector or a parameter is almost never an exponent.
- **Subscripts are either names or indices.** θ_S and θ_T are *names*: S for student, T for teacher. xᵢ is an *index*: the i-th item in a list. A symbol can carry both, like θ⁰_S, which reads "the initial parameters of the student". With no subscript, θ⁰ is the shared starting point, the one used when θ⁰_S = θ⁰_T.
- **The Greek roster.** θ (theta) is the parameters; ε (epsilon) and α (alpha) are small positive step sizes; ℓ (script ell) is the per-example loss; Δ (capital delta) means "change in", so Δθ is a change to θ.
- **Distribution notation.** x ∼ D means "x is drawn from the distribution D". You will see it again in the probability tier.
- **Named and parked.** Some symbols you cannot compute with yet: ∇ (gradient), 𝔼 (expectation), and the dot · between vectors. That is fine. Give each a name, say what *kind* of object it produces, and note which tier teaches it. You can read the structure of a sentence without evaluating every piece.

### Worked example

Annotate the passage's first sentence as a table. The columns are the format we will reuse at the checkpoint.

| Symbol | Read aloud | Type/meaning | Session learned |
|---|---|---|---|
| θ⁰_S | "theta-zero sub S" | the student's initial parameters, an element of Θ | 0.8 |
| θ⁰_T | "theta-zero sub T" | the teacher's initial parameters, an element of Θ | 0.8 |
| L_T | "L sub T" | the teacher's loss, a function Θ → ℝ | 0.5 |
| Θ | "capital theta" | the set of all parameter vectors; think ℝⁿ | 0.5 |
| ℝ | "the reals" | the set of real numbers, the codomain of L_T | 0.1 |

Notice what the table does. "Student" and "teacher" are just two labels on the same kind of object. The type of L_T tells you that feeding it parameters gives back one number, so an expression like L_T(θ⁰) is a number, and the symbols still waiting for you (∇, ·, 𝔼) sit on top of things you already understand.

## Half B — Practice

### Problems

1. In θ^ε_T := θ⁰_T + εΔθ_T, which superscripts are labels and which (if any) are exponents? How can you tell?
2. Say "x ∼ D_S" in a plain-English sentence.
3. "For some learning rate ε > 0" versus "for all ε > 0" later on: in each phrase, is ε fixed or ranging over values?
4. Rewrite θ^ε_S := θ⁰_S + αΔθ^ε_S entirely in words.
5. Given θ⁰ = (1, 2), Δθ = (−0.5, 0.25), and ε = 0.1, compute θ^ε = θ⁰ + εΔθ component by component.
6. 🐍 Do problem 5 with numpy arrays. Then loop over ε ∈ {0.01, 0.1, 0.5, 1}, plot the points θ^ε in the plane, and describe the shape they make.

### Proof thread

State Theorem 1's hypothesis and its two possible conclusions in your own words. Which conclusion uses "for sufficiently small ε"? Write that one in ∃δ∀ε form (from 0.4).

### Done when

You can say what kind of thing every symbol in the passage is, even before knowing what ∇ computes.
