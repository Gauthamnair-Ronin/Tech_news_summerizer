# modules/comparative_analysis.py

import json
from collections import Counter, defaultdict
from modules.utils import (
    generate_comparison,
    generate_impact,
    generate_topics_summary,
    generate_final_sentiment
)

def generate_comparative_analysis(summaries_data: dict, sentiment_data: dict) -> dict:
    article_summaries = []
    all_topics = []
    article_topic_map = {}
    sentiment_counter = Counter()
    topic_counts = defaultdict(int)

    for i, (title, content) in enumerate(summaries_data.items(), start=1):
        summary = content["Summary"]
        topics = content["Topics"]
        compressed_summary = " ".join(summary.split()[:30])  # Trim summary
        article_summaries.append(f"Article {i}: {compressed_summary}...")

        lowered_topics = [topic.lower() for topic in topics]
        topic_set = set(lowered_topics)
        all_topics.append(topic_set)

        for topic in topic_set:
            topic_counts[topic] += 1

        article_topic_map[f"Article {i}"] = lowered_topics

        sentiment = sentiment_data.get(title, {}).get("sentiment", "neutral").lower()
        sentiment_counter[sentiment] += 1

    # Topic Overlap
    topic_overlap = generate_topics_summary(article_topic_map)

    # Comparison + Impact
    joined_summaries = "\n".join(article_summaries)
    comparison_text = generate_comparison(joined_summaries)
    impact_text = generate_impact(comparison_text)

    # Final Sentiment Summary
    final_sentiment = generate_final_sentiment(dict(sentiment_counter), comparison_text)

    # Final Structuring
    comparative_results = {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": dict(sentiment_counter),
            "Coverage Differences": [{
                "Comparison": comparison_text,
                "Impact": impact_text
            }],
            "Topic Overlap": topic_overlap,
            "Final Sentiment Analysis": final_sentiment
        }
    }

    return comparative_results
