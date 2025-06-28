from fastapi import FastAPI
from pydantic import BaseModel
from app.chat_agent import chat_response

app = FastAPI()
session_state = {}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat/")
def chat_endpoint(req: ChatRequest):
    reply = chat_response(req.message, session_state)
    return {"response": reply}