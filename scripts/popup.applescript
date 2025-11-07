on run args
    set folder_path to item 1 of args
    set time_delay to item 2 of args

    set message_path to (POSIX file (folder_path & "message.txt"))
    set break_message to read file message_path

    set pressed to display alert "Break Reminder" message break_message buttons {"Close", "Restart"} default button "Restart"
    set button to button returned of pressed

    do shell script "sh " & folder_path & "/scripts/addcron.sh " & folder_path & " unset 20"

    if button is "Restart" then
        do shell script "sh " & folder_path & "/scripts/addcron.sh " & folder_path & " set " & time_delay
    else
        do shell script "sh " & folder_path & "/scripts/change_mode.sh " & folder_path & " unset 20"
    end if

end run
