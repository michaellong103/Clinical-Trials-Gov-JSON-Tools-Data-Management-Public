import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED_DIR = os.path.join(BASE_DIR, '../', 'data', 'extracted')
EXTRACTED_WORKING_DIR = os.path.join(BASE_DIR, 'data_batch', 'extracted_working')

def count_files(directory):
    return sum([len(files) for r, d, files in os.walk(directory)])

def main():
    extracted_count = count_files(EXTRACTED_DIR)
    extracted_working_count = count_files(EXTRACTED_WORKING_DIR)
    difference = extracted_count - extracted_working_count
    
    print(f"Number of files in extracted: {extracted_count}")
    print(f"Number of files in extracted_working: {extracted_working_count}")
    print(f"Difference: {difference}")

if __name__ == "__main__":
    main()
