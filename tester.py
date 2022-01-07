import tkinter as tk
import speedtest
import csv
import time
import threading
import math
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

interval = 10
# How often to test in minutes

duration = 10
# How long to test for in hours

iterations = (duration*60)//interval

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def set_interval():
    interval_current_label.config( text = "Current: " + interval_clicked.get())
    global interval
    interval = int(interval_clicked.get())

def set_duration():
    duration_current_label.config( text = "Current: " + duration_clicked.get())
    global duration
    duration = int(duration_clicked.get())

def graph():
    #load
    data = pd.read_csv('Speedtest.csv')

    #plot
    plt.figure(figsize=(6.8,4.2))
    plt.plot(data['Time'],data['Download'], label="Download")
    plt.plot(data['Time'],data['Upload'], label="Upload")
    plt.xlabel('Time')
    plt.ylabel('Speed Mbit/s')
    plt.legend(loc=1)
    plt.title('Internet Speed vs Time')
    
    plt.show()

def execute_test():

    flag.config( text = "Running \n Exit to cancel")

    execute_button.config(state="disabled")
    
    s = speedtest.Speedtest()

    file = pathlib.Path("speedtest.csv")

    if file.exists():
        with open('Speedtest.csv','r') as f:
            reader = csv.reader(f)
            first_line = next(reader)

        if(first_line != ['Date', 'Time', 'Download', 'Upload']):   
            with open('Speedtest.csv','w',newline='') as f:
                writer = csv.writer(f,  escapechar=' ', quoting=csv.QUOTE_NONE)

                entry = ["Date","Time","Download","Upload"]

                writer.writerow(entry)
    else:
        with open('Speedtest.csv','w',newline='') as f:
                writer = csv.writer(f,  escapechar=' ', quoting=csv.QUOTE_NONE)

                entry = ["Date","Time","Download","Upload"]

                writer.writerow(entry)

    for x in range(iterations):

        with open('Speedtest.csv','a+',newline='') as f:

            writer = csv.writer(f,  escapechar=' ', quoting=csv.QUOTE_NONE)   

            down = s.download(threads=1)/1000000
            up = s.upload(threads=1)/1000000

            current_speed.config( text = "D: " + str(truncate(down,2)) + "\nU: " + str(truncate(up,2)) )

            test_date = time.strftime('%m/%d/%Y', time.localtime())
            test_time = time.strftime('%H:%M:%S', time.localtime())
        
            entry = [test_date, test_time, down, up]

            writer.writerow(entry)
            print(x)

        time.sleep(interval*60)
        #test
        #time.sleep(1)

    flag.config( text = "")
    execute_button.config(state="normal")

def threaded_execute():
    execute_thread = threading.Thread(target=execute_test, name="Executer")
    execute_thread.start()

#TK GUI SETUP
root = tk.Tk()
root.title("Speed Test Logger")

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=4, rowspan=4)

title = tk.Label(root, text="Speed Test Logger", font="Raleway")
title.grid(column=1,row=0)

#INTERVAL

interval_label = tk.Label(root,text="Interval time(minutes): ", font="Raleway")
interval_label.grid(column=0,row=1)

interval_options = ["1", "10", "20", "30"]

interval_clicked = tk.StringVar()
interval_clicked.set("10")

interval_drop = tk.OptionMenu(root, interval_clicked, *interval_options)
interval_drop.grid(column=1, row=1)

interval_button = tk.Button(root, text="Set", command = set_interval)
interval_button.grid(column=2,row=1)

interval_current_label = tk.Label( root, text = "Current: " + interval_clicked.get() )
interval_current_label.grid(column=3, row=1)

#DURATION

duration_label = tk.Label(root,text="Duration time(hours): ", font="Raleway")
duration_label.grid(column=0,row=2)

duration_options = ["1", "5", "10", "15", "20"]

duration_clicked = tk.StringVar()
duration_clicked.set("10")

duration_drop = tk.OptionMenu(root, duration_clicked, *duration_options)
duration_drop.grid(column=1, row=2)

duration_button = tk.Button(root, text="Set", command = set_duration)
duration_button.grid(column=2,row=2)

duration_current_label = tk.Label(root, text = "Current: " + duration_clicked.get() )
duration_current_label.grid(column=3, row=2)

#EXECUTE

execute_button = tk.Button(root, text="Execute", command = threaded_execute, bg="light green", fg="white", activebackground="white")
execute_button.grid(column=1, row=3)

#GRAPH

graph_button = tk.Button(root, text="Graph", command = graph)
graph_button.grid(column=0, row=3)

#RUNNING

flag = tk.Label(root, text=" ", font="Raleway", fg="red")
flag.grid(column=2,row=3)

current_speed = tk.Label(root, text="", font="Raleway")
current_speed.grid(column=3,row=3)

root.mainloop()
