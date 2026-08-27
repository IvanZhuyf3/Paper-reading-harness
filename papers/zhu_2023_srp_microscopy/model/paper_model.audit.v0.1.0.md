# Paper-Model Mechanical Audit

- **Model:** `paper_model.pending.toml`
- **Overall:** PASS
- **Checks passed:** 21/21
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
| IDEA view contains only problem-state roles | PASS | roles=['background', 'constraint', 'existing_routes', 'gap', 'limitation'] |
| CLAIMS starts only from T0 | PASS | claims_start=['T0'] |
| Evidence results remain hidden until independent reading | PASS | violations=[] |
| Selection policies match protocol | PASS | mismatch={} |
| Source PDF exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\zhu_2023_srp_microscopy\source\Zhu_et_al_2023_SRP_microscopy.pdf |
| Source SHA-256 matches | PASS | expected=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09, actual=B51735420198D699D8C0F3976617F9CA3DFAA2D8E25EE5B3145A70D884CC8A09 |
| Supplement PDF exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\zhu_2023_srp_microscopy\source\Zhu_et_al_2023_SRP_microscopy_supplement.pdf |
| Supplement SHA-256 matches | PASS | expected=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2, actual=F697113130FEC858E5852D50ACCBFFC052894AF4C3F69915AD9DD591D16023B2 |
| Compiler audit flags are finalized | PASS | {'parse_validated': True, 'anchor_audit': 'pass', 'visibility_audit': 'pass'} |

## Scope

This report validates parseability, identity/hash linkage, graph references, anchor presence, disclosure-view membership, and selection-policy invariants. It does not determine whether the paper's scientific trajectory is normatively optimal, and it does not visually prove that every prose anchor points to the intended paragraph.

## Manual source and visibility audit

- PASS — all 12 pages of the supplied main PDF were rendered and visually inspected.
- PASS — supplement pages containing Figs. S2–S4, S8–S12, S17–S18, and Table S1 were rendered and visually inspected.
- PASS — prose anchors use main-PDF page, section, and visible paragraph-opening words.
- PASS — figure/table/equation anchors use labels that are visible in the supplied main or supplement PDF.
- PASS — the IDEA problem-state view contains no author-solution, title-claim, Results-claim, or evidence node.
- PASS — CLAIMS begins only from T0; EVIDENCE result details remain hidden until independent reading.
- NOTE — the main-text fold statements associated with Fig. S18D do not transparently match ratios calculated from the table values. Both source representations are preserved in E9 without agent resolution.
- STATUS — mechanically validated pending model; not human approved and not eligible for automatic cross-session reuse.
