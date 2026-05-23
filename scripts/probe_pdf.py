#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def load_pdfium(extra_path: str | None):
    if extra_path:
        import sys

        sys.path.insert(0, extra_path)
    try:
        import pypdfium2 as pdfium  # type: ignore

        return pdfium
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe a paper PDF for reader generation.")
    parser.add_argument("--pdf", required=True, help="Input PDF path")
    parser.add_argument("--out", required=True, help="Output probe directory")
    parser.add_argument("--render-pages", action="store_true", help="Render page preview PNGs when pypdfium2 is available")
    parser.add_argument("--extract-images", action="store_true", help="Extract embedded image objects with pypdf")
    parser.add_argument("--scale", type=float, default=2.0, help="Render scale for page previews")
    parser.add_argument("--pypdfium2-path", default=None, help="Optional directory to prepend for pypdfium2 import")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages = []
    text_dir = out_dir / "text"
    text_dir.mkdir(exist_ok=True)
    image_dir = out_dir / "images"
    if args.extract_images:
        image_dir.mkdir(exist_ok=True)

    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        (text_dir / f"page_{page_index}.txt").write_text(text, encoding="utf-8")
        images = list(page.images)
        image_records = []
        if args.extract_images:
            for image_index, image in enumerate(images):
                ext = os.path.splitext(image.name)[1] or ".png"
                image_path = image_dir / f"p{page_index}_img{image_index}{ext}"
                try:
                    image_path.write_bytes(image.data)
                    image_records.append({"index": image_index, "name": image.name, "path": str(image_path), "bytes": image_path.stat().st_size})
                except Exception as exc:
                    image_records.append({"index": image_index, "name": image.name, "error": repr(exc)})
        pages.append(
            {
                "page": page_index,
                "chars": len(text),
                "text_preview": " ".join(text.split())[:500],
                "image_count": len(images),
                "images": image_records,
            }
        )

    rendered_pages = []
    if args.render_pages:
        pdfium = load_pdfium(args.pypdfium2_path)
        if pdfium is not None:
            page_dir = out_dir / "pages"
            page_dir.mkdir(exist_ok=True)
            doc = pdfium.PdfDocument(str(pdf_path))
            for page_index in range(len(doc)):
                image = doc[page_index].render(scale=args.scale).to_pil().convert("RGB")
                path = page_dir / f"page_{page_index + 1}.png"
                image.save(path)
                rendered_pages.append({"page": page_index + 1, "path": str(path), "size": image.size})

    result = {
        "pdf": str(pdf_path),
        "sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
        "page_count": len(reader.pages),
        "pages": pages,
        "rendered_pages": rendered_pages,
    }
    (out_dir / "pdf_probe.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"out": str(out_dir), "page_count": len(reader.pages), "rendered_pages": len(rendered_pages)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
