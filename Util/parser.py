import  json
import  os

def segmentAndCreateJsons() :

    with open("Temp/transcriptText.txt", "r", encoding="utf-8") as f:
        textInput = f.read()
    
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
        semesterBraces = ["Fall", "Spring", "Summer", "Course Code", "Semester", "Cumulative", "Academic Standing", "Student ID", "Name", "Faculty", "Language of Instruction"]
    elif trannnskriptLanguage == "Turkish":
        textInput = textInput[4:]
        semesterBraces = ["Güz", "Bahar", "Yaz", "Ders Kodu", "Dönem Alınan", "Genel Alınan", "Akademik Durum", "Öğrenci Numarası", "Adı", "Fakülte", "Eğitim Dili"]

    studentInfo = textInput[:4]
    textInput = textInput[4:]
        
    xCleaned = []
    for line in textInput :
        if not any(semesterBraces in line for semesterBraces in semesterBraces):
            xCleaned.append(line)

    allCourses = {}
    courseIndex = 0
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

        allCourses[courseCode] = [courseName, courseLanguage, courseEtcs, courseNotation, courseGrade, courseIndex]

        courseIndex += 1
        
    # create temp folder if not exists
    if not os.path.exists("Temp"):
        os.makedirs("Temp")

    with open ("Temp/transcriptData.json", "w", encoding="utf-8") as f:
        json.dump(allCourses, f, indent=4)
    with open ("Temp/transcriptDataInit.json", "w", encoding="utf-8") as f:
        json.dump(allCourses, f, indent=4)

    studentID = studentInfo[0][studentInfo[0].find("0"):studentInfo[0].find("0")+9]
    nationalID = studentInfo[0][-11:]
    if trannnskriptLanguage == "English":
        studentName = studentInfo[1][5:studentInfo[1].find("Surname")-1]
        studentSurname = studentInfo[1][studentInfo[1].find("Surname")+8:]
        facultyAndDepartment = studentInfo[2][21:studentInfo[2].find("Program Name")-1]
        programName = studentInfo[2][studentInfo[2].find("Program Name")+13:]
        languageOfInstution = studentInfo[3][studentInfo[3].find("Language of Instruction")+24:studentInfo[3].find("Student")-1]
        studentStatus = studentInfo[3][studentInfo[3].find("Student")+15:]
    else :
        studentName = studentInfo[1][4:studentInfo[1].find("Soyadı")-1]
        studentSurname = studentInfo[1][studentInfo[1].find("Soyadı")+7:]
        facultyAndDepartment = studentInfo[2][studentInfo[2].find("Fakülte")+8:studentInfo[2].find("Bölüm")-1]
        programName = studentInfo[2][studentInfo[2].find("Bölüm")+6:]
        languageOfInstution = studentInfo[3][studentInfo[3].find("Dil")+5:studentInfo[3].find("Öğrenci")-1]
        studentStatus = studentInfo[3][studentInfo[3].find("Öğrenci")+18:]

    with open ("Temp/studentData.json", "w", encoding="utf-8") as f:
        json.dump([studentID, nationalID, studentName, studentSurname, facultyAndDepartment, programName, languageOfInstution, studentStatus], f, ensure_ascii=False, indent=4)