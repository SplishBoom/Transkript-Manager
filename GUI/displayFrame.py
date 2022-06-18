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

        self.calculateCGPA(isInit=True)

        self.updateCGPA("MATH 115", "A")
        self.updateCGPA("MATH 224", "A")
        self.updateCGPA("EE 212", "A")
        self.updateCGPA("MATH 108", "A")
        self.updateCGPA("EE 203", "A")
        self.updateCGPA("COMP 206", "A")
        self.updateCGPA("ENG 101", "A")
        self.updateCGPA("ENGR 301", "A")
        self.resetCGPA()
        print(self.CGPA)

    def loadData(self, isReset=False, isInit=False):
        
        if isInit :
            with open ("Temp/transkriptData.json", "r", encoding="utf-8") as f :
                self.allCourses = json.load(f)
            with open ("Temp/transkriptDataSave.json", "w", encoding="utf-8") as f :
                json.dump(self.allCourses, f, ensure_ascii=False, indent=4)
        else :
            if isReset :
                with open ("Temp/transkriptDataSave.json", "r", encoding="utf-8") as f :
                    self.allCourses = json.load(f)
            else :    
                with open ("Temp/transkriptData.json", "r", encoding="utf-8") as f :
                    self.allCourses = json.load(f)

    def uploadData(self) :
        with open ("Temp/transkriptData.json", "w", encoding="utf-8") as f :
            json.dump(self.allCourses, f, ensure_ascii=False, indent=4)

    def calculateCGPA(self, isReset=False, isInit=False) :

        self.totalQualityPoints = 0
        self.totalCredits = 0
        self.totalSuccessfulCredits = 0
        self.CGPA = 0

        self.loadData(isReset=isReset, isInit=isInit)

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
        courseValues[-2] = weight * float(courseValues[-4])

        self.allCourses[courseCode] = courseValues

        self.uploadData()

        self.calculateCGPA()

    def resetCGPA(self) :
        self.calculateCGPA(isReset=True)