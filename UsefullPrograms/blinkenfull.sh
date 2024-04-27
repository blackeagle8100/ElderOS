#!/bin/bash

# Het spel starten
exec ~/.local/share/flatpak/exports/bin/org.kde.blinken

# Het spel in full screen zetten
xdotool windowactivate "Blinken"
xdotool windowmaximize "Blinken"

