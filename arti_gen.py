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

# Prompt template for article generation
template = """
Write a detailed article on the topic: {topic}.
Tone: {tone}
Word Count: Around {words} words
Keywords to include: {keywords}

Structure:
1. Introduction
2. Main Content
3. Conclusion
"""

prompt = PromptTemplate(
    input_variables=["topic", "tone", "words", "keywords"],
    template=template,
)

# LLM chain
article_chain = LLMChain(llm=llm, prompt=prompt)

def generate_article(topic, tone="informative", words=500, keywords=""):
    return article_chain.run(topic=topic, tone=tone, words=words, keywords=keywords)
