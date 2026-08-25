"""CLI entry used by CI."""

from __future__ import annotations

import sys

from efablab.cli import main

if __name__ == "__main__":
    sys.exit(main())
