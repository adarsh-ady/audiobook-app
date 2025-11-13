import streamlit as st
from gtts import gTTS
import pdfplumber
import tempfile

st.set_page_config(page_title="AudioBook for Visually Impaired Students", page_icon="🎧")

st.title("📚 AudioBook for Visually Impaired Students 🇮🇳")
st.write("Upload a PDF, preview the extracted text, and listen to it in an Indian accent voice.")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    if not text.strip():
        st.error("⚠️ Could not extract text. This might be a scanned or image-based PDF.")
    else:
        st.success("✅ Text extracted successfully!")

        # 🧐 Preview before conversion
        st.subheader("🔍 Preview Extracted Text (First 2000 characters)")
        st.text_area("Please verify before generating audio:", text[:2000], height=300)

        if st.button("🎤 Convert to Audio"):
            st.info("Generating audio... please wait ⏳")

            max_len = 4000
            text_chunks = [text[i:i + max_len] for i in range(0, len(text), max_len)]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                for chunk in text_chunks:
                    tts = gTTS(text=chunk, lang='en', tld='co.in')
                    tts.save(temp_audio.name)

                st.audio(temp_audio.name)
                st.success("🎧 Audio generated successfully!")
                st.download_button(
                    label="⬇️ Download Audio File",
                    data=open(temp_audio.name, "rb"),
                    file_name="audiobook.mp3",
                    mime="audio/mpeg"
                )
