# Async Persistence Acceptance Review — 2026-08-27

## Outcome

**Conditional pass.** The asynchronous scribe preserved the scientific content and canonical recovery state well, but the human-readable audit chronology and two reconstructed checkpoint reports are not reliable enough for unconditional acceptance.

## Scope

- Scribe commits reviewed: `17f847c` through `f6fdea0`.
- Canonical session state: `papers/zhu_2023_srp_microscopy/sessions/2026-08-27_core_training.state.toml`.
- Human-readable log: `papers/zhu_2023_srp_microscopy/sessions/2026-08-27_core_training.md`.
- Frozen paper model: version 0.1.3, selection policy 1.2, SHA-256 `706E5E5642349F277D110F84475241C37E67232AFA9B5C9EC3CB42204B99AD2F`.

## Passed checks

- PASS — user responses for events 8–27 are retained verbatim in the canonical TOML event stream.
- PASS — event sequence is contiguous through event 27.
- PASS — paper-model identity, source hashes, model version, policy version, and session pin agree.
- PASS — paper-model validator passes 22/22 mechanical checks.
- PASS — session-state validator passes its current 15/15 mechanical checks.
- PASS — human claim/evidence content is represented without paper-result values being inserted into the human rollout.
- PASS — the paper proof architecture copied into the session contains design, control, and anchor fields but no `result_detail` values or numerical outcomes.
- PASS — the transferability rule is stated abstractly in normative documents; the user's concrete examples remain in the session rather than becoming few-shot rules.
- PASS — repository worktree was clean and `git diff --check` passed at review time.

## Findings

### P1 — Markdown event chronology is wrong

The canonical TOML event stream is ordered correctly, but the Markdown log places event 24 after event 27 and after the independent-reading transition. The visible order is events 23, 25, 26, 27, then 24.

Impact:

- a human auditor reading only the Markdown log sees a false interaction order;
- compaction recovery is safe only because TOML is authoritative;
- later append operations can select a stale insertion point and repeat the problem.

Recommended design: treat TOML events as the single source of truth and deterministically regenerate the Markdown event projection by `sequence`, instead of independently patching both representations.

### P1 — Event-25 and event-26 checkpoint audits are not reproducible checkpoints

Events 25–27 were committed together in `8721499`. The event-25 and event-26 files were created afterward in `f6fdea0`; no corresponding state snapshots or commits exist for those intermediate states. Nevertheless, the files claim `PASS 15/15 at the event-25 checkpoint` and `PASS 15/15 at the event-26 checkpoint`.

These files are reconstructed summaries, not validator outputs against immutable checkpoint state. They should be labeled as reconstructed history, or accompanied by the exact state snapshot/hash they validate. A PASS audit should not be asserted against state that was not preserved.

### P2 — The 15/15 session validator has material blind spots

The current validator does not check:

- `revealed_paper_evidence_ids` against model evidence IDs;
- uniqueness and target resolution for human evidence/control/application records;
- equality of copied `paper_evidence_designs` to the frozen model;
- absence of paper `result_detail` fields in the session disclosure;
- parent/child status consistency;
- asked-prompt/event/pending-prompt correspondence;
- chronological order of the Markdown event log.

Therefore, 15/15 PASS is a valid statement about the checks implemented, but not evidence that the complete persisted session is internally consistent.

### P2 — Several terminal statuses are internally inconsistent

Examples in the canonical state:

- `H-C3.3` is `closed` while several immediate children remain `open`;
- `H-E-M3-APPLICATION-PERFORMANCE-LINK` remains `open/partial` although its feature-recognition child is closed and the EVIDENCE rollout is complete;
- `H-E-M1-THERMOMETRY` remains `human_designed` rather than receiving an explicit terminal disposition.

An unfinished human branch is allowed when the human ends a rollout, but the status should say `left_open_at_rollout_close` or equivalent. Plain `open` is ambiguous and could make a resumed selector treat it as eligible.

### P2 — Mid-session policy provenance is flattened

The session began under selection policy 1.1 and later changed to 1.2. Only the current top-level policy version is stored; individual events do not record which policy selected their prompt. Git history preserves the transition indirectly, but the session artifact alone does not.

Recommended design: store `selection_policy_version` on each prompt-selection event whenever a session permits live policy changes.

### P2 — Stage skipping has no faithful state representation

The user has now explicitly skipped DELTA. The current state machine and validator require completed stages to form a full prefix, but do not distinguish `completed` from `skipped`. Marking the session complete would either leave it stuck at independent reading or falsely record DELTA as completed.

Recommended design: persist per-stage disposition such as `completed`, `skipped`, or `not_applicable`, and validate ordering separately from completion semantics.

### P3 — Persistence granularity is heavier than needed

The scribe produced 20 per-event audit files and 18 commits after the initial human claim entry. This is recoverable but creates repository noise and background I/O without increasing scientific fidelity.

Recommended operating pattern:

1. update canonical TOML and regenerate Markdown asynchronously after every turn;
2. run a cheap canonical validation after every turn;
3. persist immutable audit reports and Git commits at stage boundaries, failures, policy changes, or explicit checkpoints;
4. batch ordinary within-stage turns.

## Acceptance summary

| Dimension | Result |
|---|---|
| Raw response fidelity | PASS |
| Scientific structure retention | PASS |
| Paper-model/source pinning | PASS |
| Spoiler/result-detail boundary | PASS |
| Canonical recovery state | PASS with validator limitations |
| Human-readable log chronology | FAIL |
| Historical checkpoint auditability | FAIL |
| Persistence efficiency | PARTIAL |

The asynchronous division of labor is worth keeping. Before relying on it for longer sessions, make TOML the sole event source, generate Markdown deterministically, strengthen evidence/status validation, and reduce audit/commit frequency.
