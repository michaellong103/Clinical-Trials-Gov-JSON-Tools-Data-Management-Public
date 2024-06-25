import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED_WORKING_DIR = os.path.join(BASE_DIR, 'data_batch', 'extracted_working')
CLEANED_DIR = os.path.join(BASE_DIR, 'data_batch', 'cleaned')
CATEGORIZED_CONDITIONS_DIR = os.path.join(BASE_DIR, 'data_batch', 'categorized_conditions')

def count_files(directory):
    file_count = 0
    for root, _, files in os.walk(directory):
        file_count += len(files)
    return file_count

def print_colored(key, value, key_color, value_color):
    reset_color = "\033[0m"
    print(f"{key_color}{key}{reset_color}: {value_color}{value}{reset_color}")

def get_latest_folder(directory):
    folders = [d for d in glob.glob(os.path.join(directory, '*')) if os.path.isdir(d)]
    latest_folder = max(folders, key=os.path.getmtime) if folders else None
    return latest_folder

def main():
    extracted_working_count = count_files(EXTRACTED_WORKING_DIR)
    cleaned_count = count_files(CLEANED_DIR)
    categorized_conditions_count = count_files(CATEGORIZED_CONDITIONS_DIR)
    total_processed_count = cleaned_count + categorized_conditions_count
    latest_folder = get_latest_folder(CATEGORIZED_CONDITIONS_DIR)

    print(f"\033[93mChecking directories:\033[0m")
    print_colored("  Extracted Working Directory", EXTRACTED_WORKING_DIR, "\033[94m", "\033[96m")
    print_colored("  Cleaned Directory", CLEANED_DIR, "\033[94m", "\033[96m")
    print_colored("  Categorized Conditions Directory", CATEGORIZED_CONDITIONS_DIR, "\033[94m", "\033[96m")

    print(f"\033[93mFile counts:\033[0m")
    print_colored("Number of files in extracted_working", extracted_working_count, "\033[92m", "\033[95m")
    print_colored("Number of files in cleaned", cleaned_count, "\033[92m", "\033[95m")
    print_colored("Number of files in categorized_conditions", categorized_conditions_count, "\033[92m", "\033[95m")
    print_colored("Total number of files processed", total_processed_count, "\033[92m", "\033[95m")
    
    if extracted_working_count != total_processed_count:
        differential = extracted_working_count - total_processed_count
        print(f"\033[91mMismatch found! Differential: {differential} files.\033[0m")
    else:
        print("\033[92mThe number of files match!\033[0m")

    if latest_folder:
        print_colored("Latest folder added to categorized_conditions", os.path.basename(latest_folder), "\033[93m", "\033[95m")

if __name__ == "__main__":
    main()
