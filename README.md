# Paper Zh Layout Reader

`paper-zh-layout-reader` is a Codex skill for converting English academic paper PDFs into Chinese reading artifacts.

It is designed around a practical workflow: read one paper, preserve source traceability, extract figures/tables, rebuild important equations in a MathType-compatible format, and produce both a bilingual Markdown reader and a Chinese same-layout HTML/PDF version.

## What It Produces

For each paper, the skill aims to generate:

- `paper.md` — full-paper Chinese-English paragraph-aligned reader
- `paper_zh_layout.html` — Chinese translated layout version
- `paper_zh_layout.pdf` — PDF printed from the layout HTML
- `source_map.json` — stable source IDs, page numbers, figures, tables, equations, confidence notes
- `translation_notes.md` — OCR, crop, equation, and low-confidence notes
- `assets/` — extracted or cropped figures and tables
- `assets/equations/*.mml` — MathML files that can be opened or reused by MathType-compatible tools

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
- Chinese translated PDF/HTML versions that follow the original page order
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

The scripts expect Python packages such as `pypdf`, and optionally `pypdfium2` for page rendering and PDF preview validation.

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
