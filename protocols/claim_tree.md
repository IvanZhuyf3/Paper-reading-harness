# Unified Claim-Tree Protocol

The project uses one continuous claim structure for the paper:

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
evidence / proof
```

The Introduction region converges on why the title claim is significant. The Results region expands what supports it. These are regions of one model, not separate ontologies.

## Title claim

`TITLE CLAIM` is the normalized central scientific claim reconstructed from the title, abstract, Introduction, Results, and other relevant paper text.

It is not required to reproduce the title literally or fit in one sentence. A complex claim may include a short explanation when needed to preserve scope, conditions, or meaning.

Always retain the original paper title separately.

## Paper-side claim node

Every important paper-side node must contain:

```text
ID: T0 / I1 / M1 / S1.1 / ...
ROLE: background / limitation / gap / title / major / subclaim
AUTHOR CLAIM: author's own concise formulation or source excerpts
SOURCE ANCHOR: PDF page + section + paragraph's first ~5 words, or an explicit figure/table/equation/supplement label
AGENT INTERPRETATION: required when materially different from AUTHOR CLAIM
PARENT / CHILD LINKS: ...
```

If the claim is distributed across passages, preserve the relevant author excerpts rather than fabricating a unified author sentence. If the agent paraphrases, compresses several passages, adds an implicit condition, combines claims, or otherwise departs materially from the author's formulation, show `AUTHOR CLAIM` and `AGENT INTERPRETATION` side by side. Never present the latter as author text.

## Evidence node

Evidence attaches to the claim it is intended to support:

```text
ID: E1 / FIG-2A / TABLE-1 / SIM-1 / ...
TARGET CLAIM: ...
EVIDENCE / PROOF TYPE: ...
CONTROL ROLE: ...
SOURCE ANCHOR: ...
RESULT DETAIL: internally available; withheld during TRAINING until independent reading
```

For prose, use a format such as:

```text
PDF p.1, Introduction, paragraph beginning "Pushing the fundamental limit of..."
```

Preserve approximately the first five words so the human can visually locate the paragraph. For figures, tables, equations, and supplement items, use their explicit labels and include the PDF page when useful. A DOI, file path, or whole-paper citation is not a sufficient node-level anchor.

## Human rollout tree

The human supplies the scientific content. The agent supplies only the interaction structure:

```text
agent selects or displays current node
→ asks one generic structural question
→ human supplies a claim/subclaim/evidence design
→ agent attaches and renders it
→ human decides whether to continue
```

Do not add a hidden paper node to the human tree. Do not create an agent-authored normative tree. The paper tree and human tree are trajectories to be structurally compared, not ranked.

## Granularity

Prefer:

- normalized title claim;
- major claims;
- important subclaims;
- decisive proof links and controls.

Do not exhaustively annotate every sentence or panel.

## Instrument + application pattern

A paper may use a structure such as:

```text
T0 — The method enables a new measurement or science regime.

├── M1 — The design realizes a meaningful new capability.
│   ├── S1.1 — The architecture implements the intended principle.
│   ├── S1.2 — The implementation achieves the relevant performance.
│   └── S1.3 — Performance differs from the relevant baseline.
│
└── M2 — The capability enables the stated application or scientific result.
```

This is an illustrative structural pattern, not a standard answer to reveal during rollout.
