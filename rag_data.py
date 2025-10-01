from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)

file_path = '/home/mrmin50000/github/ai-transneft-chat-bot/123.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()
print(f"Total characters: {len(file_content)}")

all_splits = text_splitter.split_text(file_content)
print(f"Total splits: {len(all_splits)}")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma(
    collection_name="Transneft_info",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

ids = vector_store.add_texts(all_splits)

print(f"Persisted {len(ids)} documents to disk")