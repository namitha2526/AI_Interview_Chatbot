import uvicorn
import webbrowser
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.schemas import Message, InterviewRequest, InterviewFeedback
from backend.utils import evaluate_response, generate_feedback
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend JS access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend HTML, CSS, JS)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def serve_home():
    return FileResponse("frontend/home.html")

@app.post("/contact")
def handle_contact(msg: Message):
    print(f"Message from {msg.name} ({msg.email}): {msg.message}")
    return {"message": "Your message has been received!"}

@app.post("/score", response_model=list[InterviewFeedback])
def score_interview(data: InterviewRequest):
    feedback = []
    for ans in data.responses:
        score = evaluate_response(ans.answer)
        fb = generate_feedback(ans.answer)
        feedback.append(InterviewFeedback(
            question=ans.question,
            score=score,
            feedback=fb
        ))
    return feedback

if __name__ == "__main__":
    import threading
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8000")).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
