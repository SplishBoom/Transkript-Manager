import tkinter as tk
from tkinter import ttk


cursors = ["arrow", "circle", "clock", "cross", "dotbox", "exchange", "fleur", "heart", "heart", "man", "mouse", "pirate", "plus", "shuttle", "sizing", "spider", "spraycan", "star", "target", "tcross", "trek", "watch"]


apppp = tk.Tk()

for cursor in cursors :

    label = ttk.Label(apppp, text=cursor, cursor=cursor, font=("Segoe UI", 14, "bold"), foreground="black")
    label.pack(fill="both", expand=True)

apppp.mainloop()
