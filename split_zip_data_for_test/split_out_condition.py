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

def list_directories(base_path):
    if not os.path.exists(base_path):
        print(f"Base path '{base_path}' does not exist.")
        sys.exit(0)
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return dirs

def select_directory(directories):
    print("Please select the directory to use:")
    for idx, directory in enumerate(directories):
        print(f"{idx + 1}. {directory}")
    while True:
        try:
            choice = int(input("Enter the number of the directory: ").strip())
            if 1 <= choice <= len(directories):
                return directories[choice - 1]
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

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

def search_in_dict(d, condition, path=""):
    if isinstance(d, dict):
        for key, value in d.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, (dict, list)):
                found_path = search_in_dict(value, condition, new_path)
                if found_path:
                    return found_path
            elif isinstance(value, str):
                if condition.lower() in value.lower():
                    return new_path
    elif isinstance(d, list):
        for index, item in enumerate(d):
            new_path = f"{path}[{index}]"
            found_path = search_in_dict(item, condition, new_path)
            if found_path:
                return found_path
    return None

def filter_by_condition(data, condition):
    filtered_data = []
    total_files = len(data)
    for trial in data:
        found_path = search_in_dict(trial, condition)
        if found_path:
            filtered_data.append(trial)
    if not filtered_data:
        print(f"Searched {total_files} files; {condition} not found")
    else:
        print(f"Filtered {len(filtered_data)} trials out of {total_files} total trials for condition '{condition}'.")
    return filtered_data

def save_filtered_data(filtered_data, file_mapping, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_path, num_items in file_mapping.items():
        filename = os.path.basename(file_path)
        matching_data = filtered_data[:num_items]
        filtered_data = filtered_data[num_items:]
        
        if matching_data:
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w') as file:
                json.dump(matching_data, file, indent=2)
            print(f"Saved {len(matching_data)} items to {output_path}.")

def main(condition):
    extract_base_dir = os.path.join(BASE_DIR, '..', 'data', 'extracted')
    output_dir = os.path.join(BASE_DIR, '..', 'data', 'processed', f'subset_{condition.lower()}')

    directories = list_directories(extract_base_dir)
    
    if not directories:
        print_step("No directories found in the extracted folder. Please use the appropriate option in app.py to extract the zip file.", 0)
        sys.exit(0)

    selected_directory = select_directory(directories)
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

    # Step 2: Filter the data by the specific condition
    print_step("Step 2: Filtering data by condition...", 2)
    filtered_data = filter_by_condition(data, condition)

    # Step 3: Save the filtered data into new JSON files
    if filtered_data:
        print_step("Step 3: Saving filtered data to JSON files...", 3)
        save_filtered_data(filtered_data, file_mapping, output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process clinical trial data.')
    parser.add_argument('condition', type=str, help='The condition to filter the trials by (e.g., "Breast Cancer").')

    args = parser.parse_args()
    main(args.condition)
