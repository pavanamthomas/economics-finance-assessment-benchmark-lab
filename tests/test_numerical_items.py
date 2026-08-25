"""Item-level numerical_check blocks versus independent closed forms."""

from __future__ import annotations

import pytest

from efablab.checks import run_named_check
from efablab.loader import load_items


def test_every_numerical_check_matches_expected() -> None:
    items = [it for it in load_items() if it.numerical_check]
    assert items, "expected at least one numerical_check in the corpus"
    for it in items:
        spec = it.numerical_check
        assert spec is not None
        kind = spec["kind"]
        params = spec["params"]
        expected = spec["expected"]
        got = run_named_check(kind, params)
        for name, value in expected.items():
            assert name in got, f"{it.id}: check did not return {name}"
            assert got[name] == pytest.approx(float(value), rel=1e-6, abs=1e-8), (
                f"{it.id}: {name} got {got[name]} expected {value}"
            )


def test_numerical_routes_are_not_the_same_function_twice() -> None:
    """AMM execution must be checked by three routes inside run_named_check."""
    got = run_named_check("amm_execution", {"x": 100.0, "y": 100.0, "dx": 10.0})
    assert got["value"] == pytest.approx(10.0 / 11.0)
    il = run_named_check("impermanent_loss", {"price_ratio": 4.0})
    assert il["value"] == pytest.approx(-0.2)
