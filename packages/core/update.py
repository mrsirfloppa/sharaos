import os
import json
import subprocess
import sys

def ensure_requests():
    try:
        import requests
    except ImportError:
        print("Installing required package: requests")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    return requests

requests = ensure_requests()

VERSION_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'version.json')

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get('version', '0.1')
    return '0.1'

def set_current_version(version):
    with open(VERSION_FILE, 'w') as f:
        json.dump({'version': version}, f)

def get_latest_github_release():
    try:
        response = requests.get("https://api.github.com/repos/mrsirfloppa/sharaos/releases/latest")
        if response.status_code == 200:
            return response.json()["tag_name"].lstrip('v')
    except Exception as e:
        print(f"Error fetching latest release: {e}")
    return "Unknown"

def check_for_updates():
    current_version = get_current_version()
    try:
        response = requests.get("https://api.github.com/repos/mrsirfloppa/sharaos/releases/latest")
        if response.status_code == 200:
            latest_version = response.json()["tag_name"].lstrip('v')
            if latest_version > current_version:
                return latest_version
    except Exception as e:
        print(f"Error checking for updates: {e}")
    return None

def update_sharaos():
    latest_version = check_for_updates()
    if latest_version:
        print(f"Updating SharaOS to version {latest_version}")
        # Here you would implement the actual update logic
        # For example, pulling the latest changes from git
        try:
            subprocess.check_call(["git", "pull", "origin", "main"])
            set_current_version(latest_version)
            print("Update successful. Please restart SharaOS.")
        except subprocess.CalledProcessError as e:
            print(f"Update failed: {e}")
    else:
        print("SharaOS is up to date.")

def run(sharaos, *args):
    if len(args) > 0 and args[0] == "check":
        latest_version = check_for_updates()
        if latest_version:
            print(f"An update is available: version {latest_version}")
        else:
            print("SharaOS is up to date.")
    elif len(args) > 0 and args[0] == "version":
        print(f"Current SharaOS version: {get_current_version()}")
    else:
        update_sharaos()
