from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to COVID19 Sentiment Prediction API. Go to /docs for documentation."}