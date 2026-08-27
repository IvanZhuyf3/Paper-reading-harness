# Paper Reading Harness

A lightweight agent-session system for learning scientific papers before the reader has read them.

The system turns a paper into a structured environment for reasoning. It is not primarily a summarizer, a figure walkthrough, or a post-reading quiz.

## Shared infrastructure

All applications use the same source-anchored paper model:

```text
PAPER MODEL
├── TRAINING
│   ├── FOUNDATION
│   ├── CORE
│   └── ADVANCED
├── EFFICIENT_READING
└── EXAM (future)
```

- **TRAINING:** the human generates first; the paper is a reality-tested verifier trajectory.
- **EFFICIENT_READING:** the agent presents the paper architecture first and expands requested branches.
- **EXAM:** a future runner for measuring the human's independent capability. It shares the paper model but requires separate disclosure and scoring rules.

`EFFICIENT_READING` is an application, not a fourth training level.

## Unified paper architecture

Introduction and Results are two regions of one claim structure:

```text
established / background claims
            ↓ converge
limitation → tension → gap
            ↓
normalized TITLE CLAIM
            ↓ expand
major claims
            ↓
subclaims
            ↓
evidence / proof anchors
```

The Introduction side establishes why the title claim is significant. The Results side unfolds what the paper does to support it.

`TITLE CLAIM` is a normalized central scientific claim, not a mechanical rewrite of the title. A complex title claim may require several sentences.

Every important paper-side node must have a source anchor. When the agent's interpretation differs materially from the author's formulation, preserve both with explicit labels:

```text
AUTHOR CLAIM
SOURCE ANCHOR
AGENT INTERPRETATION
```

## Training sequence

The default assumption is that the human has not read the paper.

```text
KNOWLEDGE → IDEA → CLAIMS → EVIDENCE → independent paper reading → DELTA
```

Each generative stage follows the same control loop:

```text
paper state currently allowed at this stage
→ human rollout
→ human declares the rollout complete
→ agent presents a descriptive structural diff against the paper
→ session re-anchors to the paper trajectory
→ next stage starts
```

The human's divergent trajectory is retained as useful output, but it does not redirect later stages into a hypothetical different paper.

The paper is not a unique answer key. It is a high-quality trajectory that survived contact with reality.

## Agent boundary

The agent may actively verify prerequisite facts and inject concise knowledge pretraining. During IDEA, CLAIMS, EVIDENCE, and DELTA, its role is structural:

- ask one generic structural question at a time;
- maintain and render the evolving structure;
- reconstruct the paper faithfully with source anchors;
- present descriptive structural differences.

The agent must not supply the student's scientific content, lead from the hidden paper tree, rank the student and paper trajectories, or interpret the student's delta.

## Training levels

The human explicitly selects a level at session start.

- **FOUNDATION:** high KNOWLEDGE weight; skip human IDEA generation; retain interactive CLAIMS and EVIDENCE rollouts.
- **CORE:** moderate knowledge alignment; one serious IDEA rollout; full CLAIMS and EVIDENCE rollouts.
- **ADVANCED:** knowledge only when needed; multiple independent IDEA rollouts; full CLAIMS and EVIDENCE rollouts.

The FOUNDATION exception follows a simple premise: thinking searches over the graph of the mind; the graph must exist before productive idea search is possible.

## Paper-model trust lifecycle

- Newly generated models may be saved under `paper_models/pending/`.
- Pending models are provisional and must not be automatically reused in later sessions.
- A human-approved record enters `curriculum/` and the approved index.
- An approved record has priority over a fresh agent reconstruction.

See `protocols/` for session behavior, `templates/` for artifacts, `paper_models/` for provisional models, and `curriculum/` for approved reusable records.
