#!/bin/zsh

echo "What name would you like to give this alias? (enter 'none' to skip): "
read aliasname

new_entry="alias ${aliasname}='python3 $(pwd)/reminder.py'"

if grep -q "$new_entry" ~/.zshrc; then
    echo "alias already exists"
elif [ "$aliasname" = "none" ]; then
    echo "skipped alias creation"
else
    echo "$new_entry" >> ~/.zshrc
    echo "created alias ${aliasname} in ~/.zshrc"
    source ~/.zshrc
    exit
fi
