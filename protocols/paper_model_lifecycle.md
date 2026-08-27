# Paper-Model Lifecycle

Paper models have two trust states.

## 1. Pending

Location:

```text
papers/<paper_slug>/model/paper_model.pending.toml
papers/<paper_slug>/model/paper_model.audit.md
```

A pending model:

- may be generated and saved after a session;
- should normally be compiled and validated before the originating runner begins;
- must be visibly labeled `PENDING — NOT HUMAN APPROVED`;
- may be inspected or edited by a human;
- must not be automatically selected as a reusable reference in a later session;
- must not appear in the approved curriculum index.

The originating session may use the freshly compiled pending model when its path, version, source hash, and audit status are pinned in the session record. This is current-session execution, not cross-session reuse.

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
no approved record → compile, persist, and validate a pending model
pending record exists → do not auto-reuse; leave it for human review
```

Never silently promote a pending model. Human approval is the only transition into the reusable set.
