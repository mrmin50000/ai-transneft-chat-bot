from langchain_text_splitters import RecursiveCharacterTextSplitter
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
    """Ты ассистент-помощник в компании "Транснефть", который должен отвечать на вопросы пользователей исходя из данной тебе информации про компанию.
    Используй нужные куски данного тебе контекста (context) для ответа на вопросы (question). Если ты не знаешь ответа на вопрос, то отвечай "Я не знаю" 
    Question: {question}
    Context: {context}
    Answer:""")

llm = OllamaLLM(model='llama3')

question = "Когда день рождения у транснефти?"

retrieved_docs = vector_store.similarity_search(question, k=3)

docs_content = "\n".join([str(doc) for doc in retrieved_docs])

message = prompt.invoke({"question": question, "context": docs_content})

answer = llm.invoke(message)

print(answer)