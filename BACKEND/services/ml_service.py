import re
import nltk
import numpy as np
import pandas as pd
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import Dict, Any

class MLService:
    def __init__(self, model_path: str, data_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self._download_nltk_data()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        df = pd.read_csv(data_path, encoding='latin1')
        

        df['Processed_Text'] = df['OriginalTweet'].apply(self._preprocess)
        
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(oov_token='nothing')
        self.tokenizer.fit_on_texts(df['Processed_Text'])
        
        sequences = self.tokenizer.texts_to_sequences(df['Processed_Text'])
        self.max_length = max(len(tokens) for tokens in sequences)
        
        self.sentiment_map = {
            0: "Neutral",
            1: "Negative",
            2: "Positive"
        }

    def _download_nltk_data(self):
        packages = ['stopwords', 'wordnet', 'omw-1.4']
        for package in packages:
            try:
                nltk.data.find(f'corpora/{package}')
            except LookupError:
                nltk.download(package, quiet=True)

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"http\S+|www\S+", "", text)
        text = re.sub(r"@\w+", "", text)
        text = re.sub(r"#\w+", "", text)
        text = re.sub(r"\d+", "", text)
        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        return text.lower().strip()

    def _remove_stopwords_and_lemmatize(self, text: str) -> str:
        words = text.split()
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        return ' '.join(lemmatized_words)

    def _preprocess(self, text: str) -> str:
        cleaned_text = self._clean_text(text)
        final_text = self._remove_stopwords_and_lemmatize(cleaned_text)
        return final_text

    def predict(self, text_input: str) -> Dict[str, Any]:
        processed_text = self._preprocess(text_input)

        sequences = self.tokenizer.texts_to_sequences([processed_text])
        padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=self.max_length, padding='post')

        prediction_proba = self.model.predict(padded_sequences)
        
        sentiment_score = int(np.argmax(prediction_proba[0]))
        sentiment_label = self.sentiment_map.get(sentiment_score, "Undefined")
        
        return {
            "predicted_label": sentiment_label,
            "predicted_score": sentiment_score,
            "prediction_probabilities": prediction_proba[0].tolist()
        }

ml_service = MLService(
        model_path='../ML/Model/sentiment_model.h5',
        data_path='../ML/Data/Corona_NLP_train.csv', 
)