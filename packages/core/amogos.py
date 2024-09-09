import os
import importlib
import subprocess
import sys
import json

def ensure_requests():
    try:
        import requests
    except ImportError:
        print("Installing required package: requests")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests

def run(sharaos, *args):
    ensure_requests()
    import requests  # Import requests here after ensuring it's installed

    if not args:
        print("Usage: amogos <command> [package_name]")
        print("Commands: install, remove, list, update, add-repo, list-repos")
        return

    command = args[0]
    if command == "install" and len(args) > 1:
        install_package(sharaos, args[1])
    elif command == "remove" and len(args) > 1:
        remove_package(sharaos, args[1])
    elif command == "list":
        list_packages(sharaos)
    elif command == "update":
        update_packages(sharaos)
    elif command == "add-repo" and len(args) > 2:
        add_repository(sharaos, args[1], args[2])
    elif command == "list-repos":
        list_repositories(sharaos)
    else:
        print("Invalid command or missing arguments.")

def get_amogospacks_dir(sharaos):
    amogospacks_dir = os.path.join(sharaos.root_directory, 'packages', 'amogospacks')
    if not os.path.exists(amogospacks_dir):
        os.makedirs(amogospacks_dir)
    return amogospacks_dir

def get_repos_file(sharaos):
    return os.path.join(sharaos.root_directory, 'amogos_repos.json')

def load_repositories(sharaos):
    repos_file = get_repos_file(sharaos)
    if os.path.exists(repos_file):
        with open(repos_file, 'r') as f:
            return json.load(f)
    else:
        default_repos = {
            "default": "https://raw.githubusercontent.com/yourusername/sharaos-packages/main/"
        }
        with open(repos_file, 'w') as f:
            json.dump(default_repos, f, indent=2)
        return default_repos

def save_repositories(sharaos, repos):
    repos_file = get_repos_file(sharaos)
    with open(repos_file, 'w') as f:
        json.dump(repos, f, indent=2)

def add_repository(sharaos, name, url):
    repos = load_repositories(sharaos)
    repos[name] = url
    save_repositories(sharaos, repos)
    print(f"Repository '{name}' added successfully.")

def list_repositories(sharaos):
    repos = load_repositories(sharaos)
    print("Available repositories:")
    for name, url in repos.items():
        print(f"  {name}: {url}")

def install_package(sharaos, package_name):
    repos = load_repositories(sharaos)
    for repo_name, repo_url in repos.items():
        package_url = f"{repo_url}{package_name}.py"
        try:
            response = requests.get(package_url)
            if response.status_code == 200:
                amogospacks_dir = get_amogospacks_dir(sharaos)
                with open(os.path.join(amogospacks_dir, f"{package_name}.py"), 'w') as f:
                    f.write(response.text)
                print(f"Package '{package_name}' installed successfully from repository '{repo_name}'.")
                sharaos.reload_commands()
                return
        except Exception as e:
            print(f"Error installing package from repository '{repo_name}': {str(e)}")
    
    print(f"Package '{package_name}' not found in any repository.")

def remove_package(sharaos, package_name):
    amogospacks_dir = get_amogospacks_dir(sharaos)
    package_path = os.path.join(amogospacks_dir, f"{package_name}.py")
    if os.path.exists(package_path):
        os.remove(package_path)
        print(f"Package '{package_name}' removed successfully.")
        sharaos.reload_commands()
    else:
        print(f"Package '{package_name}' not found.")

def list_packages(sharaos):
    amogospacks_dir = get_amogospacks_dir(sharaos)
    print("Installed packages:")
    for filename in os.listdir(amogospacks_dir):
        if filename.endswith('.py'):
            print(f"  {filename[:-3]}")

def update_packages(sharaos):
    # Implement package updating logic here
    print("Package updating not implemented yet.")
