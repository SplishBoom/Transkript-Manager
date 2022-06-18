from    tkinter     import  ANCHOR, ttk
import  tkinter     as      tk
import  json
from    Util        import sortTrJsonDataByElement

class ControllFrame(tk.Frame) :
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        for columno in range(0, 7) :
            self.columnconfigure(columno, weight=1)

        self.configure(bg="white", relief="sunken", borderwidth=1)

        self.sortCombines = {"Course Code":False, "Course Name":False, "Course Language":False, "Course ETCS":False, "Course Notation":False, "Course Grade":False, "Reset":False}

        resetButton = tk.Button(self, text="Queue", command=lambda : self.sortData("Reset"))
        courseCodeButton = tk.Button(self, text="Course Code", command=lambda : self.sortData("Course Code"))
        courseNameButton = tk.Button(self, text="Course Name", command=lambda : self.sortData("Course Name"))
        courseLanguageButton = tk.Button(self, text="Course Language", command=lambda : self.sortData("Course Language"))
        courseEtcsButton = tk.Button(self, text="Course ETCS", command=lambda : self.sortData("Course ETCS"))
        courseNotationButton = tk.Button(self, text="Course Notation", command=lambda : self.sortData("Course Notation"))
        courseGradeButton = tk.Button(self, text="Course Grade", command=lambda : self.sortData("Course Grade"))

        resetButton.grid(row=0, column=0)
        courseCodeButton.grid(row=0, column=1)
        courseNameButton.grid(row=0, column=2)
        courseLanguageButton.grid(row=0, column=3)
        courseEtcsButton.grid(row=0, column=4)
        courseNotationButton.grid(row=0, column=5)
        courseGradeButton.grid(row=0, column=6)

        for label in self.winfo_children():
            label.configure(font=("Segoe UI", 11, "bold"), foreground="black")
            label.grid_configure(padx=1)

    def sortData(self, element, *event) :
        sortTrJsonDataByElement(element, self.sortCombines[element])
        self.sortCombines[element] = not self.sortCombines[element]
