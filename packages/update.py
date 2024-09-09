import os
import requests
import zipfile
import shutil

def download_zip_from_github(url, save_path):
    """Download the zip file from GitHub."""
    try:
        print(f"Downloading from {url}...")
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"Downloaded zip file to {save_path}")
    except Exception as e:
        print(f"Error downloading from GitHub: {e}")
        return False
    return True

def extract_zip(zip_path, extract_to):
    """Extract the zip file to the specified directory."""
    try:
        print(f"Extracting {zip_path} to {extract_to}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Extraction complete.")
    except Exception as e:
        print(f"Error extracting zip file: {e}")
        return False
    return True

def move_extracted_files(source_dir, target_dir):
    """Move files from the extracted directory to the target directory."""
    try:
        print(f"Moving files from {source_dir} to {target_dir}...")
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(target_dir, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        print("Files moved successfully.")
    except Exception as e:
        print(f"Error moving files: {e}")
        return False
    return True

def cleanup_old_files(target_directory):
    """Optional: Clean up old files in the directory."""
    try:
        print(f"Cleaning up old files in {target_directory}...")
        for root, dirs, files in os.walk(target_directory):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
        print("Old files cleaned up.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return False
    return True

def run_updater():
    """Run the updater to download the latest files from GitHub and extract them."""
    GITHUB_ZIP_URL = "https://github.com/mrsirfloppa/sharaos/archive/refs/heads/master.zip"
    ZIP_PATH = "latest_sharaos.zip"
    EXTRACT_TO = "."

    # Step 1: Download the zip file from GitHub
    if not download_zip_from_github(GITHUB_ZIP_URL, ZIP_PATH):
        return

    # Step 2: Extract the zip file into the current directory
    extract_path = os.path.join(EXTRACT_TO, "sharaos-master")
    if not extract_zip(ZIP_PATH, EXTRACT_TO):
        return

    # Step 3: Move files from 'sharaos-master' to the current directory
    if not move_extracted_files(extract_path, EXTRACT_TO):
        return

    # Step 4: Clean up - remove the downloaded zip and the temporary extraction folder
    os.remove(ZIP_PATH)
    shutil.rmtree(extract_path)
    
    print("Updater complete! The system has been updated with the latest files from GitHub.")

def run_command():
    """Run the updater as a command."""
    run_updater()

if __name__ == "__main__":
    run_updater()
