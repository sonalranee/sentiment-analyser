import pandas as pd
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def load_data():
    files = [
        "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv",
        "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv"
    ]
    dfs = []
    for f in files:
        path = os.path.join(RAW_DIR, f)
        df = pd.read_csv(path, low_memory=False)
        dfs.append(df)
        print(f"Loaded {f}: {len(df)} rows, columns: {list(df.columns)}")
    return pd.concat(dfs, ignore_index=True)

def clean_data(df):
    cols_needed = ["name", "brand", "reviews.rating", "reviews.text", "reviews.title", "reviews.date"]
    df = df[cols_needed].copy()
    df.columns = ["product", "brand", "rating", "review_text", "review_title", "review_date"]

    df.dropna(subset=["review_text", "rating"], inplace=True)
    df["review_text"] = df["review_text"].astype(str).str.strip()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df.dropna(subset=["rating"], inplace=True)
    df["rating"] = df["rating"].astype(int)
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["brand"] = df["brand"].fillna("Unknown").str.strip().str.title()
    df["product"] = df["product"].fillna("Unknown").str.strip()

    df.drop_duplicates(subset=["review_text"], inplace=True)

    print(f"\nCleaned data: {len(df)} rows")
    print(f"Brands: {df['brand'].value_counts().head(10)}")
    return df

if __name__ == "__main__":
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = load_data()
    df = clean_data(df)
    df.to_csv(os.path.join(PROCESSED_DIR, "reviews_cleaned.csv"), index=False)
    print("\nSaved to data/processed/reviews_cleaned.csv")