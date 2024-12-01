from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts.prompt import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("groq_api_key")



def resume_checkup(resume_summary,jd_summary):
    template = """
    You are a skilled ATS(Applicany Tracking System) scanner with a deep understanding of data science and other non IT fields and ATS Functionality. Your task is to evaluate the resume summary:{resume_summary} against the provided job description summary:{jd_summary}. Give me the percentage of match if the resume matches with the job description. First output should come as percentage and then keywords missing and final thought about the candidate."""
    prompt = PromptTemplate(input_variables=["resume_summary","jd_summary"],template=template)

    llm=ChatGroq(model="llama-3.1-8b-instant")

    llm_chain = prompt | llm
    response=llm_chain.invoke({"resume_summary":resume_summary,"jd_summary":jd_summary})
    
    complete_prompt = prompt.format(resume_summary=resume_summary,jd_summary=jd_summary)

    return complete_prompt,response.content


