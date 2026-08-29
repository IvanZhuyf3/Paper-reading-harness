# BABYSITTING Training Mode Specification

Status: normative implementation specification.

## Purpose and boundary

`BABYSITTING` is a TRAINING mode for a learner who cannot yet usefully generate an idea, claim tree, or evidence design because the paper's concepts and logical relations are unfamiliar.

The runner actively exposes the paper's claim tree, the logical relation carried by every displayed edge, and the terminology needed to read the tree. The learner then chooses whichever term or relation is unclear. The runner teaches and checks that item until the learner understands it, then returns control to the learner to choose the next item.

`BABYSITTING` is guided comprehension, not a generative rollout, an assessment, EFFICIENT_READING, or a substitute for reading figures and numerical results.

## Runner selection

- `BABYSITTING` is selected explicitly as a TRAINING mode.
- For command-line and state-schema compatibility, `level = "babysitting"` is the canonical persisted selector. It is not treated as a fourth difficulty rank.
- `FOUNDATION`, `CORE`, and `ADVANCED` retain their current behavior.
- `EXAM` remains reserved.
- A paper can start `BABYSITTING` only when its pinned paper model contains a validated babysitting disclosure packet and the reusable assets referenced by that packet. Missing assets must produce a clear initialization error rather than compile content during the live turn.

## Initial disclosure

The first runner response must be renderable entirely from the pinned paper model. It presents:

1. the continuous paper claim tree from established/background claims through the gap and normalized title claim to major claims and subclaims;
2. an explicit label and concise explanation for each displayed logical edge;
3. a terminology inventory keyed to the displayed nodes and edges; and
4. the fixed learner prompt: `Which term or logical relation is unclear? Pick one.`

The disclosure may contain source-anchored author claims and clearly labeled agent interpretations. It must not expose evidence-node result details, interpret plots, judge whether evidence is convincing, or manufacture claims absent from the compiled model.

## Paper-model assets

A paper model that supports `BABYSITTING` must contain all of the following before the session begins.

### Terminology nodes

Each terminology node has:

- a stable unique ID;
- the display term;
- optional aliases;
- a concise definition suitable for the compiled paper context;
- prerequisite terminology-node IDs;
- related claim-node IDs;
- at least one reader-locatable source anchor for the term's use in the paper.

Definitions are reusable orientation material, not a script for every teaching turn. Teaching may expand the definition in response to the learner's question. A learner-raised term that is absent from the inventory may be handled in the current session, but it is not silently added to the reusable paper model.

### Logical edges

Each logical edge has:

- a stable unique ID;
- one or more source claim-node IDs;
- one target claim-node ID;
- a controlled relation label;
- a concise explanation of the relation; and
- source-node references sufficient to audit the relation.

The controlled relation labels are `establishes_context`, `creates_tension`, `defines_gap`, `motivates_significance`, `resolves_gap`, `decomposes`, `supports`, and `operationalizes`. A model may use only the smallest label set needed by the paper. Relation explanations must be descriptive rather than evaluative.

### Prefilled disclosure packet

The model contains one `BABYSITTING_START` transition packet with:

- `target_stage = "knowledge"`;
- `eligible_levels = ["babysitting"]`;
- all displayed claim IDs, terminology IDs, and logical-edge IDs;
- no revealed evidence IDs;
- complete prefilled display content;
- the fixed initial prompt and a stable prompt ID; and
- dynamic slots for the learner-selected item only.

For model schema version 0.3 or later, a model that declares babysitting support must contain exactly one such packet. Models from earlier schema versions remain valid for their existing modes but cannot initialize `BABYSITTING`.

## Interaction loop

The learner controls item selection. There is no seeded sampling or predetermined quiz order.

1. If no item is active, ask the fixed learner prompt and wait.
2. Resolve the learner's selected term or logical relation against the visible disclosure. If the selection is ambiguous, ask one clarification question.
3. Explain only the prerequisite chain and relation needed for the selected item, using concise language.
4. Ask one check question that requires the learner to restate, predict, distinguish, or connect the selected item.
5. If the response contains a factual or relational error, correct it concisely and ask one new check on the same item.
6. Keep the same item active until the learner demonstrates the intended understanding or explicitly states that the item is understood.
7. Mark the item verified, show the remaining unresolved inventory, and return to the fixed learner prompt.
8. End only when the learner declares that no displayed term or logical relation remains unresolved.

The runner may answer a direct learner question before issuing the check. It must not turn the loop into idea generation, claim generation, evidence design, figure interpretation, or broad terminology testing unrelated to the learner-selected item.

Verification is local to the checked item. Completion must not be described as proof of general mastery.

## Stage semantics

`BABYSITTING` uses the existing `knowledge` stage for its entire active loop; no new stage is added.

At initialization:

- `current_stage = "knowledge"`;
- `knowledge = "in_progress"`; and
- `idea`, `claims`, `evidence`, `independent_reading`, and `delta` are `not_applicable`.

At learner-declared completion:

- `knowledge = "completed"`;
- all other stages remain `not_applicable`;
- `current_stage = "complete"`; and
- the rollout is complete.

The ordinary TRAINING stage sequence and dispositions are unchanged for `FOUNDATION`, `CORE`, and `ADVANCED`.

## Recoverable session state

The canonical state must be sufficient to resume after compaction without inferring mastery from transcript prose. It records:

- the pinned model identity, version, source hash, and frozen disclosure packet;
- the active selected item ID and kind, if any;
- explained terminology and relation IDs;
- verified terminology and relation IDs;
- unresolved terminology and relation IDs;
- the current check prompt and resume cursor;
- every learner question, explanation, check, and response as canonical events; and
- the current dispositions and completion status.

Resume cursors distinguish item selection from an active item check. The Markdown session view remains a deterministic render of canonical state/events and may be updated asynchronously.

Runtime session artifacts remain local and Git-ignored. This change does not add a Codex SQLite reader, transcript importer, or new persistence backend.

## Performance requirements

- The initial disclosure is loaded from the frozen packet and must not wait for live paper reconstruction.
- The interactive response path performs only item resolution, teaching, one check selection, and a lightweight state append.
- Rendering, full validation, audit generation, and other durable bookkeeping remain delegated to the background scribe when available.
- No Git commit occurs per turn, item, or session stage.

## Validation and compatibility

Implementation must:

- accept `babysitting` during session creation;
- reject babysitting initialization when the pinned model lacks valid babysitting assets;
- validate terminology prerequisites and related-claim references;
- validate logical-edge claim references and relation labels;
- validate the single disclosure packet and its frozen session copy;
- validate the babysitting-specific disposition exception;
- preserve compatibility with valid 0.1 and 0.2 paper models and existing sessions; and
- leave ordinary TRAINING and EFFICIENT_READING behavior unchanged.

The paper-model template, session template, root instructions, README, and script documentation must describe the new mode without presenting it as a difficulty rank.

## Acceptance tests

Automated coverage must demonstrate:

- successful initialization from a valid babysitting-capable model;
- correct initial and terminal dispositions;
- deterministic freezing of the disclosure packet and its referenced assets;
- rejection of missing, duplicate, or dangling terminology and logical-edge references;
- recovery of an active selected item and its check cursor;
- validation of a complete babysitting session;
- unchanged initialization and validation for `FOUNDATION`, `CORE`, and `ADVANCED`; and
- rejection of `BABYSITTING` against a legacy model that does not declare support.

