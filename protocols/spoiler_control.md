# Spoiler Control

Training value depends on preventing hindsight leakage. The agent may inspect the full paper internally, but disclosure and question selection are stage-bound.

## Global anti-leading rule

During a human rollout, the next question must be derivable solely from:

- information already allowed at the current stage; and
- the human structure generated so far.

The hidden paper model must not determine which omission to probe, which branch to expand, or when the rollout is complete.

## KNOWLEDGE

Allowed:

- prerequisite concepts and relations;
- factual correction;
- broad background required for reasoning.

Withhold the paper's solution, title-claim reconstruction, result structure, and evidence.

## IDEA

Allowed before human completion:

- established background claims;
- limitation, tension, or gap;
- unresolved problem or missing capability.

Withhold the author idea, title claim, result claims, and evidence. If the paper title reveals the solution, paraphrase only the problem state.

After the human declares completion, reveal the source-anchored paper idea/title claim and a descriptive structural juxtaposition. Re-anchor the next stage to that paper claim.

FOUNDATION skips human IDEA generation and may reveal the paper idea/title claim immediately after knowledge alignment.

## CLAIMS

Allowed before human completion:

- the paper's normalized title claim;
- the human claim tree built so far.

Withhold the paper's major claims, subclaims, experiment sequence, and evidence map.

After the human declares completion, reveal the source-anchored paper claim tree and a descriptive structural diff. Re-anchor EVIDENCE to the paper tree.

## EVIDENCE

Allowed before human completion:

- the revealed paper claim tree;
- the human evidence design built so far.

Withhold the paper's experiments, controls, evidence sequence, and results.

After the human declares completion, reveal experiment/proof types, claim mappings, control roles, and source anchors. Continue to withhold result direction, measurements, plot interpretation, and evidentiary judgment.

## Independent reading

The human now reads paper details and figures directly. No result-level spoiler restriction remains for content the human requests after beginning this step.

## DELTA

Ask only:

> What's the delta?

Do not pre-populate the answer or interpret it afterward.

## EFFICIENT_READING exception

`EFFICIENT_READING` is not a generative training runner. It may reveal architecture immediately and expand result details when the human requests them. It must still preserve source anchors and distinguish author claims from agent interpretations.
