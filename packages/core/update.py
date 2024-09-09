import subprocess, sys

def ensure_requests():
    try: import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    return requests

requests = ensure_requests()

def get_latest_github_release():
    try:
        response = requests.get("https://api.github.com/repos/mrsirfloppa/sharaos/releases/latest")
        return response.json()["tag_name"].lstrip('v') if response.status_code == 200 else "Unknown"
    except Exception as e:
        print(f"Error fetching latest release: {e}")
        return "Unknown"

def update_sharaos():
    print("Updating SharaOS...")
    try:
        subprocess.check_call(["git", "pull", "origin", "main"])
        print("Update successful. Please restart SharaOS.")
    except subprocess.CalledProcessError as e:
        print(f"Update failed: {e}")

def run(sharaos, *args):
    if args and args[0] == "check":
        latest = get_latest_github_release()
        print(f"Latest release on GitHub: {latest}" if latest != "Unknown" else "Unable to fetch the latest release information.")
    else:
        update_sharaos()
