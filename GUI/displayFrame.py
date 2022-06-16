from    tkinter     import  ANCHOR, ttk
import  tkinter     as      tk
import  json

def segmentAndCreateJson(textInput) :
    
    if textInput.startswith("MEF UNIVERSITY"):
        trannnskriptLanguage = "English"
    elif textInput.startswith("T.C."):
        trannnskriptLanguage = "Turkish"
    else :
        exit()

    textInput = textInput.split('\n')

    textInput = textInput[:-5]
    if trannnskriptLanguage == "English":
        textInput = textInput[3:]
        semesterBraces = ["Fall", "Spring", "Summer", "Course Code", "Semester", "Cumulative", "Academic Standing"]
    elif trannnskriptLanguage == "Turkish":
        textInput = textInput[4:]
        semesterBraces = ["Güz", "Bahar", "Yaz", "Ders Kodu", "Dönem Alınan", "Genel Alınan", "Akademik Durum"]

    studentInfo = textInput[:4]

    textInput = textInput[4:]

    xCleaned = []
    for line in textInput :
        if not any(semesterBraces in line for semesterBraces in semesterBraces):
            xCleaned.append(line)

    allCourses = {}
    for line in xCleaned :
        line = line.split(" ")

        if line[0].startswith("PREP") or line[0].startswith("PREP*"):
            continue

        courseCode = (line[0]+" "+line[1]).replace("*", "")
        courseName = " ".join(line[2:-4])
        courseLanguage = line[-4]
        courseEtcs = line[-3]
        courseNotation = line[-2]
        courseGrade = float(line[-1])

        allCourses[courseCode] = [courseName, courseLanguage, courseEtcs, courseNotation, courseGrade]

    with open ("Temp/transkriptData.json", "w", encoding="utf-8") as f:
        json.dump(allCourses, f, indent=4)

    print(studentInfo[2:])
    studentID = studentInfo[0][studentInfo[0].find("0"):studentInfo[0].find("0")+9]
    nationalID = studentInfo[0][-11:]
    studentName = " ".join(studentInfo[1].split(" ")[1:-2])
    studentSurname = studentInfo[1].split(" ")[-1]
    if trannnskriptLanguage == "English":
        facultyAndDepartment = studentInfo[2][21:studentInfo[2].find("Program Name")-1]
        programName = studentInfo[2][studentInfo[2].find("Program Name")+13:]
        languageOfInstution = studentInfo[3][studentInfo[3].find("Language of Instruction")+24:studentInfo[3].find("Student")-1]
        studentStatus = studentInfo[3][studentInfo[3].find("Student")+15:]
    else :
        facultyAndDepartment = studentInfo[2][studentInfo[2].find("Fakülte")+8:studentInfo[2].find("Bölüm")-1]
        programName = studentInfo[2][studentInfo[2].find("Bölüm")+6:]
        languageOfInstution = studentInfo[3][studentInfo[3].find("Dil")+5:studentInfo[3].find("Öğrenci")-1]
        studentStatus = studentInfo[3][studentInfo[3].find("Öğrenci")+18:]

    return studentID, nationalID, studentName, studentSurname, facultyAndDepartment, programName, languageOfInstution, studentStatus

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

            list.append([courseCodeLabel, courseNameLabel, courseLanguageLabel, courseEtcsLabel, currentNotation, courseGradeLabel])

            courseCodeLabel.grid(row=startRow, column=0)
            courseNameLabel.grid(row=startRow, column=1)
            courseLanguageLabel.grid(row=startRow, column=2)
            courseEtcsLabel.grid(row=startRow, column=3)
            self.courseNotationComboBox.grid(row=startRow, column=4)
            courseGradeLabel.grid(row=startRow, column=5)
            
            startRow += 1

        for label in self.scrollbarFrame.winfo_children():
            label.configure(font=("Segoe UI", 11, "bold"), foreground="black", background="white")
            label.grid_configure(padx=6, pady=5)

    def calculateCGPA(self) :

        self.totalQualityPoints = 0
        self.totalCredits = 0
        self.totalSuccessfulCredits = 0

        for courseValues in self.allCourses.values() :

            if courseValues[-2] in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"] :
                self.totalQualityPoints += float(courseValues[-1])
                self.totalCredits += float(courseValues[-3])
                self.totalSuccessfulCredits += int(courseValues[-3])
            elif courseValues[-2] == "I" :
                continue
            elif courseValues[-2] == "W" :
                self.totalSuccessfulCredits += int(courseValues[-3])
            else :
                self.totalQualityPoints += 0
                self.totalCredits += float(courseValues[-3])

        self.CGPA = self.totalQualityPoints / self.totalCredits

    def updateCGPA(self, courseCode, newNotation, *event) :
        
        courseValues = self.allCourses[courseCode]
        
        courseValues[-2] = newNotation
        try :
            weight = self.weights[newNotation]
        except KeyError :
            weight = 0
        courseValues[-1] = weight * float(courseValues[-3])

        self.allCourses[courseCode] = courseValues

        self.calculateCGPA()
