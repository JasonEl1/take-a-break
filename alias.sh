#!/bin/zsh

read -p "What name would you like to give this alias?: " aliasname

new_entry="alias ${aliasname}='python3 $(pwd)/reminder.py'"

if grep -q "$new_entry" ~/.zshrc; then
    echo "alias already exists"
else
    echo "$new_entry" >> ~/.zshrc
    echo "created alias ${aliasname} in ~/.zshrc"
    source ~/.zshrc
    exit
fi
