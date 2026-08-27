# Compiler–Runner Verification — 2026-08-27

## Outcome

The harness now compiles and persists an auditable paper model before runner questions, and stores a separate machine-recoverable session state. Question selection is rule-governed rather than purely random. IDEA policy 1.1 adds a minimal checkability gate: normally one challenge or clarification, with no requirement for exhaustive deliberation. Selection policy 1.2 adds a transferability/reusability filter so default CLAIMS/EVIDENCE follow-up favors reusable scientific reasoning primitives over low-transfer paper-specific apparatus optimization.

## Architecture artifacts

- `protocols/model_compilation.md`
- `protocols/question_selection.md`
- `templates/paper_model.pending.toml`
- `templates/paper_session.state.toml`
- `scripts/validate_paper_model.py`
- `scripts/validate_session_state.py`

## SRP paper-model build

- Model: `papers/zhu_2023_srp_microscopy/model/paper_model.pending.toml`
- Version: 0.1.3
- Model SHA-256: `706E5E5642349F277D110F84475241C37E67232AFA9B5C9EC3CB42204B99AD2F`
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
| `paper_model.audit.v0.1.3.md` | 22/22 | Transferability/reusability filter and selection policy 1.2 |

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
- Unique next interaction cursor: `EVIDENCE.M3.awaiting_application_performance_link`.

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

## Current session checkpoint — event 10

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 10.
- Unique next interaction cursor: `CLAIMS.T0.awaiting_next_major_claim`.
- Pending prompt ID: `CLAIMS_ADD_T0_3`.

## Current session checkpoint — event 12

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 12.
- Unique next interaction cursor: `CLAIMS.H-C3.2.awaiting_resolution_calibration`.
- Pending prompt ID: `CLAIMS_EXPAND_H-C3.2_RESOLUTION`.

## Current session checkpoint — event 13

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 13.
- Unique next interaction cursor: `CLAIMS.H-C3.3.awaiting_spectral_fidelity_definition`.
- Pending prompt ID: `CLAIMS_EXPAND_H-C3.3_SPECTRAL_FIDELITY`.

## Current session checkpoint — event 14

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 14.
- Unique next interaction cursor: `CLAIMS.H-C3.3.awaiting_similarity_metric`.
- Pending prompt ID: `CLAIMS_CLARIFY_H-C3.3_SIMILARITY_METRIC`.

## Current session checkpoint — event 15

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 15.
- Unique next interaction cursor: `CLAIMS.H-C3.5.awaiting_speed_metric`.
- Pending prompt ID: `CLAIMS_EXPAND_H-C3.5_SPEED`.

## Current session checkpoint — event 16

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 16.
- Unique next interaction cursor: `CLAIMS.awaiting_finish_or_add`.
- Pending prompt ID: `CLAIMS_FINISH_OR_ADD`.

## Current session checkpoint — event 17

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 17.
- Unique next interaction cursor: `CLAIMS.awaiting_finish_confirmation`.
- Pending prompt ID: `CLAIMS_FINISH`.

## Current session checkpoint — event 18

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 18.
- Current stage: `evidence`.
- Revealed paper-claim IDs: `T0`, `M1`, `S1.1`, `S1.2`, `S1.3`, `M2`, `S2.1`, `S2.2`, `S2.3`, `M3`, `S3.1`, `S3.2`, `S3.3`.
- Unique next interaction cursor: `EVIDENCE.M1.awaiting_thermometry_validity`.
- Pending prompt ID: `EVIDENCE_M1_THERMOMETRY_VALIDITY`.

## Current session checkpoint — event 19

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 19.
- Unique next interaction cursor: `EVIDENCE.M1.awaiting_thermometry_controls`.
- Pending prompt ID: `EVIDENCE_M1_THERMOMETRY_CONFOUNDS`.

## Current session checkpoint — event 20

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 20.
- Unique next interaction cursor: `EVIDENCE.M1.awaiting_bleach_control_implementation`.
- Pending prompt ID: `EVIDENCE_M1_BLEACH_ONLY_CONTROL_IMPLEMENTATION`.

## Current session checkpoint — event 21

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 21.
- Unique next interaction cursor: `EVIDENCE.M2.awaiting_matched_sensitivity_comparison`.
- Pending prompt ID: `EVIDENCE_M2_MATCHED_SENSITIVITY_COMPARISON`.

## Current session checkpoint — event 22

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 22.
- Unique next interaction cursor: `EVIDENCE.M2.awaiting_bead_deconvolution`.
- Pending prompt ID: `EVIDENCE_M2_RESOLUTION_BEAD_DECONVOLUTION`.

## Current session checkpoint — event 23

- Canonical session-state audit: PASS — 15/15 checks.
- Event sequence: contiguous through event 23.
- Unique next interaction cursor: `EVIDENCE.M3.awaiting_application_performance_link`.
- Pending prompt ID: `EVIDENCE_M3_APPLICATION_PERFORMANCE_LINK`.

## Code checks

- PASS — both validator scripts compile under Python 3.12.
- PASS — paper-model TOML parses with the Python standard library.
- PASS — session-state TOML parses with the Python standard library.
- PASS — repository text scan found no trailing whitespace.
- PASS — `git diff --cached --check` completed without errors.

## Remaining limitations

- The paper model is pending and cannot be automatically reused by a later session until human approval.
- Because the current human disclosed being a paper author, this trial cannot validate spoiler control for a genuinely unread participant.
