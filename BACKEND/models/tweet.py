from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.connection import Base

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment_score = Column(Integer, nullable=False)
    sentiment_label = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    