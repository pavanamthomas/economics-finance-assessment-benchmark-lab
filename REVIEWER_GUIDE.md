# Reviewer guide

This is a short entry point into five flagship items. It is not a substitute for reading the YAML, derivations, references, and failure log.

## Market microstructure — `MM-E-01`

**Question:** When does a statistically attractive mark cease to be economically executable?

**Decisive assumption:** distinguish mid-mark, touch, and finite-depth execution, with hidden size excluded.

**Strongest distractor:** the answer that treats a non-executable mark as P&L.

**Independent check:** reconstruct the executable book and compare the finite fill with the quoted/mid marks.

**Smallest answer-flip:** reduce spread/depth costs enough that the executable book becomes positive; the mid-only claim still remains non-executable.

## Macroprudential policy — `MP-E-01`

**Question:** Can individually reasonable balance-sheet repair create a system-level constraint violation?

**Decisive assumption:** each bank takes price as given while aggregate sales move the common-security price.

**Strongest distractor:** the claim that a bank above the regulatory minimum cannot rationally sell. The repaired stem separates the stricter internal target from the regulatory minimum.

**Independent check:** flatten inverse demand. The price externality and the Nash-versus-freeze wedge disappear.

**Smallest answer-flip:** make aggregate inverse demand flat.

## Behavioral finance / experimental economics — `BF-E-01`

**Question:** Is the current market price enough to select a unique CPT choice?

**Decisive assumption:** the reference point and the relevant value/weighting parameters must be stated.

**Strongest distractor:** the current-price-as-reference shortcut.

**Independent check:** recode the same 70/80/90 outcomes under purchase-price, expectations-based, and goal references.

**Smallest answer-flip:** specify a reference plus sufficient curvature/weighting parameters to make one choice unique.

## Urban economics — `UE-H-01`

**Question:** Who captures an amenity gain in open versus closed city equilibrium?

**Decisive assumption:** whether population or utility is the margin that clears.

**Strongest distractor:** 'amenities are good, therefore residents are better off in both models.'

**Independent check:** in the open-city limit, pin utility to the outside option and let rent/population adjust.

**Smallest answer-flip:** close migration; utility becomes endogenous and incumbents can retain part of the gain.

## Tokenomics / DeFi — `TD-E-01`

**Question:** Which AMM price is being asked for: pre-trade marginal, finite-trade average, or post-trade marginal?

**Decisive assumption:** fee-free constant-product pool and an explicitly finite trade.

**Strongest distractor:** using the initial marginal price as the finite fill.

**Independent check:** closed form, path integral, and geometric mean of endpoint marginal prices agree on the average execution price.

**Smallest answer-flip:** take trade size to zero; the three prices collapse.

## What the automated checks do not prove

Balanced key positions, schema checks, and numerical identities remove detectable implementation defects. They do not prove that a qualitative economic key is true. The remaining standard is adversarial manual review: attempt to rescue the strongest distractor under the stated assumptions, verify the decisive claim against the cited source, and state the smallest assumption change that would alter the key.
