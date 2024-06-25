import os
import json
import argparse
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def print_step(message, step):
    shades_of_green = [
        "\033[32m",  # Green
        "\033[92m",  # Light green
        "\033[32;1m",  # Bright green
        "\033[92;1m",  # Brighter green
    ]
    reset_color = "\033[0m"
    color = shades_of_green[step % len(shades_of_green)]
    print(f"{color}{message}{reset_color}")

def print_in_red(message):
    print(f"\033[31m{message}\033[0m")

def print_in_yellow(message):
    print(f"\033[33m{message}\033[0m")

def print_in_green(message):
    print(f"\033[92m{message}\033[0m")

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"\033[91mError decoding JSON from file: {file_path}\033[0m")
        print(e)
        return None

def search_in_dict(d, condition, path=""):
    if isinstance(d, dict):
        for key, value in d.items():
            new_path = f"{path}.{key}" if path else key
            if key == "BriefTitle" and isinstance(value, str):
                if condition.lower() in value.lower():
                    return new_path
            if isinstance(value, (dict, list)):
                found_path = search_in_dict(value, condition, new_path)
                if found_path:
                    return found_path
    elif isinstance(d, list):
        for index, item in enumerate(d):
            new_path = f"{path}[{index}]"
            found_path = search_in_dict(item, condition, new_path)
            if found_path:
                return found_path
    return None

def count_files(directory):
    file_count = 0
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_count += 1
    return file_count

def move_files_by_condition(source_dir, target_condition, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    moved_files_count = 0

    for subdir, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                print_in_yellow(f"Analyzing file: {file_path}")
                data = read_json(file_path)
                found_path = search_in_dict(data, target_condition) if data else None
                if found_path:
                    dest_path = os.path.join(destination_dir, os.path.relpath(file_path, source_dir))
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(file_path, dest_path)
                    moved_files_count += 1
                    print_in_green(f"Moved {file_path} to {dest_path}")
                    print_in_green(f"Condition '{target_condition}' found at: {found_path}")

    return moved_files_count

def process_condition(condition):
    cleaned_data_dir = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'cleaned')
    condition_dir = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'categorized_conditions', condition.replace(" ", "_").lower())

    print_step("Counting files in the cleaned directory...", 1)
    initial_file_count = count_files(cleaned_data_dir)
    print_in_yellow(f"Number of files in cleaned directory before processing: {initial_file_count}")

    print_step(f"Searching for files with the condition '{condition}'...", 2)
    moved_files_count = move_files_by_condition(cleaned_data_dir, condition, condition_dir)

    final_file_count = count_files(cleaned_data_dir)
    print_in_yellow(f"Number of files in cleaned directory after processing: {final_file_count}")

    print_in_green(f"Number of files moved to {condition.replace(' ', '_').capitalize()} directory: {moved_files_count}")

def main():
    parser = argparse.ArgumentParser(description='Move files based on a condition.')
    parser.add_argument('--condition', type=str, help='The condition to filter the trials by (e.g., "Breast Cancer").')
    parser.add_argument('--conditions_file', type=str, help='Path to the JSON file containing a list of conditions.')

    args = parser.parse_args()

    if args.condition:
        process_condition(args.condition)
    elif args.conditions_file:
        with open(args.conditions_file, 'r') as file:
            conditions = json.load(file)
        for key, condition in conditions.items():
            process_condition(condition)
    else:
        parser.error("You must provide either a condition or a conditions file. Example usage: python3 step_2_split_by_condition.py --condition 'Breast Cancer' OR python3 step_2_split_by_condition.py --conditions_file 'conditions.json'")

if __name__ == '__main__':
    main()
