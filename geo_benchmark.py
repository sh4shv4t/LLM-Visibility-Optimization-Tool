"""
GEO Benchmark Analyzer

This module provides comprehensive benchmarking for Generative Engine Optimization (GEO).
It evaluates how well a website is optimized for LLM visibility using multiple dimensions
and generates detailed reports with actionable recommendations.
"""

import sys
import json
import requests
from typing import Dict, List, Tuple, Any, Callable, Optional
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

from benchmark_config import (
    GEO_DIMENSIONS,
    BENCHMARK_QUESTIONS,
    SCORING_THRESHOLDS,
    CONFIDENCE_INTERPRETATION,
    get_all_questions,
    get_weighted_questions,
    get_score_rating,
    get_recommendations_for_scores,
    QUALITY_METRICS
)

# --- Configuration ---
VECTOR_STORE_PATH = "vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "gpt-oss:20b"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# --- Improved Prompt Template with Examples ---
ANALYSIS_PROMPT_TEMPLATE = """You are an analytical assistant. Based ONLY on the context below, answer the question.

IMPORTANT: Respond with ONLY a JSON object. No other text before or after.

Format:
{{"answer": "your answer here", "confidence": 7}}

Confidence scale:
- 0: No relevant info
- 3-4: Minimal relevant info
- 5-7: Partial answer
- 8-10: Complete answer with evidence

CONTEXT:
{context}

QUESTION: {question}

JSON:"""


