import os
import json
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED_DIR = os.path.join(BASE_DIR, 'data', 'extracted')
EXTRACTED_WORKING_DIR = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'extracted_working')
CLEANED_DATA_DIR = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'cleaned')
CATEGORIZED_CONDITIONS_DIR = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'categorized_conditions')

def print_colored(message, color):
    colors = {
        'green': '\033[32m',
        'light_green': '\033[92m',
        'yellow': '\033[33m',
        'red': '\033[31m',
        'cyan': '\033[36m',
        'reset': '\033[0m'
    }
    print(f"{colors[color]}{message}{colors['reset']}")

def get_directory_info(directory):
    if not os.path.exists(directory):
        return None

    total_size = 0
    file_count = 0
    file_types = set()
    file_dates = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
            file_extension = os.path.splitext(file)[1].upper()
            file_types.add(file_extension)
            file_dates.append(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))

    creation_time = os.path.getctime(directory)
    creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'created': creation_date,
        'size': total_size,
        'file_count': file_count,
        'file_types': list(file_types),
        'file_dates': sorted(file_dates)
    }

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def print_directory_info(directory_name, info):
    if info:
        size = format_size(info['size'])
        file_types = ', '.join(info['file_types'])
        first_file_date = info['file_dates'][0].strftime('%Y-%m-%d %H:%M:%S')
        last_file_date = info['file_dates'][-1].strftime('%Y-%m-%d %H:%M:%S')
        print_colored(f"{directory_name} Directory Info", 'yellow')
        print_colored(f"  Created: {info['created']}", 'green')
        print_colored(f"  Size: {size}", 'green')
        print_colored(f"  Number of files: {info['file_count']}", 'green')
        print_colored(f"  File types: [{file_types}]", 'green')
        print_colored(f"  First file date: {first_file_date}", 'green')
        print_colored(f"  Last file date: {last_file_date}", 'green')
    else:
        print_colored(f"{directory_name} directory does not exist or is empty.", 'red')

def count_files(directory):
    file_count = 0
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_count += 1
    return file_count

def check_files_moved(condition):
    condition_dir = os.path.join(CATEGORIZED_CONDITIONS_DIR, condition.replace(" ", "_").lower())
    return count_files(condition_dir)

def check_keywords(directory, keywords):
    keyword_counts = {keyword: 0 for keyword in keywords}
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        for keyword in keywords:
                            if keyword.lower() in json.dumps(data).lower():
                                keyword_counts[keyword] += 1
                    except json.JSONDecodeError:
                        continue
    return keyword_counts

def generate_status_report():
    print_colored("Generating status report...", 'cyan')

    # Extracted Directory Info
    extracted_info = get_directory_info(EXTRACTED_DIR)
    print_directory_info('Extracted', extracted_info)

    # Extracted Working Directory Info
    extracted_working_info = get_directory_info(EXTRACTED_WORKING_DIR)
    print_directory_info('Extracted Working', extracted_working_info)

    # Cleaned Data Directory Info
    cleaned_info = get_directory_info(CLEANED_DATA_DIR)
    print_directory_info('Cleaned', cleaned_info)

    # Check conditions
    conditions_file = os.path.join(BASE_DIR, 'conditions.json')
    if os.path.isfile(conditions_file):
        with open(conditions_file, 'r') as file:
            conditions = json.load(file)
        for key, condition in conditions.items():
            moved_files = check_files_moved(condition)
            print_colored(f"Number of files moved to {condition.replace(' ', '_').capitalize()} directory: {moved_files}", 'green')

    # Check keywords in Cleaned Data Directory
    keywords = ["BriefTitle", "BriefSummary", "EligibilityCriteria"]
    keyword_counts = check_keywords(CLEANED_DATA_DIR, keywords)
    print_colored("Keyword Counts in Cleaned Data:", 'cyan')
    for keyword, count in keyword_counts.items():
        print_colored(f"  {keyword}: {count}", 'green')

if __name__ == "__main__":
    generate_status_report()
