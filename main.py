import os
import importlib
import sys

class SharaOS:
    def __init__(self):
        self.root_directory = os.path.dirname(os.path.abspath(__file__))
        self.current_directory = self.root_directory
        self.commands = {}
        self.user_commands = set()
        self.reload_commands()

    def reload_commands(self):
        self.commands = {}
        self.user_commands = set()
        core_dir = os.path.join(self.root_directory, 'packages', 'core')
        user_dir = os.path.join(self.root_directory, 'packages', 'userpacks')
        amogos_dir = os.path.join(self.root_directory, 'packages', 'amogospacks')
        
        print(f"Core directory: {core_dir}")
        print(f"User directory: {user_dir}")
        print(f"Amogos packages directory: {amogos_dir}")
        
        # Create amogospacks directory if it doesn't exist
        if not os.path.exists(amogos_dir):
            os.makedirs(amogos_dir)
            print(f"Created Amogos packages directory: {amogos_dir}")
        
        self._load_packages(core_dir, is_core=True)
        self._load_packages(user_dir, is_core=False)
        self._load_packages(amogos_dir, is_core=False)
        
        print("Loaded commands:", list(self.commands.keys()))

    def _load_packages(self, packages_dir, is_core):
        if not os.path.exists(packages_dir):
            print(f"Directory does not exist: {packages_dir}")
            return
        
        sys.path.insert(0, packages_dir)
        
        for filename in os.listdir(packages_dir):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'run'):
                        if is_core or module_name not in self.commands:
                            self.commands[module_name] = module.run
                            if not is_core:
                                self.user_commands.add(module_name)
                            print(f"Loaded {'core' if is_core else 'user'} command: {module_name}")
                        else:
                            print(f"Warning: User command '{module_name}' conflicts with a core command and will be ignored.")
                    else:
                        print(f"Warning: Module '{module_name}' does not have a 'run' function.")
                except ImportError as e:
                    print(f"Error loading {module_name}: {str(e)}")
        
        sys.path.pop(0)

    def run_command(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == 'reload':
            self.reload_commands()
            print("Commands reloaded.")
        elif cmd in self.commands:
            self.commands[cmd](self, *args)
        else:
            print(f"'{cmd}' is not recognized as an internal or external command.")

    def get_relative_path(self):
        return os.path.relpath(self.current_directory, self.root_directory)

def main():
    sharaos = SharaOS()
    print("Welcome to SharaOS")
    print("Type 'help' for a list of commands.")
    while True:
        command = input(f"{sharaos.get_relative_path()}> ")
        if command.lower() == "exit":
            break
        sharaos.run_command(command)

if __name__ == "__main__":
    main()