from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os
import json
import queue
import threading

from scraper import scrape_to_markdown
from vector_store import index_markdown_file
from qa_app import answer_question
# Import the new comprehensive GEO benchmark analyzer
from geo_benchmark import analyze_scrape_quality

app = Flask(__name__, template_folder='templates')

# Global queue for SSE messages
analysis_queue = queue.Queue()

SCRAPED_FILE_PATH = "scraped_content.md"

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_and_index():
    """
    Scrapes a URL, saves it to a file, and then indexes that
    file into the vector store.
    """
    try:
        data = request.json
        url_to_scrape = data.get('url')

        if not url_to_scrape:
            return jsonify({"error": "No URL provided"}), 400

        print(f"Scraping: {url_to_scrape}")
        scrape_to_markdown(url_to_scrape, SCRAPED_FILE_PATH)

        print(f"Indexing: {SCRAPED_FILE_PATH}")
        index_markdown_file(SCRAPED_FILE_PATH, "vector_db")

        return jsonify({"message": f"Successfully scraped and indexed: {url_to_scrape}"})

    except Exception as e:
        print(f"Error during scrape/index: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def run_analysis():
    """
    Starts the analysis in a background thread and returns immediately.
    Client should connect to /analyze/stream for progress updates.
    """
    try:
        # Clear the queue
        while not analysis_queue.empty():
            try:
                analysis_queue.get_nowait()
            except queue.Empty:
                break
        
        # Start analysis in background thread
        def run_analysis_thread():
            def progress_callback(message, data):
                # Send progress update to queue
                analysis_queue.put({
                    "message": message,
                    "data": data
                })
            
            try:
                print("Running analysis...")
                report_data = analyze_scrape_quality(progress_callback=progress_callback)
                
                if "error" in report_data:
                    analysis_queue.put({
                        "message": "ERROR",
                        "data": {"error": report_data["error"]}
                    })
                else:
                    analysis_queue.put({
                        "message": "COMPLETE",
                        "data": {"report": report_data}
                    })
            except Exception as e:
                print(f"Error during analysis: {e}")
                analysis_queue.put({
                    "message": "ERROR",
                    "data": {"error": str(e)}
                })
        
        thread = threading.Thread(target=run_analysis_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({"message": "Analysis started. Connect to /analyze/stream for progress updates."})

    except Exception as e:
        print(f"Error starting analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/stream')
def analyze_stream():
    """
    Server-Sent Events endpoint for streaming analysis progress.
    """
    def generate():
        try:
            while True:
                # Wait for message from queue
                msg = analysis_queue.get(timeout=300)  # 5 minute timeout
                
                # Format as SSE
                yield f"data: {json.dumps(msg)}\n\n"
                
                # Stop if analysis is complete or errored
                if msg["message"] in ["COMPLETE", "ERROR"]:
                    break
                    
        except queue.Empty:
            yield f"data: {json.dumps({'message': 'TIMEOUT', 'data': {}})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'message': 'ERROR', 'data': {'error': str(e)}})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/ask', methods=['POST'])
def ask():
    """
    Takes a user's question, passes it to the RAG core,
    and returns the model's answer.
    """
    try:
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        print(f"Answering question: {question}")
        answer_text = answer_question(question)

        # Send the answer back to the frontend
        return jsonify({"answer": answer_text})

    except Exception as e:
        print(f"Error during ask: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)