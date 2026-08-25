"""Alonso–Muth–Mills land-rent gradient in the linear monocentric city.

A household with income y, commuting cost t per unit distance, lot size
q, and numeraire consumption c faces

    c + R(d) q + t d = y.

Spatial equilibrium equalizes utility at every occupied d. Envelope /
first-order conditions then give the bid-rent gradient

    R'(d) = - t / q(d)  < 0.

This is an equilibrium condition, not an accounting identity and not a
statement that land at larger d is physically inferior. Lot size q(d)
is endogenous in the full AMM model; the gradient formula still holds
at the chosen q(d).
"""

from __future__ import annotations


def rent_gradient(t: float, q: float) -> float:
    if t < 0:
        raise ValueError("commuting cost t must be non-negative")
    if q <= 0:
        raise ValueError("lot size q must be positive")
    return -t / q


def closed_form_linear_rent(r0: float, t: float, q: float, d: float) -> float:
    """Rent when q is fixed (the 'fixed lot size' teaching case)."""
    return r0 + rent_gradient(t, q) * d
