"""Closed-form identities used by the numerical items."""

from __future__ import annotations

import pytest

from efablab.checks.accounting import BankBook, aave_health_factor, mark_securities
from efablab.checks.amm import (
    AmmTrade,
    average_execution_by_quadrature,
    average_execution_closed_form,
    geometric_mean_spots,
    hold_vs_lp_values,
    impermanent_loss,
    sell_x,
    spot_price,
)
from efablab.checks.bid_rent import rent_gradient
from efablab.checks.glosten_milgrom import GMParams, quotes
from efablab.checks.kyle import KyleParams, beta_star, insider_expected_profit, lambda_star
from efablab.checks.prospect import tk_value


def test_amm_three_routes_agree() -> None:
    x, y, dx = 100.0, 100.0, 10.0
    closed = average_execution_closed_form(x, y, dx)
    quad = average_execution_by_quadrature(x, y, dx)
    geom = geometric_mean_spots(x, y, dx)
    sim = sell_x(AmmTrade(x, y, dx))
    assert closed == pytest.approx(10.0 / 11.0)
    assert quad == pytest.approx(closed, rel=1e-5)
    assert geom == pytest.approx(closed)
    assert sim["avg_execution"] == pytest.approx(closed)
    assert sim["k0"] == pytest.approx(sim["x1"] * sim["y1"])
    assert sim["spot0"] == pytest.approx(1.0)
    assert sim["spot1"] == pytest.approx(100.0 / 121.0)
    assert closed < sim["spot0"]
    assert closed > sim["spot1"]


def test_amm_k_preserved_fee_free() -> None:
    out = sell_x(AmmTrade(200.0, 100.0, 50.0))
    assert out["k0"] == pytest.approx(out["k1"])
    assert out["avg_execution"] == pytest.approx(0.4)
    assert spot_price(200.0, 100.0) == pytest.approx(0.5)


def test_impermanent_loss_invariants() -> None:
    assert impermanent_loss(1.0) == pytest.approx(0.0)
    assert impermanent_loss(4.0) == pytest.approx(-0.2)
    assert impermanent_loss(4.0) == pytest.approx(impermanent_loss(0.25))
    assert impermanent_loss(1e6) < -0.99
    via = hold_vs_lp_values(100.0, 100.0, 4.0)
    assert via["il_from_values"] == pytest.approx(via["il_closed_form"])
    assert via["il_closed_form"] == pytest.approx(-0.2)


def test_kyle_foc_and_projection() -> None:
    p = KyleParams(sigma_v=2.0, sigma_u=4.0)
    lam = lambda_star(p)
    beta = beta_star(p)
    assert lam == pytest.approx(0.25)
    assert beta == pytest.approx(2.0)
    assert beta == pytest.approx(1.0 / (2.0 * lam))
    # doubling both vols leaves λ unchanged
    p2 = KyleParams(sigma_v=4.0, sigma_u=8.0)
    assert lambda_star(p2) == pytest.approx(lam)
    # insider FOC profit at v = p0 + 1
    assert insider_expected_profit(p, v=1.0) == pytest.approx(1.0 / (4.0 * lam))


def test_glosten_spread_and_boundaries() -> None:
    q = quotes(GMParams(mu=0.2, pi=0.5))
    assert q["ask"] == pytest.approx(0.6)
    assert q["bid"] == pytest.approx(0.4)
    assert q["spread"] == pytest.approx(0.2)
    tiny = quotes(GMParams(mu=1e-6, pi=0.5))
    assert tiny["spread"] == pytest.approx(0.0, abs=1e-5)
    sure = quotes(GMParams(mu=0.999, pi=0.5))
    assert sure["ask"] == pytest.approx(1.0, abs=1e-3)
    assert sure["bid"] == pytest.approx(0.0, abs=1e-3)


def test_health_factor_and_ltv_equivalence() -> None:
    hf = aave_health_factor(150.0, 100.0, 0.8)
    assert hf == pytest.approx(1.2)
    # liquidatable iff LTV > LT
    ltv = 100.0 / 150.0
    assert ltv < 0.8
    assert aave_health_factor(100.0, 100.0, 0.8) < 1.0


def test_rent_gradient_sign_and_units() -> None:
    assert rent_gradient(2.0, 0.5) == pytest.approx(-4.0)
    assert rent_gradient(0.0, 1.0) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        rent_gradient(1.0, 0.0)


def test_bank_book_identity_after_mark() -> None:
    book = BankBook(10, 40, 50, 70, 20, 10)
    assert book.balanced()
    shocked = mark_securities(book, -0.10)
    assert shocked.balanced()
    assert shocked.equity == pytest.approx(6.0)
    assert shocked.assets == pytest.approx(96.0)
    assert shocked.capital_ratio == pytest.approx(6.0 / 96.0)


def test_prospect_kink_loss_aversion() -> None:
    # λ = 2.25 makes losses loom larger than same-size gains
    assert tk_value(10.0) > 0
    assert tk_value(-10.0) < 0
    assert abs(tk_value(-10.0)) > tk_value(10.0)
    # convexity on losses: incremental pain falls with size
    assert tk_value(-20.0) - tk_value(-10.0) > tk_value(-10.0) - tk_value(0.0)


def test_amm_refuses_nonpositive_reserves() -> None:
    with pytest.raises(ValueError):
        AmmTrade(0.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        average_execution_closed_form(1.0, 1.0, 0.0)
