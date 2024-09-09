import os
import importlib

# Dictionary to store the commands and their associated functions
commands = {}

def load_commands():
    """Dynamically load all commands from the 'packages' directory."""
    packages_dir = 'packages'
    global commands  # Ensure we modify the global 'commands' dictionary
    commands.clear()  # Clear existing commands before reloading
    
    for filename in os.listdir(packages_dir):
        if filename.endswith('.py') and filename != '__init__.py':  # Ignore __init__.py if exists
            command_name = filename[:-3]  # Remove '.py' to get the module name
            try:
                module = importlib.import_module(f'packages.{command_name}')
                
                # Reload the module in case it's already loaded
                importlib.reload(module)
                
                # Register the command only if the module has a 'run_command' function
                if hasattr(module, 'run_command'):
                    commands[command_name] = module.run_command
                    print(f"Command '{command_name}' loaded successfully.")
                else:
                    print(f"Module '{command_name}' does not have a 'run_command' function.")
            except ImportError as e:
                print(f"Failed to import {command_name}: {e}")

def handle_command(command):
    """Handle a command by checking if it's registered and calling the associated function."""
    if command in commands:
        commands[command]()  # Call the associated function for the command
    else:
        print(f"No valid function found for command '{command}'.")

# Load commands from the 'packages' folder on startup
load_commands()

# Command line loop to capture and process commands
while True:
    terminal_command = input("sharacommandline> ").strip().lower()
    
    if terminal_command == "exit":
        break
    elif terminal_command == "reload":
        print("Reloading all commands...")
        load_commands()  # Reload all commands
    else:
        handle_command(terminal_command)
