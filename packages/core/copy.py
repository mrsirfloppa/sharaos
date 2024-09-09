import shutil
import os

def run(sharaos, *args):
    if len(args) != 2:
        print("Usage: copy <source> <destination>")
        return
    source, destination = args
    try:
        shutil.copy2(os.path.join(sharaos.current_directory, source),
                     os.path.join(sharaos.current_directory, destination))
        print(f"        1 file(s) copied.")
    except FileNotFoundError:
        print(f"The system cannot find the file specified.")
