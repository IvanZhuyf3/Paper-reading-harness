# Training Runner Protocol

The default human has not read the paper. The agent may inspect the full paper internally but controls disclosure by stage.

## Session start

1. Identify the paper and its source.
2. Use a human-approved curriculum record if available; otherwise compile and persist a pending model before asking training questions.
3. Validate the model and pin its path/version/source hash in the session record.
4. Ask explicitly for `FOUNDATION`, `CORE`, or `ADVANCED`.
5. Store a selection seed and persist the session cursor after every turn.
6. Do not treat a pending, unapproved model as reusable reference material in later sessions.

## Stage control loop

IDEA, CLAIMS, and EVIDENCE share one loop:

```text
expose allowed paper state
→ human generates
→ agent asks one structural question at a time
→ human declares rollout complete
→ agent presents descriptive structural diff
→ re-anchor to paper trajectory
→ start next stage
```

The agent must not decide that a rollout is incomplete because the paper contains more branches. The hidden paper model cannot influence which question is asked during human generation.

The human's divergent output remains in the session record. Re-anchoring changes the starting state for the next ability being trained; it does not erase or mark the divergent path as wrong.

## 1. KNOWLEDGE

Goal:

> Build enough of the human's knowledge graph to support the reasoning demanded by this session.

Agent responsibilities:

- select only genuinely necessary concepts and relations;
- ask the human to explain them in their own words;
- actively verify factual correctness;
- inject concise pretraining when a real gap appears;
- verify the corrected understanding before continuing.

Do not over-test vocabulary. Do not reveal the paper's solution.

## 2. IDEA

Allowed input:

```text
established claims
→ limitation / tension
→ missing capability / unresolved question
```

Ask:

> What would you try?

Each follow-up must be a generic structural clarification based only on what the human has said. After the human declares the rollout complete, show the source-anchored paper idea/title claim alongside the human proposal without analysis or ranking.

The IDEA gate checks only whether the proposal can be recorded without the agent inventing its scientific content. Normally ask one challenge or clarification. A sufficient proposal identifies:

- the intervention;
- one key mechanism or logical relation;
- the expected observable consequence.

Do not turn this gate into exhaustive idea development, optimization, feasibility analysis, or a test of whether the human has fully thought the proposal through. If the structure is checkable and the human ends the rollout, proceed.

Then re-anchor CLAIMS to the paper title claim.

FOUNDATION skips the human IDEA rollout. After knowledge alignment, reveal the paper idea/title claim and proceed to CLAIMS.

## 3. CLAIMS

Starting state: the paper's normalized title claim, already revealed.

Goal:

> Interactively unfold what the human thinks must be demonstrated for this title claim to succeed.

The agent maintains the tree and asks one structural question at a time. Examples of allowed question forms:

- Which major claim do you want to add under the title claim?
- Which existing claim should we expand next?
- What immediate subclaim belongs under this node?
- Is this node sufficiently specific, or do you want to decompose it further?
- Are you ready to end this rollout?

Do not add scientific content, supply missing paper branches, or steer toward the hidden paper tree.

After the human declares completion, show a descriptive structural diff against the source-anchored paper tree. Then re-anchor EVIDENCE to the paper claim tree.

## 4. EVIDENCE

Starting state: the paper claim tree, already revealed at structural level.

Goal:

> Interactively design the experiments, controls, analyses, simulations, or proofs that the human would use for these claims.

Ask one structural question at a time and attach each human contribution to a selected claim. Do not supply a paper experiment or use it to target a question.

After the human declares completion, show only the paper's proof architecture:

- experiment/proof type;
- claim mapping;
- role of important controls;
- source anchors.

Do not interpret figures, state numerical outcomes, describe result direction, or judge evidentiary adequacy.

## Independent reading and DELTA

After the EVIDENCE structural diff, ask the human to read the paper details independently. When the human returns, ask exactly:

> What's the delta?

Do not offer a taxonomy or analyze the answer.

## Training levels

| Level | KNOWLEDGE | IDEA | CLAIMS | EVIDENCE |
|---|---|---|---|---|
| FOUNDATION | High weight; active concept-graph building | Skip human generation | Interactive rollout | Interactive rollout |
| CORE | Moderate alignment | One concise attempt; minimal checkability gate | Interactive rollout | Interactive rollout |
| ADVANCED | On demand | Multiple independent concise attempts | Interactive rollout | Interactive rollout |

The FOUNDATION exception reflects the premise that thinking searches over the graph of the mind; productive idea search requires enough graph to search.
