# 📄 Project Documentation

## 🛠️ Project Setup

Follow these steps to set up and run the project locally or deploy it to Hugging Face Spaces.

### 1. Clone the Repository  
Clone the repository to your local machine using Git and navigate into the project directory.

### 2. Create a Virtual Environment (optional but recommended)  
Use Python’s built-in `venv` to isolate the environment.

### 3. Install Dependencies  
Install all required packages listed in `requirements.txt`.

### 4. Set up API Keys  
Create a `.env` file in the root directory and add your NewsAPI key:

```
NEWS_API_KEY=your_api_key_here
```

### 5. Run the App Locally  
Run the Streamlit frontend using the following command:

``` 
streamlit run app/app.py
```

---

## 🤖 Model Details

### 1. Summarization  
- **Model Used**: `facebook/bart-large-cnn`  
- **Library**: Hugging Face `transformers`  
- **Purpose**: Summarizes full-length scraped news articles into concise bullet points.

### 2. Sentiment Analysis  
- **Model Used**: `cardiffnlp/twitter-roberta-base-sentiment`  
- **Library**: `transformers`, `torch`  
- **Purpose**: Classifies each article as Positive, Negative, or Neutral.

### 3. Text-to-Speech (TTS)  
- **Model Used**: Google Text-to-Speech (`gTTS`)  
- **Library**: `gTTS`  
- **Purpose**: Converts Hindi-transliterated summaries into spoken audio (MP3 format).

---

## 🔌 API Development

The entire app logic is modularized into Python files. `app.py` orchestrates the modules and serves as the Streamlit frontend.

- **APIs are not exposed via FastAPI or Flask**, as the app runs fully within Streamlit.
- The pipeline functions are imported and executed directly when a user submits a query.

### Data Flow

1. User enters a company/topic name in the Streamlit UI.
2. The app triggers the pipeline:
   - Scrapes relevant news articles using NewsAPI + BeautifulSoup.
   - Performs sentiment analysis using SentimentIntensityAnalyzer from nltk.
   - Summarizes each article using BART.
   - Performs Comparative analysis on article summaries and Impact analysis of news.
   - Transliterates the summaries to Hindi.
   - Generates audio using gTTS.
3. Outputs (Summaries, Sentiments,Comparative & Impact Analysis Audio) are displayed on the Streamlit page.

---

## 🌐 API Usage

### 3rd-Party APIs Used

1. **NewsAPI**
   - **Purpose**: Fetch links to relevant news articles.
   - **Integration**: Python’s `requests` library calls NewsAPI’s `/v2/everything` endpoint.
   - **Authentication**: Requires an API key stored in the `.env` file.

2. **gTTS**
   - **Purpose**: Converts Hindi text into speech.
   - **Integration**: Offline library, no additional API key needed.
3. **Groq API**
   - **Purpose**: Used for generating comparative analysis and insights using the LLaMA 3 language model.
   - **Integration**: The `groq` Python client library is used to interact with the Groq API.
   - **Model**: `llama3-8b-8192`
   - **Authentication**: Requires an API key passed to the `Groq` client instance. This key should be kept secret and ideally stored in an environment variable or a secure vault.
   - **Usage Flow**:
     - User query is appended to a list of messages for chat context.
     - The Groq API is called via `client.chat.completions.create(...)`.
     - The model returns a generated response based on the current prompt and conversation history.

---

## ⚠️ Assumptions & Limitations

- **Assumption**: The top 10 links returned by NewsAPI belong to India Today or other valid sources. However, this isn't strictly guaranteed.
- **Limitation**: Streamlit-based apps are not suitable for high-load API consumption.
- **Limitation**: gTTS requires an internet connection; it does not work offline.
- **Limitation**: Models like BART are large (~1.2 GB), increasing cold start time during deployment.
- **Limitation**: Hindi transliteration is basic and may not be grammatically accurate.

---

