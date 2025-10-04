# This file remains for demonstrating MLflow capabilities.
# It trains a simple English sentiment model.
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from src.processing.preprocessor import clean_text_multilingual

def train():
    mlflow.set_experiment("english-sentiment-analysis")
    try:
        df = pd.read_csv("sentiment_dataset.csv") # User provides this file
    except FileNotFoundError:
        print("Create sentiment_dataset.csv with 'text' and 'sentiment' columns to train.")
        return
    df['cleaned_text'] = df['text'].apply(lambda x: clean_text_multilingual(x, lang='en'))
    X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df['sentiment'], test_size=0.2, random_state=42)
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    with mlflow.start_run():
        model = LogisticRegression()
        model.fit(X_train_vec, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test_vec))
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "sentiment_model")
        print(f"Model trained with accuracy: {accuracy}")

if __name__ == "__main__":
    train()