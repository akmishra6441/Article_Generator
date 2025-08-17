import streamlit as st
from article_gen import generate_article

st.set_page_config(page_title="AI Article Generator", layout="wide")

st.title("📝 AI Article Generator")
st.write("Generate high-quality articles using LangChain + OpenAI")

# Inputs
topic = st.text_input("Enter Topic:")
tone = st.selectbox("Select Tone:", ["informative", "casual", "professional", "storytelling"])
words = st.slider("Word Count:", 100, 2000, 500)
keywords = st.text_input("Enter Keywords (comma separated):")

# Button
if st.button("Generate Article"):
    with st.spinner("Generating..."):
        article = generate_article(topic, tone, words, keywords)
        st.subheader("Generated Article:")
        st.write(article)

        # Download button
        st.download_button("📥 Download Article", article, file_name="article.txt")
