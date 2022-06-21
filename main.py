from    GUI             import ControllFrame, DisplayFrame, InfoFrame, InputFrame, ResultFrame
from    Util            import retrieveData, segmentAndCreateJsons
from    Util            import secureStart, secureFinish
from    tkinter  import ttk
import  tkinter  as     tk

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Transcript Manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.generalPadding = 10
        self.container = ttk.Frame(self, padding=(self.generalPadding,))
        self.container.grid(row=0, column=0)

        self.inputSection = InputFrame(self.container, self)
        self.inputSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

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

        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)
        
        self.geometry("+{}+{}".format(positionRight, positionDown))

if __name__ == "__main__":
    
    secureStart()

    app = Application()
    app.mainloop()

    secureFinish()