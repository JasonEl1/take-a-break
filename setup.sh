#!/bin/sh

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

sudo cp work /usr/local/bin/work

echo "take-a-break has been installed. Uninstall with the command 'work uninstall'"
echo "Would you like to delete this folder as well? [y/n]"
read delete_original_dir

if [ $delete_original_dir = "y" ]; then
    cd ..
    rm -rf ./take-a-break
    echo "take-a-break directory deleted"
fi
