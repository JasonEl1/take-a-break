#!/usr/bin/python3
# v0.4.0

import sys
import tkinter as tk
import subprocess
import os
import datetime

fullpath = os.path.abspath(__file__)
name_len = len(os.path.basename(__file__))
temppath = fullpath[:-name_len]

workmode_path = f"{temppath}/workmode.txt"
addcron_path = f"{temppath}/addcron.sh"
sound_path = f"{temppath}/sound.wav"

def write_work_mode(mode):
    with open(workmode_path,"w") as file_write:
        file_write.write(mode)
        file_write.close()
        subprocess.call(['sh',addcron_path,mode,temppath[:-1]])
    print(f"{mode} work mode")

def read_work_mode():
    with open(workmode_path,"r") as file_read:
        mode = file_read.readlines()[0]
        return mode
        file_read.close()

def check_next():
    current_crontab = subprocess.check_output(['crontab','-l'])
    current_crontab = current_crontab.decode('utf-8')
    correct_entry = ""
    for line in current_crontab.splitlines():
        if line.endswith("reminder.py"):
            correct_entry = line
            break
    current_time = datetime.datetime.now()
    current_time = current_time.minute
    correct_entry = correct_entry.split()[0]
    first_time = int(correct_entry.split(',')[0])
    second_time = int(correct_entry.split(',')[1])

    if current_time > first_time and current_time >= second_time:
        return 60 - current_time + first_time
    elif current_time >= first_time and current_time < second_time:
        return second_time - current_time
    elif current_time <= first_time and current_time < second_time:
        return first_time - current_time
    else:
        print("Logical error...")

arg_count = len(sys.argv)
if arg_count>1:
    if sys.argv[1] == "set":
        write_work_mode("set")
    elif sys.argv[1] == "unset":
        write_work_mode("unset")
    elif sys.argv[1] == "get":
        print(f"Current mode is {read_work_mode()}")
    elif sys.argv[1] == "next":
        try:
            next = check_next()
            print(f"Next reminder is in {next} minutes.")
        except:
            print("Please enable work mode to check next reminder")
    elif sys.argv[1] == "update":
        if read_work_mode() == "set":
            subprocess.call(['sh',addcron_path, 'unset',temppath[:-1]])
            subprocess.call(['sh',addcron_path, 'set',temppath[:-1]])
            next = check_next()
            print(f"Updated. Next reminder is in {next} minutes.")
        else:
            print("Please enable work mode to update")
    else:
        print("Unknown command, please try again")
        exit()
else:
    if read_work_mode() == "set":
        os_type = subprocess.check_output(['uname'])
        os_type = os_type.decode('utf-8').strip("\n")
        process = None
        if os_type == "Darwin":
            process = subprocess.Popen(['afplay',sound_path])
        elif os_type == "Linux":
            process = subprocess.Popen(['aplay',sound_path])
        else:
            print("Your OS is not yet supported.")
        root = tk.Tk()
        root.geometry("400x100")
        root.attributes("-topmost", True)
        root.eval('tk::PlaceWindow . center')
        root.title("TAKE A BREAK!")
        root.mainloop()
        if process:
            process.terminate()
