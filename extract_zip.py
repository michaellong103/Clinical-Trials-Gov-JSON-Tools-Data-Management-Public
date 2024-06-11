import zipfile
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ANSI escape code for yellow text
YELLOW = "\033[93m"
RESET = "\033[0m"

def is_valid_zip(zip_path):
    print(f"{YELLOW}********** Starting Zip Validation **********{RESET}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as _:
            pass
        return True
    except zipfile.BadZipFile:
        return False

def extract_zip(zip_path, extract_to):
    print(f"{YELLOW}********** Starting Zip Extraction **********{RESET}")
    if not is_valid_zip(zip_path):
        print(f"{YELLOW}{zip_path} is not a valid zip file.{RESET}")
        return
    
    zip_filename = os.path.splitext(os.path.basename(zip_path))[0]
    specific_extract_to = os.path.join(extract_to, zip_filename)
    
    os.makedirs(specific_extract_to, exist_ok=True)
    os.chmod(specific_extract_to, 0o777)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        extracted_files = 0
        for file_name in zip_ref.namelist():
            if not file_name.startswith('__MACOSX/'):
                zip_ref.extract(file_name, specific_extract_to)
                print(f"{YELLOW}Extracting {file_name} to {os.path.abspath(os.path.join(specific_extract_to, file_name))}{RESET}")
                extracted_files += 1
                progress = (extracted_files / total_files) * 100
                print(f"{YELLOW}Progress: {progress:.2f}%{RESET}")
        print(f"{YELLOW}Extracted {extracted_files}/{total_files} files.{RESET}")

    print(f"{YELLOW}Extracted {zip_path} to {specific_extract_to}{RESET}")

if __name__ == "__main__":
    print(f"{YELLOW}********** Starting Zip Extraction **********{RESET}")
    zip_path = os.path.join(BASE_DIR, 'data', 'raw', 'AllAPIJSON.zip')
    extract_to = os.path.join(BASE_DIR, 'data', 'extracted')
    print(f"{YELLOW}zip_path: {os.path.abspath(zip_path)}{RESET}")
    print(f"{YELLOW}extract_to: {os.path.abspath(extract_to)}{RESET}")   
    extract_zip(zip_path, extract_to)
    print(f"{YELLOW}Finished extraction{RESET}")
    print(f"{YELLOW}Files in {extract_to}:{RESET}")
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            print(f"{YELLOW}{os.path.join(root, file)}{RESET}")
