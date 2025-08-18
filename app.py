import streamlit as st
from arti_gen import generate_blog
from seo_tools import generate_seo
from exporters import export_to_pdf, export_to_word, export_to_md

st.set_page_config(page_title="AI Article Generator", layout="wide")

st.title("📝 AI Article Generator (Phase 2)")
st.write("Generate SEO-optimized blogs with multiple export options!")

topic = st.text_input("Enter Topic:")
tone = st.selectbox("Select Tone:", ["informative", "casual", "professional", "storytelling"])
words = st.slider("Word Count:", 300, 2500, 800)
keywords = st.text_input("Enter Keywords (comma separated):")

if st.button("Generate Blog"):
    with st.spinner("Generating blog..."):
        blog = generate_blog(topic, tone, words, keywords)
        st.subheader("Generated Blog:")
        st.write(blog)

        # SEO section
        st.subheader("🔍 SEO Suggestions")
        seo = generate_seo(blog)
        st.write(seo)

        # Export buttons
        st.subheader("📦 Export Options")
        if st.download_button("Download PDF", open(export_to_pdf(blog), "rb"), file_name="article.pdf"):
            pass
        if st.download_button("Download Word", open(export_to_word(blog), "rb"), file_name="article.docx"):
            pass
        if st.download_button("Download Markdown", open(export_to_md(blog), "rb"), file_name="article.md"):
            pass
