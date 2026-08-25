# Manual review checklist

Automated validation (`efablab.validator`) checks completeness, not economics. Use this list on every accepted item. It is the residual examiner.

A passing CI run is not a substitute for this list. `FAILURES_AND_CORRECTIONS.md` §8 is the case where the schema was happy and the item was still unusable.

## Construct

- [ ] The learning objective is a mechanism, not a researcher-name recall.
- [ ] Difficulty matches the rubric in `docs/difficulty_calibration.md` (inferential branching, not algebra length).
- [ ] The stem states the model, the information set, and the units / price convention.

## Key uniqueness

- [ ] Exactly one option remains after the stated assumptions. If a second option becomes correct when an unstated switch is flipped (open/closed city, reference point, mid vs touch), the item is `RJ-02` / `RJ-10` / `RJ-11` material, not accepted.
- [ ] The uniqueness paragraph names the switch that *would* create a second key, and states that the stem shuts it.

## Distractors

- [ ] Each of the nine incorrect options is a misconception a technically competent person might have, tagged from `efablab.taxonomy`.
- [ ] No joke options, no “the Fed prints money so AMMs fail” (`RJ-07`).
- [ ] The rationale says why the option attracts *and* the precise reason it fails under the stem.

## References

- [ ] Each citation supports the *claim used in the key or derivation*, not merely the topic.
- [ ] 1979 is not used as if it were 1992; a handbook is not used as if it identified a coefficient.
- [ ] No Wikipedia, Investopedia, or SEO blog as a supporting source.

## Verification

- [ ] If the key is a number, a `numerical_check` exists and an independent route is named (closed form vs integral, formula vs hold values, FOC vs projection).
- [ ] If the key is not a number, the invariant / boundary check is an actual boundary (fee → 0, \(\mu\to 0\), \(t=0\), flat inverse demand), not a restatement of the key.
- [ ] Running the same Python function twice is not listed as independent verification.

## Integrity

- [ ] No implied desk, supervisor, protocol employment, certificate, client, AUM, or live return.
- [ ] No fabricated paper.
