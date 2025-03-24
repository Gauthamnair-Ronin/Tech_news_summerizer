
# 📰 TechSentimentStream: Company News Summarizer with Hindi TTS

A modular, end-to-end pipeline that scrapes recent news about any company, summarizes the articles using BART, compares sentiment across articles, transliterates the Hindi summary using mBART, and generates Hindi audio using AI-based TTS — all running in a Streamlit app!

---

## 🚀 Features

- 🔎 **Web Scraping** from 10 news articles fetched using newsapi.
- 🧠 **BART-based Summarization** of top 10 news articles.
- 💬 **Sentiment Analysis** using HuggingFace models.
- ⚖️ **Comparative Sentiment Summary** of article tones using Llama model.
- 🇮🇳 **Googletrans-based Hindi Transliteration**.
- 🔊 **Hindi Text-to-Speech (TTS)** with audio playback.

---

## 🛠️ Project Structure
```
project-root/ 
│ 
├── app.py # Streamlit frontend 
├── api.py # Orchestrates full pipeline 
├── requirements.txt # All dependencies 
│ └── modules/ 
            ├── scraper.py # Scrapes articles from IndiaToday RSS 
            ├── summarizer.py # Summarizes with Facebook BART 
            ├── sentiment.py # HuggingFace sentiment classification 
            ├── comparative_analysis.py# Aggregates and compares article tones 
            ├── hindi_text_audio.py # Hindi transliteration + TTS 
            └── utils.py # Helpers: content cleaning, parsing, etc.
├── README.md
# 📦 Project Dependencies

This document outlines all major dependencies used in the project along with their purpose.

---

## 🧠 Core Machine Learning

| Library         | Purpose                                                  |
|----------------|----------------------------------------------------------|
| `transformers` | Facebook BART (summarization) and mBART (Hindi) models   |
| `torch`        | Backend framework for running HuggingFace models         |
| `sentencepiece`| Required tokenizer for BART/mBART                        |

---

## 🧹 NLP and Text Processing

| Library         | Purpose                            |
|----------------|-------------------------------------|
| `pandas`        | Data structuring & sentiment table |
| `scikit-learn`  | Sentiment classification metrics   |
| `nltk`          | Optional cleanup, stopwords, etc.  |

---

## 🌐 Web Scraping

| Library           | Purpose                          |
|------------------|-----------------------------------|
| `requests`        | Fetch RSS feeds and article HTML |
| `beautifulsoup4`  | Parse and extract from HTML pages|

---

## 🔊 Hindi Text-to-Speech

| Library     | Purpose                          |
|------------|-----------------------------------|
| `TTS`      | Coqui-AI for generating Hindi audio |
| `soundfile`| For saving/generated audio buffers |
| `numpy`    | Required by audio and ML pipelines  |

---

## 🖼️ Streamlit Frontend

| Library    | Purpose                  |
|------------|--------------------------|
| `streamlit`| App UI and interactivity |
| `io`       | Display audio in browser |

---
```
## 🔧 Modules Overview

- `scraper.py` → Scrapes tech news articles from Non JS news articles using BeautifulSoup 
- `summarizer.py` → Summarizes using BART
- `sentiment.py` → Performs sentiment analysis
- `comparative_analysis.py` → Scores & summarizes overall sentiment using Llama model
- `hindi_text_audio.py` → Translates final sentiment & creates audio
- `utils.py` → Contains utility functions (translation, audio)
- `api.py` → Backend logic connecting modules
- `app.py` → Frontend (Streamlit)

---

## 🚀 How to Run

Install dependencies:
```bash
pip install -r requirements.txt
streamlit run app.py

```

📦 Model Used
facebook/bart-large-cnn from Hugging Face 🤗
Automatically downloaded & cached on first run
Llama through api from Groq  

📍 Deployment
Easily deployable on Hugging Face Spaces with Streamlit SDK. at ![Tech_News_summerizer](https://huggingface.co/spaces/PAGauthamNair/Tech_News_Summarizer)

Made with ❤️ by ![PA Gautham nair](www.linkedin.com/ini/pagauthamnair)
