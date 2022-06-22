from    tkinter     import  ttk
import  tkinter     as      tk

class ResultFrame(tk.Frame):
    
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        for i in range(0, 5):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.createWidgets()

        self.gridWidgets()

        for label in self.winfo_children():
            label.grid_configure(padx=1, pady=1)

    def createWidgets(self) :
        font = ("Arial", 10, "bold")
        self.infoLabel1 = tk.Label(self, font=font, text="Attempted Credits")
        self.infoLabel2 = tk.Label(self, font=font, text="Successful Credits")
        self.infoLabel3 = tk.Label(self, font=font, text="Included Credits")
        self.infoLabel4 = tk.Label(self, font=font, text="Quality Points")
        self.infoLabel5 = tk.Label(self, font=font, text="CGPA")

        font = ("Arial", 15, "bold")
        self.creditsAttemptedInfo = ttk.Label(self, font=font, textvariable=self.root.displaySection.creditsAttemptedVar, anchor="center")
        self.creditsSuccesfullInfo = ttk.Label(self, font=font, textvariable=self.root.displaySection.creditsSuccesfullVar, anchor="center")
        self.creditsIncludedInCPGAInfo = ttk.Label(self, font=font, textvariable=self.root.displaySection.creditsIncludedInCPGAVar, anchor="center")
        self.totalQualityPointsInfo = ttk.Label(self, font=font, textvariable=self.root.displaySection.totalQualityPointsVar, anchor="center")
        self.CGPAInfo = ttk.Label(self, font=font, textvariable=self.root.displaySection.CGPAVar, anchor="center")

        self.root.displaySection.CGPAVar.trace("w", self.awareChanges)

    def gridWidgets(self) :
        self.infoLabel1.grid(row=0, column=0, sticky="WE")
        self.infoLabel2.grid(row=0, column=1, sticky="WE")
        self.infoLabel3.grid(row=0, column=2, sticky="WE")
        self.infoLabel4.grid(row=0, column=3, sticky="WE")
        self.infoLabel5.grid(row=0, column=4, sticky="WE")

        self.creditsAttemptedInfo.grid(row=1, column=0, sticky="WE")
        self.creditsSuccesfullInfo.grid(row=1, column=1, sticky="WE")
        self.creditsIncludedInCPGAInfo.grid(row=1, column=2, sticky="WE")
        self.totalQualityPointsInfo.grid(row=1, column=3, sticky="WE")
        self.CGPAInfo.grid(row=1, column=4, sticky="WE")

    def awareChanges(self, *event) :
        self.creditsAttemptedInfo.configure(foreground=self.colorize(self.root.displaySection.creditsAttemptedVar.get().split()))
        self.creditsSuccesfullInfo.configure(foreground=self.colorize(self.root.displaySection.creditsSuccesfullVar.get().split()))
        self.creditsIncludedInCPGAInfo.configure(foreground=self.colorize(self.root.displaySection.creditsIncludedInCPGAVar.get().split()))
        self.totalQualityPointsInfo.configure(foreground=self.colorize(self.root.displaySection.totalQualityPointsVar.get().split()))
        self.CGPAInfo.configure(foreground=self.colorize(self.root.displaySection.CGPAVar.get().split()))

    def colorize(self, splitedVar) :
        return ("red" if splitedVar[0] > splitedVar[2] else ("green" if splitedVar[0] < splitedVar[2] else "black"))