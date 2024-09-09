import os

def run(sharaos, *args):
    if not args:
        print("Usage: rd <directory_name>")
        return
    directory = args[0]
    try:
        os.rmdir(os.path.join(sharaos.current_directory, directory))
        print(f"The directory was successfully removed.")
    except FileNotFoundError:
        print(f"The system cannot find the directory specified.")
    except OSError:
        print(f"The directory is not empty.")
