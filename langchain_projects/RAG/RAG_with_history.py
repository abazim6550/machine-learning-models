import streamlit as st
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_chroma import Chroma
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain






embeddingModel = OllamaEmbeddings(model= 'gemma:2b')

st.title("Conversational RAG With PDF uplaods and chat history")
st.write("Upload Pdf's and chat with their content")

llm=OllamaLLM(model="gemma:2b")

session_id=st.text_input("Session ID",value="default_session")

if "store" not in st.session_state:
    st.session_state.store = {}

uploaded_file = st.file_uploader('upload file', type='pdf', accept_multiple_files= True)  
if uploaded_file:
    documents = []
    for file in uploaded_file:
        tempPdf = f"./temp.pdf"
        with open(tempPdf, "wb") as file:
            tempPdf.write(file.getvalue())
            file_name = file.name
        loader = PyPDFLoader(tempPdf)
        docs = loader.load()
        documents.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)    
    splitted_docs = text_splitter.split_documents(documents)
    vector_store = Chroma.from_documents(documents=splitted_docs, embedding=embeddingModel)
    retriever=vector_store.as_retriever()

    contextualize_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("SYSTEM", contextualize_q_system_prompt),
            MessagesPlaceholder("HISTORY"),
            ("USER", "{input}"),
        ]
    )

chin = create_history_aware_retriever(llm, retriever, prompt)

system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
question_answer_chain=create_stuff_documents_chain(llm,qa_prompt)
rag_chain=create_retrieval_chain(history_aware_retriever,question_answer_chain)

def get_session_history(session:str)->BaseChatMessageHistory:
            
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]
        
conversational_rag_chain=RunnableWithMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

user_input = st.text_input("Your question:")
if user_input:            
    session_history=get_session_history(session_id)
    response = conversational_rag_chain.invoke(
        {"input": user_input},
        config={
                "configurable": {"session_id":session_id}
                },
            )
st.write(st.session_state.store)
st.write("Assistant:", response['answer'])
st.write("Chat History:", session_history.messages)