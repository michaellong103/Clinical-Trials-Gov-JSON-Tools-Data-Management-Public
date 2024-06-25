# ******** Part of Tools ******
import os
from datetime import datetime
import humanize  # Make sure to install the humanize package

# Base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_directory_summary(directory):
    now = datetime.now()
    created_timestamp = os.path.getctime(directory)
    modified_timestamp = os.path.getmtime(directory)
    created_date = datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    modified_date = datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    number_of_files = sum([len(files) for _, _, files in os.walk(directory)])
    total_size = sum([os.path.getsize(os.path.join(root, file)) for root, _, files in os.walk(directory) for file in files])
    created_ago = humanize.naturaltime(now - datetime.fromtimestamp(created_timestamp))
    
    # Collect file types
    file_types = set()
    for root, _, files in os.walk(directory):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            file_types.add(file_extension)
    file_types = ', '.join([f"[{ext.upper()}]" for ext in file_types])

    return {
        'created_date': f"{created_date} ({created_ago})",
        'modified_date': modified_date,
        'number_of_files': number_of_files,
        'total_size': total_size,
        'file_types': file_types
    }

def format_size(size):
    """Format the size to a readable format (bytes, KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def print_in_color(text, color_code):
    reset = '\033[0m'
    print(f"{color_code}{text}{reset}")

def print_directory_summary(summary, directory_name, color_code):
    for subdir in summary:
        created_date = subdir['created_date']
        total_size = format_size(subdir['total_size'])
        number_of_files = subdir['number_of_files']
        file_types = subdir['file_types']
        print(f"{directory_name} - Created: \033[93m{created_date}\033[0m, Size: \033[92m{total_size}\033[0m, Number of files: \033[91m{number_of_files}\033[0m, File types: \033[96m{file_types}\033[0m")  # Yellow for created_date, Green for size, Red for number of files, Cyan for file types

def print_directory_tree(directory, level=1, indent='    '):
    tree_structure = []
    nct_dirs = 0
    for root, dirs, _ in os.walk(directory):
        if root == directory:
            if not dirs:
                tree_structure.append(f"{os.path.basename(root)}/ \033[91m[EMPTY DIRECTORY]\033[0m")  # Red
            else:
                tree_structure.append(f"{os.path.basename(root)}/")
                for subdir in dirs:
                    if subdir.startswith("NCT"):
                        nct_dirs += 1
                    else:
                        subdir_path = os.path.join(root, subdir)
                        subdir_summary = get_directory_summary(subdir_path)
                        tree_structure.append(f"{indent}{subdir}/ - Created: \033[93m{subdir_summary['created_date']}\033[0m, Size: \033[92m{format_size(subdir_summary['total_size'])}\033[0m, Number of files: \033[91m{subdir_summary['number_of_files']}\033[0m, File types: \033[96m{subdir_summary['file_types']}\033[0m")
                if nct_dirs > 0:
                    tree_structure.append(f"{indent}\033[96m{nct_dirs} NCT[x] directories\033[0m")  # Cyan
            break
    return "\n".join(tree_structure)

def main():
    status = {}

    # Paths
    raw_dir = os.path.join(BASE_DIR, 'data', 'raw')
    extracted_dir = os.path.join(BASE_DIR, 'data', 'extracted')
    processed_dir = os.path.join(BASE_DIR, 'data', 'processed')
    cleaned_dir = os.path.join(BASE_DIR, 'data', 'cleaned')
    embeddings_dir = os.path.join(BASE_DIR, 'data', 'embeddings')
    md_dir = os.path.join(BASE_DIR, 'data', 'md')
    txt_dir = os.path.join(BASE_DIR, 'data', 'txt')

    # Check and report directories
    raw_exists = os.path.exists(raw_dir)
    extracted_exists = os.path.exists(extracted_dir)
    processed_exists = os.path.exists(processed_dir)
    cleaned_exists = os.path.exists(cleaned_dir)
    embeddings_exists = os.path.exists(embeddings_dir)
    md_exists = os.path.exists(md_dir)
    txt_exists = os.path.exists(txt_dir)

    if not (raw_exists or extracted_exists or processed_exists or cleaned_exists or embeddings_exists or md_exists or txt_exists):
        print_in_color("No data directories found. Please run the necessary steps to build the data directories.", '\033[91m')  # Red
        return

    # Collect summaries
    if raw_exists:
        raw_summary = get_directory_summary(raw_dir)
        status['raw'] = raw_summary

    if extracted_exists:
        extracted_summary = get_directory_summary(extracted_dir)
        status['extracted'] = extracted_summary

    if processed_exists:
        processed_summary = get_directory_summary(processed_dir)
        status['processed'] = processed_summary

    if cleaned_exists:
        cleaned_summary = get_directory_summary(cleaned_dir)
        status['cleaned'] = cleaned_summary

    if embeddings_exists:
        embeddings_summary = get_directory_summary(embeddings_dir)
        status['embeddings'] = embeddings_summary

    if md_exists:
        md_summary = get_directory_summary(md_dir)
        status['md'] = md_summary

    if txt_exists:
        txt_summary = get_directory_summary(txt_dir)
        status['txt'] = txt_summary

    # Print status
    print_in_color("=" * 50, '\033[95m')  # Pink
    print_in_color("Status Report", '\033[95m')  # Pink
    print_in_color("=" * 50, '\033[95m')  # Pink

    if raw_exists:
        print_directory_summary([status['raw']], "Step 1: Raw", '\033[95m')
        print_in_color(print_directory_tree(raw_dir), '\033[97m')  # White
        print()

    if extracted_exists:
        print_directory_summary([status['extracted']], "Step 2: Extracted", '\033[95m')
        print_in_color(print_directory_tree(extracted_dir), '\033[97m')  # White
        print()

    if processed_exists:
        print_directory_summary([status['processed']], "Step 3: Processed", '\033[95m')
        print_in_color(print_directory_tree(processed_dir), '\033[97m')  # White
        print()

    if cleaned_exists:
        print_directory_summary([status['cleaned']], "Step 4: Cleaned", '\033[95m')
        print_in_color(print_directory_tree(cleaned_dir), '\033[97m')  # White
        print()

    # Additional directories after the main process
    additional_dirs = {
        'Embeddings': embeddings_exists,
        'MD': md_exists,
        'TXT': txt_exists,
    }

    for dir_name, exists in additional_dirs.items():
        if exists:
            summary = status[dir_name.lower()]
            print_directory_summary([summary], f"{dir_name}", '\033[95m')
            directory = os.path.join(BASE_DIR, f"data/{dir_name.lower()}")
            print_in_color(print_directory_tree(directory), '\033[97m')  # White
            print()

    print_in_color("=" * 50, '\033[95m')  # Pink

if __name__ == '__main__':
    main()
