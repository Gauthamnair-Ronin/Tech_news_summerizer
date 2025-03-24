# modules/sentiment.py

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from modules.utils import get_sentiment_label

# Ensure lexicon is downloaded
nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(articles: dict) -> dict:
    analyzer = SentimentIntensityAnalyzer()
    sentiment_results = {}

    for title, content in articles.items():
        scores = analyzer.polarity_scores(content)
        compound = scores['compound']
        label = get_sentiment_label(compound)

        sentiment_results[title] = {
            'sentiment': label,
            'compound_score': compound,
            'details': scores
        }

    return sentiment_results
