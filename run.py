#!/usr/bin/env python3
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

def printc(text, color):
    print(f"{color}{text}{RESET}")

# Clear screen
os.system('clear' if os.name == 'posix' else 'cls')

# Show banner
print(f"""
{BLUE}╔══════════════════════════════════════════╗
║       PROFILE GUARD TOOL LAUNCHER       ║
║            by YUNICK                   ║
╚══════════════════════════════════════════╝{RESET}
""")

# Step 1: Git Pull
printc("[1] Checking for updates...", BLUE)
try:
    # Check if git repo
    if os.path.exists(".git"):
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if result.returncode == 0:
            if "Already up to date" in result.stdout:
                printc("[✓] Already up to date", GREEN)
            else:
                printc("[✓] Updated successfully", GREEN)
                print(result.stdout)
        else:
            printc("[!] Git pull failed", YELLOW)
    else:
        printc("[!] Not a git repository", YELLOW)
except:
    printc("[!] Git not installed", YELLOW)

print()

# Step 2: Check 64-bit
printc("[2] Checking system architecture...", BLUE)

# Get architecture
arch = platform.machine().lower()
is_64bit = platform.architecture()[0] == '64bit'

# Common 64-bit architectures
x64_archs = ['x86_64', 'amd64', 'x64', 'arm64', 'aarch64']

printc(f"System: {platform.system()}", YELLOW)
printc(f"Architecture: {arch}", YELLOW)
printc(f"Bit: {platform.architecture()[0]}", YELLOW)

# Check if 64-bit
if is_64bit or any(x in arch for x in x64_archs):
    printc("[✓] 64-bit system detected", GREEN)
    print()
    
    # Step 3: Run the tool
    printc("[3] Starting tool...", BLUE)
    
    # Check for compiled file
    if os.path.exists("guard.cpython-312.so"):
        try:
            # Run the compiled module
            import importlib.util
            spec = importlib.util.spec_from_file_location("guard", "guard.cpython-312.so")
            module = importlib.util.module_from_spec(spec)
            sys.modules["guard"] = module
            spec.loader.exec_module(module)
            
            # Check for run or main function
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()
            else:
                printc("[!] No entry point found in compiled file", RED)
        except Exception as e:
            printc(f"[!] Error running tool: {e}", RED)
    
    # Check for Python version
    elif os.path.exists("profile_guard.py"):
        printc("[•] Running Python version...", YELLOW)
        subprocess.run([sys.executable, "profile_guard.py"])
    
    else:
        printc("[!] No tool file found!", RED)
        printc("[!] Make sure guard.cpython-312.so or profile_guard.py exists", YELLOW)
        
else:
    print()
    printc("[✗] SORRY!", RED)
    printc("This tool requires 64-bit device", RED)
    printc("Your device is 32-bit which is not supported", YELLOW)
    print()
    printc("Please use a 64-bit Android device or PC", BLUE)
    input("\nPress Enter to exit...")
    sys.exit()
