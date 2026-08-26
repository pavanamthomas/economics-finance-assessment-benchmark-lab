from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGET_KEYS = {
    "MM-M-01": "A", "MM-M-02": "C", "MM-H-01": "D", "MM-H-02": "E",
    "MM-H-03": "F", "MM-E-01": "G", "MM-E-02": "H", "MM-E-03": "I",
    "MP-M-01": "J", "MP-M-02": "B", "MP-H-01": "A", "MP-H-02": "C",
    "MP-H-03": "D", "MP-E-01": "E", "MP-E-02": "F", "MP-E-03": "G",
    "BF-M-01": "H", "BF-M-02": "I", "BF-H-01": "J", "BF-H-02": "B",
    "BF-H-03": "A", "BF-E-01": "C", "BF-E-02": "D", "BF-E-03": "E",
    "UE-M-01": "F", "UE-M-02": "G", "UE-H-01": "H", "UE-H-02": "I",
    "UE-H-03": "J", "UE-E-01": "B", "UE-E-02": "A", "UE-E-03": "C",
    "TD-M-01": "D", "TD-M-02": "E", "TD-H-01": "F", "TD-H-02": "G",
    "TD-H-03": "H", "TD-E-01": "I", "TD-E-02": "J", "TD-E-03": "B",
}


def swap_section_bodies(text: str, section: str, a: str, b: str) -> str:
    if a == b:
        return text
    lines = text.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.rstrip("\r\n") == f"{section}:")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.strip() and not line.startswith((" ", "\t")):
            end = i
            break
    entry_starts: list[tuple[str, int]] = []
    for i in range(start + 1, end):
        m = re.match(r"^  ([A-J]):(?:\s*>|\s*)\r?\n?$", lines[i])
        if m:
            entry_starts.append((m.group(1), i))
    labels = [x[0] for x in entry_starts]
    if labels != list("ABCDEFGHIJ"):
        raise RuntimeError(f"{section}: expected A-J, got {labels}")
    bodies: dict[str, list[str]] = {}
    label_lines: dict[str, str] = {}
    for n, (label, idx) in enumerate(entry_starts):
        nxt = entry_starts[n + 1][1] if n + 1 < len(entry_starts) else end
        label_lines[label] = lines[idx]
        bodies[label] = lines[idx + 1:nxt]
    bodies[a], bodies[b] = bodies[b], bodies[a]
    rebuilt = lines[: start + 1]
    for label, _ in entry_starts:
        rebuilt.append(label_lines[label])
        rebuilt.extend(bodies[label])
    rebuilt.extend(lines[end:])
    return "".join(rebuilt)


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"replacement anchor not found for {label}: {old[:100]!r}")
    return text.replace(old, new)


