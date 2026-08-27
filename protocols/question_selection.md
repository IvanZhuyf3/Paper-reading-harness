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

The session records a selection-policy version, seed, selected IDs, and current cursor.

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

Follow-up questions may use only the human proposal generated so far.

## CLAIMS

Eligible nodes come only from the human's current tree. Selection may choose among human-created open nodes, using generic prompts such as add, expand, decompose, or finish.

Never select a hidden paper claim to probe an omission.

## EVIDENCE

Eligible nodes are claims already revealed by the stage protocol. Ask the human to attach an experiment, control, analysis, simulation, or proof design.

Never select a hidden paper evidence node before human rollout completion.

## DELTA

No selection. Ask exactly:

> What's the delta?

## EXAM

Reserved. A future exam policy may use seeded paper-node sampling, but must define disclosure, coverage, and scoring separately before use.
