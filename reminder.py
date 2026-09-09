#!/usr/bin/python3

VERSION = "v0.17.0"

import argparse
import os
import subprocess
import datetime
import platform
from pathlib import Path
import json
import random

fullpath = os.path.abspath(__file__)
name_len = len(os.path.basename(__file__))
fullpath = fullpath[:-name_len]

workmode_path = f"{fullpath}/workmode.txt"
addcron_path = f"{fullpath}/scripts/addcron.sh"
sound_path = f"{fullpath}/sound.wav"
applescript_path = f"{fullpath}/scripts/popup.scpt"
linux_popup_path = f"{fullpath}/scripts/popup_linux.sh"
uninstall_path = f"{fullpath}/scripts/uninstall.sh"
message_path = f"{fullpath}/message.txt"
productivity_log_path = f"{fullpath}/productivity.log"
settings_path = f"{fullpath}/settings.json"

settings = json.loads(Path(settings_path).read_text())

DEFAULT_TIME=settings["DEFAULT_TIME"]

parser = argparse.ArgumentParser(prog="work",epilog=f"take-a-break {VERSION}")

subparsers = parser.add_subparsers(dest="action", required=True, description="action commands")

get_parser = subparsers.add_parser("get", help="get the current mode")

set_parser = subparsers.add_parser("set", help="set mode to work mode")
set_parser.add_argument("-t", "--time", default=DEFAULT_TIME, help="custom time interval")
set_parser.add_argument("-m", "--message", default="", help="shortcut way to change message when setting work mode")

unset_parser = subparsers.add_parser("unset", help="unset work mode")

next_parser = subparsers.add_parser("next", help="check how long until next reminder")

log_parser = subparsers.add_parser("log", help="view statistics from producrtivity log")

message_parser = subparsers.add_parser("message", help="check or set current reminder message")
message_parser.add_argument("-m", "--message", default="",help="set a new custom reminder message")
message_parser.add_argument("-p", "--preset", default="", help="save message as a preset with a custom name")
message_parser.add_argument("-rmp", "--remove-preset",default="",help="remove a message preset")
message_parser.add_argument("-l","--list",action="store_true",help="list saved message presets")

subparsers.add_parser("reminder")

settings_parser = subparsers.add_parser("settings", help="view or edit settings")
settings_parser.add_argument("-e","--edit",nargs=2,metavar=('INDEX','VALUE'),default=("",""),help="which settings parameter to edit and the new value to assign")

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
        return "-1"
    else:
        file_write = open(workmode_path, 'a')
        file_write.write(f"set {DEFAULT_TIME}")
        file_write.close()
        return str(DEFAULT_TIME)

def write_work_mode(mode,time=DEFAULT_TIME):
    change_mode(mode,time)
    subprocess.call(['sh',addcron_path,fullpath,mode,time])
    if(mode == "set"):
        print(f"set work mode with interval {time} minutes")
    # important: call write_work_mode("unset", time) with time!=DEFAULT_TIME to hide unset output
    elif(mode == "unset" and time==DEFAULT_TIME):
        print(f"unset work mode")

def change_message(mode,message):
    path = Path(message_path)
    if(mode == "set"):
        path.write_text(message)
    elif(mode == "get"):
        current_message = path.read_text().strip('\n')
        print(f"Current message is: {current_message}")

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

def save_settings():
    try:
        with open(settings_path, 'w', encoding='utf-8') as settings_file:
            json.dump(settings, settings_file, ensure_ascii=False, indent=4)
        settings_file.close()
    except:
        print("failed to save settings")
        exit()

if(args.action == "get"):
    current_delay = read_work_delay()
    current_mode = read_work_mode()
    next = check_next()
    if((next == -1 and current_mode == "set") or (int(current_delay) > next)):
        current_mode = "unset"
        write_work_mode("unset","-1")
        current_mode = "unset"
    print(f"current mode is {current_mode}")
elif(args.action == "set"):
    already_set = False
    if(read_work_mode() == "set"):
        next = check_next()
        if(next!=-1 and int(next) <= int(read_work_delay())):
            print("work mode already set")
            already_set = True

    if already_set == False:
        if(args.time != "-1"):
            time = args.time
            try:
                time = int(time)
            except ValueError:
                print("invalid time argument - must be numeric")
                exit()
            write_work_mode("set",str(time))
            if(args.message != ""):
                change_message("set",args.message)
                print(f"set message to: {args.message}")
        else:
            write_work_mode("set",DEFAULT_TIME)
