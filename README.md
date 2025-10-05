# RAG Assistant for "Transneft" Company

## Project Description

RAG (Retrieval-Augmented Generation) assistant for answering questions about "Transneft" company. The system uses local language models via Ollama and a vector database for searching relevant information.

**Key Features:**
- Intelligent search through corporate documentation
- Natural language responses with context awareness
- Local data storage and processing
- Semantic search using vector embeddings

## System Architecture

### System Components:
1. **Vector Database** - ChromaDB for storing embeddings
2. **Embedding Model** - BGE-M3 via Ollama
3. **Language Model** - Qwen2 via Ollama
4. **Text Processor** - RecursiveCharacterTextSplitter
5. **RAG Assistant** - Main module for query processing

## Installation and Setup

### Prerequisites
- Python 3.8+
- Ollama (installed locally)
- Ollama models: `bge-m3` and `qwen2`

### Installing Dependencies

```bash
# Clone repository (if applicable)
git clone https://github.com/mrmin50000/ai-transneft-chat-bot.git
cd ai-transneft-chat-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install Python packages
pip install langchain langchain-ollama langchain-chroma langchain-text-splitters
```

### Installing Ollama and Models

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Download required models
ollama pull bge-m3
ollama pull qwen2
```

### Data Preparation

1. Place your data file in `data/data.txt` folder
2. File should be in UTF-8 encoding
3. Text files of any size are supported

## Usage

### 1. Creating Vector Database

```bash
python rag_data.py
```
### 2. Starting RAG Assistant

```bash
python query_rag.py
```
---
