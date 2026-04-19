from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import RAGChatbotExecutor
import uvicorn

app = FastAPI(title="Mutual Fund RAG API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from Implementation_Phases.Phase_I_Evaluation.feedback_manager import FeedbackManager

# Initialize the RAG Pipeline
bot = RAGChatbotExecutor()
feedback_manager = FeedbackManager()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ChatResponse(BaseModel):
    answer: str
    source_link: str
    footer: str

class FeedbackRequest(BaseModel):
    thread_id: str
    query: str
    response: str
    rating: int # 1 or -1

@app.get("/")
async def root():
    return {"message": "Mutual Fund FAQ Assistant API is online."}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = bot.ask(request.message, thread_id=request.thread_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def feedback_endpoint(request: FeedbackRequest):
    try:
        feedback_manager.record_feedback(
            request.thread_id, 
            request.query, 
            request.response, 
            request.rating
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
