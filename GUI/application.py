from    GUI         import ControllFrame, DisplayFrame, InfoFrame, InputFrame, ResultFrame
from    Util        import retrieveData, segmentAndCreateJsons
from    tkinter     import ttk
import  tkinter     as     tk

class Application(tk.Tk):
    
    def __init__(self, debug=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap("Assets/icon.ico")

        self.title("Transcript Manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure   (0, weight=1)

        self.generalPadding = 10
        self.container = ttk.Frame(self, padding=(self.generalPadding,))
        self.container.grid(row=0, column=0)

        self.inputSection = InputFrame(self.container, self)
        self.inputSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

        if debug :
            self.switchToManager()

        self.rotateApplicationWindow()

    def retrieveTranscriptData(self, username, password, statue) :
        retrieveData(username, password, statue)
        self.inputSection.isDone = True
        self.segmentateTranscriptData()

    def segmentateTranscriptData(self):
        segmentAndCreateJsons()
        self.switchToManager()

    def switchToManager(self):
        self.inputSection.grid_forget()

        self.infoSection = InfoFrame(self.container, self)
        self.infoSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

        self.controllSection = ControllFrame(self.container, self)
        self.controllSection.grid(row=1, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding/2)

        self.displaySection = DisplayFrame(self.container, self)
        self.displaySection.grid(row=2, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

        self.resultSection = ResultFrame(self.container, self)
        self.resultSection.grid(row=3, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding/2)

        self.rotateApplicationWindow()

    def closeProgram(self) :
        self.destroy()

    def restartProgram(self) :
        self.infoSection.grid_forget()
        self.controllSection.grid_forget()
        self.displaySection.grid_forget()
        self.resultSection.grid_forget()

        self.inputSection = InputFrame(self.container, self)
        self.inputSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

    def rotateApplicationWindow(self) :
        self.update()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2), int(self.winfo_screenheight()/2 - self.winfo_reqheight()/2)))