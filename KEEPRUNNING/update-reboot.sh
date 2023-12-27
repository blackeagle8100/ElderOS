#!/bin/bash
password="ChangeMe"
echo "Running apt update and full-upgrade..."
echo "$password" | su -c "apt update && apt full-upgrade -y"
echo "Finished running apt update and full-upgrade."
wget https://discordapp.com/api/download?platform=linux -O ~/Downloads/discord.deb
cd ~/Downloads
echo "$password" | su -c "apt install ./discord.deb"
echo "Rebooting system..."
systemctl reboot
