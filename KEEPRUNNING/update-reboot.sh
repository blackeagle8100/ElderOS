#!/bin/bash

# Function to decrypt the password using Python script
decrypt_password() {
    # Call the Python script to decrypt the password
    decrypted_password=$(python3 ~/VASTSYSTEEM/dencrypt.py decrypt "$1")
    echo "$decrypted_password"
}

password=$(cat ~/VASTSYSTEEM/S)
decpswd=$(decrypt_password "$password")



echo "Running apt update and full-upgrade..."
echo "$decpswd" | su -c "apt update && apt full-upgrade -y"
echo "Finished running apt update and full-upgrade."
echo "Rebooting system..."
systemctl reboot
