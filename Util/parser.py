import json

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

    return [studentID, nationalID, studentName, studentSurname, facultyAndDepartment, programName, languageOfInstution, studentStatus]