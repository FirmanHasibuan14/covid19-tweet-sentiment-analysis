import numpy as np
import tensorflow as tf
from typing import Tuple

class MLService:
    def __init__(self, model_path: str):
        try:
            self.model = tf.keras.models.load_model(model_path)
            self.sentiment_map = {
                0: "Negative",
                1: "Neutral",
                2: "Positive"
            }
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def preprocess(self, tweet_text: str) -> list[str]:
        return [tweet_text]
    
    def predict(self, data: list[str]) -> Tuple[int, str]:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        
        prediction_proba = self.model.predict(data)
        sentiment_score = int(np.argmax(prediction_proba[0]))
        sentiment_label = self.sentiment_map.get(sentiment_score, "Undefined")

        return sentiment_score, sentiment_label

ml_service = MLService(model_path="/ML/Model/sentiment_model.h5")