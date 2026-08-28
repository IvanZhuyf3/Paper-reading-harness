# Transition-Packet and Runtime Persistence Acceptance — 2026-08-28

## Outcome

PASS — reusable paper-model assets are separated from local training rollouts,
and validated stage-start packets are available for fast interactive transitions.

## Changes

- Paper model `0.2.0` adds five prevalidated transition packets: IDEA, CLAIMS,
  EVIDENCE, independent reading, and DELTA.
- New sessions copy those packets into `prefilled_transition_packets` and the
  session validator rejects packet drift or schema changes.
- Human-dependent comparisons remain dynamic slots; transition packets contain
  no paper result details.
- `papers/*/sessions/` is Git-ignored. Existing session files were removed from
  the Git index but retained on the local filesystem for inspection. Sessions
  pinned to the pre-0.2.0 model require an explicit migration before resumption.
- Git commits are reserved for reusable models, protocols, templates, validators,
  and code rather than individual training rollouts.

## Verification

- Paper-model validation: PASS — 27/27 checks.
- Session-state validation on a newly initialized packet session: PASS — 41/41 checks.
- Reusable session-state tests: PASS — 15/15.
- Deterministic Markdown render check: PASS.
- Git whitespace check: PASS.

The model remains pending human approval and is not promoted into `curriculum/`.