elif(args.action == "unset"):
    if read_work_mode() == "set":
        write_work_mode("unset",DEFAULT_TIME)
    else:
        print("work mode already unset")
elif(args.action == "next"):
    next = check_next()
    if(next!=-1 and int(next) <= int(read_work_delay())):
        print(f"next reminder is in {next} minutes")
    elif(int(next) > int(read_work_delay())):
        write_work_mode("unset","-1")
        print("enable work mode to check next reminder")
    else:
        print("enable work mode to check next reminder")
elif(args.action == "message"):
    message=args.message
    preset = args.preset
    action="set"
    if(message == ""):
        remove_preset = args.remove_preset
        if(remove_preset != ""):
            if(remove_preset in settings["MESSAGE_PRESETS"]):
                settings["MESSAGE_PRESETS"].pop(remove_preset)

                save_settings()

                print(f"successfully removed message preset {remove_preset}")
            else:
                print("message preset does not exist")
            exit()
        elif(args.list):
            print("saved message presets:\n")
            for preset in list(settings["MESSAGE_PRESETS"].keys()):
                print(f"{preset} : {settings['MESSAGE_PRESETS'][preset]}")

            exit()
        else:
            action="get"

    if(message in settings["MESSAGE_PRESETS"]):
        message=settings["MESSAGE_PRESETS"][message]
        if(isinstance(message,list)):
            message=message[random.randint(0,len(message)-1)]

    change_message(action,message)
    if(action=="set"):
        print(f"set message to: \"{message}\"")
        if(preset != ""):
            if(preset not in settings["MESSAGE_PRESETS"]):
                settings["MESSAGE_PRESETS"][preset] = message
            elif(isinstance(settings["MESSAGE_PRESETS"][preset],list)):
                settings["MESSAGE_PRESETS"][preset].append(message)
            else:
                settings["MESSAGE_PRESETS"][preset] = [settings["MESSAGE_PRESETS"][preset],message]
            save_settings()

            print(f"added {preset} to message presets list")
elif(args.action == "log"):
    try:
        print("opening productivity.log")
        subprocess.run(["open",productivity_log_path])
    except:
        print("could not open productivity.log")
        print("attempting to list productivity.log here:")
        try:
            subprocess.run(["cat",productivity_log_path])
        except:
            print("could not list productivity.log")
elif(args.action == "settings"):
    if(args.edit == ("","")):
        settings_params = list(settings.keys())
        for param_no in range(len(settings_params)):
            if(settings_params[param_no] != "MESSAGE_PRESETS"): # MESSAGE_PRESETS are managed directly by message command
                print(f"[{param_no}] : {settings_params[param_no]} = {settings[settings_params[param_no]]}")

        param_editing = print(f"\ncall the settings command with the --edit flag and one of these numeric values, along with a new value to change a settings parameter.\n\nalternatively you can edit settings.json directly, located at {settings_path}")
        print(f"\ntake-a-break {VERSION}")
    else:
        index, value = args.edit
        try:
            index = int(index)
        except ValueError:
            print("invalid index, try running the settings command without any flags first")

        settings_keys = list(settings.keys())

        if(index < 0 or index >= len(settings_keys)):
            print("setting parameter index out of range, try running the settings command without any flags")
            exit()

        if(settings_keys[index] == "MESSAGE_PRESETS"):
            print("Please use the message command along with the --remove-preset flag to remove a message preset, or the --preset flag to add one.")
        else:
            settings[list(settings.keys())[index]] = value

            save_settings()
elif(args.action == "reminder"):
    if read_work_mode() == "set":
        if(not Path(productivity_log_path).exists()):
            Path(productivity_log_path).touch()
        PLAY_SOUND = False
        if(settings["REMINDER_AUDIO"] == "true"):
            PLAY_SOUND = True
        os_type = platform.system()
        if os_type == "Darwin":
            if(PLAY_SOUND):
                process = subprocess.Popen(['afplay',sound_path])
            subprocess.run(["osascript", applescript_path,fullpath,read_work_delay()])
        elif os_type == "Linux":
            if(PLAY_SOUND):
                process = subprocess.Popen(['aplay',sound_path])

            subprocess.run(["sh",linux_popup_path,fullpath,read_work_delay()])
        elif os_type == "Windows":
            if(PLAY_SOUND):
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
    print("unknown command, please try again or use -h / --help for a list of commands")
    exit()
