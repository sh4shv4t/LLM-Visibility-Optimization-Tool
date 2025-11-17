
# LocalRAG — Your Personal AI Knowledge Base

LocalRAG is a full-stack web application that transforms any website into a private, conversational AI knowledge base. You enter a URL, it scrapes the content, embeds it locally, and lets you chat with that content using a locally-run Large Language Model.

## What This Is

LocalRAG is a self-contained Retrieval-Augmented Generation (RAG) system that runs entirely on your machine. No external APIs or cloud services are used.

## Features

- Full-Stack Application: Flask backend with an HTML + TailwindCSS frontend.
- Dynamic Web Scraping: Playwright for rendering JS-heavy pages, BeautifulSoup + markdownify for HTML → Markdown.
- Local LLM: Uses Ollama to run models like `llama3` or `gemma2` offline.
- Vector Database: ChromaDB stores embeddings generated using `all-MiniLM-L6-v2`.
- LangChain Orchestration: Handles chunking, embedding, retrieval, and prompt building.

## How It Works

### Stage 1: Scrape & Index

1. User enters a URL.
2. Flask endpoint `/scrape` triggers the scraper.
3. Playwright scrapes dynamic content.
4. HTML is cleaned and converted to Markdown.
5. LangChain splits text into chunks.
6. Embeddings are generated using HuggingFace.
7. Vectors are saved into ChromaDB (`./vector_db`).
8. UI displays success.

### Stage 2: Ask a Question

1. User asks a question.
2. Question is converted to a vector.
3. Chroma retrieves top relevant chunks.
4. LangChain constructs a grounded prompt.
5. Prompt is sent to the local LLM via Ollama.
6. Flask returns the model's answer to the UI.

## Tech Stack

- Backend: Python (Flask)
- Frontend: HTML, TailwindCSS, JavaScript
- Web Scraping: Playwright, BeautifulSoup4, markdownify
- Vector DB: ChromaDB
- Embeddings: all-MiniLM-L6-v2
- LLM Runtime: Ollama
- Orchestration: LangChain

## Installation & Setup

### 1. Install Ollama

```bash
ollama pull llama3
```

### 2. Clone the Repository

```bash
git clone https://your-repo-url.com/your-project.git
cd your-project
```

### 3. Create Virtual Environment

**Windows**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask playwright beautifulsoup4 markdownify \
langchain-community langchain-huggingface langchain-text-splitters \
langchain-ollama chromadb sentence-transformers "unstructured[md]"
```

Install Playwright drivers:

```bash
playwright install
```

## Usage

### Start the Server

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

### Step 1: Scrape & Index

* Enter a URL.
* Click **Scrape & Index**.
* Wait for success message.

### Step 2: Ask a Question

* Type a question related to the scraped content.
* Click **Ask**.
* Answer is generated using retrieved context + local LLM.

## Project Structure

```
LocalRAG/
├── app.py
├── scraper.py
├── vector_store.py
├── qa_app.py
├── templates/
│   └── index.html
├── scraped_content.md
└── vector_db/
```

## Future Improvements

* Multiple document ingestion
* Vector database management UI
* Chat history and follow-up question memory
* Streaming model responses
* PDF and text file uploads

