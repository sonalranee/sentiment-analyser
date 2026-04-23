import pandas as pd
import os
from keybert import KeyBERT

PROCESSED_DIR = "data/processed"

def extract_keywords():
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "reviews_sentiment.csv"))
    print(f"Extracting keywords from {len(df)} reviews...")

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

    # Flatten all keywords into a frequency table
    all_keywords = []
    for kws in df["keywords"].dropna():
        for kw in kws.split(", "):
            kw = kw.strip()
            if kw:
                all_keywords.append(kw)

    kw_freq = pd.Series(all_keywords).value_counts().reset_index()
    kw_freq.columns = ["keyword", "count"]

    # Also save keywords per sentiment
    for sentiment in ["positive", "negative", "neutral"]:
        subset = df[df["sentiment"] == sentiment]["keywords"].dropna()
        flat = []
        for kws in subset:
            for kw in kws.split(", "):
                kw = kw.strip()
                if kw:
                    flat.append(kw)
        freq = pd.Series(flat).value_counts().reset_index()
        freq.columns = ["keyword", "count"]
        freq.to_csv(os.path.join(PROCESSED_DIR, f"keywords_{sentiment}.csv"), index=False)
        print(f"Saved keywords_{sentiment}.csv — top 5: {freq['keyword'].head().tolist()}")

    df.to_csv(os.path.join(PROCESSED_DIR, "reviews_final.csv"), index=False)
    kw_freq.to_csv(os.path.join(PROCESSED_DIR, "keywords_all.csv"), index=False)
    print(f"\nTop 10 keywords overall:\n{kw_freq.head(10)}")
    print("Saved reviews_final.csv and keywords_all.csv")

if __name__ == "__main__":
    extract_keywords()