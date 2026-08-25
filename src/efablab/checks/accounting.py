"""Accounting identities used by macroprudential items.

These are identities or definitional ratios, not estimates of systemic
risk. A test that leverage equals assets/equity does not validate CoVaR.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BankBook:
    cash: float
    securities: float
    loans: float
    deposits: float
    wholesale: float
    equity: float

    @property
    def assets(self) -> float:
        return self.cash + self.securities + self.loans

    @property
    def liabilities_plus_equity(self) -> float:
        return self.deposits + self.wholesale + self.equity

    def balanced(self, tol: float = 1e-9) -> bool:
        return abs(self.assets - self.liabilities_plus_equity) <= tol

    @property
    def leverage(self) -> float:
        if self.equity <= 0:
            raise ZeroDivisionError("equity is non-positive")
        return self.assets / self.equity

    @property
    def capital_ratio(self) -> float:
        return self.equity / self.assets


def mark_securities(book: BankBook, return_on_securities: float) -> BankBook:
    """Apply a return to the securities book and absorb the loss in equity.

    Deposits and wholesale are unchanged. If equity would go negative the
    caller must handle default; this function does not invent a resolution
    regime.
    """
    new_sec = book.securities * (1.0 + return_on_securities)
    pnl = new_sec - book.securities
    return BankBook(
        cash=book.cash,
        securities=new_sec,
        loans=book.loans,
        deposits=book.deposits,
        wholesale=book.wholesale,
        equity=book.equity + pnl,
    )


def aave_health_factor(collateral_value: float, debt_value: float, liq_threshold: float) -> float:
    """Aave-style health factor: (collateral * liquidationThreshold) / debt.

    Liquidation is admissible when HF < 1. liq_threshold is a fraction in
    (0, 1), not a loan-to-value cap written as a percentage of 100.
    """
    if debt_value <= 0:
        raise ValueError("debt_value must be positive to define HF")
    if not 0 < liq_threshold < 1:
        raise ValueError("liquidation threshold must be in (0, 1)")
    if collateral_value < 0:
        raise ValueError("collateral_value must be non-negative")
    return (collateral_value * liq_threshold) / debt_value
