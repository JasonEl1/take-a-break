#!/usr/bin/python3

VERSION = "v0.12.1"

DEFAULT_TIME="20"
DEFAULT_MESSAGE="Take a break to be more productive!"

import argparse
import os
import subprocess
import datetime
import platform
from pathlib import Path

fullpath = os.path.abspath(__file__)
name_len = len(os.path.basename(__file__))
fullpath = fullpath[:-name_len]

workmode_path = f"{fullpath}/workmode.txt"
addcron_path = f"{fullpath}/scripts/addcron.sh"
sound_path = f"{fullpath}/sound.wav"
applescript_path = f"{fullpath}/scripts/popup.scpt"
uninstall_path = f"{fullpath}/scripts/uninstall.sh"
message_path = f"{fullpath}/message.txt"
productivity_log_path = f"{fullpath}/productivity.log"

parser = argparse.ArgumentParser(prog="work",epilog=f"take-a-break {VERSION}")
parser.add_argument("action",help="action to execute")
parser.add_argument("-t","--time",default=DEFAULT_TIME,help="(optional) reminder time interval")
parser.add_argument("-m","--message",default="",help="(optional) change reminder message. Usage: work message -m {message}")
args = parser.parse_args()

def read_work_mode():
    if os.path.exists(workmode_path):
        with open(workmode_path,"r") as file_read:
            mode = file_read.readlines()[0].split()
            file_read.close()
            return mode[0]
    else:
        file_write = open(workmode_path, 'a')
        file_write.write("unset")
        file_write.close()
        return "unset"

def read_work_delay():
    if os.path.exists(workmode_path):
        with open(workmode_path,"r") as file_read:
            mode = file_read.readlines()[0].split()
            file_read.close()
            if(mode[0]=="set"):
                return mode[1]
    else:
        file_write = open(workmode_path, 'a')
        file_write.write(f"set {DEFAULT_TIME}")
        file_write.close()
        return DEFAULT_TIME

def write_work_mode(mode,time=DEFAULT_TIME):
    change_mode(mode,time)
    subprocess.call([addcron_path,fullpath,mode,time])
    print(f"{mode} work mode")

def change_message(mode,message=DEFAULT_MESSAGE):
    path = Path(message_path)
    if(mode == "set"):
        path.write_text(message)
    elif(mode == "get"):
        print(f"Current message is: {path.read_text().strip('\n')}")

def change_mode(mode,time=DEFAULT_TIME):
    path = Path(workmode_path)
    path.write_text(f"{mode} {time}")

def check_next():
    current_crontab = subprocess.check_output(['crontab','-l'])
    current_crontab = current_crontab.decode('utf-8')
    correct_entry = ""
    for line in current_crontab.splitlines():
        if "reminder.py" in line:
            correct_entry = line
            break
    if(correct_entry!=""):
        current_time = datetime.datetime.now()
        current_mins = current_time.minute
        current_hour = current_time.hour
        correct_entry = correct_entry.split()
        reminder_mins = int(correct_entry[0])
        reminder_hour = int(correct_entry[1])

        if(reminder_hour>=current_hour):
            hours_to_next=reminder_hour-current_hour
        else:
            hours_to_next=24-current_hour+reminder_hour

        if(reminder_mins>=current_mins):
            mins_to_next=reminder_mins-current_mins
        else:
            mins_to_next=60-current_mins+reminder_mins
            hours_to_next-=1

        return 60*hours_to_next + mins_to_next
    return -1

if(args.action == "get"):
    current_mode = read_work_mode()
    if(check_next() == -1 and current_mode == "set"):
        current_mode = "unset"
        write_work_mode("unset")
    print(f"current mode is {current_mode}")
elif(args.action == "set"):
    if read_work_mode() == "unset":
        if args.time != "-1":
            time = args.time

            write_work_mode("set",time)
        else:
            write_work_mode("set",DEFAULT_TIME)
    else:
        print("work mode already set")
elif(args.action == "unset"):
    if read_work_mode() == "set":
        write_work_mode("unset",DEFAULT_TIME)
    else:
        print("work mode already unset")
elif(args.action == "next"):
    next = check_next()
    if(next!=-1):
        print(f"next reminder is in {next} minutes")
    else:
        print("enable work mode to check next reminder")
elif(args.action == "message"):
    message=args.message
    action="set"
    if(args.message == "default"):
        message=DEFAULT_MESSAGE
    elif(args.message == ""):
        action="get"
    change_message(action,message)
    if(action=="set"):
        print(f"Set message to: \"{message}\"")
elif(args.action == "log"):
    subprocess.run(["cat",productivity_log_path])
elif(args.action == "reminder"):
    if read_work_mode() == "set":
        os_type = platform.system()
        if os_type == "Darwin":
            process = subprocess.Popen(['afplay',sound_path])
            subprocess.run(["osascript", applescript_path,fullpath,read_work_delay()])
        elif os_type == "Linux":
            process = subprocess.Popen(['aplay',sound_path])

            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.title("Break Reminder")
            messagebox.showinfo("Reminder", "Reminder to take a break!")
            root.mainloop()
        elif os_type == "Windows":
            import winsound
            winsound.PlaySound(sound_path, winsound.SND_ASYNC)

            import tkinter as tk
            from tkinter import messagebox

            root = tk.Tk()
            root.title("Break Reminder")
            messagebox.showinfo("Reminder", "Reminder to take a break!")
            root.mainloop()

        else:
            print("warning : your operating system is not yet supported for the sound feature")
elif(args.action=="uninstall"):
    subprocess.call([uninstall_path])
else:
    print("unknown command, please try again")
    exit()
