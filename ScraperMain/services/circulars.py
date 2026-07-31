from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Optional


BASE_DIR = Path(__file__).resolve().parents[1]
STRUCTURED_CIRCULARS_DIR = BASE_DIR / "circulars"
H1_PATTERN = re.compile(r"^\s*#\s+(.+?)\s*$")


@dataclass(frozen=True)
class CircularDocument:
    id: str
    title: str
    path: Path
    content: str


def _clean_heading_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = cleaned.replace("<mark>", "").replace("</mark>", "")
    cleaned = cleaned.strip("*_` ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _extract_title(content: str, fallback_title: str) -> str:
    for line in content.splitlines():
        match = H1_PATTERN.match(line)
        if match:
            title = _clean_heading_text(match.group(1))
            if title:
                return title
    return fallback_title


def _list_markdown_files() -> List[Path]:
    if not STRUCTURED_CIRCULARS_DIR.exists():
        return []

    markdown_files = [
        path
        for path in STRUCTURED_CIRCULARS_DIR.iterdir()
        if path.is_file() and path.suffix.lower() == ".md"
    ]
    return sorted(markdown_files, key=lambda path: path.stem.lower())


def load_circular_documents() -> List[CircularDocument]:
    documents: List[CircularDocument] = []

    for path in _list_markdown_files():
        content = path.read_text(encoding="utf-8")
        circular_id = path.stem
        title = _extract_title(content, circular_id)
        documents.append(
            CircularDocument(
                id=circular_id,
                title=title,
                path=path,
                content=content,
            )
        )

    return documents


def load_circular_index() -> Dict[str, CircularDocument]:
    return {document.id: document for document in load_circular_documents()}


def get_circular_document(circular_id: str) -> Optional[CircularDocument]:
    normalized_id = circular_id.strip()
    if not normalized_id:
        return None

    return load_circular_index().get(normalized_id)
