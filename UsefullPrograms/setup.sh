#!/bin/bash

# Function to encrypt the password using Python script
encrypt_password() {
    # Call the Python script to encrypt the password
    encrypted_password=$(python3 ~/VASTSYSTEEM/dencrypt.py encrypt "$1")
    echo "$encrypted_password"
}

# Function to decrypt the password using Python script
decrypt_password() {
    # Call the Python script to decrypt the password
    decrypted_password=$(python3 ~/VASTSYSTEEM/dencrypt.py decrypt "$1")
    echo "$decrypted_password"
}

# Function to check sudo password
check_sudo_password() {
    if echo "$sudo_password" | su -c true >/dev/null 2>&1; then
        return 0  # Password is correct
    else
        return 1  # Password is incorrect
    fi
}

cd ~/
mv ElderOS VASTSYSTEEM
chmod -R +x VASTSYSTEEM

# Prompt user for su password until it's correct
while true; do
    # Prompt user for password and store it in a variable
    read -sp "Enter su password: " sudo_password

    # Check if the password is correct
    if check_sudo_password "$sudo_password"; then
        echo -e "\nSu password is correct."
        encrypted_password=$(encrypt_password "$sudo_password")
        touch S
        echo "$encrypted_password" > ~/VASTSYSTEEM/S
        break  # Exit the loop if the password is correct
    else
        echo -e "\nSu password is incorrect. Please try again."
    fi
done

    # Check if su password is correct
    #if check_su_password "$sudo_password"; then
    #   echo "Correct su password. Continuing."
    #   encrypted_password=$(encrypt_password "$sudo_password")
#	touch S
#   	echo "$encrypted_password" > ~/VASTSYSTEEM/S
#       break
#   else
#       echo "Incorrect su password. Please try again."
#   fi



menu() {
    clear

    echo "*******************************************************************"
    echo "*****███████***█**********██████****███████***███████**************"
    echo "*****█*********█**********█******█**█*********█*****█**************"
    echo "*****█*********█**********█******█**█*********█*****█**************"
    echo "*****███████***█**********█******█**███████***██████***************"
    echo "*****█*********█**********█******█**█*********█****█***************"
    echo "*****█*********█**********█******█**█*********█*****█**************"
    echo "*****███████***████████***██████****███████***█******█*************"
    echo "*******************************************************************"
    echo "*******************█████████***██████******************************"
    echo "*******************█*******█***█***********************************"
    echo "*******************█*******█***██████******************************"
    echo "*******************█*******█********█******************************"
    echo "*******************█████████***██████******************************"
    echo "*******************************************************************"

    # Define an array of items
    items=("Yes" "Skip" "" "" "" "" "" "" "Exit")
    menuItems=()

    # Iterate over the array and print each item with its index
    for ((i=0; i<${#items[@]}; i++)); do
        if [[ -n "${items[i]}" ]]; then
        menuItems+=("$((i+1)): ${items[i]}")
        fi
    done
}

show_items(){
    for item in "${menuItems[@]}"; do
        echo "$item"
    done
}

check_input(){
    if [[ $choice -ge 1 && $choice -le ${#items[@]} ]]; then
        if [[ $choice -ge 3 && $choice -le 8 ]]; then
            return 1
        else
            return 0
        fi
    else
        return 1
    fi
}

valid_input(){
    selected_item="${items[$((choice-1))]}"
    echo "You selected: $selected_item"
}

invalid_input(){
    echo "Invalid choice. Please enter a valid number."
}

packagesInstall(){
    
    echo "Make sure you run this from Usefullprograms!!!"
    echo "Do you want to install and setup ElderOS?"
    show_items
    read -p "" choice
    check_input
    if [ $? -eq 0 ]; then
        valid_input
        if [[ $choice == 1 ]]; then
            echo "Installing packages."
            
            echo "$sudo_password" | su -c "apt install python3-pygame python3-opencv python3-pip python3-mutagen python3-selenium xdotool python3-pyqt6 python3-pyqt6.qtwebengine python3-pyqt6.qtmultimedia python3-google-auth python3-google-auth-oauthlib scrot wmctrl notepadqq blinken htop -y"
            pip install pytube pyautogui moviepy --break-system-packages
            menu
            extensionsInstall
        elif [[ $choice == 2 ]]; then
            extensionsInstall
        elif [[ $choice == 9 ]]; then
            echo "Quiting"
            exit 0
        fi
    else
        invalid_input
    fi
}

extensionsInstall(){

    echo "Do you want to open browser to install gnome-extensions?"
    show_items
    read -p "" choice
    check_input
    if [ $? -eq 0 ]; then
        valid_input
        if [[ $choice == 1 ]]; then
            echo "gnome extensions wanted: No overview at start-up and Hide top bar and also chrome for TV"
            echo "Press Enter to open browser"
            read -r
            echo "Browser starting..."
            firefox extensions.gnome.org
            firefox https://www.google.com/intl/nl/chrome/
            echo "Press Enter to continue"
            read -r
            menu
        elif [[ $choice == 2 ]]; then
            menu
        elif [[ $choice == 9 ]]; then
            echo "Quiting"
            exit 0
        fi
    else
        invalid_input
    fi 

}

menu
cp ~/VASTSYSTEEM/KEEPRUNNING/ElderOS.desktop ~/.config/autostart
packagesInstall
exec ~/VASTSYSTEEM/UsefullPrograms/seleniumdriverdownloader.sh
