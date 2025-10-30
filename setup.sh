#!/bin/sh

mkdir ~/.local/share/take-a-break
cp reminder.py ~/.local/share/take-a-break/reminder.py
touch workmode.txt
echo "unset" > workmode.txt
cp workmode.txt ~/.local/share/take-a-break/workmode.txt
cp sound.wav ~/.local/share/take-a-break/sound.wav
cp -r ./scripts ~/.local/share/take-a-break/scripts
cp uninstall.sh ~/.local/share/take-a-break/uninstall.sh

sudo cp work /usr/local/bin/work
