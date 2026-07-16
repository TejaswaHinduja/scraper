from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
apik=os.environ.get("GEMINI_API_KEY")
print(apik)
client = genai.Client(api_key=apik)
def datafromOutput(file_path):
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            data=file.read()
            return data
    except FileNotFoundError:
        return "Error file not found"



interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=datafromOutput("output.md")
)

print(interaction.output_text.encode('utf-8', errors='replace').decode('utf-8'))
