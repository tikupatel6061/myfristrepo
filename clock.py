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
    if target <= now:  # schedule for tom
