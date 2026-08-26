# Data policy

There is no observational microdata in this repository.

Accepted and rejected items are constructed assessment fixtures. Numerical illustrations (Kyle volatilities, CPAMM reserves, a toy bank book, a health factor) are parameters in YAML and in `efablab.checks`. They are not estimates from a trading venue, a supervisor, a protocol, or a household survey.

`python scripts/run_all.py` reprints those parameters. It does not download anything.

Because there are no personal records, there is no PII workflow. Source is MIT-licensed.

Do not cite a printed number from an item stem as an empirical finding. Do not cite a passing CI run as evidence about a market.
