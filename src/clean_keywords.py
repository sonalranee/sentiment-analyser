import pandas as pd

df = pd.read_csv("data/processed/pb_keywords_combined.csv")

# Remove keywords that start with numbers
df = df[~df["keyword"].str.match(r'^\d')]

# Remove keywords shorter than 4 characters
df = df[df["keyword"].str.len() >= 4]

# Remove junk words
junk = ["product", "item", "amazon", "stars", "review", "reviews",
        "purchase", "bought", "buy", "ordered", "order", "received",
        "works", "worked", "using", "good", "great", "nice", "love",
        "like", "just", "really", "very", "well", "best", "also",
        "aa", "aaa"]
df = df[~df["keyword"].isin(junk)]
df = df[~df["keyword"].str.startswith("aa ")]
df = df[~df["keyword"].str.startswith("aaa ")]

df.to_csv("data/processed/pb_keywords_combined.csv", index=False)
print(f"Cleaned: {len(df)} rows remaining\n")

# Top keywords per category and sentiment
for category in df["category"].unique():
    for sentiment in ["positive", "negative"]:
        subset = df[(df["category"] == category) & (df["sentiment"] == sentiment)]
        top10 = subset.nlargest(10, "count")
        print(f"\n{category} - {sentiment}:")
        print(top10[["keyword", "count"]].to_string(index=False))