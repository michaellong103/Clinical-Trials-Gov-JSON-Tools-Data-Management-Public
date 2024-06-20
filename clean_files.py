import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the directories
processed_data_dir = os.path.join(BASE_DIR, 'data', 'processed')
cleaned_data_dir = os.path.join(BASE_DIR, 'data', 'cleaned')

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
        "NCTId": study_info.get("IdentificationModule", {}).get("NCTId", ""),
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

# Function to process all files in the processed data directory
def process_all_files():
    for subdir, _, files in os.walk(processed_data_dir):
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
                relative_path = os.path.relpath(file_path, processed_data_dir)
                cleaned_file_path = os.path.join(cleaned_data_dir, relative_path)

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
    process_all_files()
    print("\033[92mFinished processing all files.\033[0m")
