# Paper Training Harness

A lightweight agent-assisted system for turning scientific papers into reusable training environments.

Core sequence:

```text
1. KNOWLEDGE
2. IDEA
3. CLAIMS
4. EVIDENCE
5. What's the delta?
```

The same workflow serves both:
- first-year structured training;
- high-efficiency paper reading.

## Curated vs ordinary papers

**Ordinary paper:** the agent creates a temporary problem representation and provisional claim tree.

**Curated paper:** a PI-verified record in `curriculum/` provides the trusted problem framing, claim tree, evidence map, and training order.

A mature field curriculum may contain ~50 ordered exemplary papers, with roughly 30–35 stable core papers plus 15–20 frontier papers updated yearly.

## Modes

- `FOUNDATION`: KNOWLEDGE primary; IDEA usually skipped; CLAIMS/EVIDENCE guided.
- `CORE`: balanced four-stage training.
- `ADVANCED`: IDEA emphasized; multiple rollouts; less scaffolding.
- `EFFICIENT_READING`: run only stages with useful information gain.

The paper is not a unique answer key. It is one expert trajectory that survived reality.
