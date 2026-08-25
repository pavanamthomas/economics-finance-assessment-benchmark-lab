"""Binary Glosten–Milgrom (1985) quote identities.

Asset value v ∈ {0, 1} with P(v=1)=π. An informed trader arrives with
probability μ and trades in the direction of v. An uninformed trader
arrives with probability 1-μ and buys or sells with equal probability.
Unit trade size. Competitive specialist, no inventory preference.

    ask = E[v | buy],   bid = E[v | sell].

The quoted spread is then entirely adverse-selection. Inventory risk
is a different model (Ho–Stoll, Avellaneda–Stoikov).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GMParams:
    mu: float
    pi: float = 0.5
    v_low: float = 0.0
    v_high: float = 1.0

    def __post_init__(self) -> None:
        if not 0 < self.mu < 1:
            raise ValueError("mu must be in (0, 1)")
        if not 0 < self.pi < 1:
            raise ValueError("pi must be in (0, 1)")
        if self.v_high <= self.v_low:
            raise ValueError("v_high must exceed v_low")


def quotes(params: GMParams) -> dict[str, float]:
    mu, pi = params.mu, params.pi
    # P(buy | v_high) = μ * 1 + (1-μ) * 1/2
    p_buy_high = mu + (1.0 - mu) * 0.5
    p_buy_low = (1.0 - mu) * 0.5
    p_buy = p_buy_high * pi + p_buy_low * (1.0 - pi)
    p_high_given_buy = p_buy_high * pi / p_buy
    ask = p_high_given_buy * params.v_high + (1.0 - p_high_given_buy) * params.v_low

    p_sell_high = (1.0 - mu) * 0.5
    p_sell_low = mu + (1.0 - mu) * 0.5
    p_sell = p_sell_high * pi + p_sell_low * (1.0 - pi)
    p_high_given_sell = p_sell_high * pi / p_sell
    bid = p_high_given_sell * params.v_high + (1.0 - p_high_given_sell) * params.v_low
    return {
        "ask": ask,
        "bid": bid,
        "spread": ask - bid,
        "p_buy": p_buy,
        "p_sell": p_sell,
        "mid": 0.5 * (ask + bid),
        "unconditional": pi * params.v_high + (1.0 - pi) * params.v_low,
    }
