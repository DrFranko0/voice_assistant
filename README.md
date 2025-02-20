# AI Voice Assistant (Backend)

Welcome to the **AI Voice Assistant** backend! This project is a voice assistant that processes text-based queries using predefined intents. If an intent is unknown, it fallsback to **Google Gemini API** for responses.

Built with **FastAPI**.

## Features

-  **Predefined Query Handling**: Detects common user intents.
-  **Google Gemini API Fallback**: Leverages AI for unknown queries.
-  **FastAPI Swagger UI**: Interact effortlessly with an API interface.
-  **Docker Support**: Easily containerized for deployment.
-  **MongoDB Integration**: Stores user interactions for future analysis.
-  **Logging System**: Tracks API requests and responses.

---

##  Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DrFranko0/voice_assistant
cd voice_assistant
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4️⃣ Access API Documentation
Open your browser and go to:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

##  Run with Docker

### Run the Docker Container
```bash
docker run -d -p 8000:8000 --name ai-voice-assistant-container ai-voice-assistant
```

### Access API
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

---
