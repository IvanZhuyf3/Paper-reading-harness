# Structural Diff and Delta

The paper is a verifier trajectory, not a unique answer key. The agent presents structure; the human performs the analysis.

## Structural diff

After a human rollout is complete, align it with the corresponding source-anchored paper structure and show only descriptive relations such as:

```text
ALIGNED / OVERLAPPING NODES
HUMAN-ONLY NODES
PAPER-ONLY NODES
DIFFERENT PARENT–CHILD STRUCTURE
DIFFERENT EVIDENCE-TO-CLAIM MAPPING
```

Use neutral language. Preserve both trajectories even when they diverge substantially.

The diff must not:

- rank the trajectories;
- call one complete, superior, attractive, or correct;
- analyze assumptions, burden, cost, falsifiability, or likely success;
- construct a third normative answer;
- infer what lesson the human should take.

The human may perform any of these analyses independently.

## Re-anchoring

After each diff, the next stage starts from the paper trajectory:

```text
human IDEA → diff → paper TITLE CLAIM starts CLAIMS
human CLAIM TREE → diff → paper CLAIM TREE starts EVIDENCE
human EVIDENCE DESIGN → diff → paper proof architecture guides independent reading
```

Re-anchoring isolates the ability trained at each stage. It does not erase or invalidate the human branch.

## Delta

After the human independently reads the paper details, ask:

> What's the delta?

No required format or taxonomy. Do not manufacture, classify, critique, or summarize the delta for the human.
