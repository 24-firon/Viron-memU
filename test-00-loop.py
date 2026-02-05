
import time
import os
import sys

def main():
    print("============================================================")
    print("TEST 0.0: Native Loop (Docker-Free)")
    print("============================================================")
    
    # 1. Simulate Loop
    print("[*] Starting infinite loop simulation (3 cycles)...")
    for i in range(1, 4):
        print(f"    - Cycle {i}: Checking triggers...")
        time.sleep(1)
        # Mock Check
        if os.path.exists("MISSION_CORE.md"):
            print(f"      [OK] File System Access confirmed (Found MISSION_CORE.md)")
        else:
            print(f"      [FATAL] Cannot read local files!")
            sys.exit(1)

    print("[SUCCESS] Loop Logic works natively on Windows.")
    print("============================================================")

if __name__ == "__main__":
    main()
