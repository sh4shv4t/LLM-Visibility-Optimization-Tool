import sys
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_VECTOR_STORE_PATH = "vector_db"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def index_markdown_file(markdown_file_path, vector_store_directory):
    """
    Loads a Markdown file, splits it into chunks, creates vector
    embeddings, and stores them in a local Chroma vector database.

    Args:
        markdown_file_path (str): The path to the .md file to ingest.
        vector_store_directory (str): The folder to save the vector store in.
    """
    print(f"Starting to index '{markdown_file_path}'...")

    loader = UnstructuredMarkdownLoader(markdown_file_path)
    loaded_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    document_chunks = text_splitter.split_documents(loaded_documents)

    print(f"Loaded {len(loaded_documents)} document(s) and split into {len(document_chunks)} chunks.")

    print(f"Loading embedding model '{DEFAULT_EMBEDDING_MODEL}'...")
    embedding_model = HuggingFaceEmbeddings(
        model_name=DEFAULT_EMBEDDING_MODEL
    )
    print(f"Creating and persisting vector store at '{vector_store_directory}'...")
    vector_store = Chroma.from_documents(
        documents=document_chunks,
        embedding=embedding_model,
        persist_directory=vector_store_directory
    )
    vector_store.persist()

    print(f"Successfully indexed '{markdown_file_path}' into vector store.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_to_index = sys.argv[1]
        index_markdown_file(
            markdown_file_path=file_to_index, 
            vector_store_directory=DEFAULT_VECTOR_STORE_PATH
        )
    else:
        print("Please provide the path to a Markdown file to index.")
        print("Example: python vector_store.py scraped_content.md")
