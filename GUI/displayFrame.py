from    tkinter     import  ttk
import  tkinter     as      tk
import  json

class DisplayFrame(ttk.Frame):
    def __init__(self, parent, root, canv_w = 650, canv_h = 350, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.possibleNotations = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W"]
        self.weights = {"A":4.00, "A-":3.70, "B+":3.30, "B":3.00, "B-":2.70, "C+":2.30, "C":2.00, "C-":1.70, "D+":1.30, "D":1.00, "F":0.00}

        with open ("Temp/transkriptData.json", "r", encoding="utf-8") as f :
            self.allCourses = json.load(f)

        self.calculateCGPA()

        self.canvas = tk.Canvas(self, width=canv_w, height=canv_h)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbarFrame = ttk.Frame(self.canvas, )

        self.scrollbarFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollbarFrame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        startRow = 0
        list = []
        for courseCode, courseValues in self.allCourses.items() :

            courseCodeLabel = tk.Label(self.scrollbarFrame, text=courseCode)
            courseNameLabel = tk.Label(self.scrollbarFrame, text=courseValues[0])
            courseLanguageLabel = tk.Label(self.scrollbarFrame, text=courseValues[1])
            courseEtcsLabel = tk.Label(self.scrollbarFrame, text=courseValues[2])
            currentNotation = tk.StringVar(value=courseValues[3])
            self.courseNotationComboBox = ttk.Combobox(self.scrollbarFrame, values=self.possibleNotations, textvariable=currentNotation, width=3)
            courseGradeLabel = tk.Label(self.scrollbarFrame, text=courseValues[4])
            courseID = tk.Label(self.scrollbarFrame, text=courseValues[5])

            list.append([courseCodeLabel, courseNameLabel, courseLanguageLabel, courseEtcsLabel, currentNotation, courseGradeLabel])

            courseCodeLabel.grid(row=startRow, column=0)
            courseNameLabel.grid(row=startRow, column=1)
            courseLanguageLabel.grid(row=startRow, column=2)
            courseEtcsLabel.grid(row=startRow, column=3)
            self.courseNotationComboBox.grid(row=startRow, column=4)
            courseGradeLabel.grid(row=startRow, column=5)
            
            startRow += 1

        print(self.CGPA)
        
        for label in self.scrollbarFrame.winfo_children():
            label.configure(font=("Segoe UI", 11, "bold"), foreground="black", background="white")
            label.grid_configure(padx=6, pady=5)

    def calculateCGPA(self) :

        self.totalQualityPoints = 0
        self.totalCredits = 0
        self.totalSuccessfulCredits = 0

        for courseValues in self.allCourses.values() :

            if courseValues[-3] in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"] :
                self.totalQualityPoints += float(courseValues[-2])
                self.totalCredits += float(courseValues[-4])
                self.totalSuccessfulCredits += int(courseValues[-4])
            elif courseValues[-3] == "I" :
                continue
            elif courseValues[-3] == "W" :
                self.totalSuccessfulCredits += int(courseValues[-5])
            else :
                self.totalQualityPoints += 0
                self.totalCredits += float(courseValues[-4])

        self.CGPA = self.totalQualityPoints / self.totalCredits

    def updateCGPA(self, courseCode, newNotation, *event) :
        
        courseValues = self.allCourses[courseCode]
        
        courseValues[-3] = newNotation
        try :
            weight = self.weights[newNotation]
        except KeyError :
            weight = 0
        courseValues[-3] = weight * float(courseValues[-3])

        self.allCourses[courseCode] = courseValues

        self.calculateCGPA()
