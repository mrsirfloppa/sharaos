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
    return requests

requests = ensure_requests()

def get_repos_file():
    return os.path.join(os.path.dirname(__file__), '..', '..', 'amogos_repos.json')

def load_repositories():
    repos_file = get_repos_file()
    if os.path.exists(repos_file):
        with open(repos_file, 'r') as f:
            return json.load(f)
    return {"default": "mrsirfloppa/amogospackages"}

def save_repositories(repos):
    with open(get_repos_file(), 'w') as f:
        json.dump(repos, f, indent=2)

def get_amogospacks_dir(sharaos):
    return os.path.join(sharaos.root_directory, 'packages', 'amogospacks')

def run(sharaos, *args):
    if not args:
        print("Usage: amogos <command> [options]")
        print("Commands: install, remove, list, update, add-repo, remove-repo, list-repos")
        return

    command = args[0]
    if command == "install":
        if len(args) < 2:
            print("Usage: amogos install <package_name>")
            return
        install_package(sharaos, args[1])
    elif command == "remove":
        if len(args) < 2:
            print("Usage: amogos remove <package_name>")
            return
        remove_package(sharaos, args[1])
    elif command == "list":
        list_packages(sharaos)
    elif command == "update":
        update_packages(sharaos)
    elif command == "add-repo":
        if len(args) < 2:
            print("Usage: amogos add-repo <repo_url>")
            return
        add_repository(args[1])
    elif command == "remove-repo":
        if len(args) < 2:
            print("Usage: amogos remove-repo <repo_name>")
            return
        remove_repository(args[1])
    elif command == "list-repos":
        list_repositories()
    else:
        print(f"Unknown command: {command}")

def add_repository(repo_url):
    repos = load_repositories()
    repo_name = repo_url.split('/')[-1]
    repos[repo_name] = repo_url
    save_repositories(repos)
    print(f"Added repository: {repo_name}")

def remove_repository(repo_name):
    repos = load_repositories()
    if repo_name in repos:
        del repos[repo_name]
        save_repositories(repos)
        print(f"Removed repository: {repo_name}")
    else:
        print(f"Repository not found: {repo_name}")

def list_repositories():
    repos = load_repositories()
    print("Available repositories:")
    for name, url in repos.items():
        print(f"  {name}: {url}")

def install_package(sharaos, package_name):
    repos = load_repositories()
    amogospacks_dir = get_amogospacks_dir(sharaos)
    
    for repo_url in repos.values():
        package_url = f"https://raw.githubusercontent.com/{repo_url}/main/{package_name}.py"
        response = requests.get(package_url)
        if response.status_code == 200:
            os.makedirs(amogospacks_dir, exist_ok=True)
            with open(os.path.join(amogospacks_dir, f"{package_name}.py"), 'w') as f:
                f.write(response.text)
            print(f"Package '{package_name}' installed successfully.")
            sharaos.reload_commands()
            return
    
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
