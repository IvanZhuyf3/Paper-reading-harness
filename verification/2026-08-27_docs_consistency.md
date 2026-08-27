# Documentation Consistency Verification — 2026-08-27

## Scope

Verified the documentation rewrite that separates the shared paper model from the TRAINING, EFFICIENT_READING, and future EXAM runners.

Baseline commit before the rewrite:

```text
a00799a chore: establish paper harness baseline
```

## Mechanical checks

| Check | Result |
|---|---|
| Required core files present | PASS — 13/13 |
| Markdown trailing whitespace scan | PASS |
| `git diff --check` | PASS |
| Stale mode-table and `AI attacks` phrases absent | PASS |
| Source-anchor requirement represented across protocols/templates | PASS |
| Pending/unapproved warning represented across lifecycle/template/pool | PASS |

Commands used:

```powershell
rg --files -g "*.md"
rg -n "  $" -g "*.md" .
git diff --check
rg -n "AI asks → human reasons → AI attacks|EFFICIENT_READING \| Quick|Present-day alternatives worth allowing|FOUNDATION \| Primary \| Usually skip" -g "*.md" -g "!verification/**" .
```

## Protocol consistency review

- PASS — Default TRAINING entry assumes the human has not read the paper.
- PASS — `EFFICIENT_READING` is a separate runner rather than a training level.
- PASS — FOUNDATION skips human IDEA generation but retains CLAIMS and EVIDENCE rollouts.
- PASS — The human controls rollout completion.
- PASS — Questions during rollout may use only exposed state and the human-generated structure.
- PASS — Each stage reveals a descriptive paper diff and re-anchors the next stage to the paper trajectory.
- PASS — Agent scientific analysis/ranking is prohibited; active factual verification remains allowed in KNOWLEDGE.
- PASS — Introduction and Results use one unified claim structure centered on the normalized title claim.
- PASS — Important paper-side nodes require precise source anchors.
- PASS — Author wording/source excerpts are separated from materially different agent interpretations.
- PASS — TRAINING reveals proof architecture after EVIDENCE but does not substitute for reading results.
- PASS — DELTA is asked after independent paper reading and is not interpreted by the agent.
- PASS — Pending models are saveable but cannot be automatically reused before human approval.

## Remaining validation

No real paper session has yet been run against the rewritten protocol. The planned small trial should test question non-leadingness, stage re-anchoring, anchor usability, and whether the evidence disclosure leaves enough detail for independent figure reading.
