# Paper-Model Lifecycle

Paper models have two trust states.

## 1. Pending

Location:

```text
paper_models/pending/
```

A pending model:

- may be generated and saved after a session;
- must be visibly labeled `PENDING — NOT HUMAN APPROVED`;
- may be inspected or edited by a human;
- must not be automatically selected as a reusable reference in a later session;
- must not appear in the approved curriculum index.

Pending is a fishing pool for potentially valuable reconstructions, not a trusted cache.

## 2. Approved

Location:

```text
curriculum/
```

Approval requires human review of at least:

- paper identity;
- normalized title claim;
- important claim-tree structure;
- author-claim versus agent-interpretation labels;
- source anchors;
- evidence-to-claim mappings;
- spoiler-safe training order.

An approved record must state reviewer, approval date, and record version. It may then enter `curriculum/index.md` and be reused automatically.

## Selection rule

At a new session:

```text
approved record exists → use it
no approved record → reconstruct from the supplied paper for this session
pending record exists → do not auto-reuse; leave it for human review
```

Never silently promote a pending model. Human approval is the only transition into the reusable set.
