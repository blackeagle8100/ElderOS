#!/bin/bash

password="kwetetni"

menu() {
    clear

    echo "*******************************************************************"
    echo "***** * * * *** **********  * * **** * * * ***  ***  **************"
    echo "***** ********* ********** ****** ** ********* ***** **************"
    echo "***** ********* ********** ****** ** ********* ***** **************"
    echo "***** *** * *** ********** ****** ** *** * *** * **  **************"
    echo "***** ********* ********** ****** ** ********* **** ***************"
    echo "***** ********* ********** ****** ** ********* ***** **************"
    echo "***** * * * *** *** *  ***  * * **** * * * *** ****** *************"
    echo "*******************************************************************"
    echo "******************* * * * * *** ** ** *****************************"
    echo "******************* ******* *** ***********************************"
    echo "******************* ******* *** * *** *****************************"
    echo "******************* ******* ********* *****************************"
    echo "******************* * * * * *** * *** *****************************"
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
            cd ..
            cd ..
            chmod -R +x VASTSYSTEEM
            echo "$password" | su -c "apt install spyder python3-pygame python3-opencv python3-pip python3-mutagen python3-selenium xdotool python3-pyqt6 python3-pyqt6.qtwebengine python3-pyqt6.qtmultimedia scrot notepadqq wmctrl htop -y"
            pip install pytube pyautogui moviepy
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
            echo "gnome extensions wanted: No overview at start-up and Hide top bar"
            echo "Press Enter to continue"
            read -r
            echo "Browser starting..."
            firefox extensions.gnome.org
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

packagesInstall

