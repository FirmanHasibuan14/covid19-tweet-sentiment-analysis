from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.connection import Base

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    twwet = Column(String)
    sentiment = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    