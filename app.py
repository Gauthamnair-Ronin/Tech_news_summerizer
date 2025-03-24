import streamlit as st
from api import run_pipeline

st.set_page_config(page_title="Hindi News Sentiment Voice", page_icon="📰", layout="centered")

st.title("📰 Hindi News Sentiment Voice Summary")
st.markdown("Analyze the latest news about a company or topic, and hear a summary in **Hindi**!")

# --- User Input ---
company_name = st.text_input("Enter a company or topic to analyze:", value="Infosys")

if st.button("Run Analysis"):
    with st.spinner("🔍 Fetching news, analyzing, summarizing, translating..."):
        hindi_text, audio_buffer, comparative_result,summary_data = run_pipeline(company_name)

    # --- Output: Hindi Text ---
    st.success("✅ Analysis complete!")
    st.subheader("📜 Top 10 articles :")
    st.write(summary_data)
    st.subheader("📜 Compaarative Analysis :")
    st.json({k: v for k, v in comparative_result.items() if k != "Final Sentiment Analysis"})
    

    # --- Output: Hindi Audio ---
    st.subheader("🔊 Listen to the Hindi Audio Summary")
    st.audio(audio_buffer, format='audio/mp3')

# Optional footer
st.markdown("---")
st.caption("Made with 💚 using BART, Llama, gTTS and Streamlit")
