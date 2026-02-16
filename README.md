# 🚀 Dynamic Internal Talent Mapper (Agentic AI + Ollama)

This project matches internal employees to live project demands using **Agentic AI**, **Ollama LLM**, and **vector embeddings**.

## 🔥 Features
- Employee profiles loaded from CSV
- Project requirements loaded from CSV
- ChromaDB vector search for fast retrieval
- Ollama LLM reasoning for transferable skill matching
- Ranked candidate recommendations with match score
- Streamlit UI for demo
- Feedback loop stored in CSV

---

## 🧰 Tech Stack
- Python
- Ollama (llama3 / mistral)
- ChromaDB
- Sentence Transformers
- Streamlit

---

## 🚀 Run with Docker (Recommended)

### Step 1: Build & Start containers
```bash
docker-compose up --build
```

### Step 2: Pull Ollama model (first time only)
In another terminal:
```bash
docker exec -it ollama_server ollama pull llama3
```