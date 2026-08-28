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

## Compile before run

Do not reconstruct the hidden paper structure turn by turn. Before the first runner question:

```text
source PDF
→ extract and visually inspect source artifacts
→ compile complete paper model
→ persist model + audit report
→ validate anchors, visibility, and parseability
→ start runner from the fixed model version
```

The session stores the model path/version, current stage, selection history, current human structure, and resume cursor after every turn. This keeps the runner compatible with approved models and makes session compaction recoverable.

Each canonical event stores its prompt text and the selection-policy version used for that selection. The Markdown audit timeline is a deterministic projection of the TOML event stream; regenerate it with `scripts/render_session_markdown.bat` and verify parity with `--check`. Stage dispositions distinguish `completed`, `skipped`, and `not_applicable`, including terminal sessions with a skipped DELTA.

Question selection is rule-governed rather than purely random. KNOWLEDGE may use seeded sampling from eligible prerequisite nodes. IDEA exposes the complete problem state and normally asks only one challenge or clarification, stopping once the proposal is checkable. CLAIMS and EVIDENCE select only from the human's exposed structure and generic structural prompts; they never sample hidden paper nodes.

Question selection also applies a transferability/reusability filter: an open human node is necessary but not sufficient for default deepening. Prefer transferable measurement and claim–evidence relations. Record low-transfer, paper-specific apparatus optimization without default deep probing, unless the human requests it, clarification is required for checkability, or EFFICIENT_READING requests the expansion.

Persistence is deliberately tiered: update canonical TOML and regenerate/check Markdown after each turn; create immutable audit reports and Git commits at stage boundaries, failures, policy changes, or explicit checkpoints. Ordinary turns within one stage may be batched.

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
- **CORE:** moderate knowledge alignment; one concise IDEA attempt with a minimal checkability gate; full CLAIMS and EVIDENCE rollouts.
- **ADVANCED:** knowledge only when needed; multiple independent concise IDEA attempts; full CLAIMS and EVIDENCE rollouts.

The FOUNDATION exception follows a simple premise: thinking searches over the graph of the mind; the graph must exist before productive idea search is possible.

## Paper-model trust lifecycle

- Newly generated models are saved inside `papers/<paper_slug>/model/` and registered in the pending pool.
- Pending models are provisional and must not be automatically reused in later sessions.
- The originating session may use its freshly compiled pending model after validation.
- A human-approved record enters `curriculum/` and the approved index.
- An approved record has priority over a fresh agent reconstruction.

See `protocols/` for session behavior, `templates/` for artifacts, `scripts/` for reusable validation, `papers/` for isolated source-and-session workspaces, `paper_models/` for the general provisional pool, and `curriculum/` for approved reusable records.
