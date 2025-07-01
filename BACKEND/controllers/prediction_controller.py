from sqlalchemy.orm import Session
from services.ml_service import ml_service
from schemas.tweet import TweetCreate
from models.tweet import Tweet


def predict_sentiment(db: Session, request: TweetCreate) -> Tweet:
    tweet_text = request.text
    
    prediction_result = ml_service.predict(tweet_text)

    sentiment_score = prediction_result["predicted_score"]
    sentiment_label = prediction_result["predicted_label"]

    history_entry = Tweet(
        text=tweet_text,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label
    )

    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)

    return history_entry


def get_history_list(db: Session, skip: int = 0, limit: int = 100) -> list[Tweet]:
    return db.query(Tweet).offset(skip).limit(limit).all()