import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name, *args):
    """Run a Python script with optional arguments."""
    script_path = os.path.join(BASE_DIR, script_name)
    subprocess.run(["python3", script_path, *args])

def run_status():
    """Generates a status report for the project."""
    run_script("status.py")

def run_download():
    """Step 1: Downloads the ZIP file from ClinicalTrials.gov."""
    run_script("download.py")

def run_extract_zip():
    """Step 2: Extracts the contents of the downloaded ZIP file."""
    print("\033[95mInput directory: 'data/raw'\033[0m")
    print("\033[95mOutput directory: 'data/extracted'\033[0m")
    run_script("extract_zip.py")

def run_clean_file():
    """Step 3: Cleans the data by removing unnecessary information from individual JSON files."""
    print("\033[95mInput directory: 'data/processed'\033[0m")
    print("\033[95mOutput directory: 'data/cleaned'\033[0m")
    run_script("clean_files.py")

def run_json_to_csv():
    """Step 4: Converts JSON files to CSV format."""
    print("\033[95mInput directory: 'data/cleaned'\033[0m")
    print("\033[95mOutput directory: 'data/csv'\033[0m")
    run_script("json_to_csv.py")

def run_create_embeddings():
    """Step 5: Creates embeddings for the processed data."""
    print("\033[95mInput directory: 'data/cleaned'\033[0m")
    print("\033[95mOutput directory: 'data/embeddings'\033[0m")
    run_script("create_embeddings.py")

def run_json_to_parquet():
    """Step 6: Converts JSON files to Parquet format."""
    print("\033[95mInput directory: 'data/cleaned'\033[0m")
    print("\033[95mOutput directory: 'data/apache_parquet'\033[0m")
    run_script("json_to_parquet.py")

def run_langchain_create_json():
    """Step 7: Creates a LangChain JSON index for a specific query."""
    query = input("Enter your query for LangChain JSON index (e.g., 'Find Breast Cancer Trials'): ")
    print("\033[95mInput directory: 'data/cleaned'\033[0m")
    run_script("langchain_create_json.py", query)

def run_gpt_recommendation():
    """Uses a GPT model to recommend clinical trials based on the processed data."""
    run_script("gpt_recommendation.py")

def run_delete_json_files():
    """Deletes JSON files to free up space or remove outdated data."""
    print("\033[95mInput directory: 'data'\033[0m")
    run_script("delete_json_files.py")

def run_split_out_condition(condition):
    """Filters and processes data based on a specific condition."""
    run_script("split_zip_data_for_test/split_out_condition.py", condition)

def run_split_out_random():
    """Randomly splits the data into training and testing sets."""
    run_script("split_zip_data_for_test/split_out_random.py")

def run_split_out_breast_cancer():
    """Filters and processes data specifically for breast cancer."""
    run_split_out_condition("Breast Cancer")

def run_split_out_alzheimers():
    """Filters and processes data specifically for Alzheimer's."""
    run_split_out_condition("Alzheimer's")

def run_split_out_custom_condition():
    """Filters and processes data based on a user-specified condition."""
    condition = input("Enter the condition to filter by (e.g., 'Breast Cancer'): ")
    run_split_out_condition(condition)

def check_file_exists(file_path):
    """Check if a file exists and print a message if it does not."""
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} was not found.")
        return False
    return True

def main():
    while True:
        print("\033[33mRemember to run option 3 to clean the JSON files before creating another subset of the data.\033[0m")
        print("Choose a command to run:")
        print("1. Step 1: Download the ZIP file from ClinicalTrials.gov (download.py)")
        print("2. Step 2: Extract the contents of the downloaded ZIP file (extract_zip.py)")
        print("3. Step 3: Clean and process JSON files from the `data/processed` directory (clean_files.py)")
        print("4. Step 4: Convert JSON files to CSV format (json_to_csv.py)")
        print("5. Step 5: Create embeddings for the processed data (create_embeddings.py)")
        print("6. Step 6: Convert JSON files to Parquet format (json_to_parquet.py)")
        print("7. Step 7: Create a LangChain JSON index (langchain_create_json.py)")
        print("8. Generate a status report (status.py)")
        print("9. Delete JSON files to free up space or remove outdated data (delete_json_files.py)")
        print("10. Randomly split the data into training and testing sets (split_out_random.py)")
        print("11. Filter and process data specifically for breast cancer")
        print("12. Filter and process data specifically for Alzheimer's")
        print("13. Filter and process data based on a user-specified condition")
        print("0. Exit the program")

        choice = input("Enter the number of the command you want to run: ")

        if choice == '1':
            run_download()
        elif choice == '2':
            run_extract_zip()
        elif choice == '3':
            run_clean_file()
        elif choice == '4':
            run_json_to_csv()
        elif choice == '5':
            run_create_embeddings()
        elif choice == '6':
            run_json_to_parquet()
        elif choice == '7':
            run_langchain_create_json()
        elif choice == '8':
            run_status()
        elif choice == '9':
            run_delete_json_files()
        elif choice == '10':
            run_split_out_random()
        elif choice == '11':
            run_split_out_breast_cancer()
        elif choice == '12':
            run_split_out_alzheimers()
        elif choice == '13':
            run_split_out_custom_condition()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 13.")

if __name__ == "__main__":
    main()
