echo "Are you sure you want to uninstall take-a-break? [y/n]"
read confirmation

if [ $confirmation = "y" ]; then
    rm -rf ~/.local/share/take-a-break
    sudo rm /usr/local/bin/work
    echo "take-a-break has been uninstalled."
else
    echo "cancelling uninstallation."
fi
