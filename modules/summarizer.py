# modules/summarizer.py

from transformers import pipeline
from keybert import KeyBERT
from modules.utils import clean_keywords
import re

# Load summarizer + keyword model globally (to avoid reloading each call)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT()

def generate_summary_and_topics(articles: dict) -> dict:
    output = {}

    for title, content in articles.items():
        try:
            # Summarize (truncate to first 1024 tokens for BART)
            summary = summarizer(content[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']

            # Extract keywords using KeyBERT
            keywords = kw_model.extract_keywords(
                content,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=10
            )

            # Clean + deduplicate topics
            topics = clean_keywords(keywords)

            # Store in output
            output[title] = {
                "Summary": summary,
                "Topics": topics
            }

        except Exception as e:
            print(f"❌ Error with article: {title} → {e}")

    return output
