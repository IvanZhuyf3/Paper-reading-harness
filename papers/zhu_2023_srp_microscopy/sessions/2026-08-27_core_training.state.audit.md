# Session-State Recovery Audit

- **State:** `2026-08-27_core_training.state.toml`
- **Overall:** PASS
- **Checks passed:** 13/13

| Check | Result | Detail |
|---|---|---|
| Session TOML parses | PASS | tomllib loaded the state |
| Pinned paper model exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\zhu_2023_srp_microscopy\model\paper_model.pending.toml |
| Pinned paper-model SHA-256 matches | PASS | expected=BEB27FAA21120AF3E9D60C3E2A0B99DAC5EACE01D320C6DAA7BEFDCB0A07366A, actual=BEB27FAA21120AF3E9D60C3E2A0B99DAC5EACE01D320C6DAA7BEFDCB0A07366A |
| Paper-model version matches | PASS | state=0.1.1, model=0.1.1 |
| Selection-policy version matches | PASS | state=1.0, model=1.0 |
| Main-source hash matches model | PASS | state=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09, model=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09 |
| Supplement hash matches model | PASS | state=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2, model=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2 |
| Current stage is valid | PASS | idea |
| Asked IDs are unique | PASS | count=5 |
| Selection seed is persisted | PASS | 2026082701 |
| Human-node parents resolve | PASS | missing=[] |
| Unique next interaction is persisted | PASS | cursor=IDEA.H-I2.mechanism_confirmed.awaiting_finish, pending_prompt=IDEA_FINISH |
| Event sequence is contiguous | PASS | events=5 |

The audit verifies that the persisted TOML state can identify its frozen paper model and recover a unique next interaction. It does not evaluate the scientific content of the human rollout.
