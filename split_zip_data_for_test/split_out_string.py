# ******** Part of Process ******
import os
import json
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

def print_in_green(message):
    print(f"\033[32m{message}\033[0m")

def print_in_red(message):
    print(f"\033[31m{message}\033[0m")

def list_directories(base_path):
    if not os.path.exists(base_path):
        print(f"Base path '{base_path}' does not exist.")
        sys.exit(0)
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return dirs

def read_json_files(directory):
    data = []
    file_mapping = {}
    print(f"Listing files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r') as file:
                        json_data = json.load(file)
                        if isinstance(json_data, list):
                            data.extend(json_data)
                            file_mapping[file_path] = len(json_data)
                        else:
                            data.append(json_data)
                            file_mapping[file_path] = 1
                except json.JSONDecodeError as e:
                    print(f"Error: The file {file_path} is not a valid JSON file. Error: {e}")
                except Exception as e:
                    print(f"Error: Failed to read file {file_path}. Error: {e}")
    return data, file_mapping

def find_in_nested_dict(d, target_fields, parent_key=''):
    matches = {}
    if isinstance(d, dict):
        for key, value in d.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if key in target_fields:
                matches[key] = value
            if isinstance(value, dict):
                matches.update(find_in_nested_dict(value, target_fields, new_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    matches.update(find_in_nested_dict(item, target_fields, f"{new_key}[{i}]"))
    return matches

def search_target_string(value, target_string):
    if isinstance(value, str) and target_string.lower() in value.lower():
        return True
    elif isinstance(value, list):
        for item in value:
            if target_string.lower() in item.lower():
                return True
    return False

def print_and_save_fields(data, file_mapping, output_dir, target_string):
    target_fields = {
        "BriefTitle",
        "OfficialTitle",
        "BriefSummary",
        "DetailedDescription",
        "Condition",
        "ConditionMeshTerm"
    }

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    found_files = 0
    total_files = len(file_mapping)

    for file_path, num_items in file_mapping.items():
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            if isinstance(json_data, list):
                items_to_check = json_data
            else:
                items_to_check = [json_data]
                
            for item in items_to_check:
                matches = find_in_nested_dict(item, target_fields)
                save_item = False
                for field, value in matches.items():
                    if isinstance(value, list):
                        value = ', '.join(value)
                    if search_target_string(value, target_string):
                        print_in_green(f"Field '{field}': {value}")
                        save_item = True
                
                if save_item:
                    save_path = os.path.join(output_dir, os.path.basename(file_path))
                    with open(save_path, 'w') as save_file:
                        json.dump(item, save_file, indent=2)
                    found_files += 1

    print_in_red(f"Processed {total_files} files. Found {found_files} files containing '{target_string}'.")

def main():
    parser = argparse.ArgumentParser(description='Search and process JSON files for a specific string.')
    parser.add_argument('search_string', type=str, help='The string to search for in the JSON files.')
    args = parser.parse_args()

    extract_base_dir = os.path.join(BASE_DIR, '..', 'data', 'extracted')
    output_dir = os.path.join(BASE_DIR, '..', 'data', 'processed', 'Breast_Cancer')

    directories = list_directories(extract_base_dir)
    
    if not directories:
        print_step("No directories found in the extracted folder. Please use the appropriate option in app.py to extract the zip file.", 0)
        sys.exit(0)

    # Directly select the first directory (assuming it contains the data)
    selected_directory = directories[0]
    extract_to = os.path.join(extract_base_dir, selected_directory)

    print("Selected Extracted Directory:", extract_to)
    print("Output Directory:", output_dir)

    # Check if the extraction directory is not empty
    if not os.listdir(extract_to):
        print_step("The selected directory is empty. Please use the appropriate option in app.py to extract the zip file.", 0)
        sys.exit(0)

    # Step 1: Read the extracted JSON files
    print_step("Step 1: Reading extracted JSON files...", 1)
    data, file_mapping = read_json_files(extract_to)
    print(f"Read {len(data)} trials from extracted JSON files.")

    # Step 2: Print and save relevant fields containing the target string
    print_step(f"Step 2: Printing and saving relevant fields containing '{args.search_string}'...", 2)
    print_and_save_fields(data, file_mapping, output_dir, args.search_string)

if __name__ == '__main__':
    main()
