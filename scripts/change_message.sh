#!/bin/bash
#$1 is message.txt location, $2 is message string, $3 is action (get/set)

if [ "$3" == "set" ]; then
  echo $2 > $1
elif [ "$3" == "get" ]; then
  echo "Current message is: \"$(cat $1)\""
fi
