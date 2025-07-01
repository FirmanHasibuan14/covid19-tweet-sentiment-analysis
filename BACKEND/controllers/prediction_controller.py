from sqlalchemy.orm import Session
from services.ml_service import ml_service
from schemas.tweet import TweetCreate
from models.tweet import Tweet

def predict_sentiment(db: Session, request: TweetCreate) -> Tweet:
    tweet_text = request.text

    processed_data = ml_service.preprocess(tweet_text)
    sentiment_score, sentiment_label = ml_service.predict(processed_data)

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