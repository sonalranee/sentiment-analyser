# Consumer Electronics Sentiment Analyser

An end-to-end NLP pipeline that analyses consumer sentiment and extracts key themes from electronics product reviews. Built with Python, visualised in Jupyter and Power BI.

## Overview

This project processes Amazon electronics reviews through a multi-stage pipeline:
- Data cleaning and preprocessing
- Sentiment classification using a transformer-based NLP model
- Keyword extraction using KeyBERT
- Category-level insight generation
- Export of structured data for business intelligence dashboards

## Pipeline
raw reviews → clean.py → sentiment.py → keywords.py → export.py → Power BI

## Tech Stack

- **Python** — data processing and NLP pipeline
- **HuggingFace Transformers** — sentiment analysis (cardiffnlp/twitter-roberta-base-sentiment-latest)
- **KeyBERT** — keyword and keyphrase extraction
- **Pandas** — data manipulation
- **Matplotlib / Seaborn** — exploratory visualisations
- **Power BI** — interactive dashboard

## Project Structure
## Project Structure

| File | Description |
|---|---|
| `src/clean.py` | Data loading and preprocessing |
| `src/sentiment.py` | Sentiment classification |
| `src/keywords.py` | Keyword extraction with category mapping |
| `src/clean_keywords.py` | Keyword cleanup and filtering |
| `src/export.py` | Power BI export with category insights |
| `notebooks/analysis.ipynb` | Exploratory analysis and category insights |
| `powerbi/analysis.pbix` | Interactive Power BI dashboard |

## Dashboard Pages

**Page 1 — Executive Summary**
Overall sentiment distribution, sentiment by product category with drill down, sentiment trend over time, and key metrics including positive rate and most reviewed products.

**Page 2 — Keyword Explorer**
Interactive keyword analysis by category and sentiment. Filter by category or sentiment to explore what customers are saying about each product line.

## Key Findings

- **3,000 reviews** analysed across Amazon electronics products
- **81.7% positive** sentiment overall
- **Accessories** have the highest review volume but the lowest positive rate (73%) — battery longevity is the top complaint
- **Tablet/TV** has the highest positive rate (90%) — praised for ease of use and gifting appeal
- **Smart Speakers** receive the least negative feedback — Alexa integration drives satisfaction
- **E-Readers** show strong Kindle brand loyalty with occasional hardware complaints

## How to Run

1. Clone the repo and set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Add raw dataset CSVs to `data/raw/`

3. Run the pipeline in order:
```bash
python src/clean.py
python src/sentiment.py
python src/keywords.py
python src/clean_keywords.py
python src/export.py
```

4. Open `notebooks/analysis.ipynb` for exploratory analysis

5. Open `powerbi/Consumer_Sentiment_Dashboard.pbix` in Power BI Desktop for the interactive dashboard

## Dataset

Amazon consumer electronics reviews via [Datafiniti on Kaggle](https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products).