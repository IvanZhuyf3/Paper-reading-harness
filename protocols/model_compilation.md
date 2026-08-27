# Paper-Model Compilation

Compilation is a required pre-run phase, not an on-demand activity spread across session turns.

## Inputs

- immutable source PDF or equivalent primary paper source;
- source identity and SHA-256;
- an approved model, if one already exists.

## Compiler output

When no approved model exists, create:

```text
papers/<paper_slug>/model/paper_model.pending.toml
papers/<paper_slug>/model/paper_model.audit.md
```

The machine-readable model must contain stable IDs for:

- prerequisite knowledge nodes and dependency edges;
- problem-state claims;
- normalized title claim;
- major claims and subclaims;
- evidence/proof nodes and control roles;
- precise source anchors;
- author wording/source excerpts and materially different agent interpretations;
- stage disclosure views;
- question eligibility metadata;
- model version, compiler timestamp, source hash, and approval status.

## Required audit

Before the first runner question, verify and record:

- model parses successfully;
- paper identity and source hash match;
- every important paper-side node has a reader-locatable anchor;
- every materially reconstructed claim distinguishes author wording from agent interpretation;
- every evidence node maps to at least one claim;
- stage views do not reveal later-stage content;
- question eligibility follows the selection protocol;
- the session pins the exact model version and hash.

An audit checks traceability and protocol consistency. It does not judge whether the paper's scientific trajectory is normatively optimal.

## Pending versus approved

A validated pending model can drive the session for which it was compiled. It cannot become an automatic cross-session reference until human approval.

## Compaction recovery

The runner must be reconstructible from files alone:

```text
paper model + session cursor + selection history → next valid interaction
```

The canonical cursor and selection history must be machine-readable TOML, not inferred from a prose transcript. Keep a parallel Markdown log for human audit.

If those files are inconsistent or incomplete, stop the runner and repair the persisted state before asking another scientific question.
