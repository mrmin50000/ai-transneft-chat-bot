from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma(
    collection_name="Transneft_info",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

prompt = ChatPromptTemplate.from_template(
    """Ты ассистент-помощник в компании "Транснефть". Отвечай ТОЛЬКО на основе предоставленного контекста.

Контекст:
{context}

Вопрос: {question}

Инструкции:
- Отвечай точно и по делу
- Если ответа нет в контексте, скажи "Я не знаю"
- Не придумывай информацию
- Используй только факты из контекста

Ответ:""")

llm = OllamaLLM(model='llama3:8b')

while True:
    question = input()

    retrieved_docs = vector_store.similarity_search(question, k=3)

    docs_content = "\n".join([str(doc) for doc in retrieved_docs])

    message = prompt.invoke({"question": question, "context": docs_content})

    answer = llm.invoke(message)

    print(answer)
