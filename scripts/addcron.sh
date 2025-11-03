#!/bin/bash
# called with folder path, mode, time

crontab -l | grep -v "reminder.py" | crontab -

time="$3"
mins=$(date +%M)
mins=$((10#${mins}))
hours=$(date +%H)
hours=$((10#${hours}))

hours=$(( $hours + $(( $time / 60 ))))
mins=$(( $mins + $(( $time % 60 )) ))

if [ "$mins" -gt 60 ]; then
    mins=$((mins - 60))
    hours=$((hours + 1))
fi

if [ "$hours" -gt 24 ]; then
  hours=$((hours - 24))
fi

if [ "$2" == "set" ]; then
    (crontab -l; echo "$mins $hours * * * "$1"reminder.py reminder") | crontab -
fi

if [ "$2" == "unset" ]; then
    (crontab -l | grep -v -F "reminder") | crontab -
fi
