import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## Load enviromental properties
load_dotenv()

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the question asked"),
        ("user","Question:{question}")
    ]
)

## streamlit framework
st.title(f"Welcome to {os.getenv('APP_NAME')}")
input_text=st.text_input("What question you have in mind?")

## Ollama Llama2 model
llm=Ollama(model="gemma:2b")
output_parser=StrOutputParser()


chain=prompt|llm|output_parser


if input_text:
    st.write(chain.invoke({"question":input_text}))