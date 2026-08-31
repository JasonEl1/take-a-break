#!/bin/sh

echo "Installing take-a-break..."

echo "Will install executable in /usr/local/bin. Continue (y) or enter a custom location (n):"
read custom_install_yn

if [ $custom_install_yn = "y" ]; then

    echo "Copying executable to /usr/local/bin/work..."
    sudo cp work /usr/local/bin/work
else
    if [ $custom_install_yn = "n" ]; then
        echo "Enter custom install directory: "
        read custom_install_location
        if [ ! -d "$custom_install_location" ]; then
            echo "Directory ($custom_install_location) does not exist! Please run this script again."
            exit 1
        fi
        echo "Copying executable to $custom_install_location/work"
        cp work "$custom_install_location"/work || sudo cp work "$custom_install_location"/work
    fi
fi

echo "Copying program files to ~/.local/share/take-a-break..."
rm screenshot.png
mkdir ~/.local/share/take-a-break
cp reminder.py ~/.local/share/take-a-break/reminder.py
touch workmode.txt
echo "unset" > workmode.txt
cp workmode.txt ~/.local/share/take-a-break/workmode.txt
cp sound.wav ~/.local/share/take-a-break/sound.wav
cp -r ./scripts ~/.local/share/take-a-break/scripts
cp uninstall.sh ~/.local/share/take-a-break/uninstall.sh
touch message.txt
echo "Take a break and be more productive!" > message.txt
cp message.txt ~/.local/share/take-a-break/message.txt
touch productivity.log
cp productivity.log ~/.local/share/take-a-break/productivity.log
cp settings.json ~/.local/share/take-a-break/settings.json

echo "take-a-break has been installed. Uninstall with the command 'work uninstall'"
echo "Would you like to delete this folder as well? [y/n]"
read delete_original_dir

if [ $delete_original_dir = "y" ]; then
    cd ..
    rm -rf ./take-a-break
    echo "take-a-break directory deleted"
fi

echo "skipping directory deletion"
