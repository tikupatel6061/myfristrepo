#!/usr/bin/env python3
"""
Simple Alarm Clock (no external libraries)

- Set ALARM_TIME in 24-hr "HH:MM" (optionally "HH:MM:SS")
- If that time has already passed today, it will ring tomorrow.
- Cross-platform beep: uses winsound on Windows, console bell elsewhere.
"""

import datetime as dt
import time
import sys

# ==== EDIT THESE ====
ALARM_TIME = "07:30"          # 24-hr time, e.g. "06:45" or "06:45:30"
ALARM_MESSAGE = "Wake up!"    # what to show when it rings
BEEP_SECONDS = 10             # how long to beep
# =====================

def next_alarm_datetime(alarm_str: str) -> dt.datetime:
    parts = [int(p) for p in alarm_str.split(":")]
    now = dt.datetime.now()
    hh, mm = parts[0], parts[1]
    ss = parts[2] if len(parts) == 3 else 0
    target = now.replace(hour=hh, minute=mm, second=ss, microsecond=0)
    if target <= now:  # schedule for tomorrow if time already passed
        target += dt.timedelta(days=1)
    return target

def beep_for(seconds: int):
    end = time.time() + seconds
    if sys.platform.startswith("win"):
        # Use Windows' winsound for a clean tone
        import winsound
        while time.time() < end:
            winsound.Beep(1000, 300)  # freq=1000Hz, 300ms
            time.sleep(0.1)
    else:
        # Cross-platform console bell
        while time.time() < end:
            print("\a", end="", flush=True)  # terminal bell
            time.sleep(0.3)

def main():
    target = next_alarm_datetime(ALARM_TIME)
    print(f"Alarm set for {target.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        while True:
            now = dt.datetime.now()
            remaining = (target - now).total_seconds()
            if remaining <= 0:
                print(f"\n=== {ALARM_MESSAGE} ===")
                beep_for(BEEP_SECONDS)
                break
            # Sleep in short chunks so Ctrl+C is responsive
            time.sleep(min(1, max(0.05, remaining)))
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")

if __name__ == "__main__":
    main()
