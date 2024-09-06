#!/bin/bash

# Function to decrypt the password using Python script
decrypt_password() {
    # Call the Python script to decrypt the password
    decrypted_password=$(python3 ~/VASTSYSTEEM/dencrypt.py decrypt "$1")
    echo "$decrypted_password"
}
path=$(pwd)
sed -i "s|ExecStart=~/VASTSYSTEEM/KEEPRUNNING/update-reboot.sh|ExecStart=${home_directory}/VASTSYSTEEM/KEEPRUNNING/update-reboot.sh|" "/home/${USER}/VASTSYSTEEM/KEEPRUNNING/update-reboot.service"

password=$(cat ~/VASTSYSTEEM/S)
decpswd=$(decrypt_password "$password")
echo "Copying necessary update-reboot files..."
echo "$decpswd" | sudo -S cp ~/VASTSYSTEEM/KEEPRUNNING/update-reboot.service /etc/systemd/system
echo "$decpswd" | sudo -S cp ~/VASTSYSTEEM/KEEPRUNNING/update-reboot.timer /etc/systemd/system
echo "Activating timer"
echo "$decpswd" | sudo -S systemctl daemon-reload
echo "$decpswd" | sudo -S systemctl enable update-reboot.timer
echo "$decpswd" | sudo -S systemctl start update-reboot.timer
