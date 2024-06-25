import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIZED_CONDITIONS_DIR = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'categorized_conditions')
TXT_OUTPUT_DIR = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'txt')
MAX_SIZE_MB = 10
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

# Ensure the TXT directory exists
os.makedirs(TXT_OUTPUT_DIR, exist_ok=True)

def json_to_txt(directory, condition):
    """Convert JSON files in a directory to multiple TXT files, each smaller than 10MB."""
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
        file_count = len(merged_df)
        relative_path = os.path.relpath(directory, CATEGORIZED_CONDITIONS_DIR)
        output_subdir = os.path.join(TXT_OUTPUT_DIR, relative_path)
        os.makedirs(output_subdir, exist_ok=True)
        
        file_index = 1
        start_idx = 0
        while start_idx < len(merged_df):
            chunk_size = 1000  # Start with a reasonable chunk size
            end_idx = start_idx + chunk_size
            part_df = merged_df.iloc[start_idx:end_idx]
            txt_file_path = os.path.join(output_subdir, f"{condition}_part_{file_index}.txt")
            
            # Ensure the file is smaller than MAX_SIZE_MB
            while part_df.memory_usage(deep=True).sum() > MAX_SIZE_BYTES:
                chunk_size = max(1, chunk_size // 2)  # Reduce chunk size to half
                end_idx = start_idx + chunk_size
                part_df = merged_df.iloc[start_idx:end_idx]
            
            part_df.to_csv(txt_file_path, index=False, sep='\t')
            print(f"\033[32mConverted {directory} to {txt_file_path}\033[0m")
            
            start_idx = end_idx
            file_index += 1
    else:
        file_count = 0
        txt_file_path = None

    return txt_file_path, file_count

def check_trials_count():
    """Check the number of trials listed in each file in both JSON and TXT directories."""
    for subdir in next(os.walk(CATEGORIZED_CONDITIONS_DIR))[1]:
        json_dir = os.path.join(CATEGORIZED_CONDITIONS_DIR, subdir)
        txt_dir = os.path.join(TXT_OUTPUT_DIR, subdir)
        
        json_count = 0
        for root, _, files in os.walk(json_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        json_count += len(data) if isinstance(data, list) else 1

        txt_count = 0
        if os.path.exists(txt_dir):
            for root, _, files in os.walk(txt_dir):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        df = pd.read_csv(file_path, sep='\t')
                        txt_count += len(df)
                        print(f"{os.path.basename(file_path)}: {len(df)} trials")

        print(f"\033[94m{subdir}\033[0m: \033[96m{json_count} trials in JSON\033[0m | \033[96m{txt_count} trials in TXT\033[0m :: ({'same number' if json_count == txt_count else 'different numbers'})")

def process_all_directories():
    """Process all directories in the categorized conditions directory."""
    print("\033[33mStarting to condense files...\033[0m")
    for subdir in next(os.walk(CATEGORIZED_CONDITIONS_DIR))[1]:
        json_to_txt(os.path.join(CATEGORIZED_CONDITIONS_DIR, subdir), subdir)
    check_trials_count()
    print("\033[33mFinished condensing files.\033[0m")

if __name__ == "__main__":
    process_all_directories()
