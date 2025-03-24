from modules.scraper import scrape_news
from modules.sentiment import analyze_sentiment
from modules.summarizer import generate_summary_and_topics
from modules.comparative_analysis import generate_comparative_analysis
from modules.hindi_text_audio import process_and_generate_audio
from modules.hindi_text_audio import process_and_generate_audio

def run_pipeline(company_name):
    news_articles = scrape_news(company_name)
    sentiment_data = analyze_sentiment(news_articles)
    summary_data = generate_summary_and_topics(news_articles)
    comparative_result = generate_comparative_analysis(summary_data, sentiment_data)
    final_sentiment_report = comparative_result.get("Comparative Sentiment Score", {}).get("Final Sentiment Analysis", "")
    hindi_text, audio_buffer = process_and_generate_audio(final_sentiment_report)
    return hindi_text, audio_buffer, comparative_result,summary_data