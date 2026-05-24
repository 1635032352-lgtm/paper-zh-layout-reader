# Paper Zh Layout Reader

[中文说明](README.zh-CN.md) | English

`paper-zh-layout-reader` is a Codex skill for converting English academic paper PDFs into Chinese reading artifacts.

It is designed around a practical workflow: read one paper, preserve source traceability, extract figures/tables, rebuild important equations in a MathType-compatible format, and produce a Chinese-only final paper. Bilingual source/translation artifacts are used for coverage review, not as the default final reading version.

## What It Produces

For each paper, the skill aims to generate:

- `paper.md` — source-grounded original/Chinese audit record
- `paper_zh_final_layout.html` — primary Chinese-only final paper in the original paper layout
- `paper_zh_final_layout.pdf` — primary Chinese-only final PDF printed from the original-layout HTML
- `paper_zh_full.html` — complete Chinese-only linear fallback/supplement
- `paper_zh_full.pdf` — PDF printed from the Chinese-only linear HTML
- `paper_zh_layout.html` — Chinese translated layout version
- `paper_zh_layout.pdf` — PDF printed from the layout HTML
- `source_map.json` — stable source IDs, page numbers, figures, tables, equations, confidence notes
- `translation_notes.md` — OCR, crop, equation, and low-confidence notes
- `coverage_audit.md` — final source-vs-translation text/layout review
- `assets/` — extracted or cropped figures and tables
- `assets/equations/*.mml` — MathML files that can be opened or reused by MathType-compatible tools

If a side-by-side bilingual file is needed, it should be generated only as an audit artifact such as `paper_full_bilingual.html/pdf`. The final user-facing paper should remain Chinese-only and should preserve the original paper layout when requested; a linear reading version is not a substitute for the layout final.

## When To Use

Use this skill when you want Codex to handle prompts like:

```text
Use $paper-zh-layout-reader to translate this English paper PDF into Chinese.
Generate the Chinese same-layout HTML/PDF, keep figures, captions, page numbers,
source IDs, source_map.json, translation_notes.md, and MathType-compatible formulas.
```

It is especially useful for:

- IEEE/ACM/Nature-style academic PDFs
- Chinese-English paper reading notes
- Chinese translated PDF/HTML versions that follow the original page order, columns, headers, figures/tables, and equations
- figure/table-aware translation
- equations that should remain editable through MathML/MathType-compatible sources

## Installation

Clone this repository into a Codex skills directory:

```powershell
git clone https://github.com/1635032352-lgtm/paper-zh-layout-reader.git "$env:USERPROFILE\.codex\skills\paper-zh-layout-reader"
```

Restart Codex so the skill metadata is reloaded.

You can also keep it in a project-local skills folder if your Codex setup loads project skills.

## Repository Structure

```text
paper-zh-layout-reader/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── layout.css
├── references/
│   ├── mathml_mathtype.md
│   └── output_contract.md
├── scripts/
│   ├── probe_pdf.py
│   └── validate_reader.py
├── .gitignore
└── license.txt
```

## Helper Scripts

Probe a PDF before translation:

```powershell
python scripts\probe_pdf.py --pdf "C:\path\paper.pdf" --out "D:\论文\paper-probe" --render-pages --extract-images
```

Validate a generated reader folder:

```powershell
python scripts\validate_reader.py --root "D:\论文\paper-reader" --render-previews
```

The validation step checks links, JSON, MathML counts, PDF previews, and whether a `coverage_audit.md` review exists. The scripts expect Python packages such as `pypdf`, and optionally `pypdfium2` for page rendering and PDF preview validation.

## Final Coverage Audit

Before a run is marked complete, compare the source PDF with the generated Chinese artifacts:

- confirm every extractable page or paragraph has a visible `Original` / `中文` pair in `paper.md` and a stable entry in `source_map.json`;
- render the original PDF and translated PDFs/HTML, then inspect title, method/equation, figure/table, results, references, and final pages for missing text, clipping, overlap, blank pages, or formula rendering problems;
- document the verdict, counts, layout findings, and any low-confidence content in `coverage_audit.md`;
- keep any bilingual comparison output as audit-only, and provide `paper_zh_final_layout.html/pdf` as the Chinese-only original-layout final reading version.
- if only `paper_zh_full.html/pdf` can be generated, mark the original-layout output as missing or low-confidence in `coverage_audit.md` and `translation_notes.md`; do not present the linear version as the final same-layout paper.

## Notes On Equations

HTML/PDF output cannot contain native MathType OLE objects. This skill uses MathML as the interoperable equation source:

- MathML is embedded in `paper_zh_layout.html`.
- Matching `.mml` files are saved under `assets/equations/`.
- TeX annotations are included when practical.

See `references/mathml_mathtype.md` for the detailed convention.

## Legal Boundary

Use this skill with user-provided PDFs or lawful open-access sources. It is not intended to bypass paywalls or access controls.

## License

MIT License. See `license.txt`.
