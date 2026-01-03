#!/usr/bin/env python3
import os
import sys
import struct
import subprocess
import importlib

def is_64bit():
    return struct.calcsize("P") * 8 == 64

def git_pull():
    try:
        print("[*] Updating tool (git pull)...")
        subprocess.run(
            ["git", "pull"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

def main():
    git_pull()

    if not is_64bit():
        print("❌ Sorry, your device is not supported.")
        print("⚠ This tool only works on 64-bit devices.")
        sys.exit(1)

    try:
        # IMPORTANT:
        # guard.cpython-312.so must be in the same directory
        import guard
    except ImportError as e:
        print("❌ Failed to load compiled module.")
        print("Reason:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
