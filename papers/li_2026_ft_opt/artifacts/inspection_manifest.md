# Source Inspection Manifest

## Copy verification

- Supplied file: `C:\Users\Ivanz\Downloads\temp\AP-26-149008_Proof_hi.pdf`
- Copied filename: `source/Li_et_al_2026_FT_OPT_proof.pdf`
- Source bytes: 12,531,864
- Copied bytes: 12,531,864
- Source SHA-256: `702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D`
- Copied SHA-256: `702F012A0C7FBA10ECDB9DC03619D3AF9CD8DFF05B288F52A31911C6142A6F6D`
- Hash match: PASS

## PDF inspection

- Title: Supercontinuum Fourier-transform Overtone Photothermal Spectroscopy and Microscopy
- Target journal: Advanced Photonics
- Manuscript ID: AP-26-149008
- PDF pages: 43
- Main article: PDF pp. 2-29 (article pp. 1-28)
- Embedded Supplementary Information: PDF pp. 30-43
- Encrypted: no
- Submission status: review proof, not a final published article

## Derived artifacts

- `extracted_text.txt`: UTF-8, page-delimited extraction produced with `pypdf`.
- `rendered_pages/page-01.jpg` through `page-43.jpg`: 120-DPI Poppler renders.
- `contact_sheets/contact-01.jpg` through `contact-08.jpg`: six-page visual inspection sheets, except the final partial sheet.
- `artifact_metadata.json`: source identity and artifact counts.

## Visual verification

- PASS - all 43 PDF pages produced non-empty renders.
- PASS - the title sheet, 28 article pages, and 14 supplementary pages are present.
- PASS - section transitions, equations, five main figures, seven supplementary figures, captions, Methods, references, and page numbering are visible.
- PASS - no clipped pages, black pages, missing figure panels, or unreadable page-level layouts were observed in the eight contact sheets.
- NOTE - the proof includes `For Review Only` watermarks and manuscript line numbers.
- NOTE - the embedded text layer corrupts some symbols, minus signs, units, and selected words. Exact scientific wording and numerical values must be checked against the source render rather than extraction alone.

## Model-preparation result

- Paper-model nodes: 8 knowledge, 26 claim, and 13 evidence nodes.
- Every modeled paper-side node has a paragraph, equation, figure, or Supplementary Information anchor.
- Mechanical model audit: PASS, 20/20.
- The model remains pending and cannot be automatically reused until human approval.
