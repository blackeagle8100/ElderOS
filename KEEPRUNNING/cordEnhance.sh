#!/bin/bash
password="CHANGEME"


version=$(discord --version --password-store=basic | tr -d '\0' | sed -n 's/.*version":"\([^"]*\).*/\1/p')
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
elif [[ "$version" < "$latest_version" ]]; then
    echo "There is a newer version available: $latest_version"
    pkill discord
    sleep 0.3
    wget https://discordapp.com/api/download?platform=linux -O ~/Downloads/discord.deb
    cd ~/Downloads
    echo "$password" | su -c "apt install ./discord.deb -y"
    discord --password-store=basic &
    sleep 4
    discord_window_id=$(wmctrl -lx | grep "discord" | awk '{print $1}')

    # Maximize the Discord window
    wmctrl -i -r $discord_window_id -b add,maximized_vert,maximized_horz
    
    rm discord.deb
fi
