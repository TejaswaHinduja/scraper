import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "frontend" / "public"
OUTPUT_FILE = OUTPUT_DIR / "output.md"
STRUCTURED_FILE = OUTPUT_DIR / "structured_circular.md"

def datafromOutput(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
            return data
    except FileNotFoundError:
        return "Error file not found"

def run_gemini_structuring():
    dataToSendToLLM = datafromOutput(OUTPUT_FILE)

    structured_input = [
        {
            "type": "text", 
            "text": "You are supposed to divide this text into chapters and subsections so that it is easier for humans to go through these circulars and understand how their business gets affected from these circular rulings."
        },
        {
            "type": "text", 
            "text": dataToSendToLLM
        }
    ]

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=structured_input
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(STRUCTURED_FILE, "w", encoding="utf-8") as file:
        file.write(interaction.output_text)

    print(f"Success! Response saved using Interactions API to {STRUCTURED_FILE}")
