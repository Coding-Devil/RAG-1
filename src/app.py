import streamlit as st
from embeddings_manager import EmbeddingsManager
from document_processor import DocumentProcessor
from llm_interface import LLMInterface
import asyncio
import logging
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def get_embeddings_manager():
    return EmbeddingsManager()

@st.cache_resource
def get_llm_interface():
    return LLMInterface()

def process_uploaded_file(file):
    """Process an uploaded file and add it to the vector database"""
    try:
        file_type = file.name.split('.')[-1].lower()
        text = DocumentProcessor.extract_text(file, file_type)
        
        embeddings_manager = get_embeddings_manager()
        embeddings_manager.add_document(
            text,
            metadata={"filename": file.name, "type": file_type}
        )
        return True
    except Exception as e:
        logger.error(f"Error processing file {file.name}: {str(e)}")
        return False

async def get_llm_response(query: str, context: List[str]) -> str:
    """Get response from LLM"""
    llm_interface = get_llm_interface()
    return await llm_interface.query_llm(query, context)

def main():
    st.title("📚 RAG Chatbot")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'doc', 'txt']
        )
        
        if uploaded_files:
            with st.spinner("Processing documents..."):
                for file in uploaded_files:
                    if process_uploaded_file(file):
                        st.success(f"Processed {file.name}")
                    else:
                        st.error(f"Failed to process {file.name}")
        
        # Clear database button
        if st.button("Clear Database"):
            embeddings_manager = get_embeddings_manager()
            embeddings_manager.clear_collection()
            st.session_state.chat_history = []
            st.success("Database cleared!")
        
        # Display chat history
        st.header("Chat History")
        for i, (q, a) in enumerate(st.session_state.chat_history):
            st.text(f"Q{i+1}: {q[:50]}...")

    # Main chat interface
    query = st.text_input("Ask a question about your documents:")
    
    if query:
        with st.spinner("Thinking..."):
            # Get relevant context
            embeddings_manager = get_embeddings_manager()
            context = embeddings_manager.search_documents(query)
            
            # Get LLM response
            response = asyncio.run(get_llm_response(query, context))
            
            # Update chat history
            st.session_state.chat_history.append((query, response))
            
            # Display response
            st.write("### Response:")
            st.write(response)
            
            # Display used context
            with st.expander("View Retrieved Context"):
                for i, ctx in enumerate(context, 1):
                    st.write(f"Context {i}:")
                    st.write(ctx)

if __name__ == "__main__":
    main() 