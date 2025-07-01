from fastapi import FastAPI
from routers import router
from core.config import settings


app = FastAPI(title=settings.APP_NAME)

app.include_router(router.router, prefix="/api/v1", tags=["api"])
@app.get("/")
def read_root():
    return {"message": "Welcome to COVID19 Sentiment Prediction API. Go to /docs for documentation."}