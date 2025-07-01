from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from controllers.prediction_controller import predict_sentiment, get_history_list
from schemas.tweet import TweetCreate, TweetResponse, TweetHistoryResponse

router = APIRouter()

@router.post("/predict", response_model=TweetResponse)
def predict_tweet(request: TweetCreate, db: Session = Depends(get_db)):
    try:
        prediction_record = predict_sentiment(db=db, request=request)
        return prediction_record
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

@router.get("/history", response_model=TweetHistoryResponse)
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        history_list = get_history_list(db=db, skip=skip, limit=limit)
        return TweetHistoryResponse(history=history_list)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"History not found: {e}")
