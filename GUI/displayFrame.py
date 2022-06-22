from    tkinter     import  ttk
import  tkinter     as      tk
import  json
import  os

class DisplayFrame(ttk.Frame):
    
    def __init__(self, parent, root, canv_w = 930, canv_h = 10, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.possibleNotations = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W", "S"]
        self.weights = {"A":4.00, "A-":3.70, "B+":3.30, "B":3.00, "B-":2.70, "C+":2.30, "C":2.00, "C-":1.70, "D+":1.30, "D":1.00, "F":0.00}
        self.courseNotations = {}
        self.courseLabels = []
        self.courseNotationComboboxes = []
        self.coursesShouldBeHighlighted = []

        self.saveInitialData = True
        
        self.canvas = tk.Canvas(self, width=canv_w, height=canv_h, bg="white")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.root.bind("<MouseWheel>", self._onWheel)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.gridCoursesOnCanvas()

    def handleCombobox(self, courseCode, newNotation, *event) :

        if self.allCourses[courseCode][-3] != newNotation :
            self.coursesShouldBeHighlighted.append(courseCode)

        self._updateCGPA(courseCode, newNotation)

    def gridCoursesOnCanvas(self) :

        self.calculateCGPA()

        for currentCourse in self.courseLabels :
            for currentCourseLabel in currentCourse :
                currentCourseLabel[0].grid_forget()
        self.courseLabels.clear()
        self.courseNotationComboboxes.clear()

        rowStart = 0
        for currentCourseCode, currentCourseValues in self.allCourses.items() :

            usedFont = ("Helvetica", 11, "bold")

            courseIdLabel = tk.Label(self.scrollable_frame, text=str(currentCourseValues[-1]), font=usedFont, width=6, height=2, anchor="center")
            courseCodeLabel = tk.Label(self.scrollable_frame, text=str(currentCourseCode), font=usedFont, width=15, height=2, anchor="center")
            courseNameLabel = tk.Label(self.scrollable_frame, text=str(currentCourseValues[-6]), font=usedFont, width=50, height=2, anchor="center")
            courseLanguageLabel = tk.Label(self.scrollable_frame, text=str(currentCourseValues[-5]), font=usedFont, width=5, height=2, anchor="center")
            courseETCSLabel = tk.Label(self.scrollable_frame, text=str(currentCourseValues[-4]), font=usedFont, width=10, height=2, anchor="center")
            courseNotationCombobox = ttk.Combobox(self.scrollable_frame, textvariable=(self.courseNotations[currentCourseCode]), values=self.possibleNotations, width=4, font=usedFont)
            courseGradeLabel = tk.Label(self.scrollable_frame, text=str(round(float(currentCourseValues[-2]),2)), font=usedFont, width=12, height=2, anchor="center")

            self.courseLabels.append(
                [
                    [courseIdLabel, rowStart, 0, "w", currentCourseCode],
                    [courseCodeLabel, rowStart, 1, "w", currentCourseCode], 
                    [courseNameLabel, rowStart, 2, "w", currentCourseCode], 
                    [courseLanguageLabel, rowStart, 3, "w", currentCourseCode], 
                    [courseETCSLabel, rowStart, 4, "w", currentCourseCode], 
                    [courseNotationCombobox, rowStart, 5, "w", currentCourseCode], 
                    [courseGradeLabel, rowStart, 6, "w", currentCourseCode]
                ]
            )

            self.courseNotationComboboxes.append([currentCourseCode, courseNotationCombobox])

            rowStart += 1

        cathcByWidth = {"Course Code":15, "Course Name":50, "Course Language":5, "Course ETCS":10, "Course Notation":4, "Course Grade":12, "Course Date":6, None:0}

        for currentCourseElements in self.courseLabels :
            for currentCourse in currentCourseElements :
                if currentCourse[0]["width"] == cathcByWidth[self.root.controllSection.lastSortCombine] :
                    currentCourse[0].config(foreground="blue")
        
                if currentCourse[4] in self.coursesShouldBeHighlighted :
                    currentCourse[0].config(foreground="green")

                currentCourse[0].grid(row=currentCourse[1], column=currentCourse[2], sticky=currentCourse[3])

        for currentCourseCode, currentCourseNotationCombobox in self.courseNotationComboboxes :
            currentCourseNotationCombobox.bind("<<ComboboxSelected>>", lambda event, courseCode=currentCourseCode: self.handleCombobox(courseCode, event.widget.get()))
            currentCourseNotationCombobox.unbind_class("TCombobox", "<MouseWheel>")

    def _onWheel(self, event) :
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _loadData(self):
        with open (os.path.abspath("Temp/transcriptData.json"), "r", encoding="utf-8") as f :
            self.allCourses = json.load(f)

    def _uploadData(self) :
        with open (os.path.abspath("Temp/transcriptData.json"), "w", encoding="utf-8") as f :
            json.dump(self.allCourses, f, ensure_ascii=False, indent=4)

    def _loadCourseNotations(self) :
        for courseCode, courseValues in self.allCourses.items() :
            self.courseNotations[courseCode] = tk.StringVar(value=courseValues[-3])

    def calculateCGPA(self) :
        
        self.totalQualityPoints = 0
        self.creditsAttempted = 0
        self.creditsSuccesfull = 0
        self.creditsIncludedInCPGA = 0
        self.CGPA = 0

        self._loadData()

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

        try :
            self.CGPA = self.totalQualityPoints / self.creditsIncludedInCPGA
        except ZeroDivisionError :
            self.CGPA = 0

        self._loadCourseNotations()

        seperator = "   \u279C   "
        if self.saveInitialData :
            self.saveInitialData = False

            self.totalQualityPointsInit = self.totalQualityPoints 
            self.creditsAttemptedInit = self.creditsAttempted 
            self.creditsSuccesfullInit = self.creditsSuccesfull 
            self.creditsIncludedInCPGAInit = self.creditsIncludedInCPGA 
            self.CGPAInit = self.CGPA 

            self.creditsAttemptedVar = tk.StringVar(value=(str(self.creditsAttemptedInit)+seperator+str(self.creditsAttempted)))
            self.creditsSuccesfullVar = tk.StringVar(value=(str(self.creditsSuccesfullInit)+seperator+str(self.creditsSuccesfull)))
            self.creditsIncludedInCPGAVar = tk.StringVar(value=(str(self.creditsIncludedInCPGAInit)+seperator+str(self.creditsIncludedInCPGA)))
            self.totalQualityPointsVar = tk.StringVar(value=(str(round(self.totalQualityPointsInit,2))+seperator+str(round(self.totalQualityPoints,2))))
            self.CGPAVar = tk.StringVar(value=(str(round(self.CGPAInit,2))+seperator+str(round(self.CGPA,2))))
        else :
            self.creditsAttemptedVar.set(str(self.creditsAttemptedInit)+seperator+str(self.creditsAttempted))
            self.creditsSuccesfullVar.set(str(self.creditsSuccesfullInit)+seperator+str(self.creditsSuccesfull))
            self.creditsIncludedInCPGAVar.set(str(self.creditsIncludedInCPGAInit)+seperator+str(self.creditsIncludedInCPGA))
            self.totalQualityPointsVar.set(str(round(self.totalQualityPointsInit,2))+seperator+str(round(self.totalQualityPoints,2)))
            self.CGPAVar.set(str(round(self.CGPAInit,2))+seperator+str(round(self.CGPA,2)))
        
    def _updateCGPA(self, courseCode, newNotation, *event) :
        
        courseValues = self.allCourses[courseCode]
        
        courseValues[-3] = newNotation
        try :
            weight = self.weights[newNotation]
        except KeyError :
            weight = 0
        courseValues[-2] = weight * float(courseValues[-4])

        self.allCourses[courseCode] = courseValues

        self._uploadData()

        self.gridCoursesOnCanvas()