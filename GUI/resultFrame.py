from    tkinter     import  ttk
import  tkinter     as      tk

class ResultFrame(ttk.Frame):
    
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self["style"] = "ResultFrame.TFrame"
        self.configure(relief="flat", borderwidth=1)

        for i in range(0, 5):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._createWidgets()

        self._gridWidgets()

        for label in self.winfo_children():
            label.grid_configure(padx=1, pady=1)

    def _createWidgets(self) :
        
        self.infoLabel1 = ttk.Label(self, text="Attempted Credits", style="ResultFrameInfoLabel.TLabel")
        self.infoLabel2 = ttk.Label(self, text="Successful Credits", style="ResultFrameInfoLabel.TLabel")
        self.infoLabel3 = ttk.Label(self, text="Included Credits", style="ResultFrameInfoLabel.TLabel")
        self.infoLabel4 = ttk.Label(self, text="Quality Points", style="ResultFrameInfoLabel.TLabel")
        self.infoLabel5 = ttk.Label(self, text="CGPA", style="ResultFrameInfoLabel.TLabel")

        self.creditsAttemptedInfo = ttk.Label(self, textvariable=self.root.displaySection.creditsAttemptedVar, style="ResultFrameDynamicLabel.TLabel")
        self.creditsSuccesfullInfo = ttk.Label(self, textvariable=self.root.displaySection.creditsSuccesfullVar, style="ResultFrameDynamicLabel.TLabel")
        self.creditsIncludedInCPGAInfo = ttk.Label(self, textvariable=self.root.displaySection.creditsIncludedInCPGAVar, style="ResultFrameDynamicLabel.TLabel")
        self.totalQualityPointsInfo = ttk.Label(self, textvariable=self.root.displaySection.totalQualityPointsVar, style="ResultFrameDynamicLabel.TLabel")
        self.CGPAInfo = ttk.Label(self, textvariable=self.root.displaySection.CGPAVar, style="ResultFrameDynamicLabel.TLabel")

        self.root.displaySection.CGPAVar.trace("w", self._awareChanges)

    def _gridWidgets(self) :
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

    def _awareChanges(self, *event) :
        self.creditsAttemptedInfo.configure(foreground=self._colorize(self.root.displaySection.creditsAttemptedVar.get().split()))
        self.creditsSuccesfullInfo.configure(foreground=self._colorize(self.root.displaySection.creditsSuccesfullVar.get().split()))
        self.creditsIncludedInCPGAInfo.configure(foreground=self._colorize(self.root.displaySection.creditsIncludedInCPGAVar.get().split()))
        self.totalQualityPointsInfo.configure(foreground=self._colorize(self.root.displaySection.totalQualityPointsVar.get().split()))
        self.CGPAInfo.configure(foreground=self._colorize(self.root.displaySection.CGPAVar.get().split()))

    def _colorize(self, splitedVar) :
        return ("red" if splitedVar[0] > splitedVar[2] else ("lime green" if splitedVar[0] < splitedVar[2] else "black"))