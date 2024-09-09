import os

def run(sharaos, *args):
    if not args:
        print("Usage: delete <filename>")
        return
    filename = args[0]
    try:
        os.remove(os.path.join(sharaos.current_directory, filename))
        print(f"        1 file(s) deleted.")
    except FileNotFoundError:
        print(f"The system cannot find the file specified.")
