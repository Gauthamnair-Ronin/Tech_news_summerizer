from modules.utils import english_to_hindi, generate_hindi_audio
import asyncio

def process_and_generate_audio(sentiment_text: str):
    hindi_sentiment = asyncio.run(english_to_hindi(sentiment_text))
    print("📜 Translated to Hindi:\n", hindi_sentiment)

    audio_buffer = generate_hindi_audio(hindi_sentiment)
    return hindi_sentiment, audio_buffer
