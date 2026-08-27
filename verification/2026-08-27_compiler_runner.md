# Compiler–Runner Verification — 2026-08-27

## Outcome

The harness now compiles and persists an auditable paper model before runner questions, and stores a separate machine-recoverable session state. Question selection is rule-governed rather than purely random. IDEA policy 1.1 adds a minimal checkability gate: normally one challenge or clarification, with no requirement for exhaustive deliberation.

## Architecture artifacts

- `protocols/model_compilation.md`
- `protocols/question_selection.md`
- `templates/paper_model.pending.toml`
- `templates/paper_session.state.toml`
- `scripts/validate_paper_model.py`
- `scripts/validate_session_state.py`

## SRP paper-model build

- Model: `papers/zhu_2023_srp_microscopy/model/paper_model.pending.toml`
- Version: 0.1.2
- Model SHA-256: `CB9953A2A72340F5B899F98A0C0322F32BA63EFA69A0605088237E52F9E7FAC3`
- Knowledge nodes: 6
- Claim nodes: 18
- Evidence nodes: 9
- Main source SHA-256: `B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09`
- Supplement SHA-256: `F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2`

## Preserved audit history

| Audit | Result | Purpose |
|---|---:|---|
| `paper_model.audit.preflight.md` | 18/19 | Initial graph/hash validation; compiler flags intentionally pending |
| `paper_model.audit.preflight2.md` | 20/21 | Supplement integrated; compiler flags intentionally pending |
| `paper_model.audit.v0.1.0.md` | 21/21 | First finalized mechanically valid model |
| `paper_model.audit.v0.1.1.md` | 21/21 | Author-source excerpts separated from agent interpretations |
| `paper_model.audit.v0.1.2.md` | 21/21 | IDEA minimal-checkability gate and selection policy 1.1 |

## Visual/source audit

- PASS — all 12 main-PDF pages rendered and inspected.
- PASS — the official 30-page supplement was added and hashed.
- PASS — supplement pages containing Figs. S2–S4, S8–S12, S17–S18, and Table S1 were rendered and inspected.
- PASS — prose anchors use PDF page + section + paragraph-opening words.
- PASS — figure/table/equation anchors use visible source labels.
- NOTE — the pending model preserves an apparent main-text/Fig. S18D numerical mismatch without agent resolution.

## Session recovery audit

- Canonical state: `papers/zhu_2023_srp_microscopy/sessions/2026-08-27_core_training.state.toml`
- Human-readable log: `papers/zhu_2023_srp_microscopy/sessions/2026-08-27_core_training.md`
- State audit: PASS — 15/15 checks.
- Pinned model hash: PASS.
- Selection seed/history: PASS.
- Completed-stage prefix: PASS.
- Revealed paper-claim references: PASS.
- Human-node parent graph: PASS.
- Unique next interaction cursor: `CLAIMS.H-C2.1.awaiting_architecture_claim`.

## Current session checkpoint — event 8

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 8.
- Unique next interaction cursor: `CLAIMS.T0.awaiting_next_major_claim`.
- Pending prompt ID: `CLAIMS_ADD_T0_2`.

## Current session checkpoint — event 9

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 9.
- Unique next interaction cursor: `CLAIMS.H-C2.1.awaiting_architecture_claim`.
- Pending prompt ID: `CLAIMS_EXPAND_H-C2.1_ARCHITECTURE`.

## Code checks

- PASS — both validator scripts compile under Python 3.12.
- PASS — paper-model TOML parses with the Python standard library.
- PASS — session-state TOML parses with the Python standard library.
- PASS — repository text scan found no trailing whitespace.
- PASS — `git diff --cached --check` completed without errors.

## Remaining limitations

- The paper model is pending and cannot be automatically reused by a later session until human approval.
- Because the current human disclosed being a paper author, this trial cannot validate spoiler control for a genuinely unread participant.
