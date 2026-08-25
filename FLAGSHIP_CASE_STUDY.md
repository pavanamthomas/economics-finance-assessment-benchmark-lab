# Flagship case: three prices on one CPAMM trade

**Item.** `TD-E-01` (accepted). **Rejected ancestor.** `RJ-01-multiple_defensible_answers`.

**Problem.** Write a 10-option item that tests whether an examinee distinguishes the *marginal* price of a constant-product pool from the *average execution price* of a finite trade. The first draft failed uniqueness: it asked for “the price.”

**Assumptions.** Fee-free pool, reserves \((x,y)=(100,100)\), \(k=xy=10{,}000\). Trader *sells* \(\Delta x=10\) of X into the pool (X in, Y out). Numeraire is Y per X. No concentrated liquidity.

**Formal model.** Along \(xy=k\), the spot (marginal) price of X in Y is
\[
p(x)=\frac{y}{x}=\frac{k}{x^2}.
\]
A fee-free sale that moves reserves from \(x\) to \(x'=x+\Delta x\) pays
\[
\Delta y=y-\frac{k}{x'}=y\frac{\Delta x}{x+\Delta x},
\]
so the average execution price is
\[
\frac{\Delta y}{\Delta x}=\frac{y}{x+\Delta x}.
\]
The post-trade spot is \(p'=k/(x')^2\). For this parameterisation,
\[
\sqrt{p\cdot p'}=\frac{y}{x+\Delta x}.
\]
That identity is a fee-zero fact, not a general AMM slogan.

**Implementation.** `src/efablab/checks/amm.py`. Run `python examples/inspect_flagship.py`.

**Plausible wrong approach.** Key the pre-trade spot \(p=1\), because that is “the” quoted price and because \(\Delta x/x=0.1\) “looks small.” A second wrong approach keys the post-trade spot \(p'\approx 0.8264\), because “the trade happens at the new price.”

**Why those are attractive.** Order-book language treats the touch as the executable price. CPAMM language treats \(y/x\) as *the* price in every README. Neither sentence names a finite-trade integral. Expert examinees still collapse the three objects.

**Failure (the draft).** Stem: “What is the price of X?” Options included \(1\), \(10/11\), and \(100/121\). Drafted key: \(1\). Three readings, three defensible answers. The validator could not catch this: all schema fields were filled. The quadrature check *could* catch a numerical_check that claimed the fill was \(1\); the draft had no numerical_check.

**Corrected approach.** Name the object in the stem. Key \(10/11\). Put \(1\) and \(100/121\) in the option list as `AVERAGE_VS_MARGINAL_EXECUTION_PRICE` distractors, with rationales that say *why* a competent person would pick them. Record the draft as `RJ-01`. Difficulty is Expert because uniqueness of the word “price” is the construct, not because the algebra is long.

**Independent verification.** Three routes, not the same function twice:

1. Closed form \(y/(x+\Delta x)\).
2. Trapezoid integral of \(k/s^2\) on \([x,x+\Delta x]\).
3. Geometric mean of the two spots.

They agree to \(10^{-5}\) relative on this example. \(k\) is preserved. As \(\Delta x\to 0\), all three numbers collapse to \(1\); at \(\Delta x=10\) they split. That split is the item.

**Limitation.** Fee-free, two-asset, no concentrated liquidity, no tick. A 30 bp fee breaks the exact geometric-mean identity. Uniswap v3 ranges make “the” spot a tick, not \(y/x\) on whole-pool reserves. The item does not claim a trading edge and does not use a live pool.

**Interview questions this file is meant to generate.**

1. Why is \(10/11\) between \(1\) and \(100/121\)?
2. What happens to the identity if a fee is taken on inbound X?
3. Why did the schema validator not catch the draft?
4. If the stem had asked for the *quoted* spot, would A be uniquely correct?
5. Why is this Expert rather than Medium (the algebra is one line)?

Numbers, not memory:

```
pre-trade spot      1.0000000000
average execution   0.9090909091
post-trade spot     0.8264462810
```
