# RAG Chatbot with Streamlit

A production-ready Retrieval-Augmented Generation (RAG) chatbot using ChromaDB and Llama-3.1-8B-Instruct.

## Features

- Document upload and processing (PDF, DOCX, TXT)
- Vector storage using ChromaDB
- LLM integration with Hugging Face's Llama-3.1-8B-Instruct
- Clean Streamlit interface
- Chat history tracking
- Context visualization

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Hugging Face API key:
   ```bash
   cp .env.example .env
   ```
5. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Add your environment variables in Streamlit Cloud's settings
4. Deploy!

## Usage

1. Upload documents using the sidebar
2. Ask questions in the main chat interface
3. View retrieved context and responses
4. Clear the database using the sidebar button if needed

## License

MIT 