#!/usr/bin/env python3
# run.py - Simple launcher for Profile Guard Tool

import os
import sys
import platform
import subprocess

# Colors
RED = '\033[1;91m'
GREEN = '\033[1;92m'
YELLOW = '\033[1;93m'
BLUE = '\033[1;94m'
RESET = '\033[0m'

# Clear screen
os.system('clear' if os.name == 'posix' else 'cls')

# Banner
print(f"""
{BLUE}╔══════════════════════════════════════════╗
║       PROFILE GUARD TOOL LAUNCHER       ║
║            by YUNICK                   ║
╚══════════════════════════════════════════╝{RESET}
""")

# 1. Git pull
print(f"{BLUE}[1] Git pull...{RESET}")
os.system("git pull")
print()

# 2. Check 64-bit
print(f"{BLUE}[2] Checking 64-bit...{RESET}")
arch = platform.machine().lower()
is_64bit = platform.architecture()[0] == '64bit'
x64 = ['x86_64', 'amd64', 'x64', 'arm64', 'aarch64']

if is_64bit or any(x in arch for x in x64):
    print(f"{GREEN}[✓] 64-bit system{RESET}")
    print()
    
    # 3. Run tool
    print(f"{BLUE}[3] Starting...{RESET}")
    
    # First try compiled .so file
    if os.path.exists("guard.cpython-312.so"):
        print(f"{GREEN}[•] Found compiled file{RESET}")
        
        # Try to import and run
        try:
            # Add current dir to path
            sys.path.insert(0, os.getcwd())
            
            # Import module
            import importlib.util
            spec = importlib.util.spec_from_file_location("guard", "guard.cpython-312.so")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Try to run
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()
            else:
                # If no run/main, just import guard normally
                import guard
                if hasattr(guard, 'run'):
                    guard.run()
                elif hasattr(guard, 'main'):
                    guard.main()
                else:
                    print(f"{RED}[!] No run() found in compiled file{RESET}")
                    # Fall back to Python source
                    if os.path.exists("guard.py"):
                        os.system(f"python3 guard.py")
        except Exception as e:
            print(f"{RED}[!] Compiled file error: {e}{RESET}")
            # Fall back to Python source
            if os.path.exists("guard.py"):
                print(f"{YELLOW}[•] Running Python source instead{RESET}")
                os.system(f"python3 guard.py")
                
    # If no .so file, run Python source
    elif os.path.exists("guard.py"):
        print(f"{GREEN}[•] Running Python source{RESET}")
        os.system(f"python3 guard.py")
        
    else:
        print(f"{RED}[!] No guard.py or .so file found!{RESET}")
        print("Files in current directory:")
        os.system("ls -la")
        
else:
    print(f"{RED}[✗] 32-bit system not supported{RESET}")
    input("Press Enter to exit...")
