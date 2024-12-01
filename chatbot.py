from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("groq_api_key")



def get_readychain(system_msg):

    prompt= ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=f"{system_msg}"),
            MessagesPlaceholder(variable_name="messages")
        ]
    )

    llm=ChatGroq(model="llama-3.1-8b-instant")

    chain = prompt | llm

    return chain
