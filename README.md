# PrivateSphere

**A Local, Privacy-First Multi-Agent Enterprise Research Assistant**

PrivateSphere is a completely offline Retrieval-Augmented Generation (RAG) system designed for enterprise environments. It allows teams to securely upload, query, and analyze highly sensitive internal documents (PDFs, logs, reports) using a cooperative multi-agent AI framework—without ever sending proprietary data to external cloud APIs like OpenAI, Anthropic, or Google.

---

## ✨ Key Features

- **100% Local Processing:** Guarantees zero data leakage. All vector embeddings, document storage, and LLM inference happen entirely on your local hardware.
- **Multi-Agent Architecture:** Uses specialized AI agents (Retriever and Synthesizer) to decouple document searching from report writing, drastically reducing AI hallucinations.
- **Semantic RAG Engine:** Implements recursive character chunking and dense mathematical vector embeddings to accurately map and retrieve context from complex documents.
- **Multi-Tenant Ready:** Uses metadata filtering to ensure the AI only searches within the specific document the user is currently querying, preventing cross-contamination of data.
- **Modern Interface:** Features a clean, dark-mode Streamlit UI with drag-and-drop document ingestion and real-time chat.

---

## 🏗️ Technology Stack

- **Large Language Model (LLM):** [Ollama](https://ollama.com/) running `llama3.1:8b`
- **Agent Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/) (persistent local storage)
- **Embeddings:** Hugging Face `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Document Parsing:** PyMuPDF (`fitz`)
- **Frontend UI:** [Streamlit](https://streamlit.io/)

---

## 📖 Architecture & Development Phases

The project was engineered in four distinct phases to decouple the data logic from the AI routing and user interface.

### Phase 1: Environment & Workspace Setup

- Established isolated Python virtual environments to lock in deterministic dependencies.
- Mapped the file structure into distinct modules (`ingest.py`, `agents.py`, `app.py`) to keep the data pipeline cleanly separated from the UI layer.

### Phase 2: Knowledge Ingestion Pipeline (The Memory)

- **Extraction:** Built custom functions utilizing PyMuPDF to extract text while maintaining page and document-level metadata.
- **Semantic Chunking:** Deployed LangChain's `RecursiveCharacterTextSplitter` (800-character chunks with a 150-character overlap) to prevent splitting sentences in half and losing critical context.
- **Mathematical Indexing:** Used the `all-MiniLM-L6-v2` embedding model to convert raw text chunks into spatial vectors, storing them locally using ChromaDB.

### Phase 3: Multi-Agent Logic (The Brain)

- **State Management:** Defined a strict `TypedDict` in LangGraph to pass the active filename, user query, retrieved context, and drafted response between nodes.
- **The Retriever Node:** Queries ChromaDB using cosine similarity and strict metadata filtering so the agent only searches the exact PDF the user is asking about.
- **The Synthesizer Node:** Takes the retrieved context and feeds it to the local Llama 3 model via Ollama. It utilizes strict prompt engineering to enforce factual boundaries (e.g., returning "Insufficient data" if the database lacks the answer).

### Phase 4: Interface & Styling (The UI)

- Deployed a Streamlit application with customized CSS and a `.streamlit/config.toml` file to force a persistent dark mode with enterprise-blue accents.
- Wired Streamlit's `session_state` to retain chat history and prevent the UI from reloading during asynchronous data pipeline triggers.

---

## 📁 Project Structure

```text
PrivateSphere/
│
├── .streamlit/
│   └── config.toml          # Global UI theme and color settings
├── chroma_db/               # Auto-generated persistent vector storage (created on first run)
├── app.py                   # Streamlit frontend and UI execution loop
├── agents.py                # LangGraph state definitions and agent routing logic
├── ingest.py                # PyMuPDF extraction and ChromaDB semantic chunking
├── requirements.txt         # Pinned Python dependencies
├── test_icon.jpg            # App favicon for Streamlit page config
└── README.md
```

---

## 🚀 Installation & Setup

### 1. Prerequisites

- Python 3.9+ installed on your machine
- [Ollama](https://ollama.com/) installed and running in the background

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/privatesphere.git
cd privatesphere
```

### 3. Set Up the Virtual Environment

It is highly recommended to use a virtual environment to prevent dependency conflicts.

```bash
python -m venv venv
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Download the Local LLM

Ensure your Ollama server is running, then pull the Llama 3.1 model:

```bash
ollama pull llama3.1:8b
```

---

## 💻 Usage

### Starting the Application

Launch the PrivateSphere interface from your project directory:

```bash
streamlit run app.py
```

### How to Use

1. Open your browser to [http://localhost:8501](http://localhost:8501).
2. Use the sidebar to upload a secure PDF document. Wait for the success message indicating the file has been vectorized and stored in ChromaDB.
3. Use the chat interface to ask complex questions about the uploaded document.
4. The Retriever agent finds the relevant paragraphs; the Synthesizer agent drafts a factual, grounded response.

---

## ⚠️ Troubleshooting

### Error: timed out waiting for server to start

Ollama has crashed or is not running in the background. Open a fresh terminal, start the inference server, then restart Streamlit:

```bash
ollama serve
```

### The AI says "I do not have enough information"

- Ensure your PDF contains selectable text (not only scanned images). PrivateSphere relies on text extraction.
- Check your terminal logs to confirm `ingest.py` successfully split the document into chunks.

---

## 🤝 Contributing

Contributions are welcome! If you would like to add new document loaders (e.g., `.docx` or `.csv`), improve the agent prompt engineering, or add new agent nodes (such as a web search agent), please fork the repository and submit a pull request.
