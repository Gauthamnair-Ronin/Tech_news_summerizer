from groq import Groq
from gtts import gTTS
from googletrans import Translator
import asyncio
from bs4 import BeautifulSoup
import requests
import re
from io import BytesIO

def clean_article_content(content: str) -> str:
    keyword = "advertisement"
    lowered = content.lower()
    index = lowered.find(keyword)
    if index != -1:
        return content[:index].strip()
    return content.strip()

def get_content_string(link: str, headers: dict, news_articles: dict):
    try:
        page = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract title
        title = soup.find("title").text.strip()
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()

        # Extract content
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.text for p in paragraphs])
        article_text = clean_article_content(article_text)

        if "advertisement" not in title.lower():
            news_articles[title] = article_text
    except Exception as e:
        print(f"❌ Failed to scrape {link}: {e}")


def get_sentiment_label(compound_score: float) -> str:
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def clean_keywords(keywords: list) -> list:
    """
    Takes in KeyBERT keyword tuples and returns a deduplicated list of cleaned words.
    """
    cleaned_topics = set()
    for kw in keywords:
        first_word = kw[0].split()[0]  # Only first word
        word = re.sub(r'[^a-zA-Z]', '', first_word)  # Strip symbols
        if word and len(word) > 2:
            cleaned_topics.add(word.lower())
    return list(cleaned_topics)


def initialize_messages():
    return [{"role": "system",
            "content": """You are an expert news analyst and researcher.
                        You will be given summaries of multiple news articles. Your task is to:
                        1. Perform a **comparative analysis** of how each article differs in its focus, tone, or narrative.
                        2. Identify any **similarities** across articles and group them if possible.
                        3. Understand the **main company or organization** discussed across the articles (e.g., Google, Apple, Tesla). If it is not directly named, infer it from context.
                        4. Generate a short, insightful **impact analysis** focused on real-world implications — such as political, economic, and social consequences — for the identified company or organization.

                        \---

                        ### 📝 Comparative Analysis Guidelines:
                        \- Use a format like:
                        \"Article 1 emphasizes X, while Article 2 focuses on Y...\"
                        - Highlight contrasts in tone, themes, or events.
                        - If some articles share a similar narrative, club them together.
                        - Do not repeat the same sentence structure; vary your comparisons.
                        - Focus on content, not grammar or writing style.

                        ---

                        ### 🌍 Impact Analysis Guidelines:
                        - After comparing, write a concise paragraph about the **real-world impact** of the reported events.
                        - Mention how the events affect the company’s public image, operations, stakeholders, or broader industry.
                        - Name the company explicitly when discussing impact (e.g., “This could negatively affect Google’s regulatory standing…”).
                        - Do **not** just summarize again; focus on outcomes, risks, or advantages implied by the articles.
                        - Be analytical, not speculative.

                        ---

                        You must first complete the comparative analysis and then the impact analysis. Be concise, informative, and structured.
                        """}]
messages_prmt = initialize_messages()
def llama_generate(prompt: str) -> str:
    
    client = Groq(api_key="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")
    global messages_prmt
    messages_prmt.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama3-8b-8192",
    )
    LLM_reply = response.choices[0].message.content
    return LLM_reply


def generate_comparison(texts):
    joined = "\n\n".join(texts)
    prompt = f"Compare the following articles:\n{joined}"
    return llama_generate(prompt)

def generate_impact(comparison):
    prompt = f"What is the overall impact of the following news comparison?\n{comparison}"
    return llama_generate(prompt)

def generate_topics_summary(topics: dict):
    """
    Sends a structured prompt to LLaMA asking for a comparative topic analysis
    based on extracted topics. Returns output that can be saved to JSON.
    """
    prompt = f"""
                You are an expert language model analyzing a set of topics extracted from multiple news articles.

                The topics are structured as follows:
                {topics}

                Your task is to:
                1. Identify common themes across articles.
                2. List out unique topics article-wise.
                3. Optionally, interpret what the recurring and unique topics imply about the news focus.

                🎯 Return the response in the following JSON-like format:

                {{
                "common_topics": ["..."],
                "unique_topics": {{
                    "Article 1": ["..."],
                    "Article 2": ["..."]
                }},
                }}

                Respond strictly in this format. Do not add explanations outside the JSON structure.
                """
    return llama_generate(prompt)

def generate_final_sentiment(sentiment_distribution: dict, comparison_text: str) -> str:
    
    sentiment_summary = ", ".join([f"{k}: {v}" for k, v in sentiment_distribution.items()])
    prompt = f"""
                The following is a comparative analysis of recent news articles about a company, and the distribution of their sentiment:

                Comparative Analysis:
                \"\"\"{comparison_text}\"\"\"

                Sentiment Distribution:
                {sentiment_summary}

                Based on both the comparative analysis and sentiment distribution, write a simple, clear, and final sentiment report about the company.
                Use 4 to 5  short sentences. Mention the company if it's clear from context.  Make it easy to understand.
                Avoid technical jargon and keep it natural.
                "Do not include extra titles like 'Sentiment Report' or repeat any headings. The response should be a single, readable paragraph.\n\n"
                
                """
    return llama_generate(prompt)

async def english_to_hindi(text):
    async with Translator() as translator:
        translated = await translator.translate(text, src='en', dest='hi')
        
    return translated.text


def generate_hindi_audio(text):
    try:
        tts = gTTS(text=text, lang='hi')
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        print("🔊 Hindi audio generated in memory")
        return audio_buffer
    except Exception as e:
        print("❌ Error generating Hindi audio:", e)
        return None
