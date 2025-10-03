#!/bin/bash
# called with folder path, mode, time

crontab -l | grep -v "reminder.py" | crontab -

time="$3"
mins=$(date +%M)
mins=$((10#${mins}))

next=$(( $time + $mins ))
if [ "$next" -gt 59 ]; then
    next=$(( $next - 60 ))
fi

if [ "$2" == "set" ]; then

    (crontab -l; echo "$next * * * * "$1"reminder.py reminder") | crontab -
fi

if [ "$2" == "unset" ]; then
    (crontab -l | grep -v -F "reminder") | crontab -
fi
