#!/usr/bin/python3

import sys
import tkinter as tk
import subprocess
import os

fullpath = os.path.abspath(__file__)
name_len = len(os.path.basename(__file__))
temppath = fullpath[:-name_len]

workmode_path = f"{temppath}/workmode.txt"
addcron_path = f"{temppath}/addcron.sh"

arg_count = len(sys.argv)
if arg_count>1:
    if sys.argv[1] == "set":
        print("set work mode")
        with open(workmode_path,"w") as file_write:
            file_write.write("set")
            file_write.close()
            subprocess.call(['sh',addcron_path,'set'])
    elif sys.argv[1] == "unset":
        print("unset work mode")
        with open(workmode_path,"w") as file_write:
            file_write.write("unset")
            file_write.close()
            subprocess.call(['sh',addcron_path,'unset'])
    elif sys.argv[1] == "get":
        print("current work mode: ")
        with open(workmode_path,"r") as file_read:
            print(file_read.readlines()[0])
            file_read.close()
else:
    mode = ""
    with open(workmode_path,"r") as file_read:
        mode = file_read.readlines()[0]
        if mode == "set":
            window = tk.Tk()
            window.geometry("400x400")
            window.attributes("-topmost", True)
            window.eval('tk::PlaceWindow . center')
            window.title("TAKE A BREAK!")
            reminder = tk.Label(window,text="Reminder")
            reminder.pack()
            window.mainloop()
