#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_pdfium(extra_path: str | None):
    if extra_path:
        sys.path.insert(0, extra_path)
    try:
        import pypdfium2 as pdfium  # type: ignore

        return pdfium
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated paper Chinese reader artifacts.")
    parser.add_argument("--root", required=True, help="Reader output directory")
    parser.add_argument("--html", default="paper_zh_layout.html")
    parser.add_argument("--pdf", default="paper_zh_layout.pdf")
    parser.add_argument("--render-previews", action="store_true")
    parser.add_argument("--pypdfium2-path", default=None)
    args = parser.parse_args()

    root = Path(args.root)
    html_path = root / args.html
    pdf_path = root / args.pdf
    chinese_full_html_path = root / "paper_zh_full.html"
    chinese_full_pdf_path = root / "paper_zh_full.pdf"
    source_map_path = root / "source_map.json"
    notes_path = root / "translation_notes.md"
    coverage_audit_path = root / "coverage_audit.md"
    paper_md_path = root / "paper.md"

    errors: list[str] = []
    warnings: list[str] = []

    if not html_path.exists():
        errors.append(f"missing HTML: {html_path}")
        html = ""
    else:
        html = html_path.read_text(encoding="utf-8", errors="replace")

    chinese_full_html = chinese_full_html_path.exists()
    chinese_full_pdf = chinese_full_pdf_path.exists()
    if not chinese_full_html:
        warnings.append("missing paper_zh_full.html; Chinese-only final paper not found")
    if not chinese_full_pdf:
        warnings.append("missing paper_zh_full.pdf; Chinese-only final PDF not found")

    asset_links = re.findall(r'(?:src|href)="([^"]+)"', html)
    asset_links = [link for link in asset_links if link.startswith("assets/")]
    missing_assets = [link for link in asset_links if not (root / link).exists()]
    if missing_assets:
        errors.append(f"missing asset links: {missing_assets}")

    if not source_map_path.exists():
        errors.append("missing source_map.json")
        source_map = {}
    else:
        try:
            source_map = json.loads(source_map_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"source_map.json parse failed: {exc}")
            source_map = {}

    if not notes_path.exists():
        warnings.append("missing translation_notes.md")
    if not coverage_audit_path.exists():
        warnings.append("missing coverage_audit.md")
        coverage_audit = ""
    else:
        coverage_audit = coverage_audit_path.read_text(encoding="utf-8", errors="replace")
        audit_markers = ("Original", "中文", "coverage", "覆盖", "audit", "审计", "复查")
        if not any(marker in coverage_audit for marker in audit_markers):
            warnings.append("coverage_audit.md does not appear to describe text/layout coverage")

    if not paper_md_path.exists():
        warnings.append("missing paper.md")
        md = ""
    else:
        md = paper_md_path.read_text(encoding="utf-8", errors="replace")
        if "**Original:**" not in md or "**中文:**" not in md:
            warnings.append("paper.md does not contain visible Original/Chinese pairs")

    mml_files = list((root / "assets" / "equations").glob("*.mml")) if (root / "assets" / "equations").exists() else []
    math_blocks = html.count("<math ")

    pdf_pages = None
    rendered = 0
    if pdf_path.exists():
        pdfium = load_pdfium(args.pypdfium2_path)
        if pdfium is None:
            warnings.append("pypdfium2 unavailable; skipped PDF page/render validation")
        else:
            doc = pdfium.PdfDocument(str(pdf_path))
            pdf_pages = len(doc)
            if args.render_previews:
                preview_dir = root / "_validation_previews"
                preview_dir.mkdir(exist_ok=True)
                for idx in range(len(doc)):
                    doc[idx].render(scale=1.25).to_pil().convert("RGB").save(preview_dir / f"page_{idx + 1}.png")
                    rendered += 1
    else:
        warnings.append(f"missing PDF: {pdf_path}")

    blocks = source_map.get("blocks", []) if isinstance(source_map, dict) else []
    full_page_blocks = [block for block in blocks if isinstance(block, dict) and block.get("type") == "full_page_text"]
    original_pairs = md.count("**Original:**")
    chinese_pairs = md.count("**中文:**")

    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "asset_links": len(asset_links),
        "missing_assets": missing_assets,
        "math_blocks": math_blocks,
        "mml_files": len(mml_files),
        "source_blocks": len(blocks),
        "full_page_blocks": len(full_page_blocks),
        "paper_original_pairs": original_pairs,
        "paper_chinese_pairs": chinese_pairs,
        "coverage_audit": coverage_audit_path.exists(),
        "chinese_full_html": chinese_full_html,
        "chinese_full_pdf": chinese_full_pdf,
        "figures": len(source_map.get("figures", [])) if isinstance(source_map, dict) else 0,
        "equations": len(source_map.get("equations", [])) if isinstance(source_map, dict) else 0,
        "pdf_pages": pdf_pages,
        "rendered_previews": rendered,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
