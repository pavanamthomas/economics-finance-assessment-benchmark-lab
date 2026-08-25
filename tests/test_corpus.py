"""Corpus structure: counts, uniqueness, references, rejected coverage."""

from __future__ import annotations

import re
from pathlib import Path

from efablab.loader import REPO_ROOT, load_items, load_rejected
from efablab.validator import validate_corpus


BIB = REPO_ROOT / "REFERENCES.bib"
BIB_KEY = re.compile(r"^@\w+\{([^,]+),", re.MULTILINE)


def test_corpus_validates() -> None:
    issues = validate_corpus(load_items(), load_rejected())
    assert issues == [], "\n".join(str(i) for i in issues)


def test_reference_keys_exist_in_bib() -> None:
    bib_keys = set(BIB_KEY.findall(BIB.read_text(encoding="utf-8")))
    missing: list[str] = []
    for item in load_items() + load_rejected():  # type: ignore[operator]
        for ref in item.references:
            if ref.key not in bib_keys:
                missing.append(f"{item.id}:{ref.key}")
    assert not missing, f"keys not in REFERENCES.bib: {missing}"


def test_no_wikipedia_or_investopedia_in_bib() -> None:
    text = BIB.read_text(encoding="utf-8").casefold()
    assert "wikipedia" not in text
    assert "investopedia" not in text


def test_accepted_files_match_ids() -> None:
    for path in sorted((REPO_ROOT / "items").rglob("*.yaml")):
        assert path.stem in {it.id for it in load_items()}


def test_rejected_defect_classes_unique() -> None:
    classes = [it.defect_class for it in load_rejected()]
    assert len(classes) == len(set(classes))
