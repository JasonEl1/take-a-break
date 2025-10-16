#!/bin/sh

echo "What alias do you use for take-a-break?: "
read aliasname

sed -i.bak "/alias ${aliasname}/d" ~/.zshrc

source ~/.zshrc

echo "Removed alias ${aliasname}."

folder_name=$(basename $(pwd))

echo "Delete ${folder_name} folder as well? [y/n]."
read delete_folder

if [ ${delete_folder} == "y" ]; then
  cd ..
  echo "rm -rf ${folder_name}"
fi
