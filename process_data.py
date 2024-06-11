import os
from extract_zip import extract_zip
from clean_files import load_json_files, clean_data, save_clean_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    zip_path = 'data/raw/AllAPIJSON.zip' # Test subset of ClinicalTrials.gov
    # zip_path = 'data/raw/AllAPIJSON.zip' # Everything on ClinicalTrials.gov
    extract_to = 'data/processed'
    output_path = 'data/cleaned/clinical_trials_cleaned.csv'
    
    # Step 1: Extract ZIP filed
    extract_zip(zip_path, extract_to)
    
    # Step 2: Load and clean data
    data = load_json_files(extract_to)
    cleaned_df = clean_data(data)
    
    # Step 3: Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_clean_data(cleaned_df, output_path)

if __name__ == "__main__":
    main()
