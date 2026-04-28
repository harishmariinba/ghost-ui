from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

# Enable CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Command(BaseModel):
    text: str

# Intent detection
def detect_intent(text):
    text = text.lower()

    if "project" in text:
        return "open_project"
    elif "chrome" in text or "browser" in text:
        return "open_chrome"
    elif "code" in text or "vs code" in text:
        return "open_vscode"
    elif "downloads" in text:
        return "open_downloads"

    return "unknown"


# Main API
@app.post("/command")
def process_command(command: Command):
    text = command.text
    print("Received:", text)

    intent = detect_intent(text)

    try:
        if intent == "open_project":
            subprocess.run(["open", "/Users/harish/Desktop/ghost-ui"])
            return {"response": "Opening project folder"}

        elif intent == "open_chrome":
            subprocess.run(["open", "-a", "Google Chrome"])
            return {"response": "Opening Chrome"}

        elif intent == "open_vscode":
            subprocess.run(["open", "-a", "Visual Studio Code"])
            return {"response": "Opening VS Code"}

        elif intent == "open_downloads":
            subprocess.run(["open", "/Users/harish/Downloads"])
            return {"response": "Opening Downloads"}

        else:
            return {"response": "Command not recognized"}

    except Exception as e:
        print("Error:", e)
        return {"response": "Error executing command"}