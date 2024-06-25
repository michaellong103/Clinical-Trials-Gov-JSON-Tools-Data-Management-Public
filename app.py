import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name, *args):
    """Run a Python script with optional arguments."""
    script_path = os.path.join(BASE_DIR, script_name)
    if os.path.isfile(script_path):
        subprocess.run(["python3", script_path, *args])
    else:
        print(f"Error: The file {script_path} was not found.")

def display_details(step, script_name, input_dir, output_dir):
    """Display details about the selected script."""
    print(f"\n\033[95mStep {step}: Running {script_name}\033[0m")
    print(f"\033[96mInput directory: {input_dir}\033[0m")
    print(f"\033[96mOutput directory: {output_dir}\033[0m")
    print("\033[93mWould you like to continue? (y/n)\033[0m")

def run_status():
    """Generates a status report for the project."""
    run_script("status.py")

def run_download():
    """Step 1: Downloads the ZIP file from ClinicalTrials.gov."""
    display_details(1, "download.py", "N/A", "data/raw")
    if input().strip().lower() == 'y':
        run_script("download.py")

def run_extract_zip():
    """Step 2: Extracts the contents of the downloaded ZIP file."""
    display_details(2, "extract_zip.py", 'data/raw', 'data/extracted')
    if input().strip().lower() == 'y':
        run_script("extract_zip.py")

def run_split_out_condition():
    """Step 3: Filters and processes data based on a specific condition."""
    condition = input("Enter the condition to filter by (e.g., 'Breast Cancer'): ")
    display_details(3, "split_zip_data_for_test/split_out_condition.py", 'data/extracted', 'data/processed')
    if input().strip().lower() == 'y':
        run_script("split_zip_data_for_test/split_out_condition.py", condition)

def run_clean_file():
    """Step 4: Cleans the data by removing unnecessary information from individual JSON files."""
    display_details(4, "clean_files.py", 'data/processed', 'data/cleaned')
    if input().strip().lower() == 'y':
        run_script("clean_files.py")

def run_json_to_csv_txt_parquet():
    """Step 5: Convert JSON files to CSV, TXT, and Parquet formats and condense files to >10Mgs."""
    display_details(5, "json_to_csv_txt_parquet.py", 'data/cleaned', 'data/csv, data/txt, data/apache_parquet')
    if input().strip().lower() == 'y':
        run_script("json_to_csv_txt_parquet.py")

def main():
    while True:
        print("\033[33mRemember to follow the steps in order for correct data processing.\033[0m")
        print("Choose a command to run:")
        print("1. Step 1: Download the ZIP file from ClinicalTrials.gov (download.py)")
        print("2. Step 2: Extract the contents of the downloaded ZIP file (extract_zip.py)")
        print("3. Step 3: Select a subset of the data from the extracted data (split_zip_data_for_test/split_out_condition.py)")
        print("4. Step 4: Clean the JSON files (clean_files.py)")
        print("5. Step 5: Convert JSON files to CSV, TXT, and Parquet formats (json_to_csv_txt_parquet.py)")
        print("6. Generate a status report (status.py)")
        print("7. Delete JSON files to free up space or remove outdated data (delete_json_files.py)")
        print("8. Randomly split the data into training and testing sets (split_out_random.py)")
        print("0. Exit the program")

        choice = input("Enter the number of the command you want to run: ")

        if choice == '1':
            run_download()
        elif choice == '2':
            run_extract_zip()
        elif choice == '3':
            run_split_out_condition()
        elif choice == '4':
            run_clean_file()
        elif choice == '5':
            run_json_to_csv_txt_parquet()
        elif choice == '6':
            run_status()
        elif choice == '7':
            run_delete_json_files()
        elif choice == '8':
            run_split_out_random()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 8.")

if __name__ == "__main__":
    main()
