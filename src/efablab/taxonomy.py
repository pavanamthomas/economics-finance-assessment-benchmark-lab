"""Misconception tags used to engineer distractors.

Each incorrect option in an accepted item must carry one of these tags.
The tag is a claim about the error, not a claim that every examinee who
misses the item is making that error. Automated validation checks that
the tag is from this list and that the keyed option is not tagged as a
distractor. It cannot check that the economic story is true.
"""

from __future__ import annotations

DISTRACTOR_TAGS: frozenset[str] = frozenset(
    {
        "SIGN_REVERSAL",
        "NECESSARY_VS_SUFFICIENT",
        "LEVEL_VS_MARGINAL",
        "STOCK_VS_FLOW",
        "PARTIAL_VS_GENERAL_EQUILIBRIUM",
        "WRONG_INFORMATION_SET",
        "CORRELATION_VS_IDENTIFICATION",
        "TIMING_ERROR",
        "WRONG_DENOMINATOR",
        "INCORRECT_NORMALIZATION",
        "VIOLATED_ASSUMPTION",
        "APPROXIMATION_OUTSIDE_RANGE",
        "EQUILIBRIUM_FEEDBACK_IGNORED",
        "PRIVATE_VS_SOCIAL_COST",
        "NOMINAL_VS_REAL",
        "AVERAGE_VS_MARGINAL_EXECUTION_PRICE",
        "RISK_VS_UNCERTAINTY",
        "LIQUIDITY_VS_SOLVENCY",
        "RANKING_VS_PROBABILITY",
        "STATIC_VS_DYNAMIC_EFFECT",
    }
)

# The keyed option is not a distractor. It still occupies a letter slot
# in the rationales map so the audit is complete.
KEYED_TAG = "CORRECT_KEY"

DOMAINS: frozenset[str] = frozenset(
    {
        "algorithmic_trading_market_microstructure",
        "macroprudential_policy",
        "behavioral_finance_experimental_economics",
        "urban_economics",
        "tokenomics_defi",
    }
)

DIFFICULTIES: frozenset[str] = frozenset({"MEDIUM", "HARD", "EXPERT"})

OPTION_LETTERS: tuple[str, ...] = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")

ID_PATTERN = r"^(MM|MP|BF|UE|TD)-(M|H|E)-\d{2}$"

DOMAIN_BY_PREFIX = {
    "MM": "algorithmic_trading_market_microstructure",
    "MP": "macroprudential_policy",
    "BF": "behavioral_finance_experimental_economics",
    "UE": "urban_economics",
    "TD": "tokenomics_defi",
}

DIFFICULTY_BY_INFIX = {
    "M": "MEDIUM",
    "H": "HARD",
    "E": "EXPERT",
}

# Target counts. Tests fail if the accepted corpus drifts from this.
TARGET_COUNTS = {
    "total": 40,
    "by_difficulty": {"MEDIUM": 10, "HARD": 15, "EXPERT": 15},
    "by_domain": {
        "algorithmic_trading_market_microstructure": 8,
        "macroprudential_policy": 8,
        "behavioral_finance_experimental_economics": 8,
        "urban_economics": 8,
        "tokenomics_defi": 8,
    },
    "per_domain_difficulty": {"MEDIUM": 2, "HARD": 3, "EXPERT": 3},
}
