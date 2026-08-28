#!/usr/bin/env python3
"""Extract and render a source PDF into reusable inspection artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def extract_text(reader: PdfReader, output: Path) -> None:
    sections = []
    for page_number, page in enumerate(reader.pages, start=1):
        sections.append(
            f"===== PDF PAGE {page_number} =====\n{page.extract_text() or ''}\n"
        )
    output.write_text("\n".join(sections), encoding="utf-8")


def render_pages(source: Path, output_dir: Path, dpi: int) -> list[Path]:
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise RuntimeError("pdftoppm is required but was not found on PATH")
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [renderer, "-jpeg", "-r", str(dpi), str(source), str(output_dir / "page")],
        check=True,
    )
    return sorted(output_dir.glob("page-*.jpg"))


def make_contact_sheets(
    pages: list[Path], output_dir: Path, columns: int = 3, rows: int = 2
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    per_sheet = columns * rows
    thumb_width = 360
    footer_height = 28
    gap = 12
    outputs = []
    for sheet_index in range(0, len(pages), per_sheet):
        batch = pages[sheet_index : sheet_index + per_sheet]
        thumbs = []
        for page_path in batch:
            with Image.open(page_path) as image:
                thumb = image.convert("RGB")
                thumb.thumbnail((thumb_width, 520))
                thumbs.append((page_path, thumb.copy()))
        cell_width = max(image.width for _, image in thumbs)
        cell_height = max(image.height for _, image in thumbs) + footer_height
        sheet = Image.new(
            "RGB",
            (
                columns * cell_width + (columns + 1) * gap,
                rows * cell_height + (rows + 1) * gap,
            ),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        for index, (page_path, image) in enumerate(thumbs):
            row, column = divmod(index, columns)
            x = gap + column * (cell_width + gap) + (cell_width - image.width) // 2
            y = gap + row * (cell_height + gap)
            sheet.paste(image, (x, y))
            label = page_path.stem.replace("page-", "PDF page ")
            draw.text((x, y + image.height + 5), label, fill="black")
        output = output_dir / f"contact-{sheet_index // per_sheet + 1:02d}.jpg"
        sheet.save(output, quality=88)
        outputs.append(output)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("artifacts_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()

    source = args.source.resolve()
    artifacts_dir = args.artifacts_dir.resolve()
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(source)

    extracted_text = artifacts_dir / "extracted_text.txt"
    extract_text(reader, extracted_text)
    pages = render_pages(source, artifacts_dir / "rendered_pages", args.dpi)
    contacts = make_contact_sheets(pages, artifacts_dir / "contact_sheets")

    metadata = {
        "source": source.name,
        "sha256": sha256(source),
        "bytes": source.stat().st_size,
        "pdf_pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "render_dpi": args.dpi,
        "rendered_pages": len(pages),
        "contact_sheets": len(contacts),
    }
    (artifacts_dir / "artifact_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
