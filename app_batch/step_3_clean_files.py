import json 
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the directories
extracted_working_dir = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'extracted_working')
cleaned_data_dir = os.path.join(BASE_DIR, 'app_batch', 'data_batch', 'cleaned')

# Function to read and parse JSON data from a file
def read_json(file_path):
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"\033[91mError decoding JSON from file: {file_path}\033[0m")
            print(e)
            return None

# Function to clean and extract necessary information from a single study
def clean_study_data(study):
    cleaned_study = {}
    
    if not isinstance(study, dict):
        print(f"\033[91mInvalid study format: {type(study)}. Expected a dictionary.\033[0m")
        return cleaned_study

    study_info = study.get("ProtocolSection", {})
    nct_id = study_info.get("IdentificationModule", {}).get("NCTId", "")
    nct_id_link = f"clinicaltrials.gov/study/{nct_id}"

    # Extract necessary fields
    cleaned_study = {
        "BriefTitle": study_info.get("IdentificationModule", {}).get("BriefTitle", ""),
        "BriefSummary": study_info.get("DescriptionModule", {}).get("BriefSummary", ""),
        "EligibilityCriteria": study_info.get("EligibilityModule", {}).get("EligibilityCriteria", ""),
        "HealthyVolunteers": study_info.get("EligibilityModule", {}).get("HealthyVolunteers", ""),
        "Gender": study_info.get("EligibilityModule", {}).get("Gender", ""),
        "MinimumAge": study_info.get("EligibilityModule", {}).get("MinimumAge", ""),
        "Location": [
            {
                "Facility": loc.get("LocationFacility", ""),
                "City": loc.get("LocationCity", ""),
                "State": loc.get("LocationState", ""),
                "Zip": loc.get("LocationZip", ""),
                "Country": loc.get("LocationCountry", "")
            } for loc in study_info.get("ContactsLocationsModule", {}).get("LocationList", {}).get("Location", [])
        ],
        "Conditions": study_info.get("ConditionsModule", {}).get("ConditionList", {}).get("Condition", []),
        "Keywords": study_info.get("ConditionsModule", {}).get("KeywordList", {}).get("Keyword", []),
        "Intervention": [
            {
                "Type": intervention.get("InterventionType", ""),
                "Name": intervention.get("InterventionName", "")
            } for intervention in study_info.get("ArmsInterventionsModule", {}).get("InterventionList", {}).get("Intervention", [])
        ],
        "NCTId": nct_id,
        "NCTId_link": nct_id_link,
        "MoreInfoLink": study_info.get("IdentificationModule", {}).get("SecondaryIdInfoList", {}).get("SecondaryIdInfo", [])[0].get("SecondaryIdLink", "") if study_info.get("IdentificationModule", {}).get("SecondaryIdInfoList", {}).get("SecondaryIdInfo", []) else ""
    }

    return cleaned_study

# Function to clean and extract necessary information
def clean_data(raw_data):
    cleaned_data = []

    if isinstance(raw_data, list):
        for item in raw_data:
            full_study = item.get("FullStudy", {})
            study = full_study.get("Study", {})
            cleaned_study = clean_study_data(study)
            if cleaned_study:
                cleaned_data.append(cleaned_study)
    elif isinstance(raw_data, dict):
        full_study = raw_data.get("FullStudy", {})
        study = full_study.get("Study", {})
        cleaned_study = clean_study_data(study)
        if cleaned_study:
            cleaned_data.append(cleaned_study)
    else:
        print(f"\033[91mInvalid data format: {type(raw_data)}. Expected a dictionary or list.\033[0m")

    return cleaned_data

# Function to print colored key-value pairs
def print_colored(key, value):
    key_color = "\033[32m"  # Green
    value_color = "\033[36m"  # Cyan
    reset_color = "\033[0m"
    print(f"{key_color}{key}{reset_color}: {value_color}{value}{reset_color}")

# Function to print directory info
def print_directory_info(directory_name, info):
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

# Function to get directory info
def get_directory_info(directory):
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

# Function to format size to be more human-readable
def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

# Function to process all files in the extracted_working directory
def process_all_files():
    for subdir, _, files in os.walk(extracted_working_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.endswith('.json'):  # Ensure the file is a JSON file
                print(f"\033[92mProcessing file: {file_path}\033[0m")
                raw_json = read_json(file_path)
                if raw_json is None:
                    print(f"\033[91mFailed to read JSON file: {file_path}\033[0m")
                    continue
                cleaned_data = clean_data(raw_json)

                # Debugging: Print cleaned data to ensure it's not empty
                if not cleaned_data:
                    print(f"\033[91mNo data extracted from file: {file_path}\033[0m")
                else:
                    print(f"\033[92mExtracted data: {cleaned_data}\033[0m")

                # Create a corresponding path in the cleaned data directory
                relative_path = os.path.relpath(file_path, extracted_working_dir)
                cleaned_file_path = os.path.join(cleaned_data_dir, relative_path)

                # Append '_cleaned' to the file name
                cleaned_file_path = os.path.splitext(cleaned_file_path)[0] + '_cleaned.json'

                # Ensure the directory exists
                os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)

                # Save the cleaned data
                with open(cleaned_file_path, 'w') as outfile:
                    json.dump(cleaned_data, outfile, indent=4)
                print(f"\033[92mSaved cleaned data to: {cleaned_file_path}\033[0m")

# Ensure the cleaned data directory exists
os.makedirs(cleaned_data_dir, exist_ok=True)
print(f"\033[92mCreated cleaned data directory: {cleaned_data_dir}\033[0m")

# Run the processing function
if __name__ == "__main__":
    print("\033[92mStarting to process all files...\033[0m")
    extracted_info = get_directory_info(extracted_working_dir)
    print_directory_info('Extracted Working', extracted_info)
    process_all_files()
    cleaned_info = get_directory_info(cleaned_data_dir)
    print_directory_info('Cleaned', cleaned_info)
    print("\033[92mFinished processing all files.\033[0m")
