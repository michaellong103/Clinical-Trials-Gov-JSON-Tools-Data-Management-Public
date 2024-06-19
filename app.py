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
    """Downloads the ZIP file from ClinicalTrials.gov."""
    run_script("download.py")

def run_extract_zip():
    """Extracts the contents of the downloaded ZIP file."""
    run_script("extract_zip.py")

def run_gpt_recommendation():
    """Uses a GPT model to recommend clinical trials based on the processed data."""
    run_script("gpt_recommendation.py")

def run_clean_file():
    """Cleans the data by removing unnecessary information from individual JSON files."""
    run_script("clean_files.py")

def run_delete_json_files():
    """Deletes JSON files to free up space or remove outdated data."""
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
        print("\033[33mRemember to run option 5 to clean the JSON files before creating another subset of the data.\033[0m")
        print("Choose a command to run:")
        print("1. Generate a status report (status.py)")
        print("2. Download the ZIP file from ClinicalTrials.gov (download.py)")
        print("3. Extract the contents of the downloaded ZIP file (extract_zip.py)")
        print("4. Use a GPT model to recommend clinical trials based on the processed data (gpt_recommendation.py)")
        print("5. Clean and process JSON files from the `data/processed` directory and save the cleaned data into the `data/cleaned` directory (clean_files.py)")
        print("6. Delete JSON files to free up space or remove outdated data (delete_json_files.py)")
        print("7. Randomly split the data into training and testing sets (split_out_random.py)")
        print("8. Filter and process data based on a specific condition (split_out_condition.py)")
        print("9. Filter and process data specifically for breast cancer")
        print("10. Filter and process data specifically for Alzheimer's")
        print("11. Filter and process data based on a user-specified condition")
        print("0. Exit the program")

        choice = input("Enter the number of the command you want to run: ")

        if choice == '1':
            run_status()
        elif choice == '2':
            run_download()
        elif choice == '3':
            run_extract_zip()
        elif choice == '4':
            run_gpt_recommendation()
        elif choice == '5':
            run_clean_file()
        elif choice == '6':
            run_delete_json_files()
        elif choice == '7':
            run_split_out_random()
        elif choice == '8':
            condition = input("Enter the condition to filter by (e.g., 'Breast Cancer'): ")
            run_split_out_condition(condition)
        elif choice == '9':
            run_split_out_breast_cancer()
        elif choice == '10':
            run_split_out_alzheimers()
        elif choice == '11':
            run_split_out_custom_condition()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 11.")

if __name__ == "__main__":
    main()
