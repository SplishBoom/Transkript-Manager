from    tkinter     import  ttk
import  tkinter     as      tk
import  json
import  os

class InfoFrame(ttk.Frame):
    
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self["style"] = "InfoFrame.TFrame"
        self.configure(relief="flat", borderwidth=1)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)

        for i in range(0,4) :
            self.rowconfigure(i, weight=1)

        with open (os.path.abspath("Temp/studentData.json"), "r", encoding="utf-8") as f:
            studentID, nationalID, studentName, studentSurname, facultyAndDepartment, programName, languageOfInstution, studentStatus = json.load(f)

        infoFirstLabel = ttk.Label(self, text=studentID, style="InfoFrameLabel.TLabel")
        infoSecondLabel = ttk.Label(self, text=nationalID, style="InfoFrameLabel.TLabel")
        infoThirdLabel = ttk.Label(self, text=studentName, style="InfoFrameLabel.TLabel")
        infoFourthLabel = ttk.Label(self, text=studentSurname, style="InfoFrameLabel.TLabel")
        infoFifthLabel = ttk.Label(self, text=facultyAndDepartment, style="InfoFrameLabel.TLabel")
        infoSixthLabel = ttk.Label(self, text=programName, style="InfoFrameLabel.TLabel")
        infoSeventhLabel = ttk.Label(self, text=languageOfInstution, style="InfoFrameLabel.TLabel")
        infoEighthLabel = ttk.Label(self, text=studentStatus, style="InfoFrameLabel.TLabel")

        infoFirstLabel.grid(row=0, column=0)
        infoSecondLabel.grid(row=0, column=1)
        infoThirdLabel.grid(row=1, column=0)
        infoFourthLabel.grid(row=1, column=1)
        infoFifthLabel.grid(row=2, column=0)
        infoSixthLabel.grid(row=2, column=1)
        infoSeventhLabel.grid(row=3, column=0)
        infoEighthLabel.grid(row=3, column=1)
