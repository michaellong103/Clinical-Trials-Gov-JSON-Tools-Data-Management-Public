import os
import json
import random
import sys

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

def random_split(data, test_size=0.2):
    random.shuffle(data)
    split_index = int(len(data) * (1 - test_size))
    train_data = data[:split_index]
    test_data = data[split_index:]
    return train_data, test_data

def save_split_data(data, file_mapping, output_dir, suffix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_idx = 0
    for file_path, num_items in file_mapping.items():
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir, f"{filename.split('.')[0]}_{suffix}.json")
        subset = data[start_idx:start_idx + num_items]
        start_idx += num_items
        with open(output_path, 'w') as file:
            json.dump(subset, file, indent=2)
        print(f"Saved {len(subset)} items to {output_path}.")

def main():
    # Adjust the path to the correct directory for extracted data
    extract_base_dir = os.path.join(BASE_DIR, '..', 'data', 'extracted')
    
    directories = list_directories(extract_base_dir)
    
    if not directories:
        print_step("No directories found in the extracted folder. Please use the appropriate option in app.py to extract the zip file.", 0)
        sys.exit(0)

    selected_directory = select_directory(directories)
    extract_to = os.path.join(extract_base_dir, selected_directory)
    output_dir = os.path.join(BASE_DIR, '..', 'data', 'processed', 'random_split')

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

    # Step 2: Randomly split the data
    print_step("Step 2: Randomly splitting the data...", 2)
    train_data, test_data = random_split(data, 0.2)
    print(f"Split data into {len(train_data)} training and {len(test_data)} testing items.")

    # Step 3: Save the split data
    print_step("Step 3: Saving the split data...", 3)
    save_split_data(train_data, file_mapping, output_dir, 'train')
    save_split_data(test_data, file_mapping, output_dir, 'test')

if __name__ == '__main__':
    main()
