import os
import json
import pandas as pd
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIZED_CONDITIONS_DIR = os.path.join(BASE_DIR, 'data_batch', 'categorized_conditions')
TXT_DIR = os.path.join(BASE_DIR, 'data_batch', 'txt')

def count_json_trials(directory):
    trial_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    trial_count += len(data) if isinstance(data, list) else 1
    return trial_count

def count_txt_trials(file_path):
    if not os.path.exists(file_path):
        print(f"\033[33mTXT file not found: {file_path}\033[0m")
        return 0
    df = pd.read_csv(file_path, sep='\\t')
    return len(df)

def main():
    subdirs = [d for d in os.listdir(CATEGORIZED_CONDITIONS_DIR) if os.path.isdir(os.path.join(CATEGORIZED_CONDITIONS_DIR, d))]
    random_subdirs = random.sample(subdirs, 4)
    
    for subdir in random_subdirs:
        json_count = count_json_trials(os.path.join(CATEGORIZED_CONDITIONS_DIR, subdir))
        txt_file = os.path.join(TXT_DIR, f"{subdir}_part_1.txt")
        txt_count = count_txt_trials(txt_file)
        
        color = "\033[32m" if json_count == txt_count else "\033[31m"
        reset = "\033[0m"
        
        print(f"{subdir}: {json_count} trials in JSON | {txt_count} trials in TXT | {color}({'same number' if json_count == txt_count else 'different numbers'}){reset}")

if __name__ == "__main__":
    main()
