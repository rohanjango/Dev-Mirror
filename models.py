from sqlalchemy import Column, Integer, String, JSON, DateTime
from database import Base
import datetime

class AnalysisResult(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # We store the raw results from Dhruv and Rohan as JSON
    code_metrics = Column(JSON)      # Dhruv's data
    cognitive_profile = Column(JSON) # Rohan's data
    ai_reflection = Column(String)   # Your AI insight