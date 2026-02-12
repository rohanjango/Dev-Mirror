from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests
import logging
import json

# --- IMPORT YOUR MODULES ---
# These are the files (database.py, models.py, schemas.py) 
# that must exist in your folder.
import models
import schemas
from database import engine, get_db

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DevMirror-Hub")

# --- CREATE DATABASE TABLES ---
# This automatically creates "devmirror.db" if it doesn't exist.
models.Base.metadata.create_all(bind=engine)

# --- INITIALIZE APP ---
app = FastAPI(title="DevMirror Backend Orchestrator")

# --- CORS (Allow Frontend to Talk to Us) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIG: TEAMMATE URLS ---
# Rohan's Engine (Port 8002)
PATTERN_ENGINE_URL = "http://127.0.0.1:8002/analyze_behavior"
# Dhruv's Engine (Port 8001) - Assumed
CODE_ENGINE_URL = "http://127.0.0.1:8001/analyze_code"


# --- HELPER: SAFE REQUEST ---
def safe_post_request(url: str, payload: dict, default_response: dict):
    """
    Tries to call a teammate's service.
    If they are offline, returns the default_response so we don't crash.
    """
    try:
        logger.info(f"📡 Calling: {url}")
        # Short timeout (2s) so the demo stays fast
        response = requests.post(url, json=payload, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"⚠️ Service Error {response.status_code} from {url}")
    except Exception as e:
        logger.warning(f"⚠️ Service Down ({url}): {e}")
    
    logger.info(f"🛡️ Using FALLBACK data for {url}")
    return default_response


# --- MAIN ENDPOINT ---
@app.post("/analyze", response_model=schemas.AnalysisResponse)
def analyze_dev_mirror(request: schemas.AnalysisRequest, db: Session = Depends(get_db)):
    """
    1. Receives Logs from Frontend/Extension
    2. Calls Dhruv (Code Analysis)
    3. Calls Rohan (Pattern Analysis)
    4. Generates AI Reflection
    5. Saves to Database
    6. Returns Result
    """
    logger.info(f"⚡ Analysis requested for user: {request.user_id}")

    # 1. Call Dhruv (Code Engine)
    # We send him the 'code_snapshot'
    code_result = safe_post_request(
        CODE_ENGINE_URL,
        {"code": request.code_snapshot},
        default_response={"complexity": 0, "bad_patterns": ["Simulated: Service Offline"]}
    )

    # 2. Call Rohan (Pattern Engine)
    # We send him the 'logs'
    # Convert Pydantic models to dict for JSON serialization
    logs_data = [log.dict() for log in request.logs]
    pattern_result = safe_post_request(
        PATTERN_ENGINE_URL,
        {"logs": logs_data},
        default_response={"thinking_style": "Unknown (Fallback)", "confidence": 0.0, "debug_loop": False}
    )

    # 3. Generate AI Reflection (The "Magic")
    # For now, we use a smart f-string. Tomorrow we plug in Gemini here.
    style = pattern_result.get("thinking_style", "Unknown")
    complexity = code_result.get("complexity", 0)
    
    reflection_text = (
        f"DevMirror detects a '{style}' approach. "
        f"Your code complexity is {complexity}. "
        "Try breaking down large functions to improve readability."
    )

    # 4. Save to Database (History)
    db_record = models.AnalysisResult(
        user_id=request.user_id,
        code_metrics=code_result,
        cognitive_profile=pattern_result,
        ai_reflection=reflection_text
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    logger.info("✅ Analysis saved to DB.")

    # 5. Return Structured Response
    return {
        "status": "success",
        "code_analysis": code_result,
        "cognitive_profile": pattern_result,
        "ai_reflection": reflection_text,
        "saved_at": db_record.timestamp
    }

@app.get("/")
def root():
    return {"message": "DevMirror Orchestrator is Running 🚀"}