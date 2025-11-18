import sys
import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

# --- Configuration (Must match vector_store.py) ---
VECTOR_STORE_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Use the same local model as your qa_app.py
OLLAMA_MODEL = "llama3" 

# --- Standard Questions for Analysis ---
STANDARD_QUESTIONS = [
    "What is the main topic, purpose, or primary goal of this document?",
    "List the key takeaways, main products, or services mentioned.",
    "Who is the intended audience for this content?",
    "Is there any 'About Us' section or contact information? If so, what is it?",
    "Summarize the content's structure. Does it appear to have headers, lists, or distinct sections?",
    "What specific actions does the document suggest the reader take (e.g., 'buy now', 'learn more', 'contact us')?",
    "What does this document say about 'artificial intelligence'?" # This tests how it handles a topic that may or may not be present.
]

# --- New Prompt Template (Forcing JSON Output) ---
ANALYSIS_PROMPT_TEMPLATE = """
You are an analytical assistant. Based *only* on the context provided, answer the user's question.
Return your response as a single, valid JSON object with two keys: "answer" and "confidence".
- The "answer" key should contain your text answer.
- The "confidence" key should be a number from 0 (no information) to 100 (perfect information) representing how well the context answered the question.

If the context is irrelevant or provides no information to answer the question, set "answer" to "I could not find an answer in the provided document." and "confidence" to 0.

CONTEXT:
---
{context}
---

USER'S QUESTION:
{question}

JSON Response:
"""

def analyze_scrape_quality():
    """
    Loads the vector store and runs a standard analysis
    against the indexed content, returning a report dictionary.
    """
    print(f"Loading vector store from '{VECTOR_STORE_PATH}'...")
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        vector_store = Chroma(
            persist_directory=VECTOR_STORE_PATH,
            embedding_function=embedding_model
        )
        
        print(f"Loading local LLM: '{OLLAMA_MODEL}'...")
        local_llm = Ollama(
            model=OLLAMA_MODEL, 
            format="json"  # We explicitly tell Ollama to expect and generate JSON
        )

    except Exception as e:
        error_msg = f"Error initializing models or vector store: {e}. Please ensure your vector_db exists and Ollama is running."
        print(error_msg)
        # Return an error dictionary
        return {"error": error_msg}

    total_retrieval_confidence = 0
    total_llm_confidence = 0
    question_results = []

    print(f"--- Running Website Analysis ({len(STANDARD_QUESTIONS)} Questions) ---")

    for i, question in enumerate(STANDARD_QUESTIONS):
        print(f"Analyzing question {i+1}/{len(STANDARD_QUESTIONS)}...")
        
        avg_retrieval_confidence = 0
        llm_answer = "An unknown error occurred."
        llm_confidence = 0

        try:
            # --- 1. Retrieval Step (with scores) ---
            retrieved_docs_with_scores = vector_store.similarity_search_with_score(question, k=4)
            
            if not retrieved_docs_with_scores:
                print("No relevant documents found for this question.")
                llm_answer = "N/A - No documents found"
                llm_confidence = 0
                avg_retrieval_confidence = 0
                
            else:
                # --- 2. Calculate Retrieval Confidence ---
                total_score = 0
                context_for_llm = []
                for doc, score in retrieved_docs_with_scores:
                    total_score += max(0, 1.0 - score) # 1.0 is a typical max distance
                    context_for_llm.append(doc.page_content)
                
                avg_retrieval_confidence = (total_score / len(retrieved_docs_with_scores)) * 100
                
                prompt_context = "\n\n".join(context_for_llm)
                grounded_prompt = ANALYSIS_PROMPT_TEMPLATE.format(
                    context=prompt_context,
                    question=question
                )

                # --- 3. Generation Step (with JSON) ---
                llm_response_raw = local_llm.invoke(grounded_prompt)
                
                # --- 4. Parse LLM Response ---
                llm_response_json = json.loads(llm_response_raw)
                llm_answer = llm_response_json.get("answer", "Error parsing response.")
                llm_confidence = float(llm_response_json.get("confidence", 0))

        except json.JSONDecodeError as json_err:
            print(f"Error: LLM did not return valid JSON. {json_err}")
            llm_answer = f"Error: LLM returned invalid JSON. Raw: {llm_response_raw}"
            llm_confidence = 0
        except Exception as e:
            print(f"An error occurred during analysis: {e}")
            llm_answer = f"An error occurred: {e}"
            llm_confidence = 0

        # Add to totals
        total_retrieval_confidence += avg_retrieval_confidence
        total_llm_confidence += llm_confidence

        # Store results for this question
        question_results.append({
            "question": question,
            "retrieval_confidence": avg_retrieval_confidence,
            "llm_answer": llm_answer,
            "llm_confidence": llm_confidence
        })

    # --- 5. Final Report (as a dictionary) ---
    print("--- Analysis Complete ---")
    
    final_retrieval_score = 0
    final_llm_score = 0
    if STANDARD_QUESTIONS: # Avoid division by zero
        final_retrieval_score = total_retrieval_confidence / len(STANDARD_QUESTIONS)
        final_llm_score = (total_llm_confidence / len(STANDARD_QUESTIONS))
    
    # This is the dictionary that will be returned to app.py
    report_data = {
        "overall_scores": {
            "avg_retrieval_confidence": final_retrieval_score,
            "avg_llm_confidence": final_llm_score
        },
        "individual_scores": question_results
    }
    
    return report_data


if __name__ == "__main__":
    print("Running standalone analysis...")
    report = analyze_scrape_quality()
    print("\n--- JSON Report Output ---")
    print(json.dumps(report, indent=2))