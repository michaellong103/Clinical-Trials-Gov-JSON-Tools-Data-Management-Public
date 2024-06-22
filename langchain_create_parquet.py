# ******** Part of Process (not required) ******
import os
import sys
import pandas as pd
import openai
import config
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# Ensure the OpenAI API key is set
os.environ["OPENAI_API_KEY"] = config.APIKEY

def load_documents_from_parquet(directory):
    """Recursively load documents from parquet files in a directory."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.parquet'):
                file_path = os.path.join(root, file)
                print(f"Loading document: {file_path}")
                df = pd.read_parquet(file_path)
                for _, row in df.iterrows():
                    content = "\n".join([
                        row.get("BriefTitle", ""),
                        row.get("BriefSummary", ""),
                        row.get("EligibilityCriteria", ""),
                        " ".join(row.get("Conditions", [])),
                        " ".join(row.get("Keywords", [])),
                        " ".join(interv["Name"] for interv in row.get("Intervention", []))
                    ])
                    documents.append(content)
    return documents

# Check if query is provided
if len(sys.argv) < 2:
    print("Usage: python test_LangChain.py <query>")
    sys.exit(1)

query = sys.argv[1]

print("Loading documents from the 'data/apache_parquet' directory...")
documents = load_documents_from_parquet(os.path.join("data", "apache_parquet"))

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