class GEOBenchmarkAnalyzer:
    """Comprehensive GEO benchmark analyzer with progress tracking."""
    
    def __init__(self):
        """Initialize the analyzer (models loaded lazily)."""
        self.vector_store = None
        self.llm = None
        self.embedding_model = None
        
    def initialize(self):
        """Load models and vector store."""
        print(f"Loading vector store from '{VECTOR_STORE_PATH}'...")
        
        try:
            self.embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            self.vector_store = Chroma(
                persist_directory=VECTOR_STORE_PATH,
                embedding_function=self.embedding_model
            )
            
            print(f"Loading local LLM: '{OLLAMA_MODEL}'...")
            self.llm = OllamaLLM(
                model=OLLAMA_MODEL,
                temperature=0.1
            )
            
            return True
            
        except Exception as e:
            error_msg = f"Error initializing: {e}"
            print(error_msg)
            return False
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Try to extract JSON from various text formats.
        Handles markdown code blocks, extra text, etc.
        """
        # Remove markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        text = text.strip()
        
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in text
        import re
        json_pattern = r'\{[^{}]*"answer"[^{}]*"confidence"[^{}]*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        # Try to extract just the values
        answer_match = re.search(r'"answer"\s*:\s*"([^"]*)"', text)
        conf_match = re.search(r'"confidence"\s*:\s*(\d+(?:\.\d+)?)', text)
        
        if answer_match and conf_match:
            return {
                "answer": answer_match.group(1),
                "confidence": float(conf_match.group(1))
            }
        
        return None
    
    def _call_ollama_direct(self, prompt: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        Call Ollama API directly for more reliable JSON responses.
        
        Args:
            prompt: The prompt to send
            max_retries: Number of retry attempts
            
        Returns:
            Dict with 'answer' and 'confidence' keys, or error response
        """
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    OLLAMA_API_URL,
                    json={
                        "model": OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                            "num_predict": 300  # Limit response length
                        }
                    },
                    timeout=90
                )
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get("response", "").strip()
                    
                    if not response_text:
                        if attempt < max_retries:
                            print(f"  Empty response, retrying... (attempt {attempt + 1})")
                            continue
                        return {"answer": "Error: Empty response from LLM", "confidence": 0}
                    
                    # Try to extract JSON with improved parsing
                    parsed = self._extract_json_from_text(response_text)
                    
                    if parsed and "answer" in parsed and "confidence" in parsed:
                        try:
                            return {
                                "answer": str(parsed["answer"]),
                                "confidence": float(parsed["confidence"])
                            }
                        except (ValueError, TypeError):
                            pass
                    
                    # If we still can't parse after retries, use the raw text
                    if attempt >= max_retries:
                        print(f"  Using raw response (could not parse JSON)")
                        return {"answer": response_text[:200], "confidence": 3}
                    
                    print(f"  JSON parse failed, retrying... (attempt {attempt + 1})")
                    continue
                    
                else:
                    if attempt < max_retries:
                        print(f"  HTTP {response.status_code}, retrying... (attempt {attempt + 1})")
                        continue
                    return {"answer": f"Error: HTTP {response.status_code}", "confidence": 0}
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    print(f"  Timeout, retrying... (attempt {attempt + 1})")
                    continue
                return {"answer": "Error: Request timeout", "confidence": 0}
                
            except Exception as e:
                if attempt < max_retries:
                    print(f"  Error: {e}, retrying... (attempt {attempt + 1})")
                    continue
                return {"answer": f"Error: {str(e)}", "confidence": 0}
        
        return {"answer": "Error: Max retries exceeded", "confidence": 0}
    
    def _query_with_context(self, question: str) -> Tuple[str, float, float]:
        """
        Query the vector store and LLM for a given question.
        
        Returns:
            Tuple of (answer, llm_confidence, retrieval_confidence)
        """
        try:
            # Retrieve relevant documents
            retrieved_docs_with_scores = self.vector_store.similarity_search_with_score(question, k=4)
            
            if not retrieved_docs_with_scores:
                return "No relevant documents found.", 0, 0
            
            # Calculate retrieval confidence
            total_score = sum(max(0, 1.0 - score) for _, score in retrieved_docs_with_scores)
            retrieval_confidence = (total_score / len(retrieved_docs_with_scores)) * 10
            
            # Prepare context for LLM
            context_parts = [doc.page_content for doc, _ in retrieved_docs_with_scores]
            context = "\n\n".join(context_parts)
            
            # Generate prompt
            prompt = ANALYSIS_PROMPT_TEMPLATE.format(context=context, question=question)
            
            # Call LLM using direct API
            result = self._call_ollama_direct(prompt)
            
            return result["answer"], result["confidence"], retrieval_confidence
            
        except Exception as e:
            print(f"  Error during query: {e}")
            return f"Error: {str(e)}", 0, 0
    
    def analyze(self, progress_callback: Optional[Callable[[str, dict], None]] = None) -> Dict[str, Any]:
        """
        Run comprehensive GEO benchmark analysis with progress tracking.
        
        Args:
            progress_callback: Optional function to call with progress updates.
                              Should accept (message: str, data: dict)
        
        Returns:
            Detailed analysis report as a dictionary
        """
        if not self.vector_store or not self.llm:
            return {"error": "Analyzer not initialized. Call initialize() first."}
        
        def send_progress(message: str, data: dict = None):
            """Helper to send progress updates."""
            print(message)  # Still print to console
            if progress_callback:
                progress_callback(message, data or {})
        
        send_progress(f"\n{'='*70}")
        send_progress("Starting GEO Benchmark Analysis", {"type": "start"})
        send_progress(f"{'='*70}\n")
        
        all_results = []
        category_scores = {}
        dimension_scores = {}
        total_questions = 0
        answered_questions = 0
        
        # Process each category
        for category_name, category_data in BENCHMARK_QUESTIONS.items():
            send_progress(f"\n--- Category: {category_name} ---", {
                "type": "category_start",
                "category": category_name
            })
            
            dimension = category_data["dimension"]
            weight = GEO_DIMENSIONS[dimension]["weight"]
            questions = category_data["questions"]
            
            send_progress(f"Dimension: {dimension} | Weight: {weight}")
            
            category_results = []
            category_total_confidence = 0
            
            for i, question in enumerate(questions, 1):
                total_questions += 1
                send_progress(f"  [{i}/{len(questions)}] Analyzing...", {
                    "type": "question_progress",
                    "category": category_name,
                    "current": i,
                    "total": len(questions)
                })
                
                answer, llm_conf, retrieval_conf = self._query_with_context(question)
                
                if llm_conf > 0:
                    answered_questions += 1
                
                category_total_confidence += llm_conf
                
                category_results.append({
                    "question": question,
                    "answer": answer,
                    "llm_confidence": llm_conf,
                    "retrieval_confidence": retrieval_conf
                })
            
            # Calculate category score
            avg_confidence = category_total_confidence / len(questions) if questions else 0
            weighted_score = (avg_confidence / 10) * weight * 100
            
            category_scores[category_name] = {
                "dimension": dimension,
                "weight": weight,
                "avg_confidence": avg_confidence,
                "weighted_score": weighted_score,
                "results": category_results
            }
            
            # Aggregate by dimension
            if dimension not in dimension_scores:
                dimension_scores[dimension] = []
            dimension_scores[dimension].append(weighted_score)
            
            all_results.extend(category_results)
        
        # Calculate overall metrics
        overall_score = sum(cat["weighted_score"] for cat in category_scores.values())
        answer_rate = (answered_questions / total_questions * 100) if total_questions > 0 else 0
        
        # Average dimension scores
        dimension_averages = {
            dim: sum(scores) / len(scores) if scores else 0
            for dim, scores in dimension_scores.items()
        }
        
        # Get rating info
        rating_name, rating_info = get_score_rating(overall_score)
        
        send_progress(f"\n{'='*70}")
        send_progress("Analysis Complete!", {"type": "complete"})
        send_progress(f"{'='*70}")
        send_progress(f"Overall GEO Score: {overall_score:.1f}/100 ({rating_name.upper()})")
        send_progress(f"Answer Rate: {answer_rate:.1f}%")
        if rating_info:
            send_progress(f"Rating: {rating_info.get('description', '')}")
        send_progress(f"{'='*70}\n")
        
        # Build final report
        rating_name, rating_info = get_score_rating(overall_score)
        
        report = {
            "overall_geo_score": round(overall_score, 2),
            "rating": rating_name.upper(),
            "rating_description": rating_info.get('description', '') if rating_info else '',
            "statistics": {
                "answer_rate": answer_rate / 100,  # Convert to decimal for frontend
                "answered_questions": answered_questions,
                "total_questions": total_questions,
                "avg_llm_confidence": sum(r["llm_confidence"] for r in all_results) / len(all_results) if all_results else 0
            },
            "dimension_scores": {k: round(v, 2) for k, v in dimension_averages.items()},
            "category_scores": category_scores,
            "recommendations": get_recommendations_for_scores(dimension_averages),
            "all_results": all_results
        }
        
        return report


def analyze_scrape_quality(progress_callback: Optional[Callable[[str, dict], None]] = None) -> Dict[str, Any]:
    """
    Main entry point for GEO benchmark analysis.
    
    Args:
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Comprehensive analysis report
    """
    analyzer = GEOBenchmarkAnalyzer()
    
    if not analyzer.initialize():
        return {"error": "Failed to initialize analyzer"}
    
    return analyzer.analyze(progress_callback)


if __name__ == "__main__":
    print("Running standalone GEO benchmark analysis...")
    report = analyze_scrape_quality()
    
    if "error" in report:
        print(f"\nError: {report['error']}")
        sys.exit(1)
    
    print("\n--- JSON Report Output ---")
    print(json.dumps(report, indent=2))
