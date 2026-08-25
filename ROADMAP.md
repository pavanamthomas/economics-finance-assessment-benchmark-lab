# Roadmap

Open technical work. Not a kanban of decorative chores.

## Uniqueness under an alternative risk-aversion convention

`BF-E-01` uses TK92 curvature and a given \(\lambda\). If the examinee is allowed to use expected-utility CRRA on final wealth, locking 80 versus gambling \(\{70,90\}\) is a different problem and does not need a reference point. The item states CPT. A later item could ask whether the *same numbers* flip under EU, with the reference-point machinery shut.

## Queue-priority sensitivity

`MM-E-03` is a two-path selection argument at a sticky bid. It does not compute fill probabilities under a Hawkes flow or a queue-reactive intensity. That computation would be a different laboratory (order-book simulation). It is not required to key the item, and adding it here without a new uniqueness audit would be decoration.

## Discrete versus continuous liquidation

`TD-H-02` uses an Aave-style health factor and a hard \(HF<1\) rule. Some protocols close a position in one transaction; others close a fraction. The item does not distinguish those mechanics. A follow-up would need a stated close-factor and a stated incentive, otherwise it recreates `RJ-01` (unnamed object).

## CCyB under endogenous credit supply

`MP-H-01` treats the credit-to-GDP gap as a guide. It does not solve a model in which banks' lending *is* the gap. Endogenous credit would change whether “raise now” is even feasible without a demand-side instrument. That is a research paper, not a missing YAML field.

## Second derivation of the IL boundary

`TD-H-01` has IL\(\to -1\) as \(r\to 0\) or \(r\to\infty\). A second derivation: the LP is eventually all of the depreciating asset, so its value relative to a hold that kept the appreciating asset goes to 0. The current tests check the formula and symmetry, not this verbal limit as a separate coded identity.

## What this laboratory will not absorb

Standalone behavioral-finance or urban-economics *implementation* repositories are not justified by this corpus yet. The assessment items in those domains are the evidence. A simulation lab would need a DGP and tests that are not a restatement of the YAML.

The companion `ai-response-evaluation-benchmarks` repository is frozen from this work. A proposed extension path is written in `docs/proposed_ai_eval_extension.md` and is not a commit to that repo.
