# Economics and Finance Assessment Benchmark Lab

A 10-option assessment item is not a quiz. It is a claim that exactly one of ten statements is the unique implication of a stated model, and that the other nine are errors a technically competent person might actually make.

This repository is a laboratory for **authoring** and **verifying** such items in five domains: market microstructure, macroprudential policy, behavioral finance / experimental economics, urban economics, and tokenomics / DeFi. It is self-directed technical study and benchmark-development practice. It is not employment at a trading desk, a supervisor, a protocol, or a test publisher, and it does not claim a CFA, FRM, or similar credential.

Dr. Pavanam Thomas · [pavanamthomas](https://github.com/pavanamthomas) · thomaspavanam@gmail.com
MIT License · Copyright 2026

The companion repository [ai-response-evaluation-benchmarks](https://github.com/pavanamthomas/ai-response-evaluation-benchmarks) scores *answers*. This laboratory writes the *questions*, including the ones that were rejected. That repository is not modified here.

## 10-second signal

| Object | What is here |
| --- | --- |
| Exact technical object | 40 accepted 10-option items plus 11 rejected drafts, with a validator that does **not** pretend to prove economic correctness |
| Implemented | Schema, distractor taxonomy, closed-form checks (Kyle λ, Glosten–Milgrom quotes, CPAMM execution, IL, health factor, bid-rent, bank-book identities) |
| Independently verified | AMM average execution by three routes (closed form, quadrature, geometric mean of spots); IL by formula versus hold-versus-LP values |
| Failure mode on display | A draft that keyed the CPAMM *spot* as the fill of a finite trade; quadrature disagreed. See `FLAGSHIP_CASE_STUDY.md` and `rejected_items/RJ-01-*.yaml` |

## 60-second evidence

Open [`FLAGSHIP_CASE_STUDY.md`](FLAGSHIP_CASE_STUDY.md) and [`items/tokenomics_defi/TD-E-01.yaml`](items/tokenomics_defi/TD-E-01.yaml).

A fee-free pool (100, 100) and a sale of 10 X. Three numbers: pre-trade spot 1, average execution 10/11, post-trade spot 100/121. A stem that asks for “the price” has three defensible keys. The repaired item names the object. `python examples/inspect_flagship.py` reprints the three routes.

That is the job analogue: uniqueness audit, not item count.

## What the validator does and does not do

`efablab` will refuse an item that has the wrong number of options, two keyed letters, a duplicate option after normalisation, a missing uniqueness write-up, or a citation count outside 1–5. Passing CI means the YAML is complete and the numerical blocks match the independent code.

It does **not** mean the economics is true. Economic correctness is the written derivation, the uniqueness audit, `MANUAL_REVIEW_CHECKLIST.md`, and whoever reads them.

## Corpus

40 accepted items (10 Medium, 15 Hard, 15 Expert), eight in each domain:

| Prefix | Domain | Flagship inside the domain |
| --- | --- | --- |
| MM | Algorithmic trading / market microstructure | `MM-E-01` mid-mark versus executable books |
| MP | Macroprudential policy | `MP-E-01` Nash fire sale versus coordinated freeze |
| BF | Behavioral finance / experimental economics | `BF-E-01` reference point changes the CPT key |
| UE | Urban economics | `UE-H-01` open versus closed city amenity shock |
| TD | Tokenomics / DeFi | `TD-E-01` AMM average versus marginal price |

Rejected drafts live in `rejected_items/`. Each one names a defect class (multiple keys, hidden assumption, wrong key, no correct option, unsupported reference, difficulty miscalibration, joke distractors, timing ambiguity, missing equilibrium, undefined price, ambiguous information set), whether it is repairable, and whether the key changes.

## Layout

```
items/                  accepted YAML, one file per id
rejected_items/         drafts that failed verification
src/efablab/            schema, loader, validator, taxonomy
src/efablab/checks/     closed forms used by numerical_check blocks
tests/                  corpus rules and economic identities
examples/inspect_flagship.py
FLAGSHIP_CASE_STUDY.md
INTERVIEW_GUIDE.md
FAILURES_AND_CORRECTIONS.md
MANUAL_REVIEW_CHECKLIST.md
REFERENCES.bib
```

## Install and checks

Python 3.11+:

```bash
pip install -e ".[dev]"
pytest -q
python scripts/validate_items.py
python scripts/run_all.py
python examples/inspect_flagship.py
```

CI runs the same four commands (the last two as validate + inventory).

## Related work, not modified

- [ai-response-evaluation-benchmarks](https://github.com/pavanamthomas/ai-response-evaluation-benchmarks) — scoring AI answers. A *proposed* later extension is in `docs/proposed_ai_eval_extension.md`. Not committed to that repository.
- [econometrics-causal-inference-lab](https://github.com/pavanamthomas/econometrics-causal-inference-lab) — identification designs, not MCQ authoring.
- Standalone market-microstructure, tokenomics, and macroprudential implementation labs are *not* this repository. This one is the assessment object.

## Boundaries

- Constructed items. Not licensed exam content, not a live trading system, not a supervisory model, not a mainnet deployment.
- Numerical checks cover the items that have a closed form. The rest are audited on paper.
- One author wrote the keys. There is no second-rater study and no claimed inter-rater kappa on this corpus.
- References are real papers and technical documents. A key in `REFERENCES.bib` is not a claim that the paper “finds” the MCQ.
- Nothing here is a certificate, a client, AUM, or a production impact statistic.

## Citation

See `CITATION.cff`.
