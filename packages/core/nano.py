import os

def run(sharaos, *args):
    if not args:
        print("Usage: nano <filename>")
        return

    filename = args[0]
    filepath = os.path.join(sharaos.current_directory, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            content = file.read().splitlines()
    else:
        content = []

    print(f"Editing {filename}. Commands:")
    print("  :q    - Quit without saving")
    print("  :w    - Save and quit")
    print("  :n    - Go to next line")
    print("  :p    - Go to previous line")
    print("  :NUM  - Go to line number NUM")
    print("  :h    - Show this help message")
    
    current_line = 0
    while True:
        print("\n".join(f"{i+1}: {line}" for i, line in enumerate(content)))
        print(f"\nCurrent line: {current_line + 1}")
        
        user_input = input("> ")
        
        if user_input == ":q":
            print("Quitting without saving.")
            return
        elif user_input == ":w":
            with open(filepath, 'w') as file:
                file.write("\n".join(content))
            print(f"File {filename} saved.")
            return
        elif user_input == ":n":
            current_line = min(current_line + 1, len(content))
        elif user_input == ":p":
            current_line = max(current_line - 1, 0)
        elif user_input.startswith(":") and user_input[1:].isdigit():
            line_num = int(user_input[1:]) - 1
            if 0 <= line_num < len(content):
                current_line = line_num
            else:
                print("Invalid line number.")
        elif user_input == ":h":
            print("Commands:")
            print("  :q    - Quit without saving")
            print("  :w    - Save and quit")
            print("  :n    - Go to next line")
            print("  :p    - Go to previous line")
            print("  :NUM  - Go to line number NUM")
            print("  :h    - Show this help message")
        else:
            if current_line == len(content):
                content.append(user_input)
            else:
                content[current_line] = user_input
            current_line += 1
