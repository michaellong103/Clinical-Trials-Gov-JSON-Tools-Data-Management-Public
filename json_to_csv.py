# ******** Part of Process ******
import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cleaned_data_dir = os.path.join(BASE_DIR, 'data', 'cleaned')
csv_output_dir = os.path.join(BASE_DIR, 'data', 'csv')

# Ensure the CSV directory exists
os.makedirs(csv_output_dir, exist_ok=True)

def json_to_csv(directory):
    """Convert JSON files in a directory to a single CSV file."""
    data_frames = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        df = pd.json_normalize(data)
                    else:
                        df = pd.json_normalize([data])
                    data_frames.append(df)

    if data_frames:
        merged_df = pd.concat(data_frames, ignore_index=True)
        relative_path = os.path.relpath(directory, cleaned_data_dir)
        # Ensure the corresponding directory structure exists in the CSV output directory
        output_subdir = os.path.join(csv_output_dir, os.path.dirname(relative_path))
        os.makedirs(output_subdir, exist_ok=True)
        csv_file_path = os.path.join(output_subdir, f"{os.path.basename(relative_path)}_cleaned.csv")
        merged_df.to_csv(csv_file_path, index=False)
        print(f"Converted {directory} to {csv_file_path}")

def process_all_directories():
    """Process all directories in the cleaned data directory."""
    for subdir in next(os.walk(cleaned_data_dir))[1]:
        json_to_csv(os.path.join(cleaned_data_dir, subdir))

if __name__ == "__main__":
    process_all_directories()
