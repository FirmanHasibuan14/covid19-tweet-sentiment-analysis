from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TweetCreate(BaseModel):
    text: str

class TweetResponse(BaseModel):
    id: int
    text: str
    sentiment_score: int
    sentiment_label: str
    created_at: datetime

    class Config:
        from_attributes = True

class TweetHistoryResponse(BaseModel):
    history: List[TweetResponse]