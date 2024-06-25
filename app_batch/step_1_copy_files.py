import os
import shutil
import datetime

def get_directory_info(directory):
    """Get information about the directory."""
    if not os.path.exists(directory):
        return None

    total_size = 0
    file_count = 0
    file_types = set()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
            file_extension = os.path.splitext(file)[1].upper()
            file_types.add(file_extension)
    
    creation_time = os.path.getctime(directory)
    creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'created': creation_date,
        'size': total_size,
        'file_count': file_count,
        'file_types': list(file_types)
    }

def format_size(size):
    """Format size to be more human-readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def print_colored(key, value):
    """Print key and value with different colors."""
    key_color = "\033[32m"  # Green
    value_color = "\033[36m"  # Cyan
    reset_color = "\033[0m"
    print(f"{key_color}{key}{reset_color}: {value_color}{value}{reset_color}")

def print_directory_info(directory_name, info):
    """Print formatted directory information."""
    if info:
        size = format_size(info['size'])
        file_types = ', '.join(info['file_types'])
        print(f"\033[33m{directory_name} Directory Info\033[0m")  # Yellow title
        print_colored('Created', info['created'])
        print_colored('Size', size)
        print_colored('Number of files', info['file_count'])
        print_colored('File types', f"[{file_types}]")
    else:
        print(f"{directory_name} directory does not exist or is empty.")

def copy_directory(source_dir, destination_dir):
    """Copy the entire source_dir to destination_dir."""
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    if not os.listdir(source_dir):
        print(f"Source directory {source_dir} is empty.")
        return

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)  # Remove existing directory if it exists

    shutil.copytree(source_dir, destination_dir)
    print(f"Copied {source_dir} to {destination_dir}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    EXTRACTED_DIR = os.path.join(BASE_DIR, 'data', 'extracted')
    DESTINATION_DIR = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'extracted_working')

    source_info = get_directory_info(EXTRACTED_DIR)
    print_directory_info('Extracted', source_info)

    copy_directory(EXTRACTED_DIR, DESTINATION_DIR)

    destination_info = get_directory_info(DESTINATION_DIR)
    print_directory_info('Extracted Working', destination_info)
