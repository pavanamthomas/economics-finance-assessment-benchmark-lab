"""CLI: structural validation of the on-disk corpus."""

from __future__ import annotations

import sys

from efablab.loader import load_items, load_rejected
from efablab.validator import validate_corpus


def main() -> int:
    items = load_items()
    rejected = load_rejected()
    issues = validate_corpus(items, rejected)
    if issues:
        print(f"{len(issues)} validation issue(s):")
        for issue in issues:
            print(f"  {issue}")
        return 1
    print(f"ok: {len(items)} accepted items, {len(rejected)} rejected drafts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
