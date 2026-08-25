# Item schema

Accepted YAML fields are the contract in `efablab.schema.AssessmentItem`. Required:

`id`, `domain`, `subdomain`, `difficulty`, `learning_objective`, `stem`, `options` (A–J), `correct_option`, `solution_summary`, `solution_derivation`, `assumptions` (non-empty list), `distractor_rationales` (A–J, each with `taxonomy`, `why_chosen`, `why_wrong`), `misconception_tags`, `difficulty_rationale`, `ambiguity_audit`, `uniqueness_check`, `references` (1–5, each `key` + `claim_supported`), `verification` (`primary_solution`, `independent_check`, `invariant_or_boundary_check`), `revision_notes`.

Optional: `numerical_check` with `kind`, `params`, `expected`. Kinds are the keys of `efablab.checks.CHECK_ROUTINES`.

IDs: `{MM|MP|BF|UE|TD}-{M|H|E}-{two digits}`. Prefix must match domain; infix must match difficulty.

Rejected YAML uses a different contract (`RejectedItem`): `defect_class` from the closed list in `schema.py`, plus repair metadata (`repairable`, `key_changes`, `difficulty_changes`). Rejected drafts still have A–J so a reviewer can see what the examinee would have faced.
