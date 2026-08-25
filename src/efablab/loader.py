"""Load YAML items from the repository corpus directories."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from efablab.schema import (
    AssessmentItem,
    DistractorRationale,
    Reference,
    RejectedItem,
    Verification,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
ITEMS_DIR = REPO_ROOT / "items"
REJECTED_DIR = REPO_ROOT / "rejected_items"


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse as a mapping")
    return data


def _refs(raw: list[Any]) -> list[Reference]:
    out: list[Reference] = []
    for row in raw:
        if not isinstance(row, dict):
            raise ValueError("each reference must be a mapping with key and claim_supported")
        out.append(
            Reference(
                key=str(row["key"]),
                claim_supported=str(row["claim_supported"]),
            )
        )
    return out


def item_from_mapping(raw: dict[str, Any], *, source: str = "") -> AssessmentItem:
    rationales: dict[str, DistractorRationale] = {}
    for letter, row in raw["distractor_rationales"].items():
        rationales[str(letter)] = DistractorRationale(
            taxonomy=str(row["taxonomy"]),
            why_chosen=str(row["why_chosen"]),
            why_wrong=str(row["why_wrong"]),
        )
    ver = raw["verification"]
    numerical = raw.get("numerical_check")
    return AssessmentItem(
        id=str(raw["id"]),
        domain=str(raw["domain"]),
        subdomain=str(raw["subdomain"]),
        difficulty=str(raw["difficulty"]),
        learning_objective=str(raw["learning_objective"]),
        stem=str(raw["stem"]).strip(),
        options={str(k): str(v) for k, v in raw["options"].items()},
        correct_option=str(raw["correct_option"]),
        solution_summary=str(raw["solution_summary"]).strip(),
        solution_derivation=str(raw["solution_derivation"]).strip(),
        assumptions=[str(a) for a in raw["assumptions"]],
        distractor_rationales=rationales,
        misconception_tags=[str(t) for t in raw["misconception_tags"]],
        difficulty_rationale=str(raw["difficulty_rationale"]).strip(),
        ambiguity_audit=str(raw["ambiguity_audit"]).strip(),
        uniqueness_check=str(raw["uniqueness_check"]).strip(),
        references=_refs(raw["references"]),
        verification=Verification(
            primary_solution=str(ver["primary_solution"]).strip(),
            independent_check=str(ver["independent_check"]).strip(),
            invariant_or_boundary_check=str(ver["invariant_or_boundary_check"]).strip(),
        ),
        revision_notes=str(raw["revision_notes"]).strip(),
        numerical_check=dict(numerical) if isinstance(numerical, dict) else None,
        raw=raw,
    )


def rejected_from_mapping(raw: dict[str, Any]) -> RejectedItem:
    return RejectedItem(
        id=str(raw["id"]),
        defect_class=str(raw["defect_class"]),
        domain=str(raw["domain"]),
        difficulty_as_drafted=str(raw["difficulty_as_drafted"]),
        stem=str(raw["stem"]).strip(),
        options={str(k): str(v) for k, v in raw["options"].items()},
        drafted_key=str(raw["drafted_key"]),
        defect=str(raw["defect"]).strip(),
        why_it_matters=str(raw["why_it_matters"]).strip(),
        repairable=bool(raw["repairable"]),
        correction=str(raw["correction"]).strip(),
        key_changes=bool(raw["key_changes"]),
        difficulty_changes=bool(raw["difficulty_changes"]),
        references=_refs(raw.get("references", [])),
        raw=raw,
    )


def load_items(root: Path | None = None) -> list[AssessmentItem]:
    base = root or ITEMS_DIR
    paths = sorted(base.rglob("*.yaml"))
    items = []
    for path in paths:
        items.append(item_from_mapping(_read_yaml(path), source=str(path)))
    return items


def load_rejected(root: Path | None = None) -> list[RejectedItem]:
    base = root or REJECTED_DIR
    paths = sorted(base.glob("*.yaml"))
    return [rejected_from_mapping(_read_yaml(path)) for path in paths]
