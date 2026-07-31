import glob
from pathlib import Path

import pymupdf4llm


SCRAPER_ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = SCRAPER_ROOT / "downloads"
RAW_DIR = SCRAPER_ROOT / "raw_circulars"


def _safe_stem(pdf_path: Path) -> str:
    return pdf_path.stem.strip() or "untitled_circular"


def run_extraction() -> list[Path]:
    pdf_files = sorted(Path(p) for p in glob.glob(str(DOWNLOAD_DIR / "*.pdf")))

    if not pdf_files:
        print("Error: No PDF files found to extract.")
        return []

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    print(f"Extracting markdown from {len(pdf_files)} PDF(s)...")

    for pdf_path in pdf_files:
        circular_id = _safe_stem(pdf_path)
        output_path = RAW_DIR / f"{circular_id}.md"

        print(f"  Extracting: {pdf_path.name} -> {output_path.name}")
        markdown = pymupdf4llm.to_markdown(str(pdf_path)) or ""

        if not markdown.strip():
            if output_path.exists():
                output_path.unlink()
            print(
                f"  Warning: no extractable text in {pdf_path.name} "
                "(likely scanned/image PDF). Gemini will use the PDF directly."
            )
            continue

        output_path.write_text(markdown, encoding="utf-8")
        written.append(output_path)

    print(
        f"Extraction successful! Saved {len(written)} text file(s) to {RAW_DIR}"
    )
    return written
