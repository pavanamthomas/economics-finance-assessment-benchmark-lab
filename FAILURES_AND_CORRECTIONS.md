# Failures and corrections

These are defects caught while writing the corpus, not a reconstructed history. Each row has a regression test or a rejected-item file that would fail if the same mistake were keyed again.

## 1. CPAMM fill keyed at the spot

**What failed.** A draft item asked for “the price” of a 10-unit sale into a (100, 100) pool and keyed \(1 = y/x\).

**How it was detected.** Writing the average-execution closed form \(\Delta y/\Delta x = y/(x+\Delta x) = 10/11\) for the same numbers. A quadrature of \(k/s^2\) agreed with \(10/11\), not with \(1\).

**Why it failed.** “Price” unnamed. The spot is the derivative. The fill is the path average.

**What changed.** `TD-E-01` names the object. The draft is `RJ-01`. `tests/test_invariants.py` requires the three routes to agree and to sit strictly between the two spots.

**What would fail if it recurred.** `test_amm_three_routes_agree` if someone “fixed” the closed form to return the spot; `test_every_numerical_check_matches_expected` on `TD-E-01` if the YAML expected value were set back to \(1\).

## 2. Impermanent loss signed as a long-vol gain

**What failed.** First pass keyed IL\((r=4)=+20\%\), using an options slogan (LP is long volatility).

**How it was detected.** `hold_vs_lp_values`: LP value versus holding the original inventory is \(2\sqrt{r}/(1+r)-1 = -0.2\).

**Why it failed.** Fees are the premium in that slogan. The stem was fee-free.

**What changed.** `TD-H-01` keys \(-20\%\). The wrong sign is `RJ-03`.

**Regression.** `test_impermanent_loss_invariants`.

## 3. Kyle \(\lambda\) missing the factor of two

**What failed.** A draft option list contained \(\sigma_v/\sigma_u=0.5\) and not \(0.25\). Drafted key \(0.50\).

**How it was detected.** Substituting \(\beta=1/(2\lambda)\) into the market maker's projection. `beta_star * 2 * lambda_star` must be \(1\).

**What changed.** `MM-H-01` includes \(0.25\). The no-correct-option draft is `RJ-04`.

**Regression.** `test_kyle_foc_and_projection`.

## 4. Fourfold pattern cited to 1979 for a 1992 claim

**What failed.** A draft keyed “\(\lambda>1\) in Kahneman–Tversky (1979)” as the generator of the fourfold pattern.

**How it was detected.** Reading the claim against the two papers: 1979 has the value function and a weighting sketch; the fourfold CPT package is Tversky–Kahneman (1992).

**What changed.** `BF-H-01`. The citation defect is `RJ-05`. The validator still cannot catch this; the bib test only checks that keys exist.

## 5. CCyB “now” without a cycle date

**What failed.** A draft asked what to do to the CCyB “now” given high capital ratios, and keyed *release*.

**How it was detected.** The same high ratios appear in a boom (build) and after a repair (maybe hold). “Now” was not a phase.

**What changed.** `MP-H-01` dates a boom. `RJ-08` keeps the ambiguous draft.

## 6. Closed-city amenity key used as if unique

**What failed.** “Rents rise and residents are better off” keyed without stating closed versus open city.

**How it was detected.** Open-city \(u^\ast=\bar u\) capitalises the amenity into land (`UE-H-01`).

**What changed.** The split is the item. `RJ-02` is the hidden-assumption draft.

## 7. Health-factor LTV inequality reversed in a rationale

**What failed.** A sentence in an early `TD-H-02` draft said 67 percent LTV was “above” an 80 percent threshold.

**How it was detected.** \(100/150\approx 0.667<0.80\), and `aave_health_factor` returned \(1.2\).

**What changed.** The reversed comparison is distractor F, not the derivation.

**Regression.** `test_health_factor_and_ltv_equivalence`.

## 8. Schema accepted a joke-distractor item

**What failed.** An early bounce item had nine non-economic options. The validator passed: ten letters, one key, uniqueness paragraph present.

**How it was detected.** Reading it. Automated validation does not score plausibility.

**What changed.** `RJ-07` documents the defect class. `MANUAL_REVIEW_CHECKLIST.md` includes a distractor-plausibility line. No test will ever fully own that line; claiming otherwise would be a new failure.

## 9. Answer-position leakage across the retained corpus

**What failed.** Every retained item used the same keyed letter. The economics could still be correct, but the corpus leaked the answer position and made letter-frequency guessing rational.

**How it was detected.** A corpus-level adversarial audit counted `correct_option` rather than reading items one at a time.

**What changed.** The 40 retained items were re-keyed without changing their substantive option sets: keyed and distractor bodies were permuted consistently, producing exactly four keys for each letter A–J. `validate_corpus` and `tests/test_corpus.py` now enforce the distribution.

**Why this matters.** Item validity includes presentation. A perfect derivation does not rescue a benchmark whose answer positions reveal the key.

## 10. Substantive wording and modelling repairs from the same audit

The audit also repaired several model-level defects: internal-target versus regulatory-minimum language in `MP-E-01`; DSTI terminology in `MP-H-02`; the sign of the CPAMM derivative in `TD-M-01`; governance arithmetic in `TD-H-03`; a duplicated correct numerical spread in `MM-H-02`; benchmark-object visibility in `MM-H-03`; under-parameterised CPT language in `BF-E-01`; separation of multiplicity from attrition in `BF-E-02`; comparability assumptions in `UE-E-02`; hedonic-identification wording in `UE-H-03`; TWAP-lag wording in `TD-E-02`; and explicit cost/competition conditions in `TD-E-03`.

These are recorded because a useful benchmark should expose its corrections rather than imply that the first draft was perfect.

