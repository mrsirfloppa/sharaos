import os

def run(sharaos, *args):
    if not args:
        print("Usage: md <directory_name>")
        return
    directory = args[0]
    try:
        os.mkdir(os.path.join(sharaos.current_directory, directory))
        print(f"Directory {directory} created.")
    except FileExistsError:
        print(f"A subdirectory or file {directory} already exists.")
