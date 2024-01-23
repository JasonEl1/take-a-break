#!/bin/bash

crontab -l | grep -v "reminder.py" | crontab -

mins=$(date +%M)
opp_mins=0

if [ $mins -lt 30 ]; then
    opp_mins=$(($mins+30))
else
    opp_mins=$(($mins-30))
fi


if [ $1 == "set" ]; then
    crontab -l | { cat; echo "$mins,$opp_mins * * * * cd downloads && /usr/bin/python3 /Users/jasonelisei/Downloads/reminder.py"; } | crontab -
fi
