# Four-Stage Paper Training Protocol

## 1. KNOWLEDGE

Question:

> Do I understand the concepts and definitions needed to reason about this paper?

Input: prerequisite concepts from the early paper/background.

Human: explain in own words.

Agent: detect real gaps and inject concise pretraining only where needed.

---

## 2. IDEA

Question:

> Given the problem state, what would I try?

Input: background, limitations, unresolved problem — before the authors' solution.

Human: generate candidate approaches.

Agent: after rollout, reveal the author's idea and compare trajectories.

---

## 3. CLAIMS

Question:

> If this idea is to count as successful science, what must be shown?

Input: background + problem + proposed idea.

Human: construct title/major/subclaims.

Agent: compare with PI-curated tree if available, otherwise a provisional reconstruction.

---

## 4. EVIDENCE

Question:

> What evidence would establish or falsify these claims?

Input: current claim tree, without unrevealed later experiments.

Human: design experiments, controls, analyses, simulations.

Agent: then reveal and compare with paper evidence.

---

## 5. DELTA

Ask:

> What's the delta?

No required format.

---

## Mode toggle

| Mode | Knowledge | Idea | Claims | Evidence |
|---|---|---|---|---|
| FOUNDATION | Primary | Usually skip | Guided | Guided |
| CORE | Moderate | 1 rollout | Full | Full |
| ADVANCED | On demand | Multiple rollouts | Less scaffold | Less scaffold |
| EFFICIENT_READING | Quick | Optional | Major claims | Decisive evidence |
