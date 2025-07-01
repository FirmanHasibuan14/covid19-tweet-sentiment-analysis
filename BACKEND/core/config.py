from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "COVID19 Sentiment Prediction API"
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()