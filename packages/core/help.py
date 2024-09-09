def run(sharaos, *args):
    print("Available commands:")
    print("\nCore commands:")
    for cmd in sorted(sharaos.commands.keys()):
        if cmd not in sharaos.user_commands:
            print(f"  {cmd}")
    
    print("\nUser commands:")
    for cmd in sorted(sharaos.user_commands):
        print(f"  {cmd}")
    
    print("\nSystem commands:")
    print("  reload  - Reload all commands")
    print("  exit    - Exit SharaOS")
