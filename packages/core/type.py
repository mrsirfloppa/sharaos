import os

def run(sharaos, *args):
    if not args:
        print("Usage: type <filename>")
        return
    filename = args[0]
    try:
        with open(os.path.join(sharaos.current_directory, filename), 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"The system cannot find the file specified.")
