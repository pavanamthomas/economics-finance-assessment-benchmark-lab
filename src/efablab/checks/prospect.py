"""Tiny prospect-theory evaluation used by one behavioral item.

Tversky–Kahneman (1992) value function on certain outcomes, with a
reference of 0:

    v(x) = x^α           if x ≥ 0
    v(x) = -λ (-x)^β     if x < 0

This is not a full CPT calculator. Probability weighting is a separate
object (π(p)). Tests check the kink (loss aversion λ > 1) and that
mixing up λ with α reverses a comparison that the item relies on.
"""

from __future__ import annotations


def tk_value(x: float, alpha: float = 0.88, beta: float = 0.88, lam: float = 2.25) -> float:
    if x >= 0:
        return x**alpha
    return -lam * ((-x) ** beta)
