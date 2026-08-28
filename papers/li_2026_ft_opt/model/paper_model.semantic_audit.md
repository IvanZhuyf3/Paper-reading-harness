# Pending Paper-Model Semantic Audit

## Scope

This audit records the human-reviewable judgments that are not established by
the mechanical validator. It does not assess whether the paper's scientific
trajectory is correct or normatively optimal.

## Source coverage

- The 28-page main article and 14-page embedded Supplementary Information were inspected.
- Introduction, Results, Discussion, Methods, all five main figures, and Supplementary Figs. S1-S7 were included in the reconstruction.
- The model represents the Introduction and Results as one continuous structure from background and limitations through `T0` to major claims, subclaims, and evidence.

## Claim fidelity

- `author_claim` fields preserve concise source wording. Ellipses mark omitted intervening text; distributed claims are not rewritten as fabricated author sentences.
- `agent_interpretation` fields contain the normalization or synthesis needed to expose the logical role of each source passage.
- The normalized title claim `T0` is explicitly a synthesis of the Abstract, final Introduction paragraph, and Discussion rather than a purported verbatim title sentence.
- Paragraph anchors use PDF page, section, and opening words; figure, equation, and supplementary anchors use explicit labels.

## Visibility and runner boundary

- The IDEA view contains only established context, limitations, existing routes, and the unresolved capability gap.
- The title claim and proposed FT-OPT mechanism are withheld until IDEA rollout completion.
- Paper claim branches are withheld until CLAIMS rollout completion.
- Evidence designs are withheld until EVIDENCE rollout completion, and every `result_detail` remains hidden until independent reading starts.
- Paper-specific optical construction and calibration nodes (`S1.3`, `E2`) are marked low-transfer and ineligible for default deep follow-up.
- Version 0.2.0 includes prevalidated transition packets for IDEA, CLAIMS, EVIDENCE, independent reading, and DELTA. Fixed paper-side disclosure is cached; human-dependent comparisons remain explicit dynamic slots.

## Known source limitations

- The supplied document is a review proof, so bibliographic metadata and wording may change before publication.
- Its embedded text layer has damaged glyph mappings in several equations, units, and sentences. Numerical and verbatim content was cross-checked against page renders where extraction was unreliable.
- The abstract's broad speed statement, the implemented approximately 0.842 s refresh period, and the projected approximately 464 microsecond optimized refresh describe different comparison levels; the model does not collapse them into one result.

## Disposition

- Semantic compilation: READY FOR ORIGINATING TRAINING SESSION.
- Reuse status: PENDING HUMAN REVIEW; DO NOT PROMOTE TO `curriculum/` AUTOMATICALLY.
