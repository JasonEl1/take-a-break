#!/bin/bash

FOLDER_PATH="$1"
TIME_DELAY="$2"

MESSAGE_PATH="${FOLDER_PATH}/message.txt"
if [ -f "$MESSAGE_PATH" ]; then
    BREAK_MESSAGE=$(cat "$MESSAGE_PATH")
fi

BUTTON=$(zenity --question \
    --title="Break Reminder" \
    --text="$BREAK_MESSAGE" \
    --cancel-label="Unset" \
    --ok-label="Restart")


if [ "$BUTTON" = "Unset" ]; then
    BUTTON_PRESSED="Unset"
elif [ $? -eq 0 ]; then
    BUTTON_PRESSED="Restart"
fi


if [ "$BUTTON_PRESSED" = "Restart" ]; then
    sh "${FOLDER_PATH}/scripts/addcron.sh" "$FOLDER_PATH" "set" "$TIME_DELAY"
else
    sh "${FOLDER_PATH}/scripts/change_mode.sh" "$FOLDER_PATH" "unset" "20"
fi

PRODUCTIVITY_SCORE=$(zenity --entry \
    --title="optional" \
    --text="How productive were you since the last break? (1-10)" \
    --entry-text="")

if [ -z "$PRODUCTIVITY_SCORE" ]; then
    PRODUCTIVITY_SCORE=-1
fi

if [ $productivity_score -ne -1 ] && [ $productivity_score -gt 0 ] && [ $productivity_score -lt 11]; then
    date_time=$(date +'%Y-%m-%d %H:%M')
    echo "$date_time,$productivity_score" >> "$folder_path"/productivity.log
fi