# 📰 Tech News Summarizer & Sentiment Analyzer (Hindi Audio Output)

A powerful NLP pipeline that:
- Scrapes tech news headlines & content 📰
- Summarizes them using BART (`facebook/bart-large-cnn`) 📚
- Analyzes sentiment of each article + final comparative score 📈
- Translates final sentiment report to Hindi 🇮🇳
- Generates Hindi audio using gTTS 🔊
- Displays all results via a clean Streamlit UI 🚀

---

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
Easily deployable on Hugging Face Spaces with Streamlit SDK.

Made with ❤️ by ![PA Gautham nair](www.linkedin.com/ini/pagauthamnair)