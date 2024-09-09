import os

def run(sharaos, *args):
    if not args:
        print("Usage: touch <filename>")
        return
    filename = args[0]
    open(os.path.join(sharaos.current_directory, filename), 'a').close()
    print(f"File {filename} created.")
