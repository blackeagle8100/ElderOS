#!/bin/bash
password="CHANGEME!" #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! inifile password sudo?
echo "Copying necessary update-reboot files..."
echo "$password" | su -c "cp update-reboot.service /etc/systemd/system"
echo "$password" | su -c "cp update-reboot.timer /etc/systemd/system"
echo "Activating timer"
echo "$password" | su -c "systemctl daemon-reload"
echo "$password" | su -c "systemctl start update-reboot.timer"
echo "$password" | su -c "systemctl enable update-reboot.timer"
