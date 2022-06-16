from    tkinter     import  ANCHOR, ttk
import  tkinter     as      tk
import  json

class ControllFrame(tk.Frame) :
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.configure(bg="white", relief="sunken", borderwidth=1)

        courseCodeButton = tk.Button(self, text="Course Code", command=lambda : self.sortJsonByElement("Course Code"))
        courseNameButton = tk.Button(self, text="Course Name", command=lambda : self.sortJsonByElement("Course Name"))
        courseLanguageButton = tk.Button(self, text="Course Language", command=lambda : self.sortJsonByElement("Course Language"))
        courseEtcsButton = tk.Button(self, text="Course ETCS", command=lambda : self.sortJsonByElement("Course ETCS"))
        courseNotationButton = tk.Button(self, text="Course Notation", command=lambda : self.sortJsonByElement("Course Notation"))
        courseGradeButton = tk.Button(self, text="Course Grade", command=lambda : self.sortJsonByElement("Course Grade"))

        courseCodeButton.grid(row=0, column=0)
        courseNameButton.grid(row=0, column=1)
        courseLanguageButton.grid(row=0, column=2)
        courseEtcsButton.grid(row=0, column=3)
        courseNotationButton.grid(row=0, column=4)
        courseGradeButton.grid(row=0, column=5)

        for label in self.winfo_children():
            label.configure(font=("Segoe UI", 11, "bold"), foreground="black")
            label.grid_configure(padx=1)

    def sortJsonByElement(self, element, *event) :
        pass