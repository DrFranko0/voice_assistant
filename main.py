import os
import time
from datetime import datetime
import logging

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from google import genai

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in environment variables")
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in environment variables")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ai_voice_assistant")

client = MongoClient(MONGO_URI)
db = client['voice-assistant']
collection = db['assistant']

app = FastAPI(
    title="Simple AI Voice Assistant API",
    description="API for processing text input, recognizing intents, and storing interactions",
    version="1.0.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log HTTP requests."""
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Response: {response.status_code} returned in {duration:.2f} seconds")
    return response

class VoiceInput(BaseModel):
    text: str

def recognize_intent(text: str) -> str:
    """Simple intent recognition function."""
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
    gemini_response_text = None

    if intent == "unknown_intent":
        try:
            chat = gemini_client.chats.create(model="gemini-2.0-flash")
            response = chat.send_message(voice_input.text)
            gemini_response_text = response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            logger.error(f"Error with Gemini API: {e}")
            raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

    interaction = {
        "text": voice_input.text,
        "intent": intent,
        "ai_response": gemini_response_text if gemini_response_text else None,
        "timestamp": datetime.utcnow()
    }
    result = collection.insert_one(interaction)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to store the interaction")

    return {
        "intent": intent,
        "message": "Interaction processed successfully",
        "ai_response": gemini_response_text
    }
