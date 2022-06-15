import json
import tkinter as tk
from tkinter import ttk
import os
os.system("cls")

def getdata(isWithGui=True) :
    
    if not isWithGui:
        with open ("oto1.txt", "r") as otoCopyF :
            with open ("data.txt", "w") as f:
                f.write(otoCopyF.read())
    else :
        root = tk.Tk()

        inputArea = tk.Text(root, height=10, width=25, wrap="word", font=("Cambiria", 12, "bold"), foreground="black", background="gray86", selectbackground="black", selectforeground="yellow")
        inputArea.grid(row=0, column=0, sticky="nsew")
        inputArea.focus_force()

        areaScrollBarY = ttk.Scrollbar(root, orient="vertical", command=inputArea.yview)
        areaScrollBarY.grid(row=0, column=1, sticky="nsew")

        inputArea.config(yscrollcommand=areaScrollBarY.set)

        def clearTextContent(event):
            inputArea.delete("1.0", "end")

        def saveTextContent(event):
            textContent = inputArea.get("1.0", "end")
            with open ("data.txt", "w", encoding="utf-8") as f:
                for line in textContent.splitlines():
                    f.write(line + "\n")
            root.destroy()
                
        inputArea.insert(tk.END, "Enter the assembly code here")
        inputArea.bind("<Button-1>", clearTextContent)

        inputArea.bind("<Delete>", saveTextContent)

        root.mainloop()

def formatData() :
    content = []

    with open ("data.txt", "r") as f:

        f.seek(0)

        for line in f:
            if line.strip():
                content.append(line)

    contentIndex = 0
    while contentIndex < len(content):
        contentLine = content[contentIndex]

        courseBraces = ["Fall", "Spring", "Summer", "Student ID"]

        if any(course in contentLine for course in courseBraces):
            content[contentIndex-1] += "\n"

        contentIndex += 1

    content = content[:-2]
    content[-3] += "\n"
    content[-1] += "\n"
    content = "".join(content)
    
    with open ("data.txt", "w") as f:
        f.write(content)

def loadDataInfo() :
    with open ("data.txt", "r", encoding="utf-8") as f:
        nativeContent = f.readlines()

    parsedInformations = []
    subLine = []
    for line in nativeContent:
        if line[-1] == "\n" and len(line) < 2:
            parsedInformations.append(subLine)
            subLine = []
        else:
            subLine.append(line.rsplit("\n")[0])
        
    generalInfo = parsedInformations[0]
    studentInfo = parsedInformations[1]
    semesterInfos = parsedInformations[2:-1]
    
    return generalInfo, studentInfo, semesterInfos

def initializeData(generalInfo, studentInfo, semesterInfos) :
    class User() :
        
        def __init__(self, generalInfo, studentInfo) :
            self.initializeGeneralInfo(generalInfo)
            self.initializeStudentInfo(studentInfo)

        def initializeGeneralInfo(self, generalInfo):
            self.instution = generalInfo[0]
            self.ownerShip = generalInfo[1]
            self.creationDate = generalInfo[2]

        def initializeStudentInfo(self, studentInfo):
            self.studentID = studentInfo[0][11:20]
            self.nationalID = studentInfo[0][33:]
            self.name = studentInfo[1].replace("Name", "").replace("Surname", " ").replace("\t", "")
            self.facultyAndDepartment = studentInfo[2][studentInfo[2].find("\t")+1:studentInfo[2].find("Program")]
            self.programName = studentInfo[2][studentInfo[2].find("Program Name\t")+13:]
            self.languageOfInstitution = studentInfo[3][studentInfo[3].find("\t")+1:studentInfo[3].find("Student Status\t")-1]
            self.studentStatus = studentInfo[3][studentInfo[3].find("Student Status\t")+15:]

        def __str__(self) -> str:
            return "Instutition : {}, Ownership : {}, Creating Date : {}\nStudent ID : {}, National ID : {}\nName : {}\nFaculty and Department : {}, Program Name : {}\nLanguage of Institution : {}, Student Status : {}".format(self.instution, self.ownerShip, self.creationDate, self.studentID, self.nationalID, self.name, self.facultyAndDepartment, self.programName, self.languageOfInstitution, self.studentStatus)

        def getUser(self) :
            return self.instution, self.ownerShip, self.creationDate, self.studentID, self.nationalID, self.name, self.facultyAndDepartment, self.programName, self.languageOfInstitution, self.studentStatus
            
    allCourses = {}
    for currentSemester in semesterInfos :
        currentSemester = currentSemester[2:]
        for currentCourse in currentSemester :
            if currentCourse.startswith("Semester") or currentCourse.startswith("PREP") :
                break
            else :
                currentCourseName = currentCourse[:currentCourse.find("\t")].replace("*", "")
                allCourses[currentCourseName] = (currentCourse[currentCourse.find("\t")+1:].split("\t"))

    student = User(generalInfo, studentInfo)
    with open ("test.json", "w", encoding="utf-8") as f:
        json.dump(allCourses, f, indent=4)

    return student

def calculateCGPA() :
    
    with open ("test.json", "r", encoding="utf-8") as f:
        allCourses = json.load(f)

    totalQualityPoints = 0
    totalCreditHours = 0
    totalSuccessfulCreditHours = 0
    for courseValues in allCourses.values() :
        
        print(courseValues)
        if courseValues[-2] in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]:
            totalQualityPoints += float(courseValues[-1])
            totalCreditHours += int(courseValues[-3])
            totalSuccessfulCreditHours += int(courseValues[-3])
        elif courseValues[-2] == "I":
            continue
        elif courseValues[-2] == "W":
            totalSuccessfulCreditHours += int(courseValues[-3])

    print(totalQualityPoints/totalCreditHours)

getdata()
formatData()
generalInfo, studentInfo, semesterInfos = loadDataInfo()
studentObject = initializeData(generalInfo, studentInfo, semesterInfos)
calculateCGPA()