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

MAX_FILE_SIZE = 10 * 1024 * 1024  # 20 MB in bytes

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

# Function to write embeddings to file ensuring no file exceeds the maximum size
def write_embeddings_to_file(directory_name, filename_suffix, embeddings):
    file_count = 1
    current_embeddings = []
    current_size = 0

    for embedding in embeddings:
        embedding_size = len(json.dumps(embedding).encode('utf-8'))
        
        if current_size + embedding_size > MAX_FILE_SIZE:
            output_file_path = os.path.join(embeddings_output_dir, f'{directory_name}_embeddings_{filename_suffix}_{file_count}.json')
            with open(output_file_path, 'w') as outfile:
                json.dump(current_embeddings, outfile, indent=4)
            print(f"Saved embeddings to: {output_file_path}")
            print(f"File size: {os.path.getsize(output_file_path)} bytes")

            if os.path.getsize(output_file_path) > MAX_FILE_SIZE:
                print(f"Error: File size {os.path.getsize(output_file_path)} exceeds 20 MB for {output_file_path}")

            file_count += 1
            current_embeddings = []
            current_size = 0
        
        current_embeddings.append(embedding)
        current_size += embedding_size

    if current_embeddings:
        output_file_path = os.path.join(embeddings_output_dir, f'{directory_name}_embeddings_{filename_suffix}_{file_count}.json')
        with open(output_file_path, 'w') as outfile:
            json.dump(current_embeddings, outfile, indent=4)
        print(f"Saved embeddings to: {output_file_path}")
        print(f"File size: {os.path.getsize(output_file_path)} bytes")

        if os.path.getsize(output_file_path) > MAX_FILE_SIZE:
            print(f"Error: File size {os.path.getsize(output_file_path)} exceeds 20 MB for {output_file_path}")

# Function to process all files in the processed data directory
def process_all_files(limit_files):
    for subdir, _, files in os.walk(processed_data_dir):
        all_embeddings = []
        directory_name = os.path.basename(subdir)
        
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

        # Write embeddings to file, ensuring no file exceeds the maximum size
        filename_suffix = "first10" if limit_files else "all"
        write_embeddings_to_file(directory_name, filename_suffix, all_embeddings)

# Run the processing function
if __name__ == "__main__":
    print("Do you want to process the first 10 files or all files?")
    choice = input("Enter '10' for first 10 files or 'all' for all files: ").strip().lower()
    
    limit_files = (choice == '10')
    
    print("Starting to process all files...")
    process_all_files(limit_files)
    print("Finished processing all files.")
