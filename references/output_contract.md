# Output Contract

## Required Folder Shape

```text
<paper-slug>-reader/
├── paper.md
├── paper_zh_layout.html
├── paper_zh_layout.pdf
├── paper_full_bilingual.html   # when full bilingual text does not fit same-layout pages
├── paper_full_bilingual.pdf    # when full bilingual text does not fit same-layout pages
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

## Validation Checklist

- `paper.md` contains visible `**Original:**` and `**中文:**` pairs unless the user asked only for Chinese layout.
- Every `assets/...` link in HTML/Markdown exists.
- `source_map.json` parses as JSON and includes stable IDs.
- Important formulas are MathML in HTML and have matching `.mml` files.
- PDF opens, has expected page count, and rendered previews are not blank or badly overlapped.
- `coverage_audit.md` exists and explicitly states whether every extractable page/paragraph has a source/translation pair.
- If the same-layout Chinese PDF omits or compresses text, a complete bilingual comparison artifact exists or the omission is clearly marked as draft/low confidence.
