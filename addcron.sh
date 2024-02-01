#!/bin/bash

crontab -l | grep -v "reminder.py" | crontab -

mins=$(date +%M)
opp_mins=0

if [ $mins -lt 30 ]; then
    opp_mins=$(($mins+30))
else
    opp_mins=$(($mins-30))
fi

first=0
second=0

if [ $mins -lt $opp_mins ]; then
    first=$mins
    second=$opp_mins
else
    first=$opp_mins
    second=$mins
fi


if [ $1 == "set" ]; then
    crontab -l | { cat; echo "$first,$second * * * * cd $2 && source ./venv/bin/activate && /usr/bin/python3 reminder.py"; } | crontab -
fi
