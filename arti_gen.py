import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI model
llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o-mini", temperature=0.7)

# Multi-section template
template = """
Generate a detailed blog post with the following details:

Topic: {topic}
Tone: {tone}
Word Count: Around {words} words
Keywords: {keywords}

Structure:
1. Blog Title
2. Introduction
3. 3-5 Subheadings with detailed explanations
4. Conclusion
"""

prompt = PromptTemplate(
    input_variables=["topic", "tone", "words", "keywords"],
    template=template,
)

article_chain = LLMChain(llm=llm, prompt=prompt)

def generate_blog(topic, tone="informative", words=500, keywords=""):
    return article_chain.run(topic=topic, tone=tone, words=words, keywords=keywords)
