"""Executable numerical checks referenced by item `numerical_check` blocks."""

from __future__ import annotations

from typing import Any, Callable

from efablab.checks.accounting import BankBook, aave_health_factor, mark_securities
from efablab.checks.amm import (
    AmmTrade,
    average_execution_by_quadrature,
    average_execution_closed_form,
    geometric_mean_spots,
    hold_vs_lp_values,
    impermanent_loss,
    sell_x,
)
from efablab.checks.bid_rent import rent_gradient
from efablab.checks.glosten_milgrom import GMParams, quotes
from efablab.checks.kyle import KyleParams, beta_star, lambda_star
from efablab.checks.prospect import tk_value


def _close(a: float, b: float, tol: float = 1e-8) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


def run_amm_execution(params: dict[str, Any]) -> dict[str, float]:
    x, y, dx = float(params["x"]), float(params["y"]), float(params["dx"])
    closed = average_execution_closed_form(x, y, dx)
    quad = average_execution_by_quadrature(x, y, dx)
    geom = geometric_mean_spots(x, y, dx)
    sim = sell_x(AmmTrade(x, y, dx, fee=0.0))
    if not (
        _close(closed, quad, 1e-5)
        and _close(closed, geom)
        and _close(closed, sim["avg_execution"])
    ):
        raise AssertionError(
            f"AMM execution routes disagree: closed={closed}, quad={quad}, "
            f"geom={geom}, sim={sim['avg_execution']}"
        )
    return {"value": closed, "spot0": sim["spot0"], "spot1": sim["spot1"]}


def run_impermanent_loss(params: dict[str, Any]) -> dict[str, float]:
    r = float(params["price_ratio"])
    x, y = float(params.get("x", 100.0)), float(params.get("y", 100.0))
    closed = impermanent_loss(r)
    via = hold_vs_lp_values(x, y, r)["il_from_values"]
    if not _close(closed, via, 1e-9):
        raise AssertionError(f"IL routes disagree: closed={closed}, values={via}")
    return {"value": closed}


def run_kyle_lambda(params: dict[str, Any]) -> dict[str, float]:
    kp = KyleParams(sigma_v=float(params["sigma_v"]), sigma_u=float(params["sigma_u"]))
    return {"lambda": lambda_star(kp), "beta": beta_star(kp)}


def run_glosten_spread(params: dict[str, Any]) -> dict[str, float]:
    return quotes(GMParams(mu=float(params["mu"]), pi=float(params.get("pi", 0.5))))


def run_health_factor(params: dict[str, Any]) -> dict[str, float]:
    hf = aave_health_factor(
        float(params["collateral"]),
        float(params["debt"]),
        float(params["liq_threshold"]),
    )
    return {"value": hf}


def run_rent_gradient(params: dict[str, Any]) -> dict[str, float]:
    return {"value": rent_gradient(float(params["t"]), float(params["q"]))}


def run_bank_shock(params: dict[str, Any]) -> dict[str, float]:
    book = BankBook(
        cash=float(params["cash"]),
        securities=float(params["securities"]),
        loans=float(params["loans"]),
        deposits=float(params["deposits"]),
        wholesale=float(params["wholesale"]),
        equity=float(params["equity"]),
    )
    if not book.balanced():
        raise AssertionError("initial book does not balance")
    shocked = mark_securities(book, float(params["sec_return"]))
    if not shocked.balanced():
        raise AssertionError("shocked book does not balance")
    return {
        "equity1": shocked.equity,
        "capital_ratio1": shocked.capital_ratio,
        "assets1": shocked.assets,
    }


def run_prospect(params: dict[str, Any]) -> dict[str, float]:
    return {"value": tk_value(float(params["x"]))}


CHECK_ROUTINES: dict[str, Callable[[dict[str, Any]], dict[str, float]]] = {
    "amm_execution": run_amm_execution,
    "impermanent_loss": run_impermanent_loss,
    "kyle_lambda": run_kyle_lambda,
    "glosten_spread": run_glosten_spread,
    "health_factor": run_health_factor,
    "rent_gradient": run_rent_gradient,
    "bank_shock": run_bank_shock,
    "prospect": run_prospect,
}


def run_named_check(kind: str, params: dict[str, Any]) -> dict[str, float]:
    if kind not in CHECK_ROUTINES:
        raise KeyError(f"unknown numerical check {kind!r}")
    return CHECK_ROUTINES[kind](params)
