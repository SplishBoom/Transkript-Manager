from    tkinter     import  ttk
import  tkinter     as      tk

class InfoFrame(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.configure(bg="white", relief="sunken", borderwidth=1)

        infoFirstLabel = tk.Label(self, text=self.root.studentID)
        infoSecondLabel = tk.Label(self, text=self.root.nationalID)
        infoThirdLabel = tk.Label(self, text=self.root.studentName)
        infoFourthLabel = tk.Label(self, text=self.root.studentSurname)
        infoFifthLabel = tk.Label(self, text=self.root.facultyAndDepartment)
        infoSixthLabel = tk.Label(self, text=self.root.programName)
        infoSeventhLabel = tk.Label(self, text=self.root.languageOfInstution)
        infoEighthLabel = tk.Label(self, text=self.root.studentStatus)
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