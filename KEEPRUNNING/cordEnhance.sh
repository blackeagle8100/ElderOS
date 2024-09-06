#!/bin/bash

# Function to decrypt the password using Python script
decrypt_password() {
    # Call the Python script to decrypt the password
    decrypted_password=$(python3 ~/VASTSYSTEEM/dencrypt.py decrypt "$1")
}



password=$(cat ~/VASTSYSTEEM/S)

decpswd=$(decrypt_password "$password")


version=$(ls -d ~/.config/discord/*/ | head -n1 | grep -oP 'discord/\K[\d.]+')
echo $version
# Fetch the latest version available for download
latest_redirect=$(curl -s "https://discord.com/api/download?platform=linux&format=deb")

# Extract the final URL after following the redirect
latest_url=$(echo "$latest_redirect" | grep -oP 'href="([^"]+)"' | sed 's/href="//' | sed 's/"$//')

# Extract the version number from the URL
latest_version=$(echo "$latest_url" | grep -oP '\/linux\/([\d.]+)' | grep -oP '[\d.]+')
echo $latest_version

if [[ "$version" == "$latest_version" ]]; then
    echo "You are running the latest version of Discord."
    
elif [[ "$version" != "$latest_version" ]]; then
    echo "There is a newer version available: $latest_version"
    pkill Discord
    sleep 0.3
    wget https://discordapp.com/api/download?platform=linux -O ~/Downloads/discord.deb
    cd ~/Downloads
    echo "$decpswd" | sudo -S apt install ./discord.deb -y
    discord --password-store=basic &
    sleep 4
    discord_window_id=$(wmctrl -lx | grep "discord" | awk '{print $1}')

    # Maximize the Discord window
    wmctrl -i -r $discord_window_id -b add,maximized_vert,maximized_horz
    
    rm discord.deb
fi
