import pandas as pd
import os

PROCESSED_DIR = "data/processed"

def export_for_powerbi():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "reviews_final.csv"))
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["year"] = df["review_date"].dt.year
    df["month"] = df["review_date"].dt.month
    df["month_name"] = df["review_date"].dt.strftime("%b")

    # 1. Sentiment summary by product
    sentiment_by_product = df.groupby(["product", "sentiment"]).size().reset_index(name="count")
    sentiment_by_product.to_csv(os.path.join(PROCESSED_DIR, "pb_sentiment_by_product.csv"), index=False)

    # 2. Average rating by product
    rating_by_product = df.groupby("product")["rating"].agg(["mean", "count"]).reset_index()
    rating_by_product.columns = ["product", "avg_rating", "review_count"]
    rating_by_product["avg_rating"] = rating_by_product["avg_rating"].round(2)
    rating_by_product.to_csv(os.path.join(PROCESSED_DIR, "pb_rating_by_product.csv"), index=False)

    # 3. Sentiment trend over time
    sentiment_over_time = df.groupby(["year", "month", "month_name", "sentiment"]).size().reset_index(name="count")
    sentiment_over_time = sentiment_over_time.sort_values(["year", "month"])
    sentiment_over_time.to_csv(os.path.join(PROCESSED_DIR, "pb_sentiment_over_time.csv"), index=False)

    # 4. Keyword frequency tables (already exist, just confirm)
    for label in ["positive", "negative", "neutral", "all"]:
        path = os.path.join(PROCESSED_DIR, f"keywords_{label}.csv")
        if os.path.exists(path):
            print(f"keywords_{label}.csv ready")

    # 5. Overall sentiment summary
    sentiment_summary = df["sentiment"].value_counts().reset_index()
    sentiment_summary.columns = ["sentiment", "count"]
    sentiment_summary.to_csv(os.path.join(PROCESSED_DIR, "pb_sentiment_summary.csv"), index=False)

    print("\nAll Power BI files exported:")
    for f in os.listdir(PROCESSED_DIR):
        if f.startswith("pb_"):
            print(f"  - {f}")

if __name__ == "__main__":
    export_for_powerbi()