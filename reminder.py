#!/usr/bin/python3
# v0.3.0

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
    first_time = correct_entry.split(',')[0]
    first_time = int(first_time)
    second_time = correct_entry.split(',')[1]
    second_time = int(second_time)
    if current_time > first_time and current_time > second_time:
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
        print("set work mode")
        with open(workmode_path,"w") as file_write:
            file_write.write("set")
            file_write.close()
            subprocess.call(['sh',addcron_path,'set',temppath[:-1]])
    elif sys.argv[1] == "unset":
        print("unset work mode")
        with open(workmode_path,"w") as file_write:
            file_write.write("unset")
            file_write.close()
            subprocess.call(['sh',addcron_path,'unset',temppath[:-1]])
    elif sys.argv[1] == "get":
        with open(workmode_path,"r") as file_read:
            print(f"current work mode: {file_read.readlines()[0]}")
            file_read.close()
    elif sys.argv[1] == "next":
        try:
            next = check_next()
            print(f"Next reminder is in {next} minutes.")
        except:
            print("Please enable work mode to check next reminder")
    elif sys.argv[1] == "update":
        mode = ""
        with open(workmode_path,"r") as file_read:
            mode = file_read.readlines()[0]
        if mode == "set":
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
    mode = ""
    with open(workmode_path,"r") as file_read:
        mode = file_read.readlines()[0]
        if mode == "set":
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
