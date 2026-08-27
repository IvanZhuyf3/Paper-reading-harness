# Spoiler Control

Training value depends on preventing hindsight leakage.

The agent may inspect the whole paper internally, but each stage exposes only information available at that stage.

## KNOWLEDGE
Allowed: concepts, definitions, broad background.
Do not reveal the paper's solution.

## IDEA
Allowed: background, problem, limitations, motivation.
Do not reveal: author solution, later results, conclusion-implying details.
If the title gives away the solution, paraphrase the problem state instead.

## CLAIMS
Allowed: problem + author idea.
Do not reveal result structure or actual experiment sequence.

## EVIDENCE
Allowed: idea + currently revealed claim tree.
Do not reveal actual evidence before human design rollout.

## Anti-leading rule

Questions must be derivable from the allowed scientific state, not from hindsight.

After human rollout, reveal the matching author trajectory and then proceed.
