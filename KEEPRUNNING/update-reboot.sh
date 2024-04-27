#!/bin/bash
password="YOUR_SUDO_PASSWORD"
echo "Running apt update and full-upgrade..."
echo "$password" | su -c "apt update && apt full-upgrade -y"
echo "Finished running apt update and full-upgrade."
echo "Rebooting system..."
systemctl reboot
