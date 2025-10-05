from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
import speech_recognition as sr

class TransneftRAGAssistant:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="bge-m3")
        self.recognizer = sr.Recognizer()
        self.vector_store = Chroma(
            collection_name="Transneft_info",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )

        self.prompt = ChatPromptTemplate.from_template(
            """Ты ассистент-помощник в компании "Транснефть". Отвечай ТОЛЬКО на основе предоставленного контекста.

            Контекст: {context}

            Вопрос: {question}

            Инструкции:
            - Отвечай точно и по делу
            - Не придумывай информацию
            - Используй только факты из контекста
            - Если в вопросе есть обращение к тебе и похвала, то отвечай от души
            - Если в вопросе есть обращение к тебе и оскорбление, то отвечай "Иди нахуй, сам (Слово, которым тебя назвали)"

            Ответ:""")

        self.llm = OllamaLLM(model="qwen2")

    def get_relevant_documents(self, question: str, k: int = 3):
        try:
            retrieved_docs = self.vector_store.similarity_search(
                question,
                k=k
            )
            return retrieved_docs
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def format_context(self, documents):
        if not documents:
            return "Context not found"

        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.page_content.strip() if hasattr(doc, 'page_content') else str(doc)
            if hasattr(doc, 'metadata') and doc.metadata.get('start_index'):
                content += f" [Source: {doc.metadata['start_index']}]"
            context_parts.append(f"{i}. {content}")

        return "\n\n".join(context_parts)

    def ask_question(self, question: str):
        if not question.strip():
            return "Please, give me any question"

        if question == "IWTS":
            with sr.Microphone() as source:
                print("Speak...")
                audio = self.recognizer.listen(source)
            try:
                question = self.recognizer.recognize_vosk(audio, language="ru-RU")
            except sr.UnknownValueError:
                print("Speech recognition failed")

        print(f"Processing the request: {question}")

        retrieved_docs = self.get_relevant_documents(question)

        if not retrieved_docs:
            return "Sorry, we couldn't find relevant information in the knowledge base."

        docs_content = self.format_context(retrieved_docs)

        message = self.prompt.invoke({
            "question": question,
            "context": docs_content
        })

        try:
            answer = self.llm.invoke(message)
            return answer
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "Sorry"

def main():
    try:
        assistant = TransneftRAGAssistant()
        print("Transneft Assistant is ready to work!")
        print("Give me any question:")
    except Exception as e:
        print(f"Error initialization assistant")
        return

    while True:
        try:
            question = input("\nQuestion: ").strip()

            if not question:
                    continue

            answer = assistant.ask_question(question)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"Idk: {e}")

if __name__ == "__main__":
    main()

