# Paper-Model Mechanical Audit

- **Model:** `paper_model.pending.toml`
- **Overall:** PASS
- **Checks passed:** 23/23
- **Knowledge nodes:** 6
- **Claim nodes:** 18
- **Evidence nodes:** 9

## Checks

| Check | Result | Detail |
|---|---|---|
| TOML parses | PASS | tomllib loaded the model |
| Knowledge-node IDs are present and unique | PASS | count=6, missing=0, duplicates=[] |
| Claim-node IDs are present and unique | PASS | count=18, missing=0, duplicates=[] |
| Evidence-node IDs are present and unique | PASS | count=9, missing=0, duplicates=[] |
| IDs are unique across node types | PASS | cross-type duplicates=[] |
| Knowledge prerequisites resolve | PASS | missing=[] |
| Claim parents resolve | PASS | missing=[] |
| Evidence targets resolve | PASS | missing=[] |
| Every node has a source anchor | PASS | missing=[] |
| Anchors use reader-locatable forms | PASS | weak=[] |
| Claim nodes separate author claim and agent interpretation | PASS | missing_author=[], missing_interpretation=[] |
| Disclosure-view IDs resolve | PASS | missing=[] |
| Transition packets are present | PASS | legacy model: not required |
| IDEA view contains only problem-state roles | PASS | roles=['background', 'constraint', 'existing_routes', 'gap', 'limitation'] |
| CLAIMS starts only from T0 | PASS | claims_start=['T0'] |
| Evidence results remain hidden until independent reading | PASS | violations=[] |
| Selection-policy version is current | PASS | version=1.2 |
| Selection policies match protocol | PASS | mismatch={} |
| Source PDF exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\zhu_2023_srp_microscopy\source\Zhu_et_al_2023_SRP_microscopy.pdf |
| Source SHA-256 matches | PASS | expected=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09, actual=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09 |
| Supplement PDF exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\zhu_2023_srp_microscopy\source\Zhu_et_al_2023_SRP_microscopy_supplement.pdf |
| Supplement SHA-256 matches | PASS | expected=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2, actual=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2 |
| Compiler audit flags are finalized | PASS | {'parse_validated': True, 'anchor_audit': 'pass', 'visibility_audit': 'pass'} |

## Scope

This report validates parseability, identity/hash linkage, graph references, anchor presence, disclosure-view membership, and selection-policy invariants. It does not determine whether the paper's scientific trajectory is normatively optimal, and it does not visually prove that every prose anchor points to the intended paragraph.
