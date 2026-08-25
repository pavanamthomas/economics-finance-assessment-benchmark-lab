"""Load the corpus, run structural validation, print a short inventory."""

from __future__ import annotations

from collections import Counter

from efablab.checks import run_named_check
from efablab.loader import load_items, load_rejected
from efablab.validator import assert_valid


def main() -> None:
    items = load_items()
    rejected = load_rejected()
    assert_valid(items, rejected)
    print(f"accepted items: {len(items)}")
    print(f"rejected drafts: {len(rejected)}")
    print("by domain:")
    for domain, n in sorted(Counter(it.domain for it in items).items()):
        print(f"  {domain}: {n}")
    print("by difficulty:")
    for diff, n in sorted(Counter(it.difficulty for it in items).items()):
        print(f"  {diff}: {n}")
    print("flagship numerical checks:")
    for it in items:
        if not it.numerical_check:
            continue
        spec = it.numerical_check
        got = run_named_check(spec["kind"], spec["params"])
        print(f"  {it.id} {spec['kind']}: {got}")
    print("ok")


if __name__ == "__main__":
    main()
