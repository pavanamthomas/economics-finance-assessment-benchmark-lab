# Interview guide

This is the work I can defend. It is not a script for a job I have not held.

## A. 15-second walkthrough

I write 10-option economics items and then try to break them. The public analogue is this corpus: 40 accepted items, 11 rejected drafts, and a flagship case where “the price” on a constant-product trade had three defensible keys until the object was named.

## B. 30-second walkthrough

**Problem.** Assessment authoring for five fields, with exactly one key and nine engineered distractors.

**Method.** YAML schema plus a taxonomy of misconceptions (sign reversal, stock vs flow, average vs marginal execution, information set, …). Closed forms where they exist.

**Failure.** A CPAMM draft keyed the spot as the fill. Uniqueness failed; a quadrature check is what makes that failure visible in code.

**Validation.** Schema tests; Kyle / Glosten–Milgrom / IL / health-factor / bid-rent / bank-book identities; three-route AMM execution. The validator does not certify economic truth.

## C. 60-second walkthrough

**Target.** Items a specialist can audit: assumptions, derivation, uniqueness, a claim-level citation, and a record of drafts that failed.

**Assumptions.** Constructed stems. One author. Numerical checks only where a closed form exists.

**Implementation.** `efablab` loads YAML, refuses structural defects, and runs `numerical_check` blocks against independent code.

**Hardest failure mode.** Not a missing field. A well-formed item with two keys under a hidden modelling choice (open vs closed city; reference point in CPT; mid vs touch). Those are in `rejected_items/`.

**Independent validation.** AMM: closed form vs integral vs geometric mean. IL: formula vs hold-versus-LP values. Kyle: \(\beta=1/(2\lambda)\). GM: Bayes quotes. Bank books: assets = liabilities + equity after a mark.

**Limitation.** No second rater. No live order-book or mainnet data. No claim that automated tests replace an examiner.

## D. Hard questions I can defend

1. Why is each distractor in `TD-E-01` a real misconception rather than a joke option? (`RJ-07` is what joke options look like.)
2. Could another option in `UE-H-01` be correct under a different equilibrium concept? Yes — that is why the open/closed split is *in the stem*. See `RJ-02`.
3. What makes `MM-E-01` Expert rather than Hard? Nested feasibility (mid, touch, depth), not algebra length.
4. What is the independent verification of Kyle \(\lambda=0.25\)? `lambda_star` and the FOC identity \(\beta=1/(2\lambda)\), not printing the same formula twice.
5. Why does Kahneman–Tversky (1979) not support a fourfold-pattern key? `RJ-05` and `BF-H-01`.
6. Why was a draft CCyB item rejected? Timing of “now” was unspecified (`RJ-08`).
7. What breaks if the AMM information set includes a fee? The geometric-mean identity.
8. What changes if agents are risk-neutral in Kyle? The one-shot model already is; inventory models are a different object (`MM-H-02` vs Ho–Stoll).
9. What changes under a binding LTV cap that leaks into high-DTI loans? `MP-H-02`.
10. Is `MP-E-01` partial or general equilibrium? Nash taking the price as given, with a downward-sloping *aggregate* inverse demand — a pecuniary externality.
11. What is the economic content of \(10/11\), not the Python content? Path-average of \(k/s^2\).
12. Why isn't `MM-E-02` “just a coding result”? The mid regression can be statistically fine; the take P&L is a different left-hand side.
13. How do you know the Glosten spread is not inventory? The specialist's objective in the stem has no inventory argument; quotes are \(E[v\mid\text{side}]\).
14. If I change the reference in `BF-E-01` from 100 to 80, what happens to the domain coding of \(\{70,80,90\}\)?
15. Why does a G-SIB surcharge not identify a zero TBTF subsidy? `MP-E-03`.

## E. Change-an-assumption tests (five flagship cases)

1. **`TD-E-01`.** If \(\Delta x\to 0\), the three prices collapse. If a fee is taken on inbound X, \(k\) on displayed reserves rises and the geometric-mean identity fails.
2. **`MM-E-01`.** If the half-spread is 0.5 bp rather than 3 bp, book (2) can be positive; book (1) is still not executable. If hidden size is assumed, book (3) needs a qualifier — that is why hidden size is excluded.
3. **`MP-E-01`.** If inverse demand is flat, Nash and freeze coincide and the externality shuts. If \(n=1\), there is no externality *on others*.
4. **`BF-E-01`.** If the reference is locked at the purchase price, a unique (loss-domain) prediction can be keyed. The item exists because that lock was missing in a draft.
5. **`UE-H-01`.** If the city is large enough to move the national outside option, the open-city pin on \(u^\ast\) weakens. If housing supply is perfectly elastic, the rent increase shrinks and the population response grows.

## F. Three limitations to volunteer

1. One author coded every key. There is no second-rater study.
2. Automated validation is structural. It will not catch a conceptually wrong but well-formed uniqueness paragraph.
3. Numerical coverage is partial. `MM-H-03` (VWAP) and `TD-E-03` (ordering) are paper audits; treating them as if they had a closed-form test would be a false claim.
