# Session-State Recovery Audit

- **State:** `review_babysitting_20260829.state.toml`
- **Overall:** PASS
- **Checks passed:** 54/54

| Check | Result | Detail |
|---|---|---|
| Session TOML parses | PASS | tomllib loaded the state |
| Pinned paper model exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\li_2026_ft_opt\model\paper_model.pending.toml |
| Pinned paper-model SHA-256 matches | PASS | expected=AA9A9437455B54546D44489142EC8244D0A310FAF6BFD4C8DF1EE09E8A53D75C, actual=AA9A9437455B54546D44489142EC8244D0A310FAF6BFD4C8DF1EE09E8A53D75C |
| Paper-model version matches | PASS | state=0.3.0, model=0.3.0 |
| Selection-policy version matches | PASS | state=1.2, model=1.2 |
| Main-source hash matches model | PASS | state=702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D, model=702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D |
| Supplement hash matches model | PASS | state=None, model=None |
| Current stage is valid | PASS | knowledge |
| Stage dispositions are legal | PASS | {'knowledge': 'in_progress', 'idea': 'not_applicable', 'claims': 'not_applicable', 'evidence': 'not_applicable', 'independent_reading': 'not_applicable', 'delta': 'not_applicable'} |
| Completed stages agree with dispositions | PASS | completed=[], expected=[] |
| Stage disposition order is coherent | PASS | current=knowledge |
| Rollout terminal flag matches current stage | PASS | current=knowledge, rollout_complete=False |
| Selection seed is persisted | PASS | 991 |
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
| Session transition-packet schemas are frozen | PASS | drift=[] |
| Session transition packets equal pinned model | PASS | expected_ids=['TP_IDEA_START', 'TP_CLAIMS_START', 'TP_EVIDENCE_START', 'TP_INDEPENDENT_READING_START', 'TP_DELTA_START', 'BABYSITTING_START'], actual_ids=['TP_IDEA_START', 'TP_CLAIMS_START', 'TP_EVIDENCE_START', 'TP_INDEPENDENT_READING_START', 'TP_DELTA_START', 'BABYSITTING_START'] |
| Session transition packets contain no result details | PASS | leaks=[] |
| Session BABYSITTING terminology assets are frozen | PASS | expected=14, actual=14 |
| Session BABYSITTING logical-edge assets are frozen | PASS | expected=25, actual=25 |
| Session BABYSITTING disclosure packet is frozen | PASS | packet_present=True |
| Session BABYSITTING display claim list is exact | PASS | display claims equal packet |
| Session BABYSITTING display terminology list is exact | PASS | display terminology equal packet |
| Session BABYSITTING display logical-edge list is exact | PASS | display edges equal packet |
| Session BABYSITTING display references resolve | PASS | display references checked |
| BABYSITTING disclosure contains no evidence IDs | PASS | packet=[], state=[] |
| BABYSITTING item inventories cover and partition | PASS | terms=['TERM_BANDWIDTH_RESOLUTION', 'TERM_FOURIER_TRANSFORM', 'TERM_HYPERSPECTRAL', 'TERM_INTERFEROGRAM', 'TERM_MIR_SWIR', 'TERM_MULTIPLEX', 'TERM_PHOTOTHERMAL', 'TERM_POINT_SPREAD', 'TERM_PUMP_PROBE', 'TERM_SPECTRAL_FLOW', 'TERM_SPECTRAL_UNMIXING', 'TERM_SUPERCONTINUUM', 'TERM_TIME_DOMAIN', 'TERM_VIBRATIONAL_OVERTONE'], edges=['EDGE_G1_T0', 'EDGE_I1_I2', 'EDGE_I2_I3', 'EDGE_I3_I4', 'EDGE_I4_I5', 'EDGE_I4_I5_G1', 'EDGE_M1_S11', 'EDGE_M1_S12', 'EDGE_M1_S13', 'EDGE_M2_S21', 'EDGE_M2_S22', 'EDGE_M2_S23', 'EDGE_M2_S24', 'EDGE_M3_S31', 'EDGE_M3_S32', 'EDGE_M4_S41', 'EDGE_M4_S42', 'EDGE_M5_S51', 'EDGE_M5_S52', 'EDGE_M5_S53', 'EDGE_T0_M1', 'EDGE_T0_M2', 'EDGE_T0_M3', 'EDGE_T0_M4', 'EDGE_T0_M5'] |
| BABYSITTING active item and kind resolve | PASS | id=, kind= |
| BABYSITTING empty active item has empty kind | PASS | kind= |
| BABYSITTING selection cursor is explicit | PASS | BABYSITTING.select_item.await_response |
| BABYSITTING verified items are explained | PASS | verified subset of explained |
| Finished-stage records have explicit terminal status | PASS | ambiguous=[] |
| Closed human parents have no ambiguous open children | PASS | parents=[] |
| Event sequence is contiguous | PASS | events=0 |
| Event prompt IDs are unique | PASS | duplicates=[] |
| Every event has prompt text and policy provenance | PASS | missing=[] |
| Event policy provenance is well-formed | PASS | policies=[] |
| Asked IDs match responded events and pending prompt | PASS | expected=['BABYSITTING_START_PROMPT'], actual=['BABYSITTING_START_PROMPT'] |
| Terminal state has no pending prompt | PASS | pending_id=BABYSITTING_START_PROMPT |
| Nonterminal state has one unasked pending prompt | PASS | pending_id=BABYSITTING_START_PROMPT |
| Selection policy provenance is present on every event | PASS | model_current=1.2 |
| Markdown renderer parity | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\li_2026_ft_opt\sessions\review_babysitting_20260829.md |
| Markdown event chronology matches state | PASS | headings=[] |

The audit covers model identity, stage disposition, event provenance/order, graph and evidence consistency, terminal recovery semantics, and deterministic Markdown parity.
