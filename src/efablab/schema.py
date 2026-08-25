"""Dataclasses for accepted items and rejected drafts.

Field names match the YAML corpus. Nested maps are left as dicts so a
reviewer can open the YAML and the Python object without a second schema
layer. Required-key checks live in `validator.py`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DistractorRationale:
    taxonomy: str
    why_chosen: str
    why_wrong: str


@dataclass(frozen=True)
class Reference:
    key: str
    claim_supported: str


@dataclass(frozen=True)
class Verification:
    primary_solution: str
    independent_check: str
    invariant_or_boundary_check: str


@dataclass(frozen=True)
class AssessmentItem:
    id: str
    domain: str
    subdomain: str
    difficulty: str
    learning_objective: str
    stem: str
    options: dict[str, str]
    correct_option: str
    solution_summary: str
    solution_derivation: str
    assumptions: list[str]
    distractor_rationales: dict[str, DistractorRationale]
    misconception_tags: list[str]
    difficulty_rationale: str
    ambiguity_audit: str
    uniqueness_check: str
    references: list[Reference]
    verification: Verification
    revision_notes: str
    numerical_check: dict[str, Any] | None = None
    raw: dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True)
class RejectedItem:
    id: str
    defect_class: str
    domain: str
    difficulty_as_drafted: str
    stem: str
    options: dict[str, str]
    drafted_key: str
    defect: str
    why_it_matters: str
    repairable: bool
    correction: str
    key_changes: bool
    difficulty_changes: bool
    references: list[Reference]
    raw: dict[str, Any] = field(default_factory=dict, repr=False)


REJECTED_DEFECT_CLASSES: frozenset[str] = frozenset(
    {
        "multiple_defensible_answers",
        "hidden_assumption_changes_key",
        "incorrect_key",
        "no_correct_option",
        "reference_does_not_support_claim",
        "difficulty_miscalibration",
        "implausible_distractors",
        "timing_ambiguity",
        "missing_equilibrium_condition",
        "undefined_price_convention",
        "ambiguous_information_set",
    }
)
