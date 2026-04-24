import pandas as pd
import os
from keybert import KeyBERT

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

def extract_keywords():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "reviews_sentiment.csv"))
    df["category"] = df["product"].apply(get_category)
    print(f"Extracting keywords from {len(df)} reviews...")
    print(f"Category distribution:\n{df['category'].value_counts()}")

    kw_model = KeyBERT()

    def get_keywords(text):
        try:
            keywords = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                top_n=3
            )
            return ", ".join([kw[0] for kw in keywords])
        except:
            return ""

    df["keywords"] = df["review_text"].apply(get_keywords)
    print("Done extracting keywords!")

    # Flatten keywords with category and sentiment
    rows = []
    for _, row in df.iterrows():
        if pd.isna(row["keywords"]):
            continue
        for kw in row["keywords"].split(", "):
            kw = kw.strip()
            if kw:
                rows.append({
                    "keyword": kw,
                    "sentiment": row["sentiment"],
                    "category": row["category"]
                })

    kw_df = pd.DataFrame(rows)
    kw_freq = kw_df.groupby(["keyword", "sentiment", "category"]).size().reset_index(name="count")
    kw_freq.to_csv(os.path.join(PROCESSED_DIR, "pb_keywords_combined.csv"), index=False)
    print(f"\nSaved pb_keywords_combined.csv with {len(kw_freq)} rows")
    print(f"Sample:\n{kw_freq.head(10)}")

if __name__ == "__main__":
    extract_keywords()