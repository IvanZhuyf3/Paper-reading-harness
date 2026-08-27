# Session-State Recovery Audit

- **State:** `2026-08-27_core_training.state.toml`
- **Overall:** PASS
- **Checks passed:** 15/15

| Check | Result | Detail |
|---|---|---|
| Session TOML parses | PASS | tomllib loaded the state |
| Pinned paper model exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\zhu_2023_srp_microscopy\model\paper_model.pending.toml |
| Pinned paper-model SHA-256 matches | PASS | expected=CB9953A2A72340F5B899F98A0C0322F32BA63EFA69A0605088237E52F9E7FAC3, actual=CB9953A2A72340F5B899F98A0C0322F32BA63EFA69A0605088237E52F9E7FAC3 |
| Paper-model version matches | PASS | state=0.1.2, model=0.1.2 |
| Selection-policy version matches | PASS | state=1.1, model=1.1 |
| Main-source hash matches model | PASS | state=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09, model=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09 |
| Supplement hash matches model | PASS | state=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2, model=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2 |
| Current stage is valid | PASS | claims |
| Completed stages form the prefix before the current stage | PASS | completed=['knowledge', 'idea'], expected=['knowledge', 'idea'] |
| Asked IDs are unique | PASS | count=10 |
| Selection seed is persisted | PASS | 2026082701 |
| Revealed paper-claim IDs resolve | PASS | missing=[] |
| Human-node parents resolve | PASS | missing=[] |
| Unique next interaction is persisted | PASS | cursor=CLAIMS.H-C2.1.awaiting_architecture_claim, pending_prompt=CLAIMS_EXPAND_H-C2.1_ARCHITECTURE |
| Event sequence is contiguous | PASS | events=9 |

The audit verifies that the persisted TOML state can identify its frozen paper model and recover a unique next interaction. It does not evaluate the scientific content of the human rollout.
