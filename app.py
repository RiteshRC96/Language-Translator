import streamlit as st
from languages import LANGUAGES
from langdetect import detect, LangDetectException
from gtts import gTTS
from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from tempfile import NamedTemporaryFile

# Set up Streamlit page
st.set_page_config(page_title="EchoLango", page_icon="🗣️", layout="centered")

# Title & Subtitle
st.markdown("<h1 style='text-align: center;'>🌐 EchoLango</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>AI that echoes your thoughts in any language 🌍✨</h4>", unsafe_allow_html=True)
st.markdown("---")

# Initialize Llama 3 via Groq
chat = ChatGroq(
    temperature=0.7,
    model_name="llama3-70b-8192",
    groq_api_key="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"  # replace with your actual key
)

# Function to translate
def query_llama3(text, source_lang, target_lang):
    system_prompt = f"""
    You are a professional translator called 'EchoLango'.
    Translate only the given text from {source_lang} to {target_lang}.
    Maintain natural fluency and cultural accuracy.
    Return only the translated text.
    """
    messages = [
        SystemMessage(content=system_prompt.strip()),
        HumanMessage(content=f"Translate: {text}")
    ]
    response = chat.invoke(messages)
    return response.content

# Function to convert text to audio
def text_to_audio(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        with NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.write_to_fp(f)
            return f.name
    except Exception as e:
        st.error(f"Audio error: {e}")
        return None

# Language selectors
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("🔤 Source Language", LANGUAGES.keys(), index=0)
with col2:
    target_lang = st.selectbox("🌍 Target Language", LANGUAGES.keys(), index=1)

# Session state defaults
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "translated" not in st.session_state:
    st.session_state.translated = ""

# Input text
st.session_state.text_input = st.text_area("✍️ Enter text to translate:", value=st.session_state.text_input, height=150)

# Buttons
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col2:
    if st.button("🔁 Translate"):
        if st.session_state.text_input.strip():
            with st.spinner("Translating..."):
                st.session_state.translated = query_llama3(
                    st.session_state.text_input,
                    source_lang,
                    target_lang
                )
        else:
            st.warning("⚠️ Please enter text.")

# Output box
if st.session_state.translated:
    st.text_area("✅ Translated Text", value=st.session_state.translated, height=150)

# Audio buttons
if st.session_state.text_input:
    if st.button("🔊 Listen to Input Text"):
        audio_path = text_to_audio(st.session_state.text_input, LANGUAGES[source_lang])
        if audio_path:
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')

if st.session_state.translated:
    if st.button("🔊 Listen to Translated Text"):
        audio_path = text_to_audio(st.session_state.translated, LANGUAGES[target_lang])
        if audio_path:
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>Made by <strong>Ritesh Chougule</strong></p>", unsafe_allow_html=True)
