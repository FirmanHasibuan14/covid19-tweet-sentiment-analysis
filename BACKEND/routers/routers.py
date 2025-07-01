from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from controllers import prediction_controller
from schemas.tweet import TweetCreate, TweetResponse, TweetHistoryResponse

router = APIRouter()

@router.post("/predict", response_model=TweetResponse)
def predict_tweet(request: TweetCreate, db: Session = Depends(get_db)):
    try:
        prediction_record = prediction_controller.create_prediction(db=db, request=request)
        return prediction_record
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")

@router.get("/history", response_model=List[TweetHistoryResponse])
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        history_list = prediction_controller.get_history_list(db=db, skip=skip, limit=limit)
        return TweetHistoryResponse(history=history_list)
    except:
        raise HTTPException(status_code=404, detail="History not found")