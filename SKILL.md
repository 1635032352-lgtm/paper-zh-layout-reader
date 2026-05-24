---
name: paper-zh-layout-reader
description: Use when converting an English academic paper PDF into Chinese full-paper reader artifacts, including bilingual Markdown with stable source IDs, Chinese same-layout HTML/PDF, extracted figures/tables, bilingual captions, source_map.json, translation_notes.md, assets, and MathType-compatible MathML equation files.
---

# Paper Chinese Layout Reader

## What This Skill Does

Turn a user-provided English academic paper PDF into a complete Chinese reading package, with two preferred surfaces:

- `paper_zh_full.html` and `paper_zh_full.pdf`: complete Chinese-only final reading version. This is the default user-facing paper.
- `paper_zh_layout.html` and `paper_zh_layout.pdf`: Chinese translated version that follows the original paper's page order and layout as closely as practical.
- `paper.md` and/or audit-only bilingual artifacts: source-grounded original/Chinese pairs used to check omissions, not the default final reading surface.

Default output folder: `D:\论文\<paper-slug>-reader\`, unless the user specifies another path.

## Output Contract

Always produce at least:

- `paper.md`
- `paper_zh_full.html`
- `paper_zh_full.pdf` when Chrome/headless browser printing is available
- `paper_zh_layout.html`
- `paper_zh_layout.pdf` when Chrome/headless browser printing is available
- `source_map.json`
- `translation_notes.md`
- `coverage_audit.md`
- `assets\`
- `assets\equations\*.mml` for equations that are reproduced or rebuilt

For exact field expectations and validation checklist, read `references/output_contract.md`.

## Workflow

1. **Probe the PDF first.**
   - Confirm the PDF exists and is readable.
   - Inspect page count, selectable text, image objects, candidate figures/tables, captions, and equations.
   - Use `scripts/probe_pdf.py` when helpful:
     `python scripts/probe_pdf.py --pdf <paper.pdf> --out <workdir>\probe --render-pages --extract-images`

2. **Build a source map before translating.**
   - Assign stable IDs: `S001...` for body blocks, `F001...` for figures, `T001...` for tables, `C001...` for captions, `E001...` for equations.
   - Preserve page number, source text, Chinese translation, confidence, and nearby figure/table references.
   - If OCR or extraction is weak, continue with a draft and mark the weakness in `translation_notes.md`.

3. **Translate conservatively.**
   - Translate the full extractable paper, not only the abstract or highlights.
   - Preserve equations, units, symbols, citation markers, qualifiers, and technical hedging.
   - Use clear Chinese technical prose, but do not turn the paper into a summary.
   - Keep references searchable; bibliographic entries may remain mostly English unless the user asks otherwise.

4. **Handle figures and tables near the first real discussion.**
   - Extract embedded images or crop rendered pages tightly.
   - Do not include unrelated surrounding prose in crops.
   - Put figures/tables near their first substantive discussion in both `paper.md` and the layout HTML.
   - Captions in `paper.md` must be bilingual; captions in same-layout HTML may be Chinese-only when space is tight.

5. **Use MathType-compatible equation handling.**
   - Rebuild important formulas as MathML in HTML.
   - Save each formula as `assets\equations\<id>.mml`.
   - Include a TeX annotation inside MathML when practical.
   - Do not claim that HTML/PDF contains MathType OLE objects. For HTML/PDF, MathML is the MathType-compatible interchange format. Read `references/mathml_mathtype.md` when equations matter.

6. **Create the Chinese same-layout HTML/PDF.**
   - Use original page count and page order when feasible.
   - For IEEE-style papers, default to A4 pages with two columns.
   - Keep figures close to their original or first-discussion positions.
   - Prefer readable Chinese layout over pixel-perfect copying.
   - Print HTML to PDF with Chrome headless when available.

7. **Validate the generated files.**
   - Use `scripts/validate_reader.py --root <output-dir> --render-previews` when possible.
   - Check: JSON parses, image links exist, `.mml` count matches equation records, PDF page count is reasonable, rendered previews are nonblank and not badly overlapped.
   - Record missing/low-confidence items in `translation_notes.md`.

8. **Audit source-to-translation coverage before claiming completion.**
   - Compare the original PDF text, page previews, figures, tables, captions, equations, references, page headers/footers, and author/metadata text against the generated Chinese artifacts.
   - Confirm that `paper.md` and `source_map.json` contain visible `**Original:**` / `**中文:**` pairs for every extractable page or paragraph. Prefer paragraph-level stable IDs; if a same-layout request makes paragraph-level HTML impractical, add full-page stable IDs such as `P01-FULL` and explicitly note that the IDs are page-level.
   - Render both the original PDF and translated HTML/PDF previews. Inspect representative title, method/equation, figure/table, results, references, and final pages for missing text, blank pages, clipped text, formula rendering failures, overlapping layout, or misplaced figures.
   - Write `coverage_audit.md` with: coverage verdict, source-vs-translation text counts or block counts, pages/sections checked, layout findings, missing or low-confidence content, and whether the output is final or draft.
   - The final reading PDF/HTML should be Chinese-only. If a side-by-side or full-page bilingual artifact is useful for checking omissions, generate it as an audit artifact such as `paper_full_bilingual.html/pdf`, and clearly mark it as not the final user-facing paper.
   - Do not say the output is complete unless this audit passes. If it does not pass, deliver the usable draft and make the gaps explicit in both `coverage_audit.md` and `translation_notes.md`.

## User Preference Defaults

- Respond in Chinese.
- Use Windows/PowerShell paths and commands by default.
- Keep the chat final answer short; link the generated local files and report validation status.
- If the user asks for “中文版本的 html/pdf”, prioritize Chinese-only final outputs: `paper_zh_full.html`/`paper_zh_full.pdf`; also keep `paper_zh_layout.html`/`paper_zh_layout.pdf` when a same-layout version is feasible.
- If the user asks for “中英文对照 Markdown”, prioritize complete block-level bilingual `paper.md`.
- If the PDF is too long, scanned, or has figure/OCR issues, produce a usable draft first and clearly label limitations in `translation_notes.md`.

## Legal and Source Boundaries

Work from user-provided files or lawful open-access sources. Do not bypass paywalls or access controls. Avoid pasting long copyrighted passages into chat; put local artifacts in the requested output folder and summarize the result in the final message.
