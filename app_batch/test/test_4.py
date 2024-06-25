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
        return 0
    df = pd.read_csv(file_path, sep='\t')
    return len(df)

def find_txt_files(directory):
    txt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

def print_colored(subdir, json_count, txt_count, txt_file_path=None):
    key_color = "\033[95m"  # Light magenta
    value_color = "\033[96m"  # Light cyan
    reset = "\033[0m"
    result_color = "\033[92m" if json_count == txt_count else "\033[91m"
    result_text = "same number" if json_count == txt_count else "different numbers"
    
    print(f"{key_color}{subdir}{reset}: {value_color}{json_count} trials in JSON{reset} | {value_color}{txt_count} trials in TXT{reset} | {result_color}({result_text}){reset}")
    
    if txt_file_path:
        relative_path = os.path.relpath(txt_file_path, BASE_DIR)
        print(f"\033[94mPath to TXT file:\033[0m \033[96m{relative_path}\033[0m")

def main():
    if not os.path.exists(CATEGORIZED_CONDITIONS_DIR):
        print(f"\033[91mError: Directory {CATEGORIZED_CONDITIONS_DIR} does not exist.\033[0m")
        return

    subdirs = next(os.walk(CATEGORIZED_CONDITIONS_DIR))[1]
    if not subdirs:
        print(f"\033[91mError: No subdirectories found in {CATEGORIZED_CONDITIONS_DIR}.\033[0m")
        return

    discrepancies = []
    results = []

    for subdir in subdirs:
        json_count = count_json_trials(os.path.join(CATEGORIZED_CONDITIONS_DIR, subdir))
        txt_files = find_txt_files(TXT_DIR)
        txt_count = 0
        txt_file_path = None
        
        for txt_file in txt_files:
            if os.path.basename(txt_file).startswith(subdir):
                txt_file_path = txt_file
                txt_count = count_txt_trials(txt_file_path)
                break

        results.append((subdir, json_count, txt_count, txt_file_path))

        if json_count != txt_count:
            discrepancies.append((subdir, json_count, txt_count))

    results.sort(key=lambda x: x[0])  # Alphabetize by subdir

    for subdir, json_count, txt_count, txt_file_path in results:
        print_colored(subdir, json_count, txt_count, txt_file_path)

    if discrepancies:
        print("\033[91mDiscrepancies found:\033[0m")
        for subdir, json_count, txt_count in discrepancies:
            print(f"\033[95m{subdir}\033[0m: \033[96m{json_count} trials in JSON\033[0m | \033[96m{txt_count} trials in TXT\033[0m")
    else:
        print("\033[92mNo discrepancies found. All counts match.\033[0m")

    choice = input("Do you want to check all clinical trials or just a random one? (all/random): ").strip().lower()

    if choice == "random":
        # Pick a random txt file and print details
        txt_files = find_txt_files(TXT_DIR)
        existing_txt_files = [file for file in txt_files if os.path.exists(file)]
        
        if existing_txt_files:
            random_txt_file = random.choice(existing_txt_files)
            random_subdir = os.path.basename(random_txt_file).split('_part_1.txt')[0]
            json_count = count_json_trials(os.path.join(CATEGORIZED_CONDITIONS_DIR, random_subdir))
            txt_count = count_txt_trials(random_txt_file)
            print_colored(random_subdir, json_count, txt_count, random_txt_file)
        else:
            print("\033[91mNo TXT files found in the TXT directory.\033[0m")
    elif choice == "all":
        # Print details for all clinical trials
        for subdir in subdirs:
            source_dir = os.path.join(CATEGORIZED_CONDITIONS_DIR, subdir)
            txt_files = find_txt_files(TXT_DIR)
            txt_file_path = None
            txt_count = 0

            for txt_file in txt_files:
                if os.path.basename(txt_file).startswith(subdir):
                    txt_file_path = txt_file
                    txt_count = count_txt_trials(txt_file_path)
                    break

            if txt_file_path:
                json_count = count_json_trials(source_dir)
                print_colored(subdir, json_count, txt_count, txt_file_path)
            else:
                json_count = count_json_trials(source_dir)
                print_colored(subdir, json_count, 0)
    else:
        print("\033[91mInvalid choice. Please enter 'all' or 'random'.\033[0m")

if __name__ == "__main__":
    main()
