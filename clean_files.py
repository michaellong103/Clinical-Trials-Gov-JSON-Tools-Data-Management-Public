import json
import os
import zlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the directories
extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted', 'AllAPIJSON')
base_cleaned_data_dir = os.path.join(BASE_DIR, 'data', 'cleaned')

# Function to read and parse JSON data from a file
def read_json(file_path):
    with open(file_path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            print(f"\033[92mError decoding JSON from file: {file_path}\033[0m")
            print(e)
            return None

# Function to clean and extract necessary information
def clean_data(raw_data):
    cleaned_data = []

    if not isinstance(raw_data, dict):
        print(f"\033[92mInvalid data format: {type(raw_data)}. Expected a dictionary.\033[0m")
        return cleaned_data

    full_study = raw_data.get("FullStudy", {})
    if not isinstance(full_study, dict):
        print(f"\033[92mInvalid FullStudy format: {type(full_study)}. Expected a dictionary.\033[0m")
        return cleaned_data

    study = full_study.get("Study", {})
    if not isinstance(study, dict):
        print(f"\033[92mInvalid Study format: {type(study)}. Expected a dictionary.\033[0m")
        return cleaned_data

    study_info = study.get("ProtocolSection", {})

    # Extract necessary fields with shorter field names
    cleaned_study = {
        "SN": study_info.get("IdentificationModule", {}).get("BriefTitle", "").strip(),
        "ID": study_info.get("IdentificationModule", {}).get("NCTId", "").strip(),
        "IC": "",
        "EC": "",
        "SFSD": study_info.get("StatusModule", {}).get("StudyFirstSubmitDate", "").strip(),
        "SFPD": study_info.get("StatusModule", {}).get("StudyFirstPostDateStruct", {}).get("StudyFirstPostDate", "").strip(),
        "LUSD": study_info.get("StatusModule", {}).get("LastUpdateSubmitDate", "").strip(),
        "LUPD": study_info.get("StatusModule", {}).get("LastUpdatePostDateStruct", {}).get("LastUpdatePostDate", "").strip(),
        "L": [
            {
                "F": loc.get("LocationFacility", "").strip(),
                "C": loc.get("LocationCity", "").strip(),
                "S": loc.get("LocationState", "").strip(),
                "Ctry": loc.get("LocationCountry", "").strip()
            } for loc in study_info.get("ContactsLocationsModule", {}).get("LocationList", {}).get("Location", [])
        ]
    }

    # Extract Inclusion and Exclusion Criteria
    eligibility_criteria = study_info.get("EligibilityModule", {}).get("EligibilityCriteria", "")
    if eligibility_criteria:
        criteria_lines = eligibility_criteria.split('\n')
        inclusion_lines = []
        exclusion_lines = []
        is_inclusion = True

        for line in criteria_lines:
            line = line.strip()
            if 'Exclusion Criteria' in line:
                is_inclusion = False
            if is_inclusion:
                inclusion_lines.append(line)
            else:
                exclusion_lines.append(line)

        cleaned_study["IC"] = '\n'.join(inclusion_lines).strip()
        cleaned_study["EC"] = '\n'.join(exclusion_lines).strip()

    cleaned_data.append(cleaned_study)

    return cleaned_data

# Function to get the next job number
def get_next_job_number(base_dir):
    existing_jobs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not existing_jobs:
        return "0001"
    existing_jobs.sort()
    last_job = existing_jobs[-1]
    next_job_number = int(last_job) + 1
    return f"{next_job_number:04d}"

# Function to compress data
def compress_data(data):
    json_str = json.dumps(data, separators=(',', ':'))  # Minimize whitespace
    compressed_data = zlib.compress(json_str.encode('utf-8'))
    return compressed_data

# Function to decompress data
def decompress_data(compressed_data):
    json_str = zlib.decompress(compressed_data).decode('utf-8')
    data = json.loads(json_str)
    return data

# Function to process all files in the extracted data directory
def process_all_files():
    job_number = get_next_job_number(base_cleaned_data_dir)
    cleaned_data_dir = os.path.join(base_cleaned_data_dir, job_number)

    for subdir, _, files in os.walk(extracted_data_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file.endswith('.json'):  # Ensure the file is a JSON file
                print(f"\033[92mProcessing file: {file_path}\033[0m")
                raw_json = read_json(file_path)
                if raw_json is None:
                    continue
                cleaned_data = clean_data(raw_json)

                # Create a corresponding path in the cleaned data directory
                relative_path = os.path.relpath(file_path, extracted_data_dir)
                cleaned_file_path = os.path.join(cleaned_data_dir, relative_path)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)

                # Compress and save the cleaned data
                compressed_data = compress_data(cleaned_data)
                with open(cleaned_file_path, 'wb') as outfile:
                    outfile.write(compressed_data)
                print(f"\033[92mSaved cleaned data to: {cleaned_file_path}\033[0m")

# Ensure the cleaned data directory exists
os.makedirs(base_cleaned_data_dir, exist_ok=True)
print(f"\033[92mCreated cleaned data directory: {base_cleaned_data_dir}\033[0m")

# Run the processing function
if __name__ == "__main__":
    print("\033[92mStarting to process all files...\033[0m")
    process_all_files()
    print("\033[92mFinished processing all files.\033[0m")
