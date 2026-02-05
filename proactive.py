
"""
proactive.py
------------
The heartbeat of Viron-memU (Native Phase 1).
Implements a hybrid Loop/Cron pattern.

Functionality:
1. Infinite Loop (State: Active)
2. Schedule Checks (Mocking pg_cron)
3. File Watcher (Basic Polling)
"""

import time
import datetime
import sys
import os

# Configuration
tick_rate = 5  # Seconds between ticks
active_hours = (8, 22) # Only run between 08:00 and 22:00

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [PROACTIVE] {msg}")

def check_schedule():
    """Simulate internal Cron jobs"""
    now = datetime.datetime.now()
    
    # Simple check: Is it top of the hour?
    if now.minute == 0 and now.second < 10:
        log("Executing Hourly Routine (Memory Consolidation)...")
        # TODO: Call memory consolidation logic
        pass

def check_filesystem():
    """Layer 1 Input: Watch files"""
    # Placeholder for watchdog logic
    if os.path.exists("trigger.txt"):
        log("Found 'trigger.txt'! Reacting...")
        try:
            os.remove("trigger.txt")
            log("Trigger consumed.")
        except Exception as e:
            log(f"Error reading trigger: {e}")

def main():
    log("System START. Type: Native Loop (Phase 1).")
    log(f"Config: Tick every {tick_rate}s.")

    try:
        while True:
            # 1. Resource Guard (Sleep if PC is 'off' or out of hours - Mocked)
            # In Phase 1, we just run.
            
            # 2. Execute Checks
            check_schedule()
            check_filesystem()
            
            # 3. Heartbeat
            # log("Tick...") 
            
            # 4. Sleep
            time.sleep(tick_rate)
            
    except KeyboardInterrupt:
        log("System END (User Interrupt).")
        sys.exit(0)

if __name__ == "__main__":
    main()
