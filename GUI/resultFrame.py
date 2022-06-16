from    tkinter     import  ANCHOR, ttk
import  tkinter     as      tk

class ResultFrame(tk.Frame) :
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.configure(bg="white", relief="sunken", borderwidth=1)