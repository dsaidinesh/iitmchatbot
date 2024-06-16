import logging
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import streamlit as st
import warnings
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize the vector database
vectordb = Chroma(
    persist_directory="D:/education/iitmchatbot/chromaDB/db", 
    embedding_function=SentenceTransformerEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
)

retriever = vectordb.as_retriever()

# Define the model repository ID
repo_id = "google/gemma-1.1-2b-it"

# Get the model
llm = HuggingFaceEndpoint(
    repo_id=repo_id, 
    model_kwargs={'max_length': 1024},
    temperature=0.1,
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=True
)

# Function to process and display the LLM response
def process_llm_response(llm_response):
    result = llm_response['result']
    sources = [source.metadata['source'] for source in llm_response["source_documents"]]
    return result, sources

# Streamlit interface
st.title("Question Answering System")

query = st.text_input("Enter your query:")

if st.button("Submit"):
    llm_response = qa_chain.invoke(query)
    result, sources = process_llm_response(llm_response)
    st.write("### Result")
    st.write(result)
    st.write("### Sources")
    for source in sources:
        st.write(source)
