
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from retrieve_answer import KnowledgeRetriever, DATA_FILE

app = FastAPI(title="AI Voice Chatbox")

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Load the knowledge dataset when the app starts.
retriever = KnowledgeRetriever(DATA_FILE)

# Serve frontend CSS and JavaScript.
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    result = retriever.search(question)

    return {
        "answer": result["answer"],
        "found": result["found"],
        "matched_question": result["matched_question"],
        "score": result["score"]
    }
