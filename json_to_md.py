# ******** Part of Process (required) ******
import os
import sys
import json
import pandas as pd

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def json_to_markdown_append(json_data, output_file):
    """Append JSON data to a markdown file."""
    df = pd.json_normalize(json_data)
    with open(output_file, 'a') as f:
        f.write(df.to_markdown(index=False))
        f.write('\n\n')  # Add spacing between tables

def load_json_files_from_directory(directory):
    """Recursively load JSON files from directory."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') or file.endswith('.jsonl'):
                file_path = os.path.join(root, file)
                print(f"Loading file: {file_path}")
                with open(file_path, 'r') as f:
                    try:
                        json_data = json.load(f)
                        relative_path = os.path.relpath(root, directory)
                        documents.append((json_data, file, relative_path))
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file: {file_path}")
                        print(e)
    return documents

def main():
    # Directory containing JSON files
    input_directory = os.path.join("data", "cleaned")
    output_directory = os.path.join("data", "md")

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    print("Loading JSON files from the input directory...")
    json_files = load_json_files_from_directory(input_directory)

    if not json_files:
        print("No JSON files found.")
        sys.exit(1)

    print(f"Number of JSON files loaded: {len(json_files)}")

    for _, _, relative_path in json_files:
        # Ensure the output directory structure matches the input directory structure
        output_dir = os.path.join(output_directory, relative_path)
        os.makedirs(output_dir, exist_ok=True)

    # Combine JSON files into large Markdown files
    current_file_index = 0
    current_file_size = 0
    current_output_file = None

    for json_data, filename, relative_path in json_files:
        if current_output_file is None:
            output_dir = os.path.join(output_directory, relative_path)
            os.makedirs(output_dir, exist_ok=True)
            current_output_file = os.path.join(output_dir, f"combined_{current_file_index}.md")
        
        temp_file = os.path.join(output_dir, "temp.md")
        json_to_markdown_append(json_data, temp_file)

        temp_file_size = os.path.getsize(temp_file)

        if current_file_size + temp_file_size > MAX_FILE_SIZE_BYTES:
            current_file_index += 1
            current_output_file = os.path.join(output_dir, f"combined_{current_file_index}.md")
            current_file_size = 0

        with open(temp_file, 'r') as src, open(current_output_file, 'a') as dest:
            dest.write(src.read())

        current_file_size += temp_file_size
        os.remove(temp_file)
        print(f"Added {filename} to {current_output_file}")

if __name__ == "__main__":
    main()
