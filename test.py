from tkinter import *
import time
import os
import threading

root = Tk()

frameCnt = 150
frames = [PhotoImage(file='Assets/loader.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(20, update, ind)

def loop():

        for i in range(280000) :
            print(i)

        return "anan"

def start(event) :
    root.after(0, update, 0)
    x = threading.Thread(target=loop).start()
    print("start", x)

label = Label(root)

label.pack()

root.bind('<Key>', start)

root.mainloop()