from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

# --- INPUT SCHEMAS (Data coming IN) ---
class ActivityLog(BaseModel):
    file: str
    event: str
    error_type: Optional[str] = None
    timestamp: str

class AnalysisRequest(BaseModel):
    user_id: str
    logs: List[ActivityLog]
    code_snapshot: Optional[str] = ""

# --- OUTPUT SCHEMAS (Data going OUT) ---
class AnalysisResponse(BaseModel):
    status: str
    code_analysis: dict
    cognitive_profile: dict
    ai_reflection: str
    saved_at: datetime

    class Config:
        orm_mode = True