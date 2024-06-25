import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT_DIR = os.path.join(BASE_DIR, 'data_batch', 'txt')
MAX_SIZE_MB = 10

def find_txt_files(directory):
    txt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                txt_files.append((file_path, file_size))
    return txt_files

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def count_trials_in_txt(file_path):
    try:
        df = pd.read_csv(file_path, sep='\t')
        return len(df)
    except Exception as e:
        print(f"\033[91mError reading {file_path}: {e}\033[0m")
        return 0

def main():
    if not os.path.exists(TXT_DIR):
        print(f"\033[91mError: Directory {TXT_DIR} does not exist.\033[0m")
        return
    
    txt_files = find_txt_files(TXT_DIR)
    large_files = [f for f in txt_files if f[1] > MAX_SIZE_MB * 1024 * 1024]
    
    print("\033[93mAll .txt files and their sizes:\033[0m")
    for file_path, file_size in txt_files:
        relative_path = os.path.relpath(file_path, BASE_DIR)
        formatted_size = format_size(file_size)
        trials_count = count_trials_in_txt(file_path)
        print(f"\033[94m{relative_path}\033[0m: \033[96m{formatted_size}\033[0m, \033[92m{trials_count} trials\033[0m")
    
    if large_files:
        print(f"\n\033[91mFiles larger than {MAX_SIZE_MB}MB:\033[0m")
        for file_path, file_size in large_files:
            relative_path = os.path.relpath(file_path, BASE_DIR)
            formatted_size = format_size(file_size)
            trials_count = count_trials_in_txt(file_path)
            print(f"\033[94m{relative_path}\033[0m: \033[96m{formatted_size}\033[0m, \033[92m{trials_count} trials\033[0m")
    else:
        print(f"\n\033[92mNo files larger than {MAX_SIZE_MB}MB found.\033[0m")

if __name__ == "__main__":
    main()
