import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Configure page layout
st.set_page_config(page_title="Local PDF Chatbot", layout="wide")
st.title("Chat with my PDF (100% Local M5 RAG)")

# Define a localized persistent directory for your Vector DB
DB_DIR = "./chroma_db"

# Initialize local LLM and Embeddings via Ollama
@st.cache_resource
def init_models():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://127.0.0.1:11434"
    )
    llm = ChatOllama(
        model="llama3.1:8b", 
        temperature=0.2,
        base_url="http://127.0.0.1:11434"
    )
    return embeddings, llm

embeddings, llm = init_models()

# Sidebar for PDF Ingestion
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        # Save uploaded buffer file to disk temporarily
        temp_path = os.path.join("./", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("File uploaded successfully!")
        
        if st.button("Process & Index PDF"):
            with st.spinner("Parsing text and calculating vector embeddings..."):
                # 1. Parse PDF text
                loader = PyPDFLoader(temp_path)
                docs = loader.load()
                
                # 2. Chunk text into digestible overlap slices
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                final_chunks = text_splitter.split_documents(docs)
                
                # 3. Store slices in our local Vector DB
                vector_store = Chroma.from_documents(
                    documents=final_chunks, 
                    embedding=embeddings, 
                    persist_directory=DB_DIR
                )
                st.success(f"Indexed {len(final_chunks)} distinct text segments!")
                
        # Clean up local raw file dump
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Main Chat Interface Logic
st.header("Ask your Document Anything")

# Check if DB contains data to establish a retriever link
if os.path.exists(DB_DIR) and len(os.listdir(DB_DIR)) > 0:
    vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 relevant chunks
    
    # Structure system engineering prompt constraints
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know.\n\n"
        "Context:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Construct the RAG operational chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # UI Chat input text field
    user_query = st.chat_input("What would you like to extract from this document?")
    
    if user_query:
        st.chat_message("user").write(user_query)
        
        with st.spinner("Searching database and thinking..."):
            response = rag_chain.invoke({"input": user_query})
            
        with st.chat_message("assistant"):
            st.write(response["answer"])
else:
    st.info("Please upload and process a PDF file in the sidebar to wake up the assistant.")
