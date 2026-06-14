import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

#load environment variables from .env file
load_dotenv()

#load the PDF file
def load_pdf(file):
    loader = PyPDFLoader(file)
    documents = loader.load()
    return documents

#split the documents into smaller chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

#store the chunks in a vector database
def store_chunks(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))
    vectorstore = Chroma.from_documents( embedding=embeddings,documents=chunks, collection_name="pdf_chunks", persist_directory="./chroma_db")
    return vectorstore

#retrieve relevant chunks from the vector database
def retrieve_chunks(query, vectorstore):
    relevant_chunks = vectorstore.similarity_search(query,k=3)
    return relevant_chunks

#get the answer from the language model
def get_answer(query, relevant_chunks):
    llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))


    prompt = PromptTemplate(input_variables=["query", "relevant_chunks"], template=""" 
        you are the world best professor and helpful assistant 
        for answering questions based on the following relevant chunks
        of information from a PDF document: {relevant_chunks}. 
        Please provide a accurate answer to the following question: {query}
        if you don't know the answer just say "THIS INFORMATION IS NOT PRESENT IN YOUR PDF".
        if the user want 16 mark answer give long answer with sub headings like "INTRODUCTION,with sub HEADINGS,CONCLUSION".
        if the user want 2 mark answer give a 4 line short answer""")
    

    answer = llm.invoke(prompt.format(query=query, relevant_chunks="\n".join([chunk.page_content for chunk in relevant_chunks])))
    return answer

#main function 
def chat_with_pdf(file, query):
    documents = load_pdf(file)
    chunks = split_documents(documents)
    vectorstore = store_chunks(chunks)
    relevant_chunks = retrieve_chunks(query, vectorstore)
    answer = get_answer(query, relevant_chunks)
    return answer
