import os

def run(sharaos, *args):
    if not args:
        print(sharaos.get_relative_path())
    else:
        path = args[0]
        try:
            new_path = os.path.normpath(os.path.join(sharaos.current_directory, path))
            if not new_path.startswith(sharaos.root_directory):
                print("Access denied: Cannot navigate outside the project folder.")
                return
            if os.path.isdir(new_path):
                sharaos.current_directory = new_path
            else:
                print(f"The system cannot find the path specified.")
        except Exception as e:
            print(f"Error: {str(e)}")