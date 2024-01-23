#!/usr/bin/python3

import sys
import tkinter as tk

arg_count = len(sys.argv)
if arg_count>1:
    if sys.argv[1] == "set":
        print("set work mode")
        with open("workmode.txt","w") as file_write:
            file_write.write("set")
            file_write.close()
            #should add offset so that 30 min reminders don't just happen at :30 and :00, but rather 30 minutes and 1 hour after the original command was run.
    elif sys.argv[1] == "unset":
        print("unset work mode")
        with open("workmode.txt","w") as file_write:
            file_write.write("unset")
            file_write.close()
    elif sys.argv[1] == "get":
        print("current work mode: ")
        with open("workmode.txt","r") as file_read:
            print(file_read.readlines()[0])
            file_read.close()
else:
    mode = ""
    with open("workmode.txt","r") as file_read:
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
