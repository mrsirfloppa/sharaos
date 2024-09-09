import os, subprocess, sys

def ensure_requests():
    try: import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    return requests

requests = ensure_requests()

def get_repos_file():
    return os.path.join(os.path.dirname(__file__), '..', '..', 'amogos_repos.json')

def load_repositories():
    repos_file = get_repos_file()
    return [line.strip() for line in open(repos_file)] if os.path.exists(repos_file) else ["mrsirfloppa/amogospackages"]

def save_repositories(repos):
    with open(get_repos_file(), 'w') as f:
        f.write('\n'.join(repos))

def get_amogospacks_dir(sharaos):
    return os.path.join(sharaos.root_directory, 'packages', 'amogospacks')

def list_all_available_packages():
    return [item['name'][:-3] for repo in load_repositories() for item in requests.get(f"https://api.github.com/repos/{repo}/contents").json() if item['name'].endswith('.py')]

def run(sharaos, *args):
    if not args:
        print("Usage: amogos <command> [options]\nCommands: install, remove, list, update, add-repo, remove-repo, list-repos")
        return
    
    command, *options = args
    if command == "install" and options:
        install_package(sharaos, options[0])
    elif command == "remove" and options:
        remove_package(sharaos, options[0])
    elif command == "list":
        list_packages(sharaos)
    elif command == "update":
        update_packages(sharaos)
    elif command == "add-repo" and options:
        add_repository(options[0])
    elif command == "remove-repo" and options:
        remove_repository(options[0])
    elif command == "list-repos":
        list_repositories()
    else:
        print(f"Invalid command or missing options: {command}")

def add_repository(repo_url):
    repos = load_repositories()
    if repo_url not in repos:
        repos.append(repo_url)
        save_repositories(repos)
        print(f"Added repository: {repo_url}")
    else:
        print(f"Repository already exists: {repo_url}")

def remove_repository(repo_url):
    repos = load_repositories()
    if repo_url in repos:
        repos.remove(repo_url)
        save_repositories(repos)
        print(f"Removed repository: {repo_url}")
    else:
        print(f"Repository not found: {repo_url}")

def list_repositories():
    print("Available repositories:")
    for repo in load_repositories():
        print(f"  {repo}")

def install_package(sharaos, package_name):
    for repo in load_repositories():
        response = requests.get(f"https://raw.githubusercontent.com/{repo}/main/{package_name}.py")
        if response.status_code == 200:
            amogospacks_dir = get_amogospacks_dir(sharaos)
            os.makedirs(amogospacks_dir, exist_ok=True)
            with open(os.path.join(amogospacks_dir, f"{package_name}.py"), 'w') as f:
                f.write(response.text)
            print(f"Package '{package_name}' installed successfully.")
            sharaos.reload_commands()
            return
    print(f"Package '{package_name}' not found in any repository.")

def remove_package(sharaos, package_name):
    package_path = os.path.join(get_amogospacks_dir(sharaos), f"{package_name}.py")
    if os.path.exists(package_path):
        os.remove(package_path)
        print(f"Package '{package_name}' removed successfully.")
        sharaos.reload_commands()
    else:
        print(f"Package '{package_name}' not found.")

def list_packages(sharaos):
    print("Installed packages:")
    for filename in os.listdir(get_amogospacks_dir(sharaos)):
        if filename.endswith('.py'):
            print(f"  {filename[:-3]}")

def update_packages(sharaos):
    print("Package updating not implemented yet.")
