# Local PDF RAG - Chat with Your PDF (100% Local)

A fully local Retrieval-Augmented Generation (RAG) chatbot that lets you upload PDF documents and ask questions about their content. Everything runs on your machine with no external APIs or cloud dependencies.

## 🌟 Features

- 🏠 **100% Local** - No cloud services, complete privacy
- 📄 **PDF Support** - Upload and index PDF documents
- 🤖 **Offline LLM** - Uses Llama 3.1:8B via Ollama
- 🔍 **Semantic Search** - Vector embeddings with nomic-embed-text
- 💬 **Interactive Chat** - Streamlit web interface
- 💾 **Persistent Storage** - Vector database saves between sessions

---

## 🔧 Prerequisites

Before you begin, ensure you have:

- **Python 3.9 or higher** - [Install Python](https://www.python.org/downloads/)
- **Ollama** - [Install Ollama](https://ollama.ai)
- **Git** (optional) - [Install Git](https://git-scm.com)

---

## 📋 Step-by-Step Setup Guide

### Step 1: Clone or Download the Project

**Using Git:**
```bash
git clone <your-repository-url>
cd local-pdf-rag
```

**Or download manually:**
- Download the project folder and navigate into it

### Step 2: Create and Activate Virtual Environment

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web UI framework
- `langchain` - RAG orchestration
- `langchain-community` - Document loaders
- `langchain-chroma` - Vector database
- `langchain-ollama` - LLM/embeddings
- `pypdf` - PDF processing
- `chromadb` - Vector storage

### Step 4: Download Required Ollama Models

Open a terminal and run these commands:

```bash
# Download the LLM model (Llama 3.1:8B)
ollama pull llama3.1:8b

# Download the embedding model
ollama pull nomic-embed-text
```

This may take 5-10 minutes depending on internet speed. Models are cached locally.

### Step 5: Start Ollama Server

In a separate terminal, run:

```bash
ollama serve
```

You should see output like:
```
2026-08-16 14:30:00 - Listening on 127.0.0.1:11434
```

**Keep this terminal open** while using the app.

---

## 🚀 Running the Application

### Step 1: Activate Virtual Environment (if not already active)

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 2: Start the Streamlit App

```bash
streamlit run app.py
```

### Step 3: Access the Application

The app will automatically open in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy and paste the URL into your browser.

---

## 📖 How to Use the Application

### Upload and Index a PDF

1. **Open the app** in your browser
2. **Go to the sidebar** (left panel)
3. **Click "Choose a PDF file"** and select a PDF from your computer
4. **Click "Process & Index PDF"** button
5. **Wait for processing** - You'll see a status message
6. ✅ **Success!** - The app will show the number of indexed text chunks

### Ask Questions

1. **In the main chat area**, type your question in the input field
2. **Press Enter** or click the send button
3. **Wait for response** - The app searches your PDF and generates an answer
4. **View the answer** - The AI response will appear in the chat

### Example Questions
- "What is the main topic of this document?"
- "Summarize the key points from the document"
- "What are the dates mentioned?"
- "Who is the author?"

---

## 🛠️ Troubleshooting

### Issue: "Port already in use" when starting Ollama

**Solution:**
```bash
# Check what's using port 11434
lsof -i :11434

# Kill the process (replace 1234 with the PID)
kill 1234

# Try starting Ollama again
ollama serve
```

### Issue: "ResponseError: Post ... EOF (status code: 400)"

**Cause:** Ollama server is not running or not responding

**Solution:**
1. Ensure Ollama is running: `ollama serve`
2. Wait a few seconds for the server to start
3. Refresh the browser page
4. Try uploading the PDF again

### Issue: "Model not found" error

**Cause:** Required models weren't downloaded

**Solution:**
```bash
# Download models again
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### Issue: "No assistant response" or app says "Please upload and process a PDF"

**Cause:** No PDF has been indexed yet

**Solution:**
1. Upload a PDF file from the sidebar
2. Click "Process & Index PDF"
3. Wait for the success message
4. Then ask questions

### Issue: App is slow or laggy

**Possible causes:**
- Large PDF files (>100 pages) - May take time to process
- Low system RAM - Ollama needs 8GB+ RAM recommended
- CPU-intensive machine - Other apps consuming resources

**Solutions:**
- Try with a smaller PDF first
- Close other applications
- Ensure sufficient disk space (models need ~10GB)

---

## 📁 Project Structure

```
local-pdf-rag/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── README.md                # This file
├── ARCHITECTURE.md          # Detailed architecture documentation
├── chroma_db/               # Vector database (created after first use)
│   ├── chroma.sqlite3
│   └── [embeddings & collections]
└── venv/                    # Virtual environment (auto-created)
```

---

## 🔐 Privacy & Security

✅ **100% Local Processing**
- All PDFs stay on your machine
- No data sent to external servers
- No API keys or subscriptions needed
- Vector database stored locally in `./chroma_db/`

---

## ⚙️ Configuration

Edit `app.py` to customize:

| Setting | Line | Default | Notes |
|---------|------|---------|-------|
| LLM Model | 24 | `llama3.1:8b` | Change to different Ollama model |
| Temperature | 25 | `0.2` | Lower = deterministic, Higher = creative |
| Ollama URL | 21, 26 | `http://127.0.0.1:11434` | Ollama server address |
| Chunk Size | 56 | `1000` | Text chunk size for embeddings |
| Chunk Overlap | 56 | `200` | Overlap between chunks |
| Top-K Results | 72 | `3` | Number of chunks to retrieve |

---

## 📊 Performance Tips

- **First run is slowest** - Embeddings are calculated and cached
- **Smaller PDFs process faster** - Test with 5-10 page PDFs first
- **Better questions get better answers** - Be specific in queries
- **Reload app to clear chat** - Click refresh in browser

---

## 🤝 Contributing

To modify or improve this project:

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Create a Pull Request

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [LangChain Documentation](https://python.langchain.com)
- [Ollama Documentation](https://ollama.ai/docs)
- [Chroma Documentation](https://docs.trychroma.com)

---

## 📝 Project Documentation

For more details:
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **Dependencies**: See [requirements.txt](requirements.txt) for package versions

---

## 🎯 Next Steps

After getting the app running:

1. ✅ Test with a sample PDF
2. 🔄 Try different questions to explore capabilities
3. 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
4. 🛠️ Experiment with different LLM models via Ollama
5. 🚀 Deploy locally on your network (advanced)

---

## 📄 License

This project is open source. Feel free to modify and use it for your needs.

---

## 🆘 Support

If you encounter issues:

1. **Check Troubleshooting section** above
2. **Verify Ollama is running** - `lsof -i :11434` (macOS/Linux)
3. **Check Python version** - Requires Python 3.9+
4. **Review logs** - Streamlit shows detailed error messages
5. **Restart everything** - Kill Ollama and restart the app

---

## ⚡ Quick Start Checklist

- [ ] Python 3.9+ installed
- [ ] Ollama installed and running (`ollama serve`)
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Models downloaded (`ollama pull llama3.1:8b` & `ollama pull nomic-embed-text`)
- [ ] App running (`streamlit run app.py`)
- [ ] Browser opened to `http://localhost:8501`
- [ ] PDF uploaded and indexed
- [ ] Question asked and answered ✅

---

**Happy chatting with your PDFs! 🎉**
