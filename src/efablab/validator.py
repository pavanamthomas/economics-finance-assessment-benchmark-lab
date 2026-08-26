"""Structural validation of assessment items.

Passing this module means the YAML is complete and internally consistent.
It does not mean the economics is correct. Economic claims are checked
where a closed form exists (`efablab.checks`) and otherwise by the
written uniqueness audit and `MANUAL_REVIEW_CHECKLIST.md`.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass

from efablab.schema import REJECTED_DEFECT_CLASSES, AssessmentItem, RejectedItem
from efablab.taxonomy import (
    DIFFICULTIES,
    DIFFICULTY_BY_INFIX,
    DISTRACTOR_TAGS,
    DOMAIN_BY_PREFIX,
    DOMAINS,
    ID_PATTERN,
    KEYED_TAG,
    OPTION_LETTERS,
    TARGET_COUNTS,
)


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class Issue:
    item_id: str
    message: str

    def __str__(self) -> str:
        return f"{self.item_id}: {self.message}"


def _norm_text(text: str) -> str:
    return " ".join(text.casefold().split())


def validate_item(item: AssessmentItem) -> list[Issue]:
    issues: list[Issue] = []
    iid = item.id or "<missing-id>"

    if not re.match(ID_PATTERN, item.id or ""):
        issues.append(Issue(iid, f"id {item.id!r} does not match {ID_PATTERN}"))
    else:
        prefix, infix, _ = item.id.split("-")
        expected_domain = DOMAIN_BY_PREFIX[prefix]
        expected_diff = DIFFICULTY_BY_INFIX[infix]
        if item.domain != expected_domain:
            issues.append(
                Issue(iid, f"domain {item.domain!r} does not match id prefix {prefix}")
            )
        if item.difficulty != expected_diff:
            issues.append(
                Issue(
                    iid,
                    f"difficulty {item.difficulty!r} does not match id infix {infix}",
                )
            )

    if item.domain not in DOMAINS:
        issues.append(Issue(iid, f"unknown domain {item.domain!r}"))
    if item.difficulty not in DIFFICULTIES:
        issues.append(Issue(iid, f"unknown difficulty {item.difficulty!r}"))
    if not item.subdomain.strip():
        issues.append(Issue(iid, "subdomain is empty"))
    if not item.learning_objective.strip():
        issues.append(Issue(iid, "learning_objective is empty"))
    if len(item.stem.split()) < 40:
        issues.append(Issue(iid, "stem is shorter than 40 words; likely under-specified"))
    if not item.assumptions:
        issues.append(Issue(iid, "assumptions field is empty"))
    if any(not a.strip() for a in item.assumptions):
        issues.append(Issue(iid, "an assumption string is empty"))
    if not item.uniqueness_check.strip():
        issues.append(Issue(iid, "uniqueness_check is required"))
    if not item.ambiguity_audit.strip():
        issues.append(Issue(iid, "ambiguity_audit is required"))
    if not item.difficulty_rationale.strip():
        issues.append(Issue(iid, "difficulty_rationale is required"))
    if not item.solution_derivation.strip():
        issues.append(Issue(iid, "solution_derivation is required"))
    if not item.solution_summary.strip():
        issues.append(Issue(iid, "solution_summary is required"))

    letters = list(item.options.keys())
    if letters != list(OPTION_LETTERS):
        issues.append(
            Issue(iid, f"options must be exactly {list(OPTION_LETTERS)} in order, got {letters}")
        )
    if len(item.options) != 10:
        issues.append(Issue(iid, f"expected 10 options, got {len(item.options)}"))

    norms = [_norm_text(v) for v in item.options.values()]
    if any(not n for n in norms):
        issues.append(Issue(iid, "an option is empty after normalization"))
    if len(set(norms)) != len(norms):
        issues.append(Issue(iid, "duplicate options after whitespace/case normalization"))

    if item.correct_option not in OPTION_LETTERS:
        issues.append(Issue(iid, f"correct_option {item.correct_option!r} is not a letter A–J"))

    rat_letters = list(item.distractor_rationales.keys())
    if rat_letters != list(OPTION_LETTERS):
        issues.append(
            Issue(
                iid,
                f"distractor_rationales must cover A–J in order, got {rat_letters}",
            )
        )

    n_key = 0
    n_dist = 0
    for letter, rat in item.distractor_rationales.items():
        if letter == item.correct_option:
            if rat.taxonomy != KEYED_TAG:
                issues.append(
                    Issue(iid, f"keyed option {letter} must use taxonomy {KEYED_TAG}")
                )
            n_key += 1
        else:
            if rat.taxonomy == KEYED_TAG:
                issues.append(
                    Issue(iid, f"non-keyed option {letter} is tagged {KEYED_TAG}")
                )
            elif rat.taxonomy not in DISTRACTOR_TAGS:
                issues.append(Issue(iid, f"option {letter} has unknown taxonomy {rat.taxonomy!r}"))
            n_dist += 1
        if not rat.why_chosen.strip() or not rat.why_wrong.strip():
            issues.append(Issue(iid, f"option {letter} is missing why_chosen or why_wrong"))

    if n_key != 1:
        issues.append(Issue(iid, f"expected exactly one keyed option, found {n_key}"))
    if n_dist != 9:
        issues.append(Issue(iid, f"expected nine distractor rationales, found {n_dist}"))

    if not (1 <= len(item.references) <= 5):
        issues.append(
            Issue(iid, f"expected 1–5 references, found {len(item.references)}")
        )
    for ref in item.references:
        if not ref.key.strip() or not ref.claim_supported.strip():
            issues.append(Issue(iid, "a reference is missing key or claim_supported"))

    ver = item.verification
    for label, text in (
        ("primary_solution", ver.primary_solution),
        ("independent_check", ver.independent_check),
        ("invariant_or_boundary_check", ver.invariant_or_boundary_check),
    ):
        if not text.strip():
            issues.append(Issue(iid, f"verification.{label} is empty"))

    if not item.misconception_tags:
        issues.append(Issue(iid, "misconception_tags is empty"))
    for tag in item.misconception_tags:
        if tag not in DISTRACTOR_TAGS:
            issues.append(Issue(iid, f"misconception tag {tag!r} is not in the taxonomy"))

    if "wikipedia" in item.stem.casefold() or "investopedia" in item.stem.casefold():
        issues.append(Issue(iid, "stem cites a source that is not allowed as a supporting reference"))

    return issues


def validate_rejected(item: RejectedItem) -> list[Issue]:
    issues: list[Issue] = []
    iid = item.id or "<missing-rejected-id>"
    if not re.match(r"^RJ-\d{2}-[a-z0-9_]+$", item.id or ""):
        issues.append(Issue(iid, f"rejected id {item.id!r} is not RJ-NN-slug"))
    if item.defect_class not in REJECTED_DEFECT_CLASSES:
        issues.append(Issue(iid, f"unknown defect_class {item.defect_class!r}"))
    if item.domain not in DOMAINS:
        issues.append(Issue(iid, f"unknown domain {item.domain!r}"))
    if item.difficulty_as_drafted not in DIFFICULTIES:
        issues.append(Issue(iid, f"unknown drafted difficulty {item.difficulty_as_drafted!r}"))
    if list(item.options.keys()) != list(OPTION_LETTERS):
        issues.append(Issue(iid, "rejected draft must still have options A–J"))
    if item.drafted_key not in OPTION_LETTERS and item.drafted_key != "NONE":
        issues.append(Issue(iid, f"drafted_key {item.drafted_key!r} is not A–J or NONE"))
    for field_name, text in (
        ("defect", item.defect),
        ("why_it_matters", item.why_it_matters),
        ("correction", item.correction),
        ("stem", item.stem),
    ):
        if not text.strip():
            issues.append(Issue(iid, f"{field_name} is empty"))
    return issues


def validate_corpus(
    items: list[AssessmentItem],
    rejected: list[RejectedItem] | None = None,
) -> list[Issue]:
    issues: list[Issue] = []
    ids = [it.id for it in items]
    if len(ids) != len(set(ids)):
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        issues.append(Issue("CORPUS", f"duplicate ids: {dupes}"))

    for it in items:
        issues.extend(validate_item(it))

    if len(items) != TARGET_COUNTS["total"]:
        issues.append(
            Issue("CORPUS", f"expected {TARGET_COUNTS['total']} accepted items, found {len(items)}")
        )

    by_diff = Counter(it.difficulty for it in items)
    for diff, n in TARGET_COUNTS["by_difficulty"].items():
        if by_diff[diff] != n:
            issues.append(Issue("CORPUS", f"expected {n} {diff} items, found {by_diff[diff]}"))

    # Answer-position leakage is a corpus-level assessment defect.
    # With 40 retained items and ten letters, require four keys per position.
    key_counts = Counter(it.correct_option for it in items)
    expected_per_key = TARGET_COUNTS["total"] // len(OPTION_LETTERS)
    for letter in OPTION_LETTERS:
        if key_counts[letter] != expected_per_key:
            issues.append(
                Issue(
                    "CORPUS",
                    f"expected {expected_per_key} keyed items at {letter}, found {key_counts[letter]}",
                )
            )

    ordered_keys = [it.correct_option for it in sorted(items, key=lambda x: x.id)]
    longest_run = 0
    run = 0
    prev = None
    for key in ordered_keys:
        run = run + 1 if key == prev else 1
        longest_run = max(longest_run, run)
        prev = key
    if longest_run > 2:
        issues.append(Issue("CORPUS", f"answer-position streak too long: {longest_run}"))

    by_domain = Counter(it.domain for it in items)
    for domain, n in TARGET_COUNTS["by_domain"].items():
        if by_domain[domain] != n:
            issues.append(
                Issue("CORPUS", f"expected {n} items in {domain}, found {by_domain[domain]}")
            )

    cells: dict[tuple[str, str], int] = defaultdict(int)
    for it in items:
        cells[(it.domain, it.difficulty)] += 1
    for domain in TARGET_COUNTS["by_domain"]:
        for diff, n in TARGET_COUNTS["per_domain_difficulty"].items():
            got = cells[(domain, diff)]
            if got != n:
                issues.append(
                    Issue(
                        "CORPUS",
                        f"expected {n} {diff} items in {domain}, found {got}",
                    )
                )

    if rejected is not None:
        rids = [it.id for it in rejected]
        if len(rids) != len(set(rids)):
            issues.append(Issue("REJECTED", f"duplicate rejected ids: {rids}"))
        for it in rejected:
            issues.extend(validate_rejected(it))
        present = {it.defect_class for it in rejected}
        missing = REJECTED_DEFECT_CLASSES - present
        if missing:
            issues.append(
                Issue("REJECTED", f"missing defect classes: {sorted(missing)}")
            )

    return issues


def assert_valid(items: list[AssessmentItem], rejected: list[RejectedItem] | None = None) -> None:
    issues = validate_corpus(items, rejected)
    if issues:
        body = "\n".join(str(i) for i in issues)
        raise ValidationError(body)
