import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    print("Splitting text...")
    docs = text_splitter.split_documents(documents)
    return docs

def create_embedding_function():
    embedding_function = SentenceTransformerEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedding_function

def load_into_chroma(docs, embedding_function, persist_directory):
    print("Loading documents into ChromaDB...")
    db = Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)
    return db

website_folder = "/content/drive/MyDrive/www"
pdf_path = "student_handbook.pdf"

pdf_loader = PyPDFLoader(pdf_path)
print("Loading PDF data...")
pdf_documents = pdf_loader.load()


html_documents = []


for root, _, files in os.walk(website_folder):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            html_loader = BSHTMLLoader(file_path)
            html_documents.extend(html_loader.load())

splitted_html_documents = split_text(html_documents)

all_documents = []

all_documents.extend(splitted_html_documents)

all_documents.extend(pdf_documents)

embedding_function = create_embedding_function()


persist_directory = "db"

db = load_into_chroma(all_documents, embedding_function, persist_directory)

print("Documents have been embedded and stored in the local database.")