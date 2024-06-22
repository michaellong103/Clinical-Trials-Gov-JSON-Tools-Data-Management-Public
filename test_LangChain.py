# ******** Part of Tools ******
import os
import sys
import json
import openai
import config
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings

# Ensure the OpenAI API key is set
os.environ["OPENAI_API_KEY"] = config.APIKEY

def load_documents_from_directory(directory):
    """Recursively load documents from directory."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') or file.endswith('.jsonl'):
                file_path = os.path.join(root, file)
                print(f"Loading document: {file_path}")
                with open(file_path, 'r') as f:
                    try:
                        json_data = json.load(f)
                        for item in json_data:
                            content = "\n".join([
                                item.get("BriefTitle", ""),
                                item.get("BriefSummary", ""),
                                item.get("EligibilityCriteria", ""),
                                " ".join(cond for cond in item.get("Conditions", [])),
                                " ".join(key for key in item.get("Keywords", [])),
                                " ".join(interv.get("Name", "") for interv in item.get("Intervention", []))
                            ])
                            documents.append(content)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file: {file_path}")
                        print(e)
    return documents

# Check if query is provided
if len(sys.argv) < 2:
    print("Usage: python test_LangChain.py <query>")
    sys.exit(1)

query = sys.argv[1]

print("Loading documents from the 'data/cleaned' directory...")
documents = load_documents_from_directory(os.path.join("data", "cleaned"))

if not documents:
    print("No documents found.")
    sys.exit(1)

print(f"Number of documents loaded: {len(documents)}")

# Initialize OpenAI embeddings
embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002")

# Initialize Chroma vector store
chroma_vector_store = Chroma(collection_name="my_collection", embedding_function=embedding_function)

# Add documents to the vector store
print("Adding documents to the vector store...")
for doc in documents:
    try:
        print(f"Adding document: {doc[:100]}")  # Print first 100 characters for debugging
        chroma_vector_store.add_texts([doc])
    except Exception as e:
        print(f"Error adding document: {e}")

print("Documents added to the vector store.")

# Perform a search
print("Performing a similarity search...")
try:
    results = chroma_vector_store.similarity_search(query)
    if results:
        print(f"Found {len(results)} results:")
        for result in results:
            print(result)
    else:
        print("Found 0 results")
except Exception as e:
    print(f"Error during similarity search: {e}")

# Additional debugging for embeddings and queries
print("Debugging information:")
print(f"Query: {query}")
try:
    query_embedding = embedding_function.embed([query])
    print(f"Query Embedding: {query_embedding}")
except Exception as e:
    print(f"Error generating query embedding: {e}")

# Verify the size of vector store
try:
    vector_store_size = len(chroma_vector_store._index)
    print(f"Vector store size: {vector_store_size}")
except Exception as e:
    print(f"Error checking vector store size: {e}")
