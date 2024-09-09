import os
import subprocess
import sys
import requests

# Function to check if a package is installed, and if not, install it
def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"'{package_name}' not found. Installing it...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Automatically install `requests` if it's not installed
install_package("requests")

REPO_RAW_URL = "https://raw.githubusercontent.com/mrsirfloppa/amogospackages/main"
PACKAGE_DIR = 'packages'  # Directory where packages will be stored

def ensure_package_dir():
    """Ensure the packages directory exists."""
    if not os.path.exists(PACKAGE_DIR):
        os.makedirs(PACKAGE_DIR)

def download_package(package_name):
    """Download a single package file from the GitHub repository and save it to the packages folder."""
    ensure_package_dir()  # Ensure the packages folder exists

    package_url = f"{REPO_RAW_URL}/{package_name}.py"
    package_path = os.path.join(PACKAGE_DIR, f"{package_name}.py")

    try:
        response = requests.get(package_url)
        response.raise_for_status()  # Raise an error for bad responses (404, etc.)
        
        # Save the downloaded file in the 'packages' directory
        with open(package_path, 'w') as file:
            file.write(response.text)
        
        print(f"Package '{package_name}' downloaded successfully to '{PACKAGE_DIR}'.")
        return package_path

    except requests.exceptions.RequestException as e:
        print(f"Failed to download package '{package_name}': {e}")
        return None

def remove_package_file(package_name):
    """Remove the package file from the packages folder."""
    package_path = os.path.join(PACKAGE_DIR, f"{package_name}.py")
    
    if os.path.exists(package_path):
        os.remove(package_path)
        print(f"Package '{package_name}' removed successfully from '{PACKAGE_DIR}'.")
    else:
        print(f"Package '{package_name}' is not installed.")

def run_package(package_name, action):
    """Download and run the package with the specified action (install or uninstall)."""
    if action == "install":
        package_path = download_package(package_name)
        if package_path:
            print(f"Running {package_name} ({action})...")
            subprocess.run([sys.executable, package_path], input=action, text=True, check=True)
    elif action == "uninstall":
        print(f"Running {package_name} (uninstall)...")
        package_path = os.path.join(PACKAGE_DIR, f"{package_name}.py")
        if os.path.exists(package_path):
            subprocess.run([sys.executable, package_path], input=action, text=True, check=True)
        # Remove the package file after running the uninstall logic
        remove_package_file(package_name)

def list_available_packages():
    """List the available packages (hardcoded or fetched from the GitHub repo)."""
    ensure_package_dir()  # Ensure the packages folder exists
    print("Available packages in the 'packages' directory:")
    for file in os.listdir(PACKAGE_DIR):
        if file.endswith(".py"):
            print(f"- {file[:-3]}")  # Strip the ".py" extension

def run_command():
    """Run the amogos package manager."""
    print("Welcome to the Amogos Package Manager!")
    print("Available commands: install <package>, remove <package>, list, exit")
    
    while True:
        command = input("amogos> ").strip().lower()
        if command.startswith("install"):
            package_name = command.split()[1]
            run_package(package_name, "install")
        elif command.startswith("remove"):
            package_name = command.split()[1]
            run_package(package_name, "uninstall")
        elif command == "list":
            list_available_packages()
        elif command == "exit":
            print("Exiting Amogos Package Manager.")
            break
        else:
            print("Unknown command. Available commands: install <package>, remove <package>, list, exit")

if __name__ == "__main__":
    run_command()
