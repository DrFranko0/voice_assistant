import os
import time
from datetime import datetime
import logging

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ai_voice_assistant")

client = MongoClient(MONGO_URI)
db = client.get_database("ai_assistant_db")
interactions_collection = db.interactions

app = FastAPI(
    title="Simple AI Voice Assistant API",
    description="API for processing text input, recognizing intents, and storing interactions",
    version="1.0.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")  # Log request details
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Response: {response.status_code} returned in {duration:.2f} seconds")
    return response

class VoiceInput(BaseModel):
    text: str

def recognize_intent(text: str) -> str:
    lower_text = text.lower()
    if "weather" in lower_text:
        return "weather_query"
    elif "time" in lower_text:
        return "time_query"
    elif "hello" in lower_text or "hi" in lower_text:
        return "greeting"
    else:
        return "unknown_intent"


@app.post("/process", summary="Process voice input and detect intent")
async def process_voice_input(voice_input: VoiceInput):
    intent = recognize_intent(voice_input.text)
    interaction = {
        "text": voice_input.text,
        "intent": intent,
        "timestamp": datetime.utcnow()
    }
    result = interactions_collection.insert_one(interaction)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to store the interaction")
    return {"intent": intent, "message": "Interaction processed successfully"}