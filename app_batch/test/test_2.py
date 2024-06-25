import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED_WORKING_DIR = os.path.join(BASE_DIR, 'data_batch', 'extracted_working')
CLEANED_DATA_DIR = os.path.join(BASE_DIR, 'data_batch', 'cleaned')

def count_files(directory):
    return sum([len(files) for r, d, files in os.walk(directory)])

def main():
    extracted_working_count = count_files(EXTRACTED_WORKING_DIR)
    cleaned_count = count_files(CLEANED_DATA_DIR)
    difference = extracted_working_count - cleaned_count
    
    print(f"Number of files in extracted_working: {extracted_working_count}")
    print(f"Number of files in cleaned: {cleaned_count}")
    print(f"Difference: {difference}")

if __name__ == "__main__":
    main()
