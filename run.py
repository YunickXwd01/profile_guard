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
    
    # Method 1: Try to import the compiled module directly
    try:
        # First check if .so file exists
        if os.path.exists("guard.cpython-312.so"):
            printc("[•] Loading compiled module...", YELLOW)
            
            # Add current directory to Python path
            sys.path.insert(0, os.getcwd())
            
            # Try to import
            try:
                # For Cython compiled modules, we need to import differently
                import importlib.util
                
                # Get the module name from file name
                module_name = "guard"
                
                # Load the module
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    "guard.cpython-312.so"
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check what functions are available
                printc(f"[•] Module loaded: {module}", GREEN)
                
                # Try common function names
                if hasattr(module, 'run'):
                    printc("[•] Calling run() function...", YELLOW)
                    module.run()
                elif hasattr(module, 'main'):
                    printc("[•] Calling main() function...", YELLOW)
                    module.main()
                elif hasattr(module, '__main__'):
                    printc("[•] Executing __main__...", YELLOW)
                    exec(module.__main__)
                else:
                    # Try to execute the module directly
                    printc("[•] Trying direct execution...", YELLOW)
                    # If it's a Cython module with __pyx_unpickle_Enum etc.
                    # Just import it normally
                    import guard
                    
                    # Check again after import
                    if hasattr(guard, 'run'):
                        guard.run()
                    elif hasattr(guard, 'main'):
                        guard.main()
                    else:
                        printc("[!] Could not find run() or main() in module", RED)
                        printc("[!] Available functions:", YELLOW)
                        for attr in dir(guard):
                            if not attr.startswith('__'):
                                printc(f"  - {attr}", YELLOW)
                        
            except Exception as e:
                printc(f"[!] Error loading compiled module: {e}", RED)
                
                # Method 2: Try to run as Python module
                printc("[•] Trying alternative method...", YELLOW)
                try:
                    # Try to run it using python -m approach
                    subprocess.run([sys.executable, "-c", "import guard; guard.run()"])
                except:
                    pass
                
        else:
            printc("[!] Compiled file not found: guard.cpython-312.so", RED)
            
    except Exception as e:
        printc(f"[!] Error: {e}", RED)
    
    # Method 3: Check for Python source file as fallback
    if not os.path.exists("guard.cpython-312.so"):
        printc("[•] Checking for Python source file...", YELLOW)
        
        # List Python files
        py_files = [f for f in os.listdir('.') if f.endswith('.py')]
        main_files = ['profile_guard.py', 'guard.py', 'main.py', 'tool.py']
        
        # Try known main files first
        for file in main_files:
            if os.path.exists(file):
                printc(f"[•] Found Python file: {file}", GREEN)
                printc(f"[•] Running {file}...", BLUE)
                subprocess.run([sys.executable, file])
                break
        else:
            # Try any Python file
            if py_files:
                printc(f"[•] Found Python files: {py_files[0]}", GREEN)
                subprocess.run([sys.executable, py_files[0]])
            else:
                printc("[!] No Python files found!", RED)
    
else:
    print()
    printc("[✗] SORRY!", RED)
    printc("This tool requires 64-bit device", RED)
    printc("Your device is 32-bit which is not supported", YELLOW)
    print()
    printc("Please use a 64-bit Android device or PC", BLUE)
    input("\nPress Enter to exit...")
    sys.exit()
