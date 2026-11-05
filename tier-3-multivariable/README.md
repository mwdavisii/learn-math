---
type: personal
title: "Tier 3: Multivariable Calculus"
source: personal
---

# Tier 3: Multivariable Calculus

## Goal

Partial derivatives, gradients, and the multivariate chain rule, enough to read ∇_θ L and backprop.

**Status**: Skeleton. Sessions are written when you're ~2 sessions from finishing the previous tier.

## Reading

- Deisenroth, Faisal, Ong, *Mathematics for Machine Learning* (MML), ch. 5 and §7.1.
- 3Blue1Brown, *Neural Networks* (video series, backprop videos, cited by video title).

If a section number doesn't match your copy, find it by title.

## Sessions

1. Partial derivatives — MML §5.2
2. The gradient as a vector — MML §5.2
3. Directional derivatives and steepest descent — MML §5.2 + session notes
4. Gradients of vector-valued functions (Jacobians) — MML §5.3
5. The multivariate chain rule — MML §5.2.2
6. Backpropagation — MML §5.6; 3B1B "What is backpropagation really doing?", "Backpropagation calculus"
7. Linearization and multivariate Taylor — MML §5.8
8. Gradient descent in ℝⁿ — MML §7.1

## Checkpoint

MML §5.6. By hand, compute the gradient of a 2-input, 2-hidden-unit, 1-output network's squared-error loss, then verify it in numpy with finite differences.

Pass: gradients agree to 1e-6 and the hand derivation is checked by Claude.
