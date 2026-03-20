#!/bin/bash
# called with folder path, mode, time

crontab -l | grep -v "reminder.py" | crontab -

if [ "$2" == "set" ]; then
    time="$3"
    mins=$(date +%M)
    mins=$((10#${mins}))
    hours=$(date +%H)
    hours=$((10#${hours}))

    hours=$(( $hours + $(( $time / 60 ))))
    mins=$(( $mins + $(( $time % 60 )) ))

    while [ "$mins" -gt 59 ]; do
        mins=$((mins - 60))
        hours=$((hours + 1))
    done

    while [ "$hours" -gt 23 ]; do
      hours=$((hours - 24))
    done
    (crontab -l; echo "$mins $hours * * * "$1"reminder.py reminder") | crontab -
fi

if [ "$2" == "unset" ]; then
    (crontab -l | grep -v -F "reminder") | crontab -
fi
