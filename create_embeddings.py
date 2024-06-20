import os
import json
import openai

# Set your OpenAI API key here
openai.api_key = '' 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
processed_data_dir = os.path.join(BASE_DIR, 'data', 'processed')
embeddings_output_dir = os.path.join(BASE_DIR, 'data', 'embeddings')

# Ensure the embeddings directory exists
os.makedirs(embeddings_output_dir, exist_ok=True)

# Function to read and parse JSON data from a file
def read_json(file_path):
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file: {file_path}")
            print(e)
            return None

# Function to generate embeddings
def generate_embedding(text):
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f"Error generating embedding for text: {text}")
        print(e)
        return None

# Function to recursively search for BriefTitle in nested dictionaries
def find_brief_title(data):
    if isinstance(data, dict):
        if 'BriefTitle' in data:
            return data['BriefTitle']
        for key, value in data.items():
            result = find_brief_title(value)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_brief_title(item)
            if result:
                return result
    return None

# Function to process all files in the processed data directory
def process_all_files(limit_files):
    for subdir, _, files in os.walk(processed_data_dir):
        all_embeddings = []
        directory_name = os.path.basename(subdir)
        
        # Modify output filename based on the limit_files flag
        filename_suffix = "first10" if limit_files else "all"
        embeddings_output_file = os.path.join(embeddings_output_dir, f'{directory_name}_embeddings_{filename_suffix}.json')
        
        files_to_process = files[:10] if limit_files else files
        
        for file in files_to_process:
            file_path = os.path.join(subdir, file)
            if file.endswith('.json'):  # Ensure the file is a JSON file
                print(f"Processing file: {file_path}")
                raw_json = read_json(file_path)
                if raw_json is None:
                    continue

                brief_title = find_brief_title(raw_json)
                if brief_title:
                    print(f"Found BriefTitle: {brief_title}")
                    
                    embedding = generate_embedding(brief_title)
                    if embedding:
                        all_embeddings.append({
                            "file": file_path,
                            "BriefTitle": brief_title,
                            "embedding": embedding
                        })
                else:
                    print(f"No BriefTitle found in file: {file_path}")

        if all_embeddings:
            with open(embeddings_output_file, 'w') as outfile:
                json.dump(all_embeddings, outfile, indent=4)
            print(f"Saved all embeddings to: {embeddings_output_file}")
        else:
            print(f"No embeddings were generated for directory: {directory_name}")

# Run the processing function
if __name__ == "__main__":
    print("Do you want to process the first 10 files or all files?")
    choice = input("Enter '10' for first 10 files or 'all' for all files: ").strip().lower()
    
    limit_files = (choice == '10')
    
    print("Starting to process all files...")
    process_all_files(limit_files)
    print("Finished processing all files.")
