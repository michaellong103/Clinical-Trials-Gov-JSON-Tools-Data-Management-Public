# ******** Part of Tools ******
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import shutil

def delete_json_files_and_empty_folders(directory):
    # Track deleted files and folders
    deleted_files = []
    deleted_folders = []

    # Delete JSON files
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    # Delete empty third-level folders
    for root, dirs, files in os.walk(directory, topdown=False):
        if root.count(os.sep) == directory.count(os.sep) + 2:  # third-level folders
            if not files and not dirs:
                try:
                    os.rmdir(root)
                    deleted_folders.append(root)
                except Exception as e:
                    print(f"Failed to delete {root}: {e}")

    # Delete empty folders on the same level as the subfolders of processed or cleaned
    for subfolder in ['processed', 'cleaned']:
        subfolder_path = os.path.join(directory, subfolder)
        if os.path.exists(subfolder_path):
            for item in os.listdir(subfolder_path):
                item_path = os.path.join(subfolder_path, item)
                if os.path.isdir(item_path) and not os.listdir(item_path):
                    try:
                        os.rmdir(item_path)
                        deleted_folders.append(item_path)
                    except Exception as e:
                        print(f"Failed to delete {item_path}: {e}")

    return deleted_files, deleted_folders

def clear_extracted_folder(directory):
    extracted_folder = os.path.join(directory, 'raw', 'extracted')
    if os.path.exists(extracted_folder):
        for root, dirs, files in os.walk(extracted_folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    print(f"Deleted folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to delete {dir_path}: {e}")

def main():
    data_directory = 'data'  # Adjust the path to your data directory
    deleted_files, deleted_folders = delete_json_files_and_empty_folders(data_directory)
    
    print("Deleted JSON files:")
    for file in deleted_files:
        print(file)
    
    print("\nDeleted empty folders:")
    for folder in deleted_folders:
        print(folder)
    
    print("\nClearing extracted folder...")
    clear_extracted_folder(data_directory)
    
    print("Cleanup completed.")

if __name__ == '__main__':
    main()
