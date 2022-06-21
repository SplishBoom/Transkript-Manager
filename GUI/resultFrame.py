from    tkinter     import  ttk
import  tkinter     as      tk
import  json

class ResultFrame(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.configure(bg="white", relief="sunken", borderwidth=1)

        for i in range(3) :
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

        """self.root.totalCreditInfo
        self.root.totalSuccessfulCreditInfo
        self.root.cpgaInfo"""

        """totalCreditInfo = tk.Label(self, textvariable=self.root.displaySection.totalCreditInfo,bg="white", font=("Helvetica", 12))
        succesfullCreditInfo = tk.Label(self, textvariable=self.root.displaySection.totalSuccessfulCreditInfo,bg="white", font=("Helvetica", 12))
        cpgaInfo = tk.Label(self, textvariable=self.root.displaySection.cpgaInfo,bg="white", font=("Helvetica", 12))

        totalCreditInfo.grid(row=0, column=0, sticky="nsew")
        succesfullCreditInfo.grid(row=0, column=1, sticky="nsew")
        cpgaInfo.grid(row=0, column=2, sticky="nsew")"""
