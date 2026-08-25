# Proposed extension (not committed)

Repository: [ai-response-evaluation-benchmarks](https://github.com/pavanamthomas/ai-response-evaluation-benchmarks)

That repository is under review for a different application. This file is a proposal only. It is not a patch to that repo and it is not a claim that the extension has been run.

## Suggested path

`cases/economics_finance_mcq_verification/`

Each case would be a *review of an assessment item* (stem + options + drafted key), not a review of a chatbot paragraph. The defect families to cover, mapped to this laboratory's `rejected_items/`:

| Defect class | Local analogue |
| --- | --- |
| AMBIGUOUS_STEM | `RJ-01`, `RJ-10` |
| MULTIPLE_CORRECT_OPTIONS | `RJ-01`, `RJ-02` |
| NO_CORRECT_OPTION | `RJ-04` |
| WRONG_KEY | `RJ-03` |
| HIDDEN_ASSUMPTION | `RJ-02` |
| WRONG_DIFFICULTY | `RJ-06` |
| UNSUPPORTED_REFERENCE | `RJ-05` |
| INCORRECT_DERIVATION | would need new fixtures |
| TIMING_ERROR | `RJ-08` |
| UNIT_ERROR | (not yet a rejected class here) |
| EQUILIBRIUM_ERROR | `RJ-09` |
| DISTRACTOR_TOO_OBVIOUS | `RJ-07` |
| AMBIGUOUS_INFORMATION_SET | `RJ-11` |

The scoring object would remain the existing rubric (target, assumptions, method, validation, interpretation limit). The candidate response would be an item-verification memo, not an MCQ pick.

Do not copy YAML from this repository into that one without an explicit authorisation to touch it. The corpora have different schemas on purpose.
