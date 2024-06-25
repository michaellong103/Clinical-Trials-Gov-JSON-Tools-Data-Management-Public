# ******** Part of Process ******
import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cleaned_data_dir = os.path.join(BASE_DIR, 'data', 'cleaned')
txt_output_dir = os.path.join(BASE_DIR, 'data', 'txt')

# Ensure the TXT directory exists
os.makedirs(txt_output_dir, exist_ok=True)

def json_to_txt(directory):
    """Convert JSON files in a directory to a single TXT file using CSV formatting."""
    data_frames = []
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                json_files.append(file_path)
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
        # Ensure the corresponding directory structure exists in the TXT output directory
        output_subdir = os.path.join(txt_output_dir, os.path.dirname(relative_path))
        os.makedirs(output_subdir, exist_ok=True)
        txt_file_path = os.path.join(output_subdir, f"{os.path.basename(relative_path)}_txt.txt")
        merged_df.to_csv(txt_file_path, index=False, sep='\t')
        print(f"Converted {directory} to {txt_file_path}")
        return txt_file_path, json_files, len(merged_df)
    return None, json_files, 0

def check_trials_count():
    """Check the number of trials listed in each file in both JSON and TXT directories."""
    for subdir in next(os.walk(cleaned_data_dir))[1]:
        json_dir = os.path.join(cleaned_data_dir, subdir)
        txt_file_path = os.path.join(txt_output_dir, f"{subdir}_txt.txt")

        # Count trials in JSON files
        json_count = 0
        for root, _, files in os.walk(json_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        json_count += len(data) if isinstance(data, list) else 1

        # Count trials in TXT files
        if os.path.exists(txt_file_path):
            df = pd.read_csv(txt_file_path, sep='\t')
            txt_count = len(df)
            print(f"{os.path.basename(txt_file_path)}: {txt_count} trials | {subdir} Trials in [dir] : {json_count} :: ({'same number' if json_count == txt_count else 'different numbers'})")
        else:
            print(f"No TXT file found for {subdir}")

def process_all_directories():
    """Process all directories in the cleaned data directory."""
    for subdir in next(os.walk(cleaned_data_dir))[1]:
        json_to_txt(os.path.join(cleaned_data_dir, subdir))
    check_trials_count()

if __name__ == "__main__":
    process_all_directories()
