from fastapi import FastAPI
from pydantic import BaseModel
from feature_extractor import extract_features
from profile_builder import build_profile

app = FastAPI()

class LogData(BaseModel):
    user_id: str
    session_id: str
    logs: list

@app.get("/")
def home():
    return {"status": "DevMirror Pattern Engine Running"}

@app.post("/analyze_behavior")
def analyze_behavior(data: LogData):
    features = extract_features(data.logs)
    profile = build_profile(features, data.logs)

    return {
        "thinking_style": profile["thinking_style"],
        "weak_area": "debugging" if profile["debug_loop"] else "general",
        "debug_loop": profile["debug_loop"],
        "confidence": profile["confidence_score"]
    }

