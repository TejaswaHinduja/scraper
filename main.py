from pathlib import Path
import subprocess
import sys


ROOT_DIR = Path(__file__).resolve().parent

PIPELINE = [
    ("Scrape latest circular PDFs", ROOT_DIR / "scrape.py" / "mca.py"),
    ("Extract markdown from PDF", ROOT_DIR / "extract" / "extract.py"),
    ("Structure content with Gemini", ROOT_DIR / "services" / "gemini.py"),
]


def run_step(step_name: str, script_path: Path) -> None:
    if not script_path.exists():
        raise FileNotFoundError(f"Step '{step_name}' script not found: {script_path}")

    print(f"\n=== {step_name} ===")
    print(f"Running: {script_path}")

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        check=True,
    )


def main() -> None:
    for step_name, script_path in PIPELINE:
        run_step(step_name, script_path)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()