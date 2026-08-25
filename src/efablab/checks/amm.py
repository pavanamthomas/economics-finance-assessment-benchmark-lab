"""Constant-product AMM identities used to audit tokenomics items.

Notation. Reserves (x, y) of tokens X and Y satisfy x y = k. The
marginal (spot) price of X in units of Y is p = y/x. A fee-free trade
that sells Δx > 0 of X into the pool moves reserves to
x' = x + Δx and y' = k / x', and pays the trader Δy = y - y' of Y.

The average execution price of that sale is Δy/Δx = y / (x + Δx).
That object is not p and is not the post-trade spot p' = y'/x'.
It equals the geometric mean of p and p'.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class AmmTrade:
    x0: float
    y0: float
    dx: float
    fee: float = 0.0

    def __post_init__(self) -> None:
        if self.x0 <= 0 or self.y0 <= 0:
            raise ValueError("reserves must be positive")
        if self.dx <= 0:
            raise ValueError("dx must be a positive sale of X into the pool")
        if not 0 <= self.fee < 1:
            raise ValueError("fee must be in [0, 1)")


def k(x: float, y: float) -> float:
    return x * y


def spot_price(x: float, y: float) -> float:
    """Marginal price of X in units of Y."""
    return y / x


def sell_x(trade: AmmTrade) -> dict[str, float]:
    """Execute a sale of dx units of X. Fee is taken on the inbound asset."""
    x0, y0, dx, fee = trade.x0, trade.y0, trade.dx, trade.fee
    k0 = k(x0, y0)
    dx_effective = dx * (1.0 - fee)
    x1 = x0 + dx_effective
    y1 = k0 / x1
    dy = y0 - y1
    # Fee remains in the pool as extra X if fee > 0; x_reported includes it.
    x_final = x0 + dx
    y_final = y1
    k_final = x_final * y_final
    return {
        "x1": x_final,
        "y1": y_final,
        "dy": dy,
        "k0": k0,
        "k1": k_final,
        "spot0": spot_price(x0, y0),
        "spot1": spot_price(x_final, y_final),
        "avg_execution": dy / dx,
        "geom_mean_spot": float(np.sqrt(spot_price(x0, y0) * spot_price(x_final, y_final)))
        if fee == 0.0
        else float("nan"),
    }


def average_execution_closed_form(x: float, y: float, dx: float) -> float:
    """Fee-free average sale price of X in units of Y: y / (x + dx)."""
    if x <= 0 or y <= 0 or dx <= 0:
        raise ValueError("reserves and dx must be positive")
    return y / (x + dx)


def average_execution_by_quadrature(x: float, y: float, dx: float, n: int = 20_000) -> float:
    """Independent check: integrate the spot price along the reserve path.

    Along a fee-free constant-product path, p(s) = k / s^2 for s in [x, x+dx].
    The average execution price is (1/dx) ∫_x^{x+dx} p(s) ds.
    """
    k0 = x * y
    s = np.linspace(x, x + dx, n)
    p = k0 / s**2
    area = np.trapezoid(p, s) if hasattr(np, "trapezoid") else np.trapz(p, s)
    return float(area / dx)


def geometric_mean_spots(x: float, y: float, dx: float) -> float:
    x1 = x + dx
    y1 = (x * y) / x1
    return float(np.sqrt(spot_price(x, y) * spot_price(x1, y1)))


def impermanent_loss(price_ratio: float) -> float:
    """LP value relative to holding the original inventory, fees excluded.

    If the external price of X in Y moves from p0 to p1 = r p0, and the
    pool is kept at the constant-product spot, IL(r) = 2 sqrt(r)/(1+r) - 1.
    IL(1) = 0. IL(r) = IL(1/r). IL(r) → -1 as r → 0 or r → ∞.
    """
    if price_ratio <= 0:
        raise ValueError("price_ratio must be positive")
    r = price_ratio
    return float(2.0 * np.sqrt(r) / (1.0 + r) - 1.0)


def hold_vs_lp_values(x0: float, y0: float, r: float) -> dict[str, float]:
    """Value everything in Y after a relative price move r = p1/p0.

    Initial spot p0 = y0/x0. After arbitrage restores the pool to p1 = r p0,
    reserves satisfy y1/x1 = p1 and x1 y1 = x0 y0.
    """
    p0 = spot_price(x0, y0)
    p1 = r * p0
    k0 = k(x0, y0)
    x1 = np.sqrt(k0 / p1)
    y1 = np.sqrt(k0 * p1)
    lp_value = x1 * p1 + y1
    hold_value = x0 * p1 + y0
    return {
        "p0": p0,
        "p1": p1,
        "x1": float(x1),
        "y1": float(y1),
        "lp_value": float(lp_value),
        "hold_value": float(hold_value),
        "il_from_values": float(lp_value / hold_value - 1.0),
        "il_closed_form": float(impermanent_loss(r)),
    }
