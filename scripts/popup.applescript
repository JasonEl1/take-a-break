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

    set response to display dialog "How productive were you since the last break? (1-10)" with title "optional" default answer "" buttons {"Close"} default button "Close"
    set productivity_score to -1
    try
        set productivity_score to text returned of response as number
    on error

    end try

    if productivity_score is not equal to -1 and productivity_score is greater than 0 and productivity_score is less than 11 then
        set date_time to do shell script "date +'%Y-%m-%d %H:%M'"
        do shell script "echo " & ((date_time) & "," & productivity_score) & " >> " & folder_path & "/productivity.log"
    end if
end run
