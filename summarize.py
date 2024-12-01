from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("groq_api_key")
def summarize_jd(input_path,encoding="utf-8"):
    loader=TextLoader(input_path,encoding="utf-8")
    documents=loader.load()


    template = """
        Write a concise and short summary of the following job description,
        Description :{text}

    """
    prompt = PromptTemplate(input_variables=["text"],template=template)

    llm=ChatGroq(model="llama-3.1-8b-instant")

    chain=load_summarize_chain(llm,chain_type="stuff",verbose=True)
    summary=chain.invoke(documents)
    return summary


def summarize_resume(input_path,encoding="utf-8"):
    loader=TextLoader(input_path,encoding="utf-8")
    documents=loader.load()


    template = """
        Write a concise and short summary of the following Resume,
        Resume :{text}

    """
    prompt = PromptTemplate(input_variables=["text"],template=template)

    llm=ChatGroq(model="llama-3.1-8b-instant")

    chain=load_summarize_chain(llm,chain_type="stuff",verbose=True)
    summary=chain.invoke(documents)
    return summary