def edit_item(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^id:\s*([^\s]+)\s*$", text, flags=re.MULTILINE)
    if not m:
        raise RuntimeError(f"missing id in {path}")
    iid = m.group(1)
    target = TARGET_KEYS[iid]
    current = re.search(r"^correct_option:\s*([A-J])\s*$", text, flags=re.MULTILINE)
    if not current:
        raise RuntimeError(f"missing correct_option in {iid}")
    source = current.group(1)
    if source != target:
        text = swap_section_bodies(text, "options", source, target)
        text = swap_section_bodies(text, "distractor_rationales", source, target)
        text = re.sub(r"^correct_option:\s*[A-J]\s*$", f"correct_option: {target}", text, count=1, flags=re.MULTILINE)

    # Substantive corrections identified in the manual adversarial audit.
    if iid == "MP-E-01":
        text = must_replace(
            text,
            "After a 10 percent exogenous price drop, each bank's\n  capital ratio is still above its target. Each bank's rule is: sell\n  just enough of the security to restore the target leverage, taking\n  the current price as given.",
            "After a 10 percent exogenous price drop, each bank's\n  capital ratio remains above its regulatory minimum but falls below\n  its stricter internal target. Each bank's rule is: sell just enough\n  of the security to restore that internal target, taking the current\n  price as given.",
            iid,
        )
        text = must_replace(
            text,
            "At P1\n  every ratio is above target and above the micro minimum.",
            "At P1\n  every ratio is above the micro minimum but below the stricter internal target.",
            iid,
        )
    elif iid == "MP-H-02":
        text = text.replace("debt-service-to-income\n  (flow/ability-to-pay)", "debt-service-to-income (DSTI)\n  (flow/ability-to-pay)")
        text = text.replace("debt-service-to-income ratio", "debt-service-to-income (DSTI) ratio")
        text = text.replace("low DTI\n  (or DSTI)", "low DSTI")
        text = text.replace("high DTI\n  (or DSTI)", "high DSTI")
        text = text.replace("DTI/DSTI", "DSTI")
        text = re.sub(r"\bDTI\b", "DSTI", text)
        text = text.replace("subdomain: ltv_dti_complementarity", "subdomain: ltv_dsti_complementarity")
    elif iid == "TD-M-01":
        text = must_replace(
            text,
            "p = dy/dx along x y = k is y/x.",
            "For a sale of X into the pool, the marginal Y received per additional X is p = -dy/dx = y/x along x y = k.",
            iid,
        )
    elif iid == "TD-H-03":
        text = text.replace("One whale holds 30 percent of\n  supply", "One whale holds 15 percent of\n  supply")
        text = text.replace("whale's 30 percent", "whale's 15 percent")
        text = text.replace("30 percent cannot", "15 percent cannot")
        text = text.replace("30 percent is large", "15 percent is still material")
        text = text.replace("30 percent < 40", "15 percent < 40")
        text = text.replace("30/42 ≈ 71 percent", "15/42 ≈ 36 percent")
        text = text.replace("30 > 40/2", "15 > 40/2")
        text = text.replace("30 < 40.", "15 < 40.")
        text = text.replace("A 30 percent whale", "A 15 percent whale")
    elif iid == "MM-H-02":
        text = must_replace(
            text,
            "Spread = 0.20, equal to μ, which is already the adverse-selection discount.",
            "Spread = 0.10, equal to μ/2, because only half of informed arrival probability belongs on each side of the quote.",
            iid,
        )
        text = text.replace("μ = 0.20 numerically equals the spread, so μ looks like the answer.", "Splitting μ equally across bid and ask looks like a natural half-spread calculation.")
        text = text.replace("Equality with μ is an artefact of π = ½ and v ∈ {0,1}. The object\n      is ask − bid = E[v|buy] − E[v|sell], not μ itself. If π were not\n      ½, the spread would not equal μ.", "The two conditional expectations must be computed by Bayes. The spread is 0.20; halving μ is not the quote-setting rule.")
    elif iid == "MM-H-03":
        text = must_replace(
            text,
            "The desk's mandate, as written, is \"minimise shortfall versus VWAP.\" The\n  desk can choose when to trade inside the day.",
            "The desk's mandate, as written, is \"minimise shortfall versus VWAP.\" The\n  investment decision, however, is to complete the position before earnings\n  while minimising implementation shortfall relative to the arrival decision price.\n  The desk can choose when to trade inside the day.",
            iid,
        )
    elif iid == "BF-E-01":
        text = must_replace(
            text,
            "Show that changing the reference point can reverse whether an\n  outcome is coded as a gain or a loss, and therefore can reverse\n  the predicted risk attitude, so uniqueness of a CPT prediction\n  requires a stated reference.",
            "Show that changing the reference point changes gain/loss coding\n  and can change a CPT choice; a unique keyed prediction therefore\n  requires the reference point and the relevant curvature and\n  probability-weighting parameters to be stated.",
            iid,
        )
        text = must_replace(
            text,
            "Under TK92 value-function\n  curvature (concave gains, convex losses) and a given λ, the\n  predicted choice between the gamble and the lock-in is not the\n  same for every R. A commentator says the prediction is unique\n  because \"the stock is at 80, so the reference is 80.\" Which\n  statement is right?",
            "Under TK92 value-function curvature (concave gains, convex losses)\n  the gain/loss coding changes with R. The exact curvature and probability-\n  weighting parameters are not otherwise supplied. A commentator says the\n  prediction is unique because \"the stock is at 80, so the reference is 80.\"\n  Which statement is right?",
            iid,
        )
        old_b = "Coding of 70, 80, 90 as gains or losses depends on R. Under R1 the lock-in at 80 is still a loss relative to 100, and the gamble is in the loss domain (convex v, risk-seeking). Under R2 both the lock-in and the gamble are evaluated around 80 (mixed or small-gain/small-loss). Under R3 everything is still a shortfall from 110. The commentator's uniqueness claim is false; a CPT prediction without a stated reference is not a unique key."
        new_b = "Coding of 70, 80, 90 depends on R. Under R1 = 100 and R3 = 110 all three outcomes are in the loss domain; under R2 = 80 the lock-in is zero and the gamble spans a loss and a gain. These are different CPT problems. The current price does not select the reference point by itself, and without a stated reference plus the relevant curvature and weighting parameters there is no unique choice key."
        text = must_replace(text, old_b, new_b, iid)
        text = must_replace(
            text,
            "Reference dependence is not a unique map from the current price\n  to a choice. Different R recode the same cash outcomes. A keyed\n  CPT item must state R.",
            "Reference dependence is not a unique map from the current price\n  to a choice. Different R recode the same cash outcomes. A keyed\n  CPT item must state R and enough preference/weighting parameters\n  to make the resulting choice unique.",
            iid,
        )
    elif iid == "BF-E-02":
        text = must_replace(
            text,
            "The primary, fully observed outcome is the object the design identified. Three uncorrected secondaries, one of them on a selected survey sample whose response co-moves with treatment, do not restore that object. Attrition here is not a smaller i.i.d. sample; it is differential selection. Multiple testing plus selected outcomes can manufacture three 5 percent stars.",
            "Randomisation identifies the ITT for the fully observed primary outcome. The survey secondary is a different estimand and differential response makes its observed-sample contrast selection-sensitive. Testing 20 outcomes without a multiplicity plan separately inflates false-positive risk. Neither issue turns the three secondary stars into replications of the null primary result.",
            iid,
        )
        text = must_replace(
            text,
            "The identified object is the planned, fully observed primary.\n  Stars on selected secondaries are not a replication of that\n  object. Attrition that differs by arm is selection, not merely\n  n ↓.",
            "Keep three questions separate: the ITT on the fully observed\n  primary, selection into the survey outcome, and multiplicity across\n  reported outcomes. None is repaired merely by counting three stars.",
            iid,
        )
    elif iid == "UE-E-02":
        text = must_replace(
            text,
            "City P has high wages and high rents. City A has low wages and\n  high rents. City U has high wages and low rents.",
            "Three otherwise comparable cities have similar housing-supply\n  elasticities and one dominant local shock each. City P has high wages\n  and high rents. City A has low wages and high rents. City U has high\n  wages and low rents.",
            iid,
        )
        text = must_replace(
            text,
            "P (high w, high R) is the productivity-like configuration. A (low w, high R) is amenity-like. U (high w, low R) is disamenity-like, or a productivity place with very elastic housing, and is *not* the same object as P. Wages alone do not rank productivity.",
            "Under the stated comparability assumptions, P (high w, high R) is the productivity-like configuration, A (low w, high R) is amenity-like, and U (high w, low R) is disamenity-like. The wage-rent pair, not wages alone, carries the spatial-equilibrium information.",
            iid,
        )
        text = text.replace("Housing supply elasticity can differ; that is why U is not a pure productivity ranking.", "Housing-supply elasticity is comparable across the three stylised cities; relaxing that assumption would weaken this classification.")
    elif iid == "UE-H-03":
        text = must_replace(
            text,
            "A univariate regression of price on test scores confounds school quality with correlated amenities and with sorting on unobserved household tastes and income. The coefficient is not identified as WTP for schools. Boundary discontinuity designs (Black 1999 style) exist because of this problem, not as decoration.",
            "A univariate regression of price on test scores bundles school quality with correlated neighbourhood amenities and peer composition; household sorting contributes to that bundling. Rosen does not turn that reduced-form coefficient into causal marginal WTP. Boundary discontinuity designs (Black 1999 style) are used to obtain cleaner school-quality variation, not as decoration.",
            iid,
        )
    elif iid == "TD-E-02":
        text = text.replace("the\n  oracle is a 30-minute TWAP that has not yet moved; HF computed\n  on the oracle remains above 1", "the\n  oracle is a 30-minute TWAP that has moved only slightly; HF computed\n  on the oracle remains above 1")
        text = text.replace("the oracle is designed not to follow a two-minute crash", "the long-window oracle is designed to damp a two-minute move and therefore lags a genuine crash")
        text = text.replace("that variable is behind a crash: liquidations\n  that would restore HF on the spot do not trigger", "that variable lags a crash: liquidations\n  that would restore HF on the spot do not yet trigger")
    elif iid == "TD-E-03":
        text = must_replace(
            text,
            "While the transaction sits in a public\n  mempool, a searcher can (in a textbook ordering model) place a\n  buy before it and a sell after it. The user's fill is worse than\n  the pre-trade spot by approximately the user's own price impact;\n  the searcher's round-trip collects a corresponding wedge.",
            "While the transaction sits in a public\n  mempool, a searcher can (in a textbook ordering model) place a\n  buy before it and a sell after it. Abstracting from gas/priority fees\n  and competition, and provided the user's slippage bound leaves enough\n  room, the ordering can worsen the user's fill and let the searcher\n  extract part of the authorised slippage wedge.",
            iid,
        )
        text = text.replace("transferring part of the slippage the user authorised.", "potentially transferring part of the slippage the user authorised, conditional on execution costs and competition.")

    path.write_text(text, encoding="utf-8")


def update_text_file(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        text = must_replace(text, old, new, str(path.relative_to(ROOT)))
    path.write_text(text, encoding="utf-8")


def main() -> None:
    item_paths = sorted((ROOT / "items").rglob("*.yaml"))
    if len(item_paths) != 40:
        raise RuntimeError(f"expected 40 accepted item files, found {len(item_paths)}")
    ids = set()
    for path in item_paths:
        m = re.search(r"^id:\s*([^\s]+)\s*$", path.read_text(encoding="utf-8"), flags=re.MULTILINE)
        if m:
            ids.add(m.group(1))
    if ids != set(TARGET_KEYS):
        raise RuntimeError(f"target-key map mismatch: missing={set(TARGET_KEYS)-ids}, extra={ids-set(TARGET_KEYS)}")
    for path in item_paths:
        edit_item(path)

    update_text_file(ROOT / "README.md", [
        ("40 accepted 10-option items plus 11 rejected drafts", "40-item self-directed 10-option corpus retained after internal validation, plus 11 rejected drafts"),
        ("40 accepted items (10 Medium, 15 Hard, 15 Expert), eight in each domain:", "40 retained items (10 Medium, 15 Hard, 15 Expert), eight in each domain. The answer-key positions are deliberately balanced across A–J to prevent positional leakage:"),
        ("items/                  accepted YAML, one file per id", "items/                  retained YAML, one file per id"),
    ])

    checklist = ROOT / "MANUAL_REVIEW_CHECKLIST.md"
    ctext = checklist.read_text(encoding="utf-8")
    addition = """

## Answer-position and cue audit

- [ ] Key positions are balanced at corpus level; a solver cannot gain information from letter frequency or same-letter streaks.
- [ ] The correct option is not systematically longer, more qualified, more grammatical, or more numerically precise than the distractors.
- [ ] The keyed option does not uniquely repeat wording from the stem or contain explanation that belongs in the solution.
- [ ] Denominators, timing conventions, price conventions, and equilibrium concepts are explicit enough that a reasonable alternate reading cannot rescue another option.
- [ ] Ask explicitly: what is the strongest alternative option, and what smallest assumption change would make it correct?
- [ ] Claim-level citation check: the cited source supports the decisive proposition, not merely the topic.
"""
    if "## Answer-position and cue audit" not in ctext:
        checklist.write_text(ctext.rstrip() + addition + "\n", encoding="utf-8")

    failures = ROOT / "FAILURES_AND_CORRECTIONS.md"
    ftext = failures.read_text(encoding="utf-8")
    addition = """

## 9. Answer-position leakage across the retained corpus

**What failed.** Every retained item used the same keyed letter. The economics could still be correct, but the corpus leaked the answer position and made letter-frequency guessing rational.

**How it was detected.** A corpus-level adversarial audit counted `correct_option` rather than reading items one at a time.

**What changed.** The 40 retained items were re-keyed without changing their substantive option sets: keyed and distractor bodies were permuted consistently, producing exactly four keys for each letter A–J. `validate_corpus` and `tests/test_corpus.py` now enforce the distribution.

**Why this matters.** Item validity includes presentation. A perfect derivation does not rescue a benchmark whose answer positions reveal the key.

## 10. Substantive wording and modelling repairs from the same audit

The audit also repaired several model-level defects: internal-target versus regulatory-minimum language in `MP-E-01`; DSTI terminology in `MP-H-02`; the sign of the CPAMM derivative in `TD-M-01`; governance arithmetic in `TD-H-03`; a duplicated correct numerical spread in `MM-H-02`; benchmark-object visibility in `MM-H-03`; under-parameterised CPT language in `BF-E-01`; separation of multiplicity from attrition in `BF-E-02`; comparability assumptions in `UE-E-02`; hedonic-identification wording in `UE-H-03`; TWAP-lag wording in `TD-E-02`; and explicit cost/competition conditions in `TD-E-03`.

These are recorded because a useful benchmark should expose its corrections rather than imply that the first draft was perfect.
"""
    if "## 9. Answer-position leakage" not in ftext:
        failures.write_text(ftext.rstrip() + addition + "\n", encoding="utf-8")

    qpath = ROOT / "questions.md"
    qtext = qpath.read_text(encoding="utf-8")
    qtext = qtext.replace("high-DTI loans", "high-DSTI loans")
    qtext = qtext.replace("If the reference is locked at the purchase price, a unique (loss-domain) prediction can be keyed. The item exists because that lock was missing in a draft.", "Locking the reference at the purchase price fixes the gain/loss domain, but a unique choice still requires the relevant curvature and probability-weighting parameters. The item exists because reference-point ambiguity was one of the missing pieces in a draft.")
    qpath.write_text(qtext, encoding="utf-8")

    validator = ROOT / "src/efablab/validator.py"
    vtext = validator.read_text(encoding="utf-8")
    anchor = """    by_domain = Counter(it.domain for it in items)\n    for domain, n in TARGET_COUNTS[\"by_domain\"].items():\n"""
    insert = """    # Answer-position leakage is a corpus-level assessment defect.\n    # With 40 retained items and ten letters, require four keys per position.\n    key_counts = Counter(it.correct_option for it in items)\n    expected_per_key = TARGET_COUNTS[\"total\"] // len(OPTION_LETTERS)\n    for letter in OPTION_LETTERS:\n        if key_counts[letter] != expected_per_key:\n            issues.append(\n                Issue(\n                    \"CORPUS\",\n                    f\"expected {expected_per_key} keyed items at {letter}, found {key_counts[letter]}\",\n                )\n            )\n\n    ordered_keys = [it.correct_option for it in sorted(items, key=lambda x: x.id)]\n    longest_run = 0\n    run = 0\n    prev = None\n    for key in ordered_keys:\n        run = run + 1 if key == prev else 1\n        longest_run = max(longest_run, run)\n        prev = key\n    if longest_run > 2:\n        issues.append(Issue(\"CORPUS\", f\"answer-position streak too long: {longest_run}\"))\n\n""" + anchor
    if "Answer-position leakage is a corpus-level assessment defect" not in vtext:
        vtext = must_replace(vtext, anchor, insert, "validator")
        validator.write_text(vtext, encoding="utf-8")

    tpath = ROOT / "tests/test_corpus.py"
    ttext = tpath.read_text(encoding="utf-8")
    ttext = ttext.replace("import re\n", "import re\nfrom collections import Counter\n")
    test_add = """


def test_key_positions_are_balanced() -> None:
    counts = Counter(it.correct_option for it in load_items())
    assert counts == Counter({letter: 4 for letter in "ABCDEFGHIJ"})
"""
    if "test_key_positions_are_balanced" not in ttext:
        tpath.write_text(ttext.rstrip() + test_add + "\n", encoding="utf-8")

    reviewer = ROOT / "REVIEWER_GUIDE.md"
    reviewer.write_text("""# Reviewer guide\n\nThis is a short entry point into five flagship items. It is not a substitute for reading the YAML, derivations, references, and failure log.\n\n## Market microstructure — `MM-E-01`\n\n**Question:** When does a statistically attractive mark cease to be economically executable?\n\n**Decisive assumption:** distinguish mid-mark, touch, and finite-depth execution, with hidden size excluded.\n\n**Strongest distractor:** the answer that treats a non-executable mark as P&L.\n\n**Independent check:** reconstruct the executable book and compare the finite fill with the quoted/mid marks.\n\n**Smallest answer-flip:** reduce spread/depth costs enough that the executable book becomes positive; the mid-only claim still remains non-executable.\n\n## Macroprudential policy — `MP-E-01`\n\n**Question:** Can individually reasonable balance-sheet repair create a system-level constraint violation?\n\n**Decisive assumption:** each bank takes price as given while aggregate sales move the common-security price.\n\n**Strongest distractor:** the claim that a bank above the regulatory minimum cannot rationally sell. The repaired stem separates the stricter internal target from the regulatory minimum.\n\n**Independent check:** flatten inverse demand. The price externality and the Nash-versus-freeze wedge disappear.\n\n**Smallest answer-flip:** make aggregate inverse demand flat.\n\n## Behavioral finance / experimental economics — `BF-E-01`\n\n**Question:** Is the current market price enough to select a unique CPT choice?\n\n**Decisive assumption:** the reference point and the relevant value/weighting parameters must be stated.\n\n**Strongest distractor:** the current-price-as-reference shortcut.\n\n**Independent check:** recode the same 70/80/90 outcomes under purchase-price, expectations-based, and goal references.\n\n**Smallest answer-flip:** specify a reference plus sufficient curvature/weighting parameters to make one choice unique.\n\n## Urban economics — `UE-H-01`\n\n**Question:** Who captures an amenity gain in open versus closed city equilibrium?\n\n**Decisive assumption:** whether population or utility is the margin that clears.\n\n**Strongest distractor:** 'amenities are good, therefore residents are better off in both models.'\n\n**Independent check:** in the open-city limit, pin utility to the outside option and let rent/population adjust.\n\n**Smallest answer-flip:** close migration; utility becomes endogenous and incumbents can retain part of the gain.\n\n## Tokenomics / DeFi — `TD-E-01`\n\n**Question:** Which AMM price is being asked for: pre-trade marginal, finite-trade average, or post-trade marginal?\n\n**Decisive assumption:** fee-free constant-product pool and an explicitly finite trade.\n\n**Strongest distractor:** using the initial marginal price as the finite fill.\n\n**Independent check:** closed form, path integral, and geometric mean of endpoint marginal prices agree on the average execution price.\n\n**Smallest answer-flip:** take trade size to zero; the three prices collapse.\n\n## What the automated checks do not prove\n\nBalanced key positions, schema checks, and numerical identities remove detectable implementation defects. They do not prove that a qualitative economic key is true. The remaining standard is adversarial manual review: attempt to rescue the strongest distractor under the stated assumptions, verify the decisive claim against the cited source, and state the smallest assumption change that would alter the key.\n""", encoding="utf-8")

    gitignore = ROOT / ".gitignore"
    gtext = gitignore.read_text(encoding="utf-8")
    if ".cursor/" not in gtext:
        gitignore.write_text(gtext.rstrip() + "\n.cursor/\n", encoding="utf-8")
    cursor_env = ROOT / ".cursor/environment.json"
    if cursor_env.exists():
        cursor_env.unlink()

    # Remove the one-time migration machinery from the final tree.
    workflow = ROOT / ".github/workflows/apply-integrity-audit.yml"
    if workflow.exists():
        workflow.unlink()
    Path(__file__).unlink()


if __name__ == "__main__":
    main()
