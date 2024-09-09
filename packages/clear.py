import os

def run_command():
    """Clears the terminal screen."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS/Linux/Unix
        os.system('clear')
