# Efficient Reading Runner

`EFFICIENT_READING` skips generative training and directly exposes the source-anchored paper architecture.

## Entry

1. Identify the paper.
2. Load a human-approved model if available; otherwise compile, persist, and validate a pending model for this session.
3. Pin the model path/version/hash in a recoverable session record.
4. Present a compact unified claim-tree overview.

## Default overview

Show:

```text
Introduction region
background claims → limitation/tension/gap → significance of TITLE CLAIM

Results region
TITLE CLAIM → major claims → important subclaims → evidence anchors
```

Include source anchors and any required `AUTHOR CLAIM` / `AGENT INTERPRETATION` distinction.

## Interactive expansion

After the overview, ask which branch the human wants expanded. Expand only the requested region, such as:

- an Introduction premise chain;
- the normalized title claim;
- a major-claim branch;
- an evidence/control mapping;
- a figure, table, method, or result detail.

Unlike TRAINING, this runner may explain paper results when requested. Keep every important statement traceable to the paper and do not silently replace the author's claim with the agent's interpretation.

No IDEA/CLAIMS/EVIDENCE rollout or DELTA is required unless the human explicitly switches to TRAINING.
