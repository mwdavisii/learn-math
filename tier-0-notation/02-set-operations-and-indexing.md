---
type: personal
title: "0.2 Subsets, Set Operations, and Indexed Sets"
source: personal
---

# 0.2 Subsets, Set Operations, and Indexed Sets

*Why this matters for the target passage:* datasets are indexed collections, and the index notation you meet here returns in Σ.

## Half A — Learn

### Read

*Book of Proof* §1.3 Subsets, §1.5 Union, Intersection, Difference, §1.6 Complement, §1.8 Indexed Sets (about 30 minutes). The indexed sets section is the one to slow down on. The rest will feel familiar.

### Key ideas

- A ⊆ B means every element of A is also in B. The empty set ∅ has no elements.
- The basic operations: A ∪ B (in A or B or both), A ∩ B (in both), and A − B (in A but not in B).
- The **complement** of A is taken relative to a universal set U: it is U − A, everything in U that is not in A. Without a U, "complement" has no meaning.
- An **indexed family** A₁, …, Aₙ is a list of sets labeled by an index. Then ⋃ᵢ₌₁ⁿ Aᵢ is everything that is in at least one Aᵢ, and ⋂ᵢ₌₁ⁿ Aᵢ is everything that is in all of them.
- A dataset D = {(x₁,y₁), …, (x_m,y_m)} is an indexed collection of input-output pairs, with index i running from 1 to m. Writing xᵢ means "the input of the i-th example". Datasets are written with set braces, but they are really indexed lists: order matters for the indexing, and repeated pairs are allowed.

### Worked example

**(a)** Let A = {1, 2, 3, 4} and B = {3, 4, 5}.

- A ∪ B: collect everything in either set, listing each element once: {1, 2, 3, 4, 5}.
- A ∩ B: elements in both. 3 and 4 appear in each, while 1 and 2 are not in B and 5 is not in A. So A ∩ B = {3, 4}.
- A − B: elements of A that are not in B. Remove 3 and 4 from A, leaving {1, 2}.
- B − A: elements of B that are not in A. Remove 3 and 4 from B, leaving {5}.

Note that A − B ≠ B − A, so difference is not symmetric.

**(b)** Let Aᵢ = [0, 1/i] for i = 1, 2, 3. Write out the three sets:

- A₁ = [0, 1/1] = [0, 1]
- A₂ = [0, 1/2]
- A₃ = [0, 1/3]

These are nested: A₃ ⊆ A₂ ⊆ A₁, because 1/3 < 1/2 < 1.

*Union.* A point is in the union if it lies in at least one Aᵢ. Since every Aᵢ sits inside A₁, nothing outside A₁ can be in the union, and A₁ itself is part of the union. So ⋃ᵢ₌₁³ Aᵢ = A₁ = [0, 1].

*Intersection.* A point is in the intersection if it lies in all three sets. Since every set contains the next smaller one, a point lying in A₃ automatically lies in A₂ and A₁. So ⋂ᵢ₌₁³ Aᵢ = A₃ = [0, 1/3].

## Half B — Practice

### Problems

1. Is ∅ ⊆ A for every set A? Explain in one sentence.
2. A = [0,2], B = (1,3). Find A ∪ B, A ∩ B, A − B.
3. Aᵢ = {i, i+1}. Find ⋃ᵢ₌₁⁴ Aᵢ and ⋂ᵢ₌₁⁴ Aᵢ.
4. Aᵢ = (−1/i, 1/i) for i ∈ ℕ. What is ⋂ᵢ₌₁^∞ Aᵢ? Justify it. (This is your first "as small as you like" argument.)
5. The dataset {(1,2),(2,4),(3,7)} is written D = {(x₁,y₁),…,(x_m,y_m)}. What are m, x₂, and y₃?
6. 🐍 With U = set(range(10)), A = {0,2,4,6}, B = {4,5,6,7}, check De Morgan's law U − (A ∪ B) = (U − A) ∩ (U − B) in Python. Then try a few random A, B.

### Proof thread

Show A ∩ B ⊆ A by starting with "Let x ∈ A ∩ B. Then…". This "take an arbitrary element" move is the basic step in set proofs.

### Done when

You can compute indexed unions and intersections and name dataset pieces by index.
