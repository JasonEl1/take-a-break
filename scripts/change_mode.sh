#!/bin/bash
# $1 is folder name, $2 is mode, $3 is time
folder_name=$1

echo "$2 $3" > "$folder_name"/workmode.txt
