# Rule-Governed Question Selection

Question selection is constrained and reproducible. It is not pure random sampling.

## Shared requirements

Each selectable item has:

```text
stable ID
stage
prerequisite IDs
visibility rule
selection weight or priority
asked/not-asked state
```

The session records a selection-policy version, seed, selected IDs, current cursor, and the prompt text plus policy version on every event. The TOML event stream is canonical; Markdown is rendered from it and checked for parity.

### Transferability/reusability filter

Human-open-node eligibility is necessary but not sufficient for default follow-up. During CLAIMS and EVIDENCE, prefer transferable measurement and claim–evidence relations. Low-transfer, paper-specific apparatus optimization should normally be recorded and left closed rather than deepened. Select such a node only when the human explicitly requests it, when clarification is necessary to make the claim checkable, or when EFFICIENT_READING asks for that expansion.

## BABYSITTING

`BABYSITTING` is learner-directed rather than seeded. Its frozen start packet
discloses the complete source-anchored claim tree, terminology inventory, and
logical edges. The learner selects one visible unresolved term or relation;
the runner teaches and checks only that item, then returns the fixed selection
prompt. No hidden node is sampled and no evidence result is disclosed.

## KNOWLEDGE

Eligible nodes must:

- be marked necessary for the selected training level;
- have all prerequisite dependencies satisfied;
- be safe to reveal before the paper idea;
- not already be verified in the current session.

Selection may be seeded among equally eligible nodes. Stop when the required knowledge subgraph is verified; do not exhaustively quiz every concept.

## IDEA

Do not randomly sample individual problem-state claims. Expose the complete compiled problem-state view required to make the problem coherent, then use the fixed prompt:

> What would you try?

Follow-up questions may use only the human proposal generated so far. Normally select exactly one challenge or clarification targeting an ambiguous intervention, mechanism relation, or expected observable. Ask another only when the proposal still cannot be recorded without inventing content; never continue merely to make the idea detailed, optimized, or fully reasoned.

## CLAIMS

Eligible nodes come only from the human's current tree. Selection may choose among human-created open nodes using generic structural prompts, subject to the transferability/reusability filter above.

Never select a hidden paper claim to probe an omission.

## EVIDENCE

Eligible nodes are claims already revealed by the stage protocol. Ask the human to attach an experiment, control, analysis, simulation, or proof design, subject to the transferability/reusability filter above.

Never select a hidden paper evidence node before human rollout completion.

## DELTA

No selection. Ask exactly:

> What's the delta?

If the human explicitly declines DELTA, record its stage disposition as `skipped` and retain the terminal response without treating the stage as completed.

## Persistence cadence

Update canonical state and regenerate/check the Markdown projection after every turn, normally through the asynchronous single-writer scribe. Runtime sessions are local and Git-ignored. Do not commit per turn or per stage. Commit reusable paper-model versions and harness changes instead.

Load validated transition packets from the pinned paper model at session initialization. Fixed paper-side disclosures and prompts are prefilled; a normal stage change must not wait for those views to be reconstructed or committed. Human-dependent diffs remain dynamic.

## EXAM

Reserved. A future exam policy may use seeded paper-node sampling, but must define disclosure, coverage, and scoring separately before use.
