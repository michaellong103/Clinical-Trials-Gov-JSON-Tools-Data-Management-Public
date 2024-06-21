import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cleaned_data_dir = os.path.join(BASE_DIR, 'data', 'cleaned')
parquet_output_dir = os.path.join(BASE_DIR, 'data', 'apache_parquet')

# Ensure the apache_parquet directory exists
os.makedirs(parquet_output_dir, exist_ok=True)

def json_files_to_parquet(directory):
    """Convert all JSON files in a directory to a single Parquet file."""
    data_frames = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') or file.endswith('.jsonl'):
                json_file_path = os.path.join(root, file)
                with open(json_file_path, 'r') as f:
                    data = json.load(f)
                    df = pd.json_normalize(data)
                    data_frames.append(df)
    
    if data_frames:
        merged_df = pd.concat(data_frames, ignore_index=True)
        relative_path = os.path.relpath(directory, cleaned_data_dir)
        parquet_file_path = os.path.join(parquet_output_dir, f"{relative_path.replace('/', '_')}.parquet")
        merged_df.to_parquet(parquet_file_path, index=False)
        print(f"Converted {directory} to {parquet_file_path}")
    else:
        print(f"No JSON files found in {directory}")

def process_all_directories():
    """Process each subdirectory in the cleaned data directory."""
    for subdir in next(os.walk(cleaned_data_dir))[1]:
        directory = os.path.join(cleaned_data_dir, subdir)
        json_files_to_parquet(directory)

# Run the processing function
if __name__ == "__main__":
    print("Starting to convert JSON files to Parquet format...")
    process_all_directories()
    print("Finished converting JSON files to Parquet format.")
