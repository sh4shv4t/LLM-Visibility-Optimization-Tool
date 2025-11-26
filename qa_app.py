import sys
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

VECTOR_STORE_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

PROMPT_TEMPLATE = """
You are a helpful assistant. You must answer the user's question based *only* on the context provided below.

If the answer is not in the context, just say "I could not find an answer in the provided document."

CONTEXT:
---
{context}
---

USER'S QUESTION:
{question}

ANSWER:
"""

def answer_question(user_question):
    """
    Retrieves context from the vector store and generates an
    answer using a local Ollama model.
    
    Args:
        user_question (str): The question asked by the user.
    """
    
    print(f"Loading existing vector store from '{VECTOR_STORE_PATH}'...")
    
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embedding_model
    )

    print(f"Searching for relevant documents for: '{user_question}'")

    retrieved_documents = vector_store.similarity_search(user_question, k=4)

    if not retrieved_documents:
        print("No relevant documents found in the vector store.")
        return

    prompt_context = "\n\n".join(
        doc.page_content for doc in retrieved_documents
    )

    grounded_prompt = PROMPT_TEMPLATE.format(
        context=prompt_context, 
        question=user_question
    )

    print("\n--- Sending to Local LLM (Ollama) ---")
    
    local_llm = Ollama(model="gpt-oss:20b")
    
    llm_answer_text = local_llm.invoke(grounded_prompt)

    print("\n--- Answer ---")
    print(llm_answer_text)
    print("--------------\n")

    return llm_answer_text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        answer_question(question)
    else:
        print("Please provide a question.")
        print("Example: python qa_app.py \"What is this document about?\"")