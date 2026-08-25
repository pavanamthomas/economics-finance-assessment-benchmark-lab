"""One-shot Kyle (1985) linear-normal identities.

v ~ N(p0, Σ0), noise u ~ N(0, σ_u²) independent of v. The insider
observes v and submits x = β (v - p0). The market maker observes
y = x + u and sets p = p0 + λ y. In the unique linear equilibrium,

    λ = σ_v / (2 σ_u),    β = σ_u / σ_v,

where σ_v = sqrt(Σ0). The insider's expected profit is
E[π | v] = (v-p0)² / (4 λ) * (something wait)

Actually E[x (v-p) | v] = β(v-p0) * (v - p0 - λ β (v-p0)) because
E[u|v]=0, so p - p0 = λ(x+u) and E[p|v] = p0 + λ β (v-p0).
With β = 1/(2λ), E[p|v] = p0 + (v-p0)/2, so half the information
is in the price, and expected profit is (v-p0)² / (4λ) * λ? Let's
compute: x = (v-p0)/(2λ), E[v-p|v] = (v-p0)/2, profit = x * E[v-p|v]
= (v-p0)² / (4λ).

These identities are the teaching one-shot model, not Kyle's
continuous-auction paper in full.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KyleParams:
    sigma_v: float
    sigma_u: float
    p0: float = 0.0

    def __post_init__(self) -> None:
        if self.sigma_v <= 0 or self.sigma_u <= 0:
            raise ValueError("volatilities must be positive")


def lambda_star(params: KyleParams) -> float:
    return params.sigma_v / (2.0 * params.sigma_u)


def beta_star(params: KyleParams) -> float:
    return params.sigma_u / params.sigma_v


def insider_expected_profit(params: KyleParams, v: float) -> float:
    lam = lambda_star(params)
    return (v - params.p0) ** 2 / (4.0 * lam)


def price_impact_of_order(params: KyleParams, y: float) -> float:
    """Equilibrium price move λ y. This is not a profit forecast."""
    return lambda_star(params) * y
