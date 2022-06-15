
from    tkinter     import  ANCHOR, ttk
import  tkinter     as      tk
import  json

msg = msg = """MEF UNIVERSITY
Registrar’s Office
15.06.2022
Student ID 041901027 National ID 67456133140
Name EMİR ÇETİN Surname MEMİŞ
Faculty / Department Faculty of Engineering / Computer Engineering Program Name Computer Engineering
Language of Instruction English Student Status Continuing
2019-2020 Fall Semester
Course Code Course Name Language ECTS Grade Grade Point
PREP* Prep EN 0 U 0.00
2019-2020 Spring Semester
Course Code Course Name Language ECTS Grade Grade Point
PREP* Prep EN 0 U 0.00
2019-2020 Summer School
Course Code Course Name Language ECTS Grade Grade Point
PREP Prep EN 0 S 0.00
Semester Credits Attempted : 0.00 Credits Successful : Credits Included in the GPA : GPA :
Cumulative Credits Attempted : 0.00 Credits Successful : Credits Included in the CGPA : CGPA :
2020-2021 Fall Semester
Course Code Course Name Language ECTS Grade Grade Point
COMP 100 Introduction to Computer Engineering EN 3 A 12.00
COMP 109 Computer Programming (JAVA) EN 6 A 24.00
ENG 101 English for Academic Purposes I EN 4 B 12.00
MATH 115* Calculus I EN 7 C+ 16.10
PHYS 103 Physics I EN 6 A 24.00
PHYS 103L Physics I Lab. EN 2 A 8.00
TURK 111 Turkish Language and Literature I TR 2 A- 7.40
Semester Credits Attempted : 30.00 Credits Successful : 30.00 Credits Included in the GPA : 30.00 GPA : 3.45
Cumulative Credits Attempted : 30.00 Credits Successful : 30.00 Credits Included in the CGPA : 30.00 CGPA : 3.45
Academic Standing Honor
2020-2021 Spring Semester
Course Code Course Name Language ECTS Grade Grade Point
COMP 110 Object-Oriented Programming (JAVA) EN 6 A 24.00
ENG 102 English for Academic Purposes II EN 4 A- 14.80
MATH 108 Discrete and Combinatorial Mathematics EN 5 C+ 11.50
MATH 116 Calculus II EN 7 A 28.00
PHYS 104 Physics II EN 6 A 24.00
PHYS 104L Physics II Lab EN 2 A 8.00
Semester Credits Attempted : 30.00 Credits Successful : 30.00 Credits Included in the GPA : 30.00 GPA : 3.68
Cumulative Credits Attempted : 60.00 Credits Successful : 60.00 Credits Included in the CGPA : 60.00 CGPA : 3.56
Academic Standing High Honor
 2021-2022 Fall Semester
Course Code Course Name Language ECTS Grade Grade Point
COMP 201 Data Structures and Algorithms EN 6 A 24.00
COMP 205 Systems Programming EN 6 A 24.00
EE 203 Digital Systems Design EN 6 B- 16.20
ENGR 301 Technical Report Writing and Presentation EN 4 A- 14.80
HISTR 211* Principles of Ataturk and History of the Turkish Republic I TR 2 B+ 6.60
MATH 115* Calculus I EN 7 C+ 16.10
MATH 211 Linear Algebra EN 6 A- 22.20
Semester Credits Attempted : 37.00 Credits Successful : 37.00 Credits Included in the GPA : 37.00 GPA : 3.35
Cumulative Credits Attempted : 90.00 Credits Successful : 90.00 Credits Included in the CGPA : 90.00 CGPA : 3.57
Academic Standing Honor
2021-2022 Spring Semester
Course Code Course Name Language ECTS Grade Grade Point
COMP 204 Programming Studio EN 6 A 24.00
COMP 206 Computer Architecture EN 6 C 12.00
EE 212 Electrical and Electronic Circuits EN 6 I 0.00
HISTR 211 Principles of Ataturk and History of the Turkish Republic I TR 2 A- 7.40
HISTR 212 Principles of Ataturk and History of the Turkish Republic II TR 2 A- 7.40
MATH 115 Calculus I EN 7 F 0.00
MATH 224 Probability and Statistics for Engineering EN 6 C- 10.20
Semester Credits Attempted : 35.00 Credits Successful : 22.00 Credits Included in the GPA : 29.00 GPA : 2.10
Cumulative Credits Attempted : 116.00 Credits Successful : 103.00 Credits Included in the CGPA : 110.00 CGPA : 3.27
A: 4.00     A-: 3.70     B+: 3.30     B: 3.00     B-: 2.70     C+: 2.30     C: 2.00     C-: 1.70     D+: 1.30     D: 1.00     F: 0.00
S: Satisfactory    U: Unsatisfactory    I: Incomplete     EX: Exempted     W: Withdrawn     FX: No Attempt in Final Exam     FZ: No Right to Final Exam

End of record
MEF UNIVERSITY Ayazağa Cad. No.4 34396Maslak - Sarıyer / İSTANBUL TÜRKİYE http://www.mef.edu.tr"""

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

        self.aa()

        self.infoSection = InfoFrame(self.container, self)
        self.infoSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding, pady=self.generalPadding)

        self.controllSection = ControllFrame(self.container, self)
        self.controllSection.grid(row=1, column=0, sticky="nsew", padx=self.generalPadding, pady=self.generalPadding)

        self.displaySection = DisplayFrame(self.container, self)
        self.displaySection.grid(row=3, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)
    
    def aa(self) :
        self.studentID, self.nationalID, self.studentName, self.studentSurname, self.facultyAndDepartment, self.programName, self.languageOfInstution, self.studentStatus = segmentAndCreateJson(msg)

app = Application()
app.mainloop()