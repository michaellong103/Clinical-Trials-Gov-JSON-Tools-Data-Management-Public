# ******** Part of Tools ******
import os
from datetime import datetime

# Base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_directory_summary(directory):
    created = datetime.fromtimestamp(os.path.getctime(directory)).strftime('%Y-%m-%d %H:%M:%S')
    modified = datetime.fromtimestamp(os.path.getmtime(directory)).strftime('%Y-%m-%d %H:%M:%S')
    number_of_files = sum([len(files) for _, _, files in os.walk(directory)])
    number_of_subdirs = sum([len(dirs) for _, dirs, _ in os.walk(directory)])
    return {
        'created_date': created,
        'modified_date': modified,
        'number_of_files': number_of_files,
        'number_of_subdirs': number_of_subdirs
    }

def get_summary_info(base_directory):
    summary_info = []
    for root, dirs, files in os.walk(base_directory):
        if root == base_directory:
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                subdir_info = get_directory_summary(subdir_path)
                subdir_info['path'] = subdir_path
                summary_info.append(subdir_info)
    return summary_info

def print_in_pink(text):
    pink = '\033[95m'
    reset = '\033[0m'
    print(f"{pink}{text}{reset}")

def print_in_white(text):
    white = '\033[97m'
    reset = '\033[0m'
    print(f"{white}{text}{reset}")

def print_directory_tree(directory, level=1):
    for root, dirs, files in os.walk(directory):
        if root == directory:
            indent = ' ' * 4 * (level - 1)
            print(f"{indent}{os.path.basename(root)}/")
            for subdir in dirs:
                print(f"{indent}    {subdir}/")
            for file in files:
                print(f"{indent}    {file}")
            break

def check_and_report_directory(directory, directory_name):
    if not os.path.exists(directory):
        print_in_white(f"{directory_name} directory does not exist. Please run the necessary steps to build the data directories.")
        return False
    return True

def main():
    status = {}

    # Paths
    raw_dir = os.path.join(BASE_DIR, 'data', 'raw')
    processed_dir = os.path.join(BASE_DIR, 'data', 'processed')
    cleaned_dir = os.path.join(BASE_DIR, 'data', 'cleaned')
    extracted_dir = os.path.join(BASE_DIR, 'data', 'extracted')

    # Check and report directories
    raw_exists = check_and_report_directory(raw_dir, 'Raw')
    processed_exists = check_and_report_directory(processed_dir, 'Processed')
    cleaned_exists = check_and_report_directory(cleaned_dir, 'Cleaned')
    extracted_exists = check_and_report_directory(extracted_dir, 'Extracted')

    if not (raw_exists or processed_exists or cleaned_exists or extracted_exists):
        return

    if raw_exists:
        # Search for ZIP files in /raw
        raw_zip_files = [f for f in os.listdir(raw_dir) if f.endswith('.zip')]
        status['raw_zip_files'] = []
        for zip_file in raw_zip_files:
            zip_path = os.path.join(raw_dir, zip_file)
            dir_info = get_directory_summary(raw_dir)
            status['raw_zip_files'].append({
                'path': zip_path,
                'created_date': dir_info['created_date'],
                'modified_date': dir_info['modified_date'],
                'number_of_files': dir_info['number_of_files']
            })

    if processed_exists:
        # Processed JSON directories
        processed_summaries = get_summary_info(processed_dir)
        status['processed_files'] = {
            'path': processed_dir,
            'total_subdirectories': len(processed_summaries),
            'total_files': sum(info['number_of_files'] for info in processed_summaries),
            'created_date': get_directory_summary(processed_dir)['created_date'],
            'modified_date': get_directory_summary(processed_dir)['modified_date']
        }

    if cleaned_exists:
        # Cleaned JSON directories
        cleaned_summaries = get_summary_info(cleaned_dir)
        status['cleaned_files'] = {
            'path': cleaned_dir,
            'total_subdirectories': len(cleaned_summaries),
            'total_files': sum(info['number_of_files'] for info in cleaned_summaries),
            'created_date': get_directory_summary(cleaned_dir)['created_date'],
            'modified_date': get_directory_summary(cleaned_dir)['modified_date']
        }

    if extracted_exists:
        # Extracted directories
        extracted_summaries = get_summary_info(extracted_dir)
        status['extracted_files'] = {
            'path': extracted_dir,
            'total_subdirectories': len(extracted_summaries),
            'total_files': sum(info['number_of_files'] for info in extracted_summaries),
            'created_date': get_directory_summary(extracted_dir)['created_date'],
            'modified_date': get_directory_summary(extracted_dir)['modified_date']
        }

    # Print status
    print_in_pink("=" * 50)
    print_in_pink("Status Report")
    print_in_pink("=" * 50)

    if raw_exists:
        print_in_pink("Raw ZIP files:")
        for zip_file in status['raw_zip_files']:
            print_in_white(f"  Path: {zip_file['path']}")
            print_in_white(f"  Created: {zip_file['created_date']}")
            print_in_white(f"  Last modified: {zip_file['modified_date']}")
            print_in_white(f"  Number of files: {zip_file['number_of_files']}\n")

    if processed_exists:
        print_in_pink("Processed JSON directories:")
        print_in_white(f"  Path: {status['processed_files']['path']}")
        print_in_white(f"  Total subdirectories: {status['processed_files']['total_subdirectories']}")
        print_in_white(f"  Total files: {status['processed_files']['total_files']}")
        print_in_white(f"  Created: {status['processed_files']['created_date']}")
        print_in_white(f"  Last modified: {status['processed_files']['modified_date']}\n")

    if cleaned_exists:
        print_in_pink("Cleaned JSON directories:")
        print_in_white(f"  Path: {status['cleaned_files']['path']}")
        print_in_white(f"  Total subdirectories: {status['cleaned_files']['total_subdirectories']}")
        print_in_white(f"  Total files: {status['cleaned_files']['total_files']}")
        print_in_white(f"  Created: {status['cleaned_files']['created_date']}")
        print_in_white(f"  Last modified: {status['cleaned_files']['modified_date']}\n")

    if extracted_exists:
        print_in_pink("Extracted JSON directories:")
        print_in_white(f"  Path: {status['extracted_files']['path']}")
        print_in_white(f"  Total subdirectories: {status['extracted_files']['total_subdirectories']}")
        print_in_white(f"  Total files: {status['extracted_files']['total_files']}")
        print_in_white(f"  Created: {status['extracted_files']['created_date']}")
        print_in_white(f"  Last modified: {status['extracted_files']['modified_date']}\n")

    print_in_pink("=" * 50)

    # Print directory trees
    if processed_exists:
        print_in_pink("Processed Directory Tree:")
        print_directory_tree(processed_dir)
    if cleaned_exists:
        print_in_pink("Cleaned Directory Tree:")
        print_directory_tree(cleaned_dir)
    if extracted_exists:
        print_in_pink("Extracted Directory Tree:")
        print_directory_tree(extracted_dir)

if __name__ == '__main__':
    main()
