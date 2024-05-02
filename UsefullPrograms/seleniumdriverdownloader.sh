#!/bin/bash


menu() {
    clear

    echo "This is the installer for chrome and geckodrivers"
    echo "What do you want to install?"

    # Define an array of items
    items=("Chromedriver" "Geckodriver" "All" "" "" "" "" "" "Exit")
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
        if [[ $choice -ge 4 && $choice -le 8 ]]; then
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
}

invalid_input(){
    echo "Invalid choice. Please enter a valid number."
}

download_chromedriver() {
    if ! type google-chrome >/dev/null 2>&1; then
        echo "Please install chrome"
    fi
    # URL of the page
    URL="https://googlechromelabs.github.io/chrome-for-testing/#stable"
    zip="chromedriver.zip"
    # Retrieve the content of the page
    page_content=$(curl -s "$URL")
    # Extract the Channel, Version, Revision, and Status using grep
    version=$(echo "$page_content" | grep -oP '<th>Version.*?<code>(.*?)</code>' | sed -r 's/<[^>]*>//g' | grep -oP '\d+\.\d+\.\d+\.\d+')
    # Print the extracted information
    echo "Version: $version"
    # Construct the download URL
    download="https://storage.googleapis.com/chrome-for-testing-public/${version}/linux64/chromedriver-linux64.zip"
    curl -o $zip $download
    unzip $zip
    rm $zip
    mv chromedriver-linux64/chromedriver ~/VASTSYSTEEM/
    rm  -R chromedriver-linux64/
}

download_geckodriver(){

    zip="geckodriver.tar.gz"
    URL="https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    #zip="chromedriver.zip"
        # Retrieve the content of the page
    page_content=$(curl -s "$URL")
        # Extract the Channel, Version, Revision, and Status using grep
    geckourl=$(echo "$page_content" | jq -r '.assets[4].browser_download_url')
        # Print the extracted information
    curl -L -o $zip $geckourl
    tar -xzf $zip
    rm $zip
    mv geckodriver ~/VASTSYSTEEM/
}

menu
show_items
read -p "" choice
check_input
if [ $? -eq 0 ]; then
    valid_input
    if [[ $choice == 1 ]]; then
        download_chromedriver
        exit 0
    elif [[ $choice == 2 ]]; then
        download_geckodriver
        exit 0
    elif [[ $choice == 3 ]]; then
        download_chromedriver
        download_geckodriver
        exit 0
    elif [[ $choice == 9 ]]; then
        echo "Quiting"
        exit 0
    fi
else
    invalid_input
fi