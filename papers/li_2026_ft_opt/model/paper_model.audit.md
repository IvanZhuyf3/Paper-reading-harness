# Paper-Model Mechanical Audit

- **Model:** `paper_model.pending.toml`
- **Overall:** PASS
- **Checks passed:** 20/20
- **Knowledge nodes:** 8
- **Claim nodes:** 26
- **Evidence nodes:** 13

## Checks

| Check | Result | Detail |
|---|---|---|
| TOML parses | PASS | tomllib loaded the model |
| Knowledge-node IDs are present and unique | PASS | count=8, missing=0, duplicates=[] |
| Claim-node IDs are present and unique | PASS | count=26, missing=0, duplicates=[] |
| Evidence-node IDs are present and unique | PASS | count=13, missing=0, duplicates=[] |
| IDs are unique across node types | PASS | cross-type duplicates=[] |
| Knowledge prerequisites resolve | PASS | missing=[] |
| Claim parents resolve | PASS | missing=[] |
| Evidence targets resolve | PASS | missing=[] |
| Every node has a source anchor | PASS | missing=[] |
| Anchors use reader-locatable forms | PASS | weak=[] |
| Claim nodes separate author claim and agent interpretation | PASS | missing_author=[], missing_interpretation=[] |
| Disclosure-view IDs resolve | PASS | missing=[] |
| IDEA view contains only problem-state roles | PASS | roles=['background', 'existing_routes', 'gap', 'limitation'] |
| CLAIMS starts only from T0 | PASS | claims_start=['T0'] |
| Evidence results remain hidden until independent reading | PASS | violations=[] |
| Selection-policy version is current | PASS | version=1.2 |
| Selection policies match protocol | PASS | mismatch={} |
| Source PDF exists | PASS | C:\Users\Ivanz\OneDrive\ChatGPT_workspace\Research\Academic reading training\papers\li_2026_ft_opt\source\Li_et_al_2026_FT_OPT_proof.pdf |
| Source SHA-256 matches | PASS | expected=702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D, actual=702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D |
| Compiler audit flags are finalized | PASS | {'parse_validated': True, 'anchor_audit': 'pass', 'visibility_audit': 'pass'} |

## Scope

This report validates parseability, identity/hash linkage, graph references, anchor presence, disclosure-view membership, and selection-policy invariants. It does not determine whether the paper's scientific trajectory is normatively optimal, and it does not visually prove that every prose anchor points to the intended paragraph.
