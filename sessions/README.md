# Sessions

Persisting the runner state is required. Use `templates/paper_session.md` and update the cursor after every human response, before asking the next question.

The minimum recoverable state includes the pinned paper-model path/version/hash, runner and level, selection-policy version and seed, asked IDs, current human structure, stage, and resume cursor.

Store the canonical recovery state as `<session>.state.toml` and the human-readable interaction log as `<session>.md`. The TOML state controls resumption; the Markdown log supports audit.

Saving additional narrative notes remains optional.

Good reasons to save a session include:

- the human rollout is worth revisiting;
- the structural diff is informative;
- the delta is worth preserving in the human's own words;
- the paper model may become a pending review candidate.

Session records preserve human and paper trajectories separately. They must not add an agent-authored normative answer or reinterpret the human's delta.

Saving a session does not approve its paper model. Reusable approval follows `protocols/paper_model_lifecycle.md`.
