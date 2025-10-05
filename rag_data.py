from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

def create_vector_store():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        add_start_index=True,
        length_function=len,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    )


    file_path = '/home/mrmin50000/github/ai-transneft-chat-bot/data/data.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        print(f"Total characters: {len(file_content)}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    all_splits = text_splitter.split_text(file_content)
    print(f"Total splits: {len(all_splits)}")

    if not all_splits:
        print("No text splits created")
        return None

    embeddings = OllamaEmbeddings(model="bge-m3")

    vector_store = Chroma.from_texts(
        texts=all_splits,
        embedding=embeddings,
        collection_name="Transneft_info",
        persist_directory="./chroma_db"
    )

    print(f"Persisted {len(all_splits)} documents to disk")
    return vector_store

if __name__ == "__main__":
    create_vector_store()
