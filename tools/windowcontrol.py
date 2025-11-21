#!/usr/bin/env python3

import os, subprocess, time

def _get_elderos_window():
    try:
        wid = subprocess.getoutput(
            "xdotool search --name 'MAIN' 2>/dev/null || true"
        ).strip()
        return wid if wid.isdigit() else None
    except Exception:
        return None

def hide_elderos():
    wid = _get_elderos_window()
    if wid:
        os.system(f"xdotool windowunmap {wid}")

def show_elderos():
    for _ in range(10):     # probeer 1 s lang
        wid = _get_elderos_window()
        if wid:
            os.system(f"xdotool windowmap {wid}")
            os.system(f"xdotool windowactivate {wid}")
            return True
        time.sleep(0.1)
    return False
