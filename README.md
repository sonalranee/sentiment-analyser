# Consumer Electronics Sentiment Analyser

A end-to-end NLP pipeline that analyses consumer sentiment and extracts key themes from electronics product reviews. Built with Python and visualised in Power BI.

## Overview

This project processes Amazon electronics reviews through a multi-stage pipeline:
- Data cleaning and preprocessing
- Sentiment classification using a transformer-based NLP model
- Keyword extraction using KeyBERT
- Export of structured data for business intelligence dashboards

## Pipeline
raw reviews → clean.py → sentiment.py → keywords.py → export.py → Power BI

## Tech Stack

- **Python** — data processing and NLP pipeline
- **HuggingFace Transformers** — sentiment analysis (cardiffnlp/twitter-roberta-base-sentiment-latest)
- **KeyBERT** — keyword and keyphrase extraction
- **Pandas** — data manipulation
- **Power BI** — interactive dashboard and visualisation

## Project Structure
sentiment-analyser/
├── data/
│   ├── raw/          # source datasets (not tracked)
│   └── processed/    # cleaned and analysed CSVs
├── src/
│   ├── clean.py      # data loading and preprocessing
│   ├── sentiment.py  # sentiment classification
│   ├── keywords.py   # keyword extraction
│   └── export.py     # Power BI export
├── powerbi/          # .pbix dashboard file
└── README.md

## Results

- **3,000 reviews** analysed across Amazon electronics products
- **Sentiment distribution:** 81.7% positive, 9.2% neutral, 9.1% negative
- **Top positive keywords:** great price, alexa, easy use
- **Top negative keywords:** batteries, don't last long

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
python src/export.py
```

## Dataset

Amazon consumer electronics reviews via [Datafiniti on Kaggle](https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products).

