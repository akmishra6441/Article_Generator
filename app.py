import os
import streamlit as st
from generator import generate_article, VALID_TONES
from config import DEFAULT_TONE, DEFAULT_WORD_COUNT, MAX_WORD_COUNT

st.set_page_config(page_title="Article Generator", page_icon="📝", layout="wide")

st.title("📝 Article Generator")
st.caption("v1.0 – Polished & Tested")

with st.sidebar:
    st.header("Settings")
    tone = st.selectbox("Tone", VALID_TONES, index=VALID_TONES.index(DEFAULT_TONE))
    word_count = st.number_input(
        "Target word count",
        min_value=50,
        max_value=MAX_WORD_COUNT,
        value=DEFAULT_WORD_COUNT,
        step=50,
        help="Approximate length. The model may vary slightly."
    )
    temperature = st.slider(
        "Creativity (temperature)", 0.0, 1.5, 0.7, 0.1,
        help="Higher = more creative, lower = more factual"
    )

st.subheader("Enter your topic")
topic = st.text_input("Topic", placeholder="e.g., The impact of AI on remote work")

col1, col2 = st.columns([1, 1])
with col1:
    keywords = st.text_input("Optional keywords (comma-separated)", placeholder="productivity, collaboration, ethics")
with col2:
    outline = st.checkbox("Generate with outline first", value=True)

generate_btn = st.button("Generate Article", type="primary")

# Status / errors area
status_placeholder = st.empty()
output_placeholder = st.empty()

if generate_btn:
    try:
        with st.spinner("Generating... this may take a moment"):
            article, meta = generate_article(
                topic=topic,
                tone=tone,
                word_count=int(word_count),
                keywords=keywords,
                temperature=float(temperature),
                outline_first=outline,
            )
        status_placeholder.success(
            f"✅ Done • Tone: {meta['tone']} • Target words: {meta['word_count']} • Model: {meta['model']}"
        )
        st.download_button(
            label="Download as .txt",
            data=article,
            file_name=f"article_{meta['slug']}.txt",
            mime="text/plain"
        )
        output_placeholder.markdown(article)
    except ValueError as ve:
        status_placeholder.error(f"Input error: {ve}")
    except Exception as e:
        status_placeholder.error("Unexpected error. Check logs / API key.")
        st.exception(e)

st.markdown("---")
st.caption("Tip: Add your screenshots in `demo_screens/` for the README.")