#!/usr/bin/python3
# v0.6.0

import argparse
import os
import subprocess
import datetime
import platform

fullpath = os.path.abspath(__file__)
name_len = len(os.path.basename(__file__))
fullpath = fullpath[:-name_len]

workmode_path = f"{fullpath}/workmode.txt"
addcron_path = f"{fullpath}/addcron.sh"
sound_path = f"{fullpath}/sound.wav"
applescript_path = f"{fullpath}/popup.scpt"

parser = argparse.ArgumentParser(prog="Take-A-Break v0.6.0")
parser.add_argument("action",help="action to execute")
parser.add_argument("-t","--time",default="30")
args = parser.parse_args()

def read_work_mode():
    if os.path.exists(workmode_path):
        with open(workmode_path,"r") as file_read:
            mode = file_read.readlines()[0]
            file_read.close()
            return mode
    else:
        file_write = open(workmode_path, 'a')
        file_write.write("unset")
        file_write.close()
        return "unset"

def write_work_mode(mode,time="30"):
    with open(workmode_path,"w") as file_write:
        file_write.write(mode)
        file_write.close()
        subprocess.call(['sh',addcron_path,mode,time,fullpath])
    print(f"{mode} work mode")

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

if(args.action == "get"):
    print(f"current mode is {read_work_mode()}")
elif(args.action == "set"):
    if read_work_mode() == "unset":
        if args.time != "-1":
            time = args.time

            write_work_mode("set",time)
        else:
            write_work_mode("set","30")
    else:
        print("work mode already set")
elif(args.action == "unset"):
    if read_work_mode() == "set":
        write_work_mode("unset","30")
    else:
        print("work mode already unset")
elif(args.action == "next"):
    try:
        next = check_next()
        print(f"next reminder is in {next} minutes.")
    except:
        print("please enable work mode to check next reminder")
elif(args.action == "update"):
    if read_work_mode() == "set":
        subprocess.call(['sh',addcron_path, 'unset',fullpath[:-1]])
        subprocess.call(['sh',addcron_path, 'set',fullpath[:-1]])
        next = check_next()
        print("updated... " + f"next reminder is in {next} minutes")
    else:
        print("please enable work mode to update")
elif(args.action == "reminder"):
    if read_work_mode() == "set":
        os_type = platform.system()
        process = None
        if os_type == "Darwin":
            process = subprocess.Popen(['afplay',sound_path])
            applescript = 'display alert "Break Reminder" message "Take a break and be more productive!" buttons {"Close", "Cancel"} default button "Close" cancel button "Cancel"'
            subprocess.run(["osascript","-e", applescript])
            process = subprocess.Popen(['aplay',sound_path])

            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.title("Break Reminder")
            messagebox.showinfo("Reminder", "Reminder to take a break!")
            root.mainloop()
        elif os_type == "Windows":
            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.title("Break Reminder")
            messagebox.showinfo("Reminder", "Reminder to take a break!")
            root.mainloop()

        else:
            print("warning : your operating system is not yet supported for the sound feature")
else:
    print("unknown command, please try again")
    exit()
