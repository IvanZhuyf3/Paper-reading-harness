# BABYSITTING Implementation Acceptance — 2026-08-29

## Outcome

PASS — BABYSITTING is available only from a validated model-side disclosure
packet, freezes its source-anchored claim/terminology/edge assets into the
runtime state, and preserves the ordinary training modes.

## Verification

- `python scripts/validate_paper_model.py papers/li_2026_ft_opt/model/paper_model.pending.toml`: PASS (46/46 checks).
- `python scripts/validate_paper_model.py papers/zhu_2023_srp_microscopy/model/paper_model.pending.toml`: PASS (23/23 checks; legacy model remains valid and BABYSITTING unavailable).
- `python -m unittest discover -s scripts -p 'test_*.py'`: PASS (26/26 tests).
- Fresh BABYSITTING session-state validation: PASS (54/54 checks).
- Fresh CORE session-state validation against the upgraded model: PASS (41/41 checks).

## Scope notes

The mode remains in the existing `knowledge` stage. Its start packet discloses
all 26 source-anchored claim IDs, 14 terminology IDs, and 25 logical-edge IDs;
it reveals no evidence IDs or result details. Runtime state records selected,
explained, verified, unresolved, and active-check cursor fields. No SQLite
importer or alternate persistence backend was added.
