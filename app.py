import streamlit as st
from PyPDF2 import PdfReader
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from summarize import summarize_jd,summarize_resume
from resume_sim import resume_checkup
from chatbot import get_readychain



os.makedirs("Data",exist_ok=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        HumanMessage(content="Give me the percentage of match if the resume matches with the job description. First output should come as percentage and then keywords missing and final thought about the candidate")
    ]

st.set_page_config(page_title="ATS-Friendly Chatbot",layout="wide")
page=st.selectbox("Choose a page:",["Upload","Chatbot"])

if page == "Upload":
    st.title("ATS-Friendly Chatbot")
    

    st.header("Step1: Upload the Job Description")
    job_description = st.text_area("Paste the Job Description here:",height=200)


    if job_description:
        jd_file_path= os.path.join("Data","jd.txt")
        with open(jd_file_path, "w",encoding="utf-8") as jd_file:
            jd_file.write(job_description)
        
        st.success("Job Description uploaded successfully!")

    st.header("Step2: Upload the Resume")
    uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])

    extracted_text=""

    if uploaded_file:
        file_extension = os.path.splitext(uploaded_file.name)[-1].lower()
        if file_extension == ".pdf":
            st.info("Processing the file")
            pdf_reader=PdfReader(uploaded_file)
            extracted_text = " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

            resume_file_path=os.path.join("Data","resume.txt")

        else:
            st.error("Unsupported file format")


        if extracted_text:
            with open(resume_file_path, "w",encoding="utf-8") as resume_file:
                resume_file.write(extracted_text)
            st.success("Resume uploaded successfully!")
            st.text_area("Extracted Resume text:",value=extracted_text,height=150)
            st.success("You are ready, please move to chatbot page and chat with our ATS chatbot")
        else:
            st.warning("Could not extract text from the uploaded resume")

elif page == "Chatbot":
    st.title("ATS-Friendly Chatbot")
    st.subheader("Welcome to our ATS-friendly Chatbot")
    jd_summary=summarize_jd(input_path=os.path.join("Data","jd.txt"))
    resume_summary=summarize_resume(input_path=os.path.join("Data","resume.txt"))

    system_msg,first_history=resume_checkup(resume_summary,jd_summary)

    st.session_state.chat_history.append(AIMessage(first_history))

    updated_chat_list=st.session_state.chat_history.copy()

    chain = get_readychain(system_msg)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt:= st.chat_input(""):
        updated_chat_list.append(HumanMessage(content=prompt))

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            ai_msg=chain.invoke({"messages":updated_chat_list})
            stream = ai_msg.content
            response=st.write(stream)


        st.session_state.messages.append({"role":"assistant","content":stream})





