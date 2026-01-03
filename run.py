#!/usr/bin/env python3
# run.py - Simple launcher

import os
import sys
import platform

print("""
╔══════════════════════════════════════════╗
║       PROFILE GUARD TOOL LAUNCHER       ║
║            by YUNICK                   ║
╚══════════════════════════════════════════╝
""")

# 1. Git pull
print("[1] Checking updates...")
os.system("git pull")
print()

# 2. Check 64-bit
print("[2] Checking system...")
arch = platform.machine().lower()

# Check if 64-bit
if '64' in platform.architecture()[0] or any(x in arch for x in ['x86_64', 'amd64', 'arm64', 'aarch64']):
    print("[✓] 64-bit OK")
    print()
    
    # 3. Run the tool
    print("[3] Starting...")
    
    # Try compiled .so first
    so_file = "guard.cpython-312.so"
    if os.path.exists(so_file):
        print(f"[•] Running compiled version")
        try:
            # Import and run
            sys.path.insert(0, os.getcwd())
            import guard
            guard.run()
        except Exception as e:
            print(f"[!] Error: {e}")
            print("[•] Running Python source")
            if os.path.exists("guard.py"):
                exec(open("guard.py").read())
    elif os.path.exists("guard.py"):
        print("[•] Running Python source")
        exec(open("guard.py").read())
    else:
        print("[!] No guard file found!")
        
else:
    print("[✗] SORRY! 32-bit not supported")
    input("Press Enter to exit...")
