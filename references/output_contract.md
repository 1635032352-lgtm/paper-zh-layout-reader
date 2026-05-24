# Output Contract

## Required Folder Shape

```text
<paper-slug>-reader/
├── paper.md
├── paper_zh_full.html
├── paper_zh_full.pdf
├── paper_zh_layout.html
├── paper_zh_layout.pdf
├── paper_full_bilingual.html   # optional audit artifact, not final reading surface
├── paper_full_bilingual.pdf    # optional audit artifact, not final reading surface
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
- `paper_zh_full.html/pdf` exists for Chinese-only final reading when the user asks for a Chinese paper.
- Every `assets/...` link in HTML/Markdown exists.
- `source_map.json` parses as JSON and includes stable IDs.
- Important formulas are MathML in HTML and have matching `.mml` files.
- PDF opens, has expected page count, and rendered previews are not blank or badly overlapped.
- `coverage_audit.md` exists and explicitly states whether every extractable page/paragraph has a source/translation pair.
- If the same-layout Chinese PDF omits or compresses text, a complete Chinese-only full text artifact exists; any bilingual comparison artifact is marked as audit-only.
