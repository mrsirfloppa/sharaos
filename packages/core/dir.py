import os

def run(sharaos, *args):
    for item in os.listdir(sharaos.current_directory):
        if os.path.isdir(os.path.join(sharaos.current_directory, item)):
            print(f"<DIR>          {item}")
        else:
            size = os.path.getsize(os.path.join(sharaos.current_directory, item))
            print(f"         {size} {item}")
