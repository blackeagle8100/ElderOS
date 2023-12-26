#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 4 22:47:26 2023
"""

import subprocess
import time
from pynput.mouse import Listener

click_count = 0
last_click_time = 0


def on_click(x, y, button, pressed):
    global click_count, last_click_time

    if pressed:
        current_time = time.time()
        if current_time - last_click_time < 0.5:
            click_count += 1
        else:
            click_count = 1
        last_click_time = current_time

    if click_count == 3:
        mag_factor = subprocess.run(
            ['gsettings', 'get', 'org.gnome.desktop.a11y.magnifier', 'mag-factor'],
            capture_output=True, text=True
        ).stdout.strip()
        print(mag_factor)
        
        if mag_factor == '1.0':
            subprocess.run(
                ['gsettings', 'set', 'org.gnome.desktop.a11y.magnifier', 'mag-factor', '2.0']
            )
            print('Magnification factor set to 2.0')
        elif mag_factor == '2.0':
            subprocess.run(
                ['gsettings', 'set', 'org.gnome.desktop.a11y.magnifier', 'mag-factor', '1.0']
            )
            print('Magnification factor set to 1.0')
        else:
            print('Unexpected magnification factor:', mag_factor)
        click_count = 0


with Listener(on_click=on_click) as listener:
    listener.join()
