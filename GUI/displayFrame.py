from   tkinter  import ttk
import tkinter  as tk

class DisplayFrame(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        textLabel = ttk.Label(self, text="Text2:")
        textLabel.grid(row=0, column=0, sticky="nsew")