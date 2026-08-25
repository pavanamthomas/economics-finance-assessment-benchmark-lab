"""Print the flagship AMM numbers without requiring a notebook."""

from __future__ import annotations

from efablab.checks.amm import (
    AmmTrade,
    average_execution_by_quadrature,
    average_execution_closed_form,
    geometric_mean_spots,
    sell_x,
)


def main() -> None:
    x, y, dx = 100.0, 100.0, 10.0
    closed = average_execution_closed_form(x, y, dx)
    quad = average_execution_by_quadrature(x, y, dx)
    geom = geometric_mean_spots(x, y, dx)
    sim = sell_x(AmmTrade(x, y, dx))
    print("fee-free CPAMM sale of 10 X into (100, 100)")
    print(f"  pre-trade spot     {sim['spot0']:.10f}")
    print(f"  post-trade spot    {sim['spot1']:.10f}")
    print(f"  closed-form avg    {closed:.10f}")
    print(f"  quadrature avg     {quad:.10f}")
    print(f"  geom-mean of spots {geom:.10f}")
    print(f"  k before, after    {sim['k0']:.6f}, {sim['k1']:.6f}")
    print("TD-E-01 keys the closed-form average, not either spot.")


if __name__ == "__main__":
    main()
