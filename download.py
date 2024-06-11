import os
import requests
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from tqdm import tqdm  # tqdm is a progress bar library

def download_zip(zip_url, dest_dir):
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    zip_file_path = os.path.join(dest_dir, "AllAPIJSON.zip")

    print(f"Starting download from {zip_url} to {zip_file_path}")

    try:
        # Stream the download to avoid loading the entire file into memory
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()  # Raise an error if the request was unsuccessful
        
        # Get the total file size from the headers
        total_size = int(response.headers.get('content-length', 0))
        
        # Create a progress bar using tqdm
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=zip_file_path, ascii=True) as pbar:
            # Open the file to write the downloaded content
            with open(zip_file_path, 'wb') as file:
                # Download the file in chunks
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # Filter out keep-alive chunks
                        file.write(chunk)
                        # Update the progress bar
                        pbar.update(len(chunk))
        print(f"Downloaded {zip_file_path}")
    except requests.exceptions.RequestException as e:
        # Print any errors that occur during the download
        print(f"Failed to download: {e}")

    return zip_file_path

if __name__ == "__main__":
    # URL of the ZIP file to download
    zip_url = "https://classic.clinicaltrials.gov/AllAPIJSON.zip"
    # Destination directory to save the downloaded file
    dest_dir = "data/raw"
    print("Executing download script...")
    # Call the download function
    download_zip(zip_url, dest_dir)
    print("Download script finished.")
