# Output Contract

## Required Folder Shape

```text
<paper-slug>-reader/
├── paper.md
├── paper_zh_final_layout.html   # primary Chinese-only final paper, original-layout
├── paper_zh_final_layout.pdf    # primary Chinese-only final PDF, original-layout
├── source_map.json
├── translation_notes.md
├── coverage_audit.md
├── source.pdf
└── assets/
    ├── fig1.png
    ├── ...
    └── equations/
        ├── eq1.mml
        └── ...
```

Optional support files may be generated when needed, but they must not be treated as final outputs:

- `paper_full_bilingual.html/pdf`: audit-only source/translation comparison.
- `paper_zh_full.html/pdf`: linear fallback when the same-layout draft cannot contain every readable detail.

## `paper.md`

`paper.md` may contain source-grounded bilingual pairs for coverage review. It is not necessarily the final user-facing paper when the user asked for a Chinese-only version.

Use this shape for body blocks:

```markdown
<a id="S001"></a>
### S001 | p.1 | Abstract

**Original:** ...

**中文:** ...
```

Use this shape for figures:

```markdown
<a id="F001"></a>
### Fig. 1

![Fig. 1](assets/fig1.png)

**Original caption:** ...

**中文图注:** ...
```

## `source_map.json`

Minimum keys:

- `source_pdf`
- `source_sha256`
- `artifacts`
- `blocks`
- `figures`
- `tables`
- `equations`
- `notes`

For each block include:

- `id`
- `page`
- `type`
- `original`
- `translation`
- `reading_order`
- `confidence`

For each figure/table include:

- `id`
- `page`
- `asset`
- `original_caption`
- `chinese_caption`
- `placed_near`
- `confidence`

## `translation_notes.md`

Record:

- extraction/OCR quality
- figure/table crop confidence
- equation reconstruction notes
- skipped or low-confidence material
- whether the PDF is final or draft
- validation results
- which artifact is the final Chinese-only reading version
  - This should be `paper_zh_final_layout.html/pdf`.
  - If any other artifact is used as a temporary fallback, explicitly mark the run as draft/limited.

## `coverage_audit.md`

Record the final source-to-output review:

- whether the output is final or draft
- source PDF page count and translated PDF page count(s)
- source text coverage by page or paragraph
- number of visible `Original`/`中文` pairs in `paper.md`
- whether references, captions, tables, author metadata, page headers/footers, and licensing/download notices were translated or intentionally excluded
- layout review findings from rendered previews of the original and translated outputs
- missing, clipped, overlapping, low-confidence, or OCR-corrupted content
- whether a separate `paper_full_bilingual.html/pdf` was generated for full text comparison
- confirmation that side-by-side bilingual artifacts are audit/support files, not the final user-facing Chinese paper

## Validation Checklist

- `paper.md` contains visible `**Original:**` and `**中文:**` pairs unless the user asked only for Chinese layout.
- `paper_zh_final_layout.html/pdf` exists for Chinese-only final reading when the user asks for a Chinese paper in the original paper layout.
- `paper_zh_final_layout.html/pdf` visually preserves the source paper's main page structure: page headers/footers when useful, columns, title block, section order, figures/tables near discussion, and equations near the relevant text.
- No bilingual or linear artifact is presented as the final paper.
- Every `assets/...` link in HTML/Markdown exists.
- `source_map.json` parses as JSON and includes stable IDs.
- Important formulas are MathML in HTML and have matching `.mml` files.
- PDF opens, has expected page count, and rendered previews are not blank or badly overlapped.
- `coverage_audit.md` exists and explicitly states whether every extractable page/paragraph has a source/translation pair.
- If the same-layout Chinese PDF omits or compresses text, the limitation is marked; any optional fallback or bilingual comparison artifact is marked as non-final.
