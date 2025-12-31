import os
from dotenv import load_dotenv

## Load enviromental properties
load_dotenv()
print('app name is', os.getenv('APP_NAME'))
print('file name is', os.getenv('FILE_NAME'))

######## - Data Inngestion - ##########

from langchain_community.document_loaders import TextLoader

textLoader = TextLoader('speech.txt')
text_documents=textLoader.load()
#print(text_documents)
#print("-"*50)

from langchain_community.document_loaders import PyPDFLoader
pdfLoader = PyPDFLoader('attention.pdf')
pdfContent=pdfLoader.load()
print(len(pdfContent))


######## - Text splitter - ############

from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
splittedDocs = splitter.split_documents(pdfContent)

from langchain_text_splitters import CharacterTextSplitter
speech = ''
with open('speech.txt') as file:
    speech = file.read()
#print(speech)
splitter = CharacterTextSplitter(chunk_size=100,chunk_overlap=20)
docs = splitter.create_documents(speech)
#print(type(docs[0]))

######## - Embedding - ################


from langchain_community.embeddings import OllamaEmbeddings

embeddingModel = OllamaEmbeddings(model= 'gemma:2b')
#print(embeddingModel)
#embeddings = embeddingModel.embed_documents(text_documents)
#print(embedding)
print('embedding')


######## Vector DB ############

from langchain_community.vectorstores import FAISS
db=FAISS.from_documents(text_documents,embeddingModel)

print(db)
 
query="How does the speaker describe the desired outcome of the war?"
docs=db.similarity_search(query)
docs[0].page_content


retriever=db.as_retriever()
docs=retriever.invoke(query)
docs[0].page_content


#############  Saving And Loading vector DB  ############
db.save_local("faiss_index")


new_db=FAISS.load_local("faiss_index",embeddingModel,allow_dangerous_deserialization=True)
docs=new_db.similarity_search(query)