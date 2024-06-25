import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_BATCH_DIR = os.path.join(BASE_DIR, 'app_batch')

def run_script(script_name, *args):
    """Run a Python script with optional arguments."""
    script_path = os.path.join(APP_BATCH_DIR, script_name)
    if os.path.isfile(script_path):
        print(f"\033[32mRunning: {script_path} {' '.join(args)}\033[0m")
        subprocess.run(["python3", script_path, *args])
    else:
        print(f"\033[91mError: The file {script_path} was not found.\033[0m")

def main():
    print("\033[33mAutomated Batch Processing Menu\033[0m")
    print("Choose an option to run:")
    print("\033[34m1.\033[0m Copy files from 'Extracted' to 'Extracted Working' directory. (step_1_copy_files.py)")
    print("\033[34m2.\033[0m Clean files to include only necessary JSON data. (step_3_clean_files.py)")
    print("\033[34m3.\033[0m Split cleaned files into separate conditions. (step_2_split_by_condition.py)")
    print("\033[34m4.\033[0m Condense files in categorized conditions into .txt files smaller than 10MB. (step_4_condense_files.py)")
    print("\033[34m5.\033[0m Upload cleaned files to OpenAI Vector Store. (step_4_upload_to_vector_store.py)")
    print("\033[34m6.\033[0m Run tests. (test/test_runner.py)")
    print("\033[34m0.\033[0m Exit")

    choice = input("Enter the number of the command you want to run: ")

    if choice == '1':
        run_script("step_1_copy_files.py")
    elif choice == '2':
        run_script("step_3_clean_files.py")
    elif choice == '3':
        print("\033[33mChoose how to split the files:\033[0m")
        print("\033[34m1.\033[0m Split by a specific condition.")
        print("\033[34m2.\033[0m Split by all conditions in a file.")
        split_choice = input("Enter the number of the split option you want to run: ")
        if split_choice == '1':
            condition = input("Enter the condition to filter the trials by (e.g., 'Breast Cancer'): ")
            run_script("step_2_split_by_condition.py", "--condition", condition)
        elif split_choice == '2':
            conditions_file = input("Enter the path to the conditions file (e.g., 'conditions.json'): ")
            run_script("step_2_split_by_condition.py", "--conditions_file", conditions_file)
        else:
            print("\033[91mInvalid choice. Please enter 1 or 2.\033[0m")
    elif choice == '4':
        run_script("step_4_condense_files.py")
    elif choice == '5':
        run_script("step_4_upload_to_vector_store.py")
    elif choice == '6':
        run_script("test/test_runner.py")
    elif choice == '0':
        print("\033[32mExiting the program.\033[0m")
    else:
        print("\033[91mInvalid choice. Please enter a number from 0 to 6.\033[0m")

if __name__ == "__main__":
    main()
