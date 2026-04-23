import pandas as pd
import os
from transformers import pipeline

PROCESSED_DIR = "data/processed"

def load_sentiment_pipeline():
    print("Loading sentiment model...")
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        truncation=True,
        max_length=512
    )

def get_sentiment(texts, classifier, batch_size=32):
    results = []
    total = len(texts)
    for i in range(0, total, batch_size):
        batch = texts[i:i+batch_size]
        preds = classifier(batch)
        results.extend(preds)
        print(f"Processed {min(i+batch_size, total)}/{total} reviews...", end="\r")
    return results

def run_sentiment():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "reviews_cleaned.csv"))

    # Sample 3000 to keep it fast
    df = df.sample(n=3000, random_state=42).reset_index(drop=True)
    print(f"Running sentiment on {len(df)} reviews...")

    classifier = load_sentiment_pipeline()
    texts = df["review_text"].tolist()
    results = get_sentiment(texts, classifier)

    df["sentiment"] = [r["label"].lower() for r in results]
    df["sentiment_score"] = [round(r["score"], 4) for r in results]

    # Normalize label names
    df["sentiment"] = df["sentiment"].replace({
        "positive": "positive",
        "negative": "negative",
        "neutral": "neutral"
    })

    df.to_csv(os.path.join(PROCESSED_DIR, "reviews_sentiment.csv"), index=False)
    print(f"\nDone! Sentiment distribution:\n{df['sentiment'].value_counts()}")
    print("Saved to data/processed/reviews_sentiment.csv")

if __name__ == "__main__":
    run_sentiment()