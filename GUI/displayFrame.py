from    tkinter     import  font, ttk
import  tkinter     as      tk
import  json

class DisplayFrame(ttk.Frame):
    def __init__(self, parent, root, canv_w = 940, canv_h = 410, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.possibleNotations = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W"]
        self.weights = {"A":4.00, "A-":3.70, "B+":3.30, "B":3.00, "B-":2.70, "C+":2.30, "C":2.00, "C-":1.70, "D+":1.30, "D":1.00, "F":0.00}
        self.courseNotations = {}
        self.courseLabels = {}
        self.courseNotationComboboxes = []
        
        self.canvas = tk.Canvas(self, width=canv_w, height=canv_h, bg="white")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.bind("<MouseWheel>", self.onWheel)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.gridCoursesOnCanvas()

    def handleCombobox(self, courseCode, newNotation, *event) :
        self.updateCGPA(courseCode, newNotation)

    def gridCoursesOnCanvas(self) :

        self.calculateCGPA()

        for currentCourseLabel in self.courseLabels :
            currentCourseLabel.grid_forget()
        self.courseLabels.clear()
        self.courseNotationComboboxes.clear()

        rowStart = 0
        for currentCourseCode, currentCourseValues in self.allCourses.items() :

            usedFont = ("Helvetica", 11, "bold")

            courseIdLabel = tk.Label(self.scrollable_frame, text=currentCourseValues[-1], font=usedFont, width=6, height=2, anchor="center")
            courseCodeLabel = tk.Label(self.scrollable_frame, text=currentCourseCode, font=usedFont, width=15, height=2, anchor="center")
            courseNameLabel = tk.Label(self.scrollable_frame, text=currentCourseValues[-6], font=usedFont, width=50, height=2, anchor="center")
            courseLanguageLabel = tk.Label(self.scrollable_frame, text=currentCourseValues[-5], font=usedFont, width=5, height=2, anchor="center")
            courseETCSLabel = tk.Label(self.scrollable_frame, text=currentCourseValues[-4], font=usedFont, width=10, height=2, anchor="center")
            courseNotationCombobox = ttk.Combobox(self.scrollable_frame, textvariable=(self.courseNotations[currentCourseCode]), values=self.possibleNotations, width=5, font=usedFont)
            courseGradeLabel = tk.Label(self.scrollable_frame, text=str(round(float(currentCourseValues[-2]),2)), font=usedFont, width=12, height=2, anchor="center")
            
 
            self.courseLabels[courseIdLabel] = [rowStart, 0, "w"]
            self.courseLabels[courseCodeLabel] = [rowStart, 1, "w"]
            self.courseLabels[courseNameLabel] = [rowStart, 2, "w"]
            self.courseLabels[courseLanguageLabel] = [rowStart, 3, "w"]
            self.courseLabels[courseETCSLabel] = [rowStart, 4, "w"]
            self.courseLabels[courseNotationCombobox] = [rowStart, 5, "w"]
            self.courseLabels[courseGradeLabel] = [rowStart, 6, "w"]

            self.courseNotationComboboxes.append([currentCourseCode, courseNotationCombobox])

            rowStart += 1

        for currentCourseLabel, currentCourseValues in self.courseLabels.items() :
            currentCourseLabel.grid(row=currentCourseValues[0], column=currentCourseValues[1], sticky=currentCourseValues[2])

        for currentCourseCode, currentCourseNotationCombobox in self.courseNotationComboboxes :
            currentCourseNotationCombobox.bind("<<ComboboxSelected>>", lambda event, courseCode=currentCourseCode: self.handleCombobox(courseCode, event.widget.get()))

    def onWheel(self, event) :
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def loadData(self):
        with open ("Temp/transcriptData.json", "r", encoding="utf-8") as f :
            self.allCourses = json.load(f)

    def uploadData(self) :
        with open ("Temp/transcriptData.json", "w", encoding="utf-8") as f :
            json.dump(self.allCourses, f, ensure_ascii=False, indent=4)

    def loadCourseNotations(self) :
        for courseCode, courseValues in self.allCourses.items() :
            self.courseNotations[courseCode] = tk.StringVar(value=courseValues[-3])

    def calculateCGPA(self) :

        self.totalQualityPoints = 0
        self.creditsAttempted = 0
        self.creditsSuccesfull = 0
        self.creditsIncludedInCPGA = 0
        self.CGPA = 0

        self.loadData()

        for courseCode, courseValues in self.allCourses.items() :

            self.courseNotations[courseCode] = courseValues[-3]
            self.creditsAttempted += int(courseValues[-4])

            if courseValues[-3] in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D"] :
                self.creditsSuccesfull += int(courseValues[-4])
                self.creditsIncludedInCPGA += int(courseValues[-4])
                self.totalQualityPoints += float(courseValues[-2])
            elif courseValues[-3] in ["W", "S"] :
                self.creditsSuccesfull += int(courseValues[-4])

            elif courseValues[-3].startswith("F") or courseValues[-3] == "U" :
                self.creditsIncludedInCPGA += int(courseValues[-4])
                self.totalQualityPoints += int(courseValues[-2])
            elif courseValues[-3] == "I" :
                continue
            else :
                pass


        self.CGPA = self.totalQualityPoints / self.creditsIncludedInCPGA

        self.loadCourseNotations()

        """print("self.totalQualityPoints  =", self.totalQualityPoints)
        print("self.creditsAttempted    =", self.creditsAttempted)
        print("self.creditsSuccesfull   =", self.creditsSuccesfull)
        print("self.creditsIncludedInCPGA   =", self.creditsIncludedInCPGA)
        print("self.CGPA    =", self.CGPA)"""
        

    def updateCGPA(self, courseCode, newNotation, *event) :
        
        courseValues = self.allCourses[courseCode]
        
        courseValues[-3] = newNotation
        try :
            weight = self.weights[newNotation]
        except KeyError :
            weight = 0
        courseValues[-2] = weight * float(courseValues[-4])

        self.allCourses[courseCode] = courseValues

        self.uploadData()

        self.gridCoursesOnCanvas()