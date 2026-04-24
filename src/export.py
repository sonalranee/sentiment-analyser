import pandas as pd
import os

PROCESSED_DIR = "data/processed"

def get_category(product):
    product = str(product)
    if any(x in product for x in ["Kindle", "eReader", "e-Reader"]):
        return "E-Reader"
    elif any(x in product for x in ["Fire", "Tablet"]):
        return "Tablet/TV"
    elif any(x in product for x in ["Echo", "Tap", "Dot", "Alexa"]):
        return "Smart Speaker"
    elif any(x in product for x in ["Battery", "Batteries"]):
        return "Accessories"
    else:
        return "Other"

def export_for_powerbi():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "reviews_sentiment.csv"))
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["year"] = df["review_date"].dt.year
    df["month"] = df["review_date"].dt.month
    df["month_name"] = df["review_date"].dt.strftime("%b")
    df["category"] = df["product"].apply(get_category)

    # 1. Sentiment summary by category
    sentiment_by_product = df.groupby(["category", "sentiment"]).size().reset_index(name="count")
    sentiment_by_product.to_csv(os.path.join(PROCESSED_DIR, "pb_sentiment_by_product.csv"), index=False)

    # 2. Average rating by product with category
    rating_by_product = df.groupby(["product", "category"])["rating"].agg(["mean", "count"]).reset_index()
    rating_by_product.columns = ["product", "category", "avg_rating", "review_count"]
    rating_by_product["avg_rating"] = rating_by_product["avg_rating"].round(2)
    rating_by_product.to_csv(os.path.join(PROCESSED_DIR, "pb_rating_by_product.csv"), index=False)

    # 3. Sentiment trend over time
    sentiment_over_time = df.groupby(["year", "month", "month_name", "sentiment"]).size().reset_index(name="count")
    sentiment_over_time = sentiment_over_time.sort_values(["year", "month"])
    sentiment_over_time.to_csv(os.path.join(PROCESSED_DIR, "pb_sentiment_over_time.csv"), index=False)

    # 4. Overall sentiment summary
    sentiment_summary = df["sentiment"].value_counts().reset_index()
    sentiment_summary.columns = ["sentiment", "count"]
    sentiment_summary.to_csv(os.path.join(PROCESSED_DIR, "pb_sentiment_summary.csv"), index=False)

    print("\nAll Power BI files exported:")
    for f in os.listdir(PROCESSED_DIR):
        if f.startswith("pb_"):
            print(f"  - {f}")

if __name__ == "__main__":
    export_for_powerbi()