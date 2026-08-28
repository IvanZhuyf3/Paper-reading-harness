# Session-State Recovery Audit

- **State:** `2026-08-28_foundation_training.state.toml`
- **Overall:** PASS
- **Checks passed:** 38/38

| Check | Result | Detail |
|---|---|---|
| Session TOML parses | PASS | tomllib loaded the state |
| Pinned paper model exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\li_2026_ft_opt\model\paper_model.pending.toml |
| Pinned paper-model SHA-256 matches | PASS | expected=AF997481BA7FC92462E3750AC5FD14020091A25BDC02665968EF68A0F8A575B9, actual=AF997481BA7FC92462E3750AC5FD14020091A25BDC02665968EF68A0F8A575B9 |
| Paper-model version matches | PASS | state=0.1.0, model=0.1.0 |
| Selection-policy version matches | PASS | state=1.2, model=1.2 |
| Main-source hash matches model | PASS | state=702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D, model=702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D |
| Supplement hash matches model | PASS | state=None, model=None |
| Current stage is valid | PASS | idea |
| Stage dispositions are legal | PASS | {'knowledge': 'completed', 'idea': 'in_progress', 'claims': 'in_progress', 'evidence': 'in_progress', 'independent_reading': 'in_progress', 'delta': 'in_progress'} |
| Completed stages agree with dispositions | PASS | completed=['knowledge'], expected=['knowledge'] |
| Stage disposition order is coherent | PASS | current=idea |
| Rollout terminal flag matches current stage | PASS | current=idea, rollout_complete=False |
| Selection seed is persisted | PASS | 2026082801 |
| Revealed paper-claim IDs resolve | PASS | missing=[] |
| human nodes IDs are unique | PASS | duplicates=[] |
| human evidence designs IDs are unique | PASS | duplicates=[] |
| human control designs IDs are unique | PASS | duplicates=[] |
| human application metadata IDs are unique | PASS | duplicates=[] |
| human evidence candidates IDs are unique | PASS | duplicates=[] |
| Human record IDs are unique across collections | PASS | duplicates=[] |
| Human-node parents resolve | PASS | missing=[] |
| Human targets resolve | PASS | missing=[] |
| Revealed paper-evidence IDs resolve | PASS | missing=[] |
| Session paper-evidence design IDs match model | PASS | missing=[], extra=[] |
| Session paper-evidence designs equal frozen design fields | PASS | drift=[] |
| Session paper-evidence designs contain no result details | PASS | leaks=[] |
| Finished-stage records have explicit terminal status | PASS | ambiguous=[] |
| Closed human parents have no ambiguous open children | PASS | parents=[] |
| Event sequence is contiguous | PASS | events=14 |
| Event prompt IDs are unique | PASS | duplicates=[] |
| Every event has prompt text and policy provenance | PASS | missing=[] |
| Event policy provenance is well-formed | PASS | policies=['1.2'] |
| Asked IDs match responded events and pending prompt | PASS | expected=['K1', 'K1_CHECK', 'K1_NIR', 'K2_STEP1', 'K2_STEP1_REASK', 'K2_STEP2', 'K2_STEP3', 'K2_STEP4', 'K3_STEP1', 'K3_STEP2', 'IDEA_FIXED', 'K3_STEP2_REASK', 'K3_STEP2_TIME', 'K3_STEP3_LINEWIDTH', 'IDEA_FIXED_RETRY'], actual=['K1', 'K1_CHECK', 'K1_NIR', 'K2_STEP1', 'K2_STEP1_REASK', 'K2_STEP2', 'K2_STEP3', 'K2_STEP4', 'K3_STEP1', 'K3_STEP2', 'IDEA_FIXED', 'K3_STEP2_REASK', 'K3_STEP2_TIME', 'K3_STEP3_LINEWIDTH', 'IDEA_FIXED_RETRY'] |
| Terminal state has no pending prompt | PASS | pending_id=IDEA_FIXED_RETRY |
| Nonterminal state has one unasked pending prompt | PASS | pending_id=IDEA_FIXED_RETRY |
| Selection policy provenance is present on every event | PASS | model_current=1.2 |
| Markdown renderer parity | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\li_2026_ft_opt\sessions\2026-08-28_foundation_training.md |
| Markdown event chronology matches state | PASS | headings=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] |

The audit covers model identity, stage disposition, event provenance/order, graph and evidence consistency, terminal recovery semantics, and deterministic Markdown parity.
