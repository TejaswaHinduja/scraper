import base64
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

SCRAPER_ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = SCRAPER_ROOT / "downloads"
RAW_DIR = SCRAPER_ROOT / "raw_circulars"
CIRCULARS_DIR = SCRAPER_ROOT / "circulars"

STRUCTURING_PROMPT = (
    "You are supposed to divide this circular into chapters and subsections so "
    "that it is easier for humans to go through these circulars and understand "
    "how their business gets affected from these circular rulings.\n\n"
    "Start the document with a single H1 heading that is exactly: "
    '"{circular_id}". Keep the rest of the content as clear markdown with '
    "chapters and subsections. Output markdown only."
)


def _read_raw_text(circular_id: str) -> str:
    raw_path = RAW_DIR / f"{circular_id}.md"
    if not raw_path.exists():
        return ""
    return raw_path.read_text(encoding="utf-8").strip()


def _build_input(circular_id: str, pdf_path: Path, raw_text: str) -> list[dict]:
    prompt = {
        "type": "text",
        "text": STRUCTURING_PROMPT.format(circular_id=circular_id),
    }

    if raw_text:
        return [prompt, {"type": "text", "text": raw_text}]

    # Scanned / image-only PDFs have no text layer — send the PDF itself.
    pdf_b64 = base64.b64encode(pdf_path.read_bytes()).decode("ascii")
    return [
        prompt,
        {
            "type": "document",
            "mime_type": "application/pdf",
            "data": pdf_b64,
        },
    ]


def _structure_one(pdf_path: Path) -> Path:
    circular_id = pdf_path.stem.strip() or "untitled_circular"
    raw_text = _read_raw_text(circular_id)
    structured_input = _build_input(circular_id, pdf_path, raw_text)

    source = "raw markdown" if raw_text else "PDF document"
    print(f"  Structuring via {source}: {pdf_path.name}")

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=structured_input,
    )

    output_text = (interaction.output_text or "").strip()
    if not output_text:
        raise RuntimeError(f"Gemini returned empty output for {circular_id}")

    output_path = CIRCULARS_DIR / f"{circular_id}.md"
    output_path.write_text(output_text, encoding="utf-8")
    return output_path


def run_gemini_structuring() -> list[Path]:
    pdf_files = sorted(DOWNLOAD_DIR.glob("*.pdf")) if DOWNLOAD_DIR.exists() else []

    if not pdf_files:
        print("Error: No PDF files found to structure.")
        return []

    CIRCULARS_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    skipped: list[str] = []

    print(f"Structuring {len(pdf_files)} circular(s) with Gemini...")

    for pdf_path in pdf_files:
        try:
            output_path = _structure_one(pdf_path)
            written.append(output_path)
            print(f"  Saved -> {output_path}")
        except Exception as exc:
            skipped.append(pdf_path.name)
            print(f"  Failed {pdf_path.name}: {exc}")

    print(
        f"Success! Saved {len(written)} structured circular(s) to {CIRCULARS_DIR}"
    )
    if skipped:
        print(f"Skipped {len(skipped)} file(s): {', '.join(skipped)}")
    return written
