#!/usr/bin/python3
# v0.5.2

import sys
import tkinter as tk
import subprocess
import os
import datetime

fullpath = os.path.abspath(__file__)
name_len = len(os.path.basename(__file__))
fullpath = fullpath[:-name_len]

workmode_path = f"{fullpath}/workmode.txt"
addcron_path = f"{fullpath}/scripts/addcron.sh"
sound_path = f"{fullpath}/sound.wav"

def write_work_mode(mode):
    with open(workmode_path,"w") as file_write:
        file_write.write(mode)
        file_write.close()
        subprocess.call(['sh',addcron_path,mode,fullpath[:-1]])
    print(f"{mode} work mode")

def read_work_mode():
    if os.path.exists(workmode_path):
        with open(workmode_path,"r") as file_read:
            mode = file_read.readlines()[0]
            return mode
            file_read.close()
    else:
        file_write = open(workmode_path, 'a')
        file_write.write("unset")
        file_write.close()
        return "unset"

def check_next():
    current_crontab = subprocess.check_output(['crontab','-l'])
    current_crontab = current_crontab.decode('utf-8')
    correct_entry = ""
    for line in current_crontab.splitlines():
        if "reminder.py" in line:
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
        print("error...")

arg_count = len(sys.argv)
if arg_count>1:
    if sys.argv[1] == "set":
        if read_work_mode() == "unset":
            write_work_mode("set")
        else:
            print("work mode already set")
    elif sys.argv[1] == "unset":
        if read_work_mode() == "set":
            write_work_mode("unset")
        else:
            print("work mode already unset")
    elif sys.argv[1] == "get":
        print(f"current mode is {read_work_mode()}")
    elif sys.argv[1] == "next":
        try:
            next = check_next()
            print(f"next reminder is in {next} minutes.")
        except:
            print("please enable work mode to check next reminder")
    elif sys.argv[1] == "update":
        if read_work_mode() == "set":
            subprocess.call(['sh',addcron_path, 'unset',fullpath[:-1]])
            subprocess.call(['sh',addcron_path, 'set',fullpath[:-1]])
            next = check_next()
            print("updated... " + f"next reminder is in {next} minutes")
        else:
            print("please enable work mode to update")
    else:
        print("unknown command, please try again")
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
            print("warning : your operating system is not yet supported for the sound feature")
        root = tk.Tk()
        root.geometry("400x100")
        root.attributes("-topmost", True)
        root.eval('tk::PlaceWindow . center')
        root.title("TAKE A BREAK!")
        label = tk.Label(root, text="Take a break!")
        label.pack()
        root.mainloop()
        if process:
            process.terminate()
