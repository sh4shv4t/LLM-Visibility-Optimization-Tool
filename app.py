from flask import Flask, render_template, request, jsonify
import os

from scraper import scrape_to_markdown
from vector_store import index_markdown_file
from qa_app import answer_question

app = Flask(__name__, template_folder='templates')

# Define the path for our scraped content
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
        # Get the 'url' data from the incoming JSON request
        data = request.json
        url_to_scrape = data.get('url')

        if not url_to_scrape:
            # `jsonify` converts a Python dict into a JSON response
            return jsonify({"error": "No URL provided"}), 400

        # --- Step 1: Scrape ---
        print(f"Scraping: {url_to_scrape}")
        scrape_to_markdown(url_to_scrape, SCRAPED_FILE_PATH)

        # --- Step 2: Index ---
        print(f"Indexing: {SCRAPED_FILE_PATH}")
        index_markdown_file(SCRAPED_FILE_PATH, "vector_db")

        # Send a success message back to the frontend
        return jsonify({"message": f"Successfully scraped and indexed: {url_to_scrape}"})

    except Exception as e:
        print(f"Error during scrape/index: {e}")
        return jsonify({"error": str(e)}), 500

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