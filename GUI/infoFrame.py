from    tkinter     import  ttk
import  tkinter     as      tk
import  json

class InfoFrame(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)

        for i in range(0,4) :
            self.rowconfigure(i, weight=1)

        self.configure(bg="white", relief="sunken", borderwidth=1)

        with open ("Temp/studentData.json", "r", encoding="utf-8") as f:
            studentID, nationalID, studentName, studentSurname, facultyAndDepartment, programName, languageOfInstution, studentStatus = json.load(f)

        infoFirstLabel = tk.Label(self, text=studentID)
        infoSecondLabel = tk.Label(self, text=nationalID)
        infoThirdLabel = tk.Label(self, text=studentName)
        infoFourthLabel = tk.Label(self, text=studentSurname)
        infoFifthLabel = tk.Label(self, text=facultyAndDepartment)
        infoSixthLabel = tk.Label(self, text=programName)
        infoSeventhLabel = tk.Label(self, text=languageOfInstution)
        infoEighthLabel = tk.Label(self, text=studentStatus)
        infoFirstLabel.grid(row=0, column=0)
        infoSecondLabel.grid(row=0, column=1)
        infoThirdLabel.grid(row=1, column=0)
        infoFourthLabel.grid(row=1, column=1)
        infoFifthLabel.grid(row=2, column=0)
        infoSixthLabel.grid(row=2, column=1)
        infoSeventhLabel.grid(row=3, column=0)
        infoEighthLabel.grid(row=3, column=1)

        for label in self.winfo_children():
            label.configure(font=("Segoe UI", 11, "bold"), foreground="black")