from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o-mini", temperature=0.5)

meta_template = """
Generate SEO details for the following article:

Article: {article}

Provide:
1. Meta Title (under 60 chars)
2. Meta Description (under 160 chars)
3. Suggested SEO Keywords
"""

seo_prompt = PromptTemplate(
    input_variables=["article"],
    template=meta_template,
)

seo_chain = LLMChain(llm=llm, prompt=seo_prompt)

def generate_seo(article: str):
    return seo_chain.run(article=article)
