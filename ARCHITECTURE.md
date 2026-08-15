# Local PDF RAG - Project Summary & Architecture

## Project Overview

**Local PDF RAG** is a 100% locally-hosted Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their content. All processing happens on-device with no external API calls or cloud dependencies.

### Key Features
- 🏠 **Fully Local** - No cloud services, all processing on your machine
- 📄 **PDF Support** - Upload and index PDF documents
- 🤖 **LLM-Powered** - Uses Llama 3.1:8B via Ollama
- 🔍 **Vector Search** - Semantic search with nomic-embed-text embeddings
- 💬 **Interactive Chat** - Streamlit-based web UI for Q&A
- 💾 **Persistent Storage** - Vector database persists between sessions

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                         │
│  (Chat Interface + PDF Upload Sidebar)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────▼────────────────────────────────┐
        │     LangChain Orchestration Layer       │
        │  (RAG Chain, Retrieval, Prompts)        │
        └────────┬────────────────────────────────┘
                 │
    ┌────────────┴──────────────────┐
    │                               │
    ▼                               ▼
┌──────────────┐           ┌──────────────────┐
│ Chroma Vector│           │ Ollama LLM Server│
│  DB (Local)  │           │  (Port 11434)    │
│ ./chroma_db  │           │                  │
└──────────────┘           ├──────────────────┤
                           │ Models:          │
                           │ • llama3.1:8b    │
                           │ • nomic-embed-   │
                           │   text           │
                           └──────────────────┘
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web UI framework |
| **Orchestration** | LangChain | RAG pipeline management |
| **Document Loading** | PyPDFLoader | PDF text extraction |
| **Text Processing** | RecursiveCharacterTextSplitter | Document chunking |
| **Vector DB** | Chroma | Local vector storage & retrieval |
| **Embeddings** | Ollama (nomic-embed-text) | Text vectorization |
| **LLM** | Ollama (llama3.1:8b) | Question answering |

---

## Data Flow & Processing Pipeline

### 1. **PDF Ingestion Phase** (Sidebar)
```
User uploads PDF
    ↓
Save temporarily to disk
    ↓
PyPDFLoader reads PDF content
    ↓
Extract text documents
    ↓
RecursiveCharacterTextSplitter chunks text
   (chunk_size=1000, chunk_overlap=200)
    ↓
Generate embeddings via nomic-embed-text
    ↓
Store embeddings + chunks in Chroma DB (./chroma_db)
    ↓
Delete temporary PDF file
```

### 2. **Query Processing Phase** (Main Chat Interface)
```
User asks a question
    ↓
Retrieve top-3 most relevant chunks from Chroma
    ↓
Format prompt with retrieved context + user question
    ↓
Send to llama3.1:8b LLM
    ↓
LLM generates answer with context
    ↓
Display response in chat interface
```

---

## Configuration & Key Parameters

### Vector Database
- **Location**: `./chroma_db/` (persistent local storage)
- **Embeddings Model**: `nomic-embed-text`
- **Storage Engine**: SQLite (chroma.sqlite3)

### Text Chunking
- **Chunk Size**: 1000 tokens
- **Chunk Overlap**: 200 tokens
- **Purpose**: Balance between context preservation and retrieval efficiency

### Retrieval
- **Top-K Retrieval**: 3 most relevant chunks
- **Search Method**: Similarity-based vector search

### LLM Configuration
- **Model**: `llama3.1:8b`
- **Temperature**: 0.2 (deterministic, focused responses)
- **Ollama URL**: `http://127.0.0.1:11434`

### Streamlit Configuration
- **Page Title**: "Local PDF Chatbot"
- **Layout**: Wide (optimal for long documents)

---

## Project Structure

```
local-pdf-rag/
├── app.py                    # Main Streamlit application
├── chroma_db/                # Vector database (persistent)
│   ├── chroma.sqlite3
│   └── [embedding collections]
├── venv/                     # Python virtual environment
├── requirements.txt          # Python dependencies (if exists)
└── ARCHITECTURE.md          # This document
```

---

## Dependencies

**Python Libraries** (installed in venv):
- `streamlit` - Web UI framework
- `langchain` - RAG orchestration
- `langchain-community` - Document loaders
- `langchain-chroma` - Vector DB integration
- `langchain-ollama` - LLM & embedding interface
- `ollama` - Python client for Ollama

**External Services**:
- **Ollama** (must be running locally on port 11434)
  - Provides LLM inference (llama3.1:8b)
  - Provides embeddings (nomic-embed-text)

---

## Usage Flow

### Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama server: `ollama serve` (runs on port 11434)
3. Pull required models:
   - `ollama pull llama3.1:8b`
   - `ollama pull nomic-embed-text`

### Running the Application
```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

Access the app at `http://localhost:8501`

### Using the App
1. **Upload & Index** (Sidebar)
   - Choose a PDF file
   - Click "Process & Index PDF"
   - Wait for embedding calculation
   - Success message shows number of indexed chunks

2. **Ask Questions** (Main Interface)
   - Type a question in the chat input
   - LLM retrieves relevant context from Chroma
   - Generates answer based on context

---

## Error Handling & Troubleshooting

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `ResponseError: Post ... EOF (status code: 400)` | Ollama not running or wrong port | Ensure `ollama serve` is running on port 11434 |
| `Port already in use` | Another Ollama instance running | Kill existing process: `kill [PID]` |
| `Model not found` | Required models not downloaded | `ollama pull llama3.1:8b` and `ollama pull nomic-embed-text` |
| `No assistant response` | Empty vector database | Upload and process a PDF first |

---

## Performance Considerations

- **Chunking Strategy**: 1000-token chunks with 200-token overlap balance context quality with memory efficiency
- **Top-K Retrieval**: Retrieving 3 chunks provides context without overwhelming the LLM
- **Temperature 0.2**: Low temperature ensures consistent, factual answers from the retrieved context
- **Persistent Storage**: Chroma saves embeddings to disk, avoiding re-indexing on app restart

---

## Future Enhancement Ideas

- Support for multiple file formats (DOCX, TXT, etc.)
- Configurable chunk size and overlap parameters via UI
- Query result ranking/scoring display
- Batch PDF upload and indexing
- Chat history export
- Custom system prompts
- Multi-document cross-referencing

---

## Security & Privacy

✅ **100% Local Processing**
- No data sent to external APIs
- All computations on your machine
- Vector DB stored in local directory
- Ollama runs on localhost only

---

## Version Info

- **Created**: 2026-08-16
- **Stack**: Streamlit + LangChain + Chroma + Ollama
- **Python Version**: 3.9+
