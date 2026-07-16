import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def datafromOutput(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
            return data
    except FileNotFoundError:
        return "Error file not found"


dataToSendToLLM = datafromOutput("output.md")

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
    model="gemini-3.5-flash",
    input=structured_input
)


output_filename = "structured_circular.md"
with open(output_filename, "w", encoding="utf-8") as file:
    file.write(interaction.output_text)

print(f"Success! Response saved using Interactions API to {output_filename}")
