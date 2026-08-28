# Scripts

## PDF inspection artifacts

`prepare_pdf_artifacts.py` extracts page-delimited UTF-8 text, renders every PDF
page to JPEG, builds six-page contact sheets, and records source identity in
`artifact_metadata.json`. Run it with the bundled PDF runtime so `pypdf`, Pillow,
and Poppler are available:

```bat
set PYTHONIOENCODING=utf-8
python scripts\prepare_pdf_artifacts.py source.pdf papers\<paper_slug>\artifacts
```

## Paper-model validation

`validate_paper_model.py` uses only the Python 3.12 standard library. Run it through the portable Windows launcher:

```bat
scripts\validate_paper_model.bat papers\<paper_slug>\model\paper_model.pending.toml --report papers\<paper_slug>\model\paper_model.audit.md
```

The validator checks TOML parseability, graph references, anchor presence/form, disclosure views, selection-policy invariants, and source-file SHA-256. It does not judge scientific quality or visually verify that prose anchors point to the intended paragraphs.

## Session-state validation

Create a model-pinned TRAINING session before its first prompt:

```bat
python scripts\create_training_session.py papers\<paper_slug>\model\paper_model.pending.toml papers\<paper_slug>\sessions\<session>.state.toml --session-id <session> --level foundation --seed <positive-integer>
```

The initializer selects the first dependency-eligible KNOWLEDGE node, freezes
paper evidence designs without result details, writes the canonical TOML, and
creates the initial deterministic Markdown projection.

```bat
scripts\validate_session_state.bat papers\<paper_slug>\sessions\<session>.state.toml --report papers\<paper_slug>\sessions\<session>.state.audit.md
```

This checks the frozen model/source pin, stage dispositions, event prompt/policy provenance, asked-event-pending correspondence, evidence design identity and result-detail boundary, human record graph/terminal statuses, and deterministic Markdown parity.

## Deterministic Markdown projection

```bat
scripts\render_session_markdown.bat papers\<paper_slug>\sessions\<session>.state.toml
scripts\render_session_markdown.bat papers\<paper_slug>\sessions\<session>.state.toml --check
```

The TOML event stream is the only event source. The renderer preserves structural narrative, sorts legacy event narrative by sequence, and writes a generated event timeline between sentinels. `--check` exits nonzero when the Markdown projection has drifted or is out of order.

## Reusable tests

```bat
set PYTHONIOENCODING=utf-8
python -m unittest scripts\test_session_state.py
```

The standard-library tests cover renderer chronology and validator checks for IDs, evidence drift/leaks, frozen transition packets, status consistency, prompt provenance, and skipped terminal stages. Runtime session files under `papers/*/sessions/` are local and Git-ignored. Ordinary turns use the cheap validator and renderer check asynchronously; commits are for reusable paper-model and harness changes.
