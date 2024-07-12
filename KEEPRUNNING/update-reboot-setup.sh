#!/bin/bash

# Function to decrypt the password using Python script
decrypt_password() {
    # Call the Python script to decrypt the password
    decrypted_password=$(python3 ~/VASTSYSTEEM/dencrypt.py decrypt "$1")
    echo "$decrypted_password"
}
pwd
password=$(cat ~/VASTSYSTEEM/S)
decpswd=$(decrypt_password "$password")
echo "Copying necessary update-reboot files..."
echo "$decpswd" | su -c "cp VASTSYSTEEM/KEEPRUNNING/update-reboot.service /etc/systemd/system"
echo "$decpswd" | su -c "cp VASTSYSTEEM/KEEPRUNNING/update-reboot.timer /etc/systemd/system"
echo "Activating timer"
echo "$decpswd" | su -c "systemctl daemon-reload"
echo "$decpswd" | su -c "systemctl start update-reboot.timer"
echo "$decpswd" | su -c "systemctl enable update-reboot.timer"
