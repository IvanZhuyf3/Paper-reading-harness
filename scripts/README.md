# Scripts

## Paper-model validation

`validate_paper_model.py` uses only the Python 3.12 standard library. Run it through the portable Windows launcher:

```bat
scripts\validate_paper_model.bat papers\<paper_slug>\model\paper_model.pending.toml --report papers\<paper_slug>\model\paper_model.audit.md
```

The validator checks TOML parseability, graph references, anchor presence/form, disclosure views, selection-policy invariants, and source-file SHA-256. It does not judge scientific quality or visually verify that prose anchors point to the intended paragraphs.

## Session-state validation

```bat
scripts\validate_session_state.bat papers\<paper_slug>\sessions\<session>.state.toml --report papers\<paper_slug>\sessions\<session>.state.audit.md
```

This checks that the canonical session state resolves to the exact frozen paper-model hash and contains a unique compaction-recovery cursor, selection seed/history, and internally consistent human-node graph.
