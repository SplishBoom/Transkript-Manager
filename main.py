from    GUI             import DisplayFrame, InputFrame, InfoFrame, ControllFrame, ResultFrame
from    Util            import retrieveData, segmentAndCreateJsons
from    Util            import secureStart, secureFinish
from    tkinter  import ttk
import  tkinter  as     tk
"""
todo: gif add input screen
multi threading input screen
"""
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.transcriptText = ""
        self.transcriptTextLanguage = ""

        self.title("Transkript Manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.generalPadding = 10
        self.container = ttk.Frame(self, padding=(self.generalPadding))
        self.container.grid(row=0, column=0)

        self.inputSection = InputFrame(self.container, self)
        self.inputSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

    def retrieveTranscript(self):

        self.transcriptText = (retrieveData(self.inputSection.username.get(), self.inputSection.password.get(), True))
        
        segmentAndCreateJsons(self.transcriptText)

        self.inputSection.grid_forget()

        self.infoSection = InfoFrame(self.container, self)
        self.infoSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding, pady=self.generalPadding)

        self.controllSection = ControllFrame(self.container, self)
        self.controllSection.grid(row=1, column=0, sticky="nsew", padx=self.generalPadding, pady=self.generalPadding)

        self.displaySection = DisplayFrame(self.container, self)
        self.displaySection.grid(row=3, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)
        
if __name__ == "__main__":
    
    secureStart()

    app = Application()
    app.mainloop()

    secureFinish()