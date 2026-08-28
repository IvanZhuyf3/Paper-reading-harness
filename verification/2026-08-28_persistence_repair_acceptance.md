# Persistence Repair Acceptance — 2026-08-28

## Outcome

**PASS — ready to start a new paper session.**

Luna implemented the deterministic persistence repair in commits `082fc03`, `3d7eb91`, `2a44428`, and `b1cbc5c`. The primary agent then independently reviewed the implementation, restored the exact event-8 prompt, and added missing terminal-disposition and human-evidence-parent regression coverage.

## Repaired behavior

- Canonical TOML events are the sole interaction source.
- Every event stores sequence, prompt ID, exact prompt text, stage, policy version, and verbatim human response.
- The main Markdown audit timeline is generated deterministically in event-sequence order.
- Renderer `--check` detects stale or reordered Markdown.
- Stage dispositions distinguish `completed`, `skipped`, `not_applicable`, and `in_progress`.
- The completed SRP session records independent reading as `not_applicable`, DELTA as `skipped`, no pending prompt, and terminal cursor `COMPLETE.terminal`.
- Human record IDs, parents, claim targets, evidence targets, and evidence-parent links are validated.
- Revealed paper evidence must resolve to the frozen model.
- Session paper-evidence design fields must exactly match the frozen model, and result details are forbidden.
- Finished-stage records require explicit terminal status.
- Asked IDs must exactly equal responded events plus the one pending prompt, or only responded events for a terminal session.
- Event-level policy provenance preserves the 1.1 to 1.2 transition.
- Event-25/26 files remain preserved but are correctly labeled reconstructed and not independently reproducible.
- Ordinary within-stage turns may be batched; immutable audits and commits are reserved for boundaries, failures, policy changes, or explicit checkpoints.

## Independent verification

- Python: 3.12.13.
- Python compilation: PASS.
- Reusable regression tests: PASS — 13/13.
- Paper-model validation: PASS — 22/22.
- Session-state validation: PASS — 39/39.
- Markdown renderer parity: PASS.
- Markdown chronology: PASS — events 1–28.
- Terminal stage semantics: PASS.
- Frozen paper-evidence parity: PASS.
- Result-detail boundary: PASS.
- Git whitespace/error check: PASS.

Saved detailed reports:

- `verification/2026-08-28_session_tests.txt`
- `verification/2026-08-28_session_validation.txt`
- `verification/2026-08-28_paper_model_validation.txt`

## Remaining scope limitations

- The SRP paper model remains pending human approval and is not eligible for automatic cross-session reuse.
- The completed test session involved a paper author, so it does not validate spoiler control for a genuinely unread participant.
- Scientific quality remains a human-review concern; the validators enforce persistence, identity, visibility, and structural invariants rather than scientific truth.
