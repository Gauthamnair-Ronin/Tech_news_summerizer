import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (only needed once)
nltk.download('vader_lexicon')

# Load news articles from your existing JSON
with open('news_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Store results
sentiment_results = {}

for title, content in articles.items():
    # Get sentiment scores
    scores = analyzer.polarity_scores(content)

    # Choose a label based on compound score
    compound = scores['compound']
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'

    # Save result under the article title
    sentiment_results[title] = {
        'sentiment': label,
        'compound_score': compound,
        'details': scores
    }

# Export to JSON
with open('sentiment.json', 'w', encoding='utf-8') as f:
    json.dump(sentiment_results, f, indent=4, ensure_ascii=False)

print("Sentiment analysis completed and saved to sentiment.json")
