
import os
import streamlit as st
import tempfile
from rag import chat_with_pdf


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()



# Set page configuration
st.set_page_config(page_title="STERLA AI",layout="wide")
st.sidebar.title("STERLA AI")
st.sidebar.markdown("*STERLA is an AI-tool that helps your studies.*")
st.title("**Welcome to STERLA AI!**")


# File uploader
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    st.sidebar.success("File uploaded successfully!")
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

# User query
query = st.chat_input("Enter your question about the PDF:")

if query:
    st.write(query)
    with st.spinner("Generating answer..."):
        answer = chat_with_pdf(tmp_file_path, query)
   

    #store the conversation in session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    st.session_state.conversation.append({"query": query, "answer": answer})

    #display the chat history
    for chat in st.session_state.get("conversation",[]):
        with st.chat_message("user"):
            st.write(chat["query"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])




 
           

   
  
