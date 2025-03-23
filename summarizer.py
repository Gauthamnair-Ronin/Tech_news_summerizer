from transformers import pipeline
from keybert import KeyBERT
import json
import re
  
# Load the summarizer (lightweight version for Hugging Face)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Load KeyBERT with default (MiniLM) model
kw_model = KeyBERT()

# Load articles
with open("news_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

output = {}

for title, content in articles.items():
    try:
        # Summarize
        summary = summarizer(content[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']


        # Extract topics using KeyBERT
        keywords = kw_model.extract_keywords(
            content,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=10  # You can increase to capture more ideas
        )

        # Extract first word, clean it, and deduplicate
        cleaned_topics = set()
        for kw in keywords:
            first_word = kw[0].split()[0]  # Take only the first word
            word = re.sub(r'[^a-zA-Z]', '', first_word)  # Remove non-alphabetic chars
            if word and len(word) > 2:  # Avoid short or empty strings
                cleaned_topics.add(word.lower())

        topics = list(cleaned_topics)

        # Store the output
        output[title] = {
            "Summary": summary,
            "Topics": topics
        }

    except Exception as e:
        print(f"❌ Error with article: {title} → {e}")

# Save result
with open("summary_topics.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Summary + Topics saved to summary_topics.json")
