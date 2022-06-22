import  requests
import  shutil
import  json
import  os

def secureStart(passed=False) :
    neccessaryFolders = ("Assets", "GUI", "Sources", "Util")

    for folder in neccessaryFolders:
        if not os.path.exists(os.path.abspath(folder)):
            print("Folder " + folder + " not found. Terminating application...")
            exit()

    if not passed :
        try :
            os.makedirs(os.path.abspath("Temp"))
        except :
            shutil.rmtree(os.path.abspath("Temp"))
            os.makedirs(os.path.abspath("Temp"))
        
def secureFinish(passed=False) :
    if passed :
        unncessaryFolders = ("Util/__pycache__", "GUI/__pycache__")
    else :
        unncessaryFolders = ("Temp", "Util/__pycache__", "GUI/__pycache__")

    for unncessaryFolder in unncessaryFolders:
        try :
            shutil.rmtree(os.path.abspath(unncessaryFolder))
        except :
            pass

def authenticate(username, password) :

    logUrl = "https://sis.mef.edu.tr/auth/login/ln/tr"
    secUrl = "https://sis.mef.edu.tr/"

    payload = {"kullanici_adi": username, "kullanici_sifre": password}
    
    with requests.Session() as s:
        s.post(logUrl, data=payload)
        r = s.get(secUrl)

        if r.url == secUrl:
            return True

    return False

def sortTrJsonDataByElement(element, isReverse=False) :

    with open(os.path.abspath("Temp/transcriptData.json"), "r") as f:
        jsonDataIn = json.load(f)

    allCourses = []

    for currentCourseCode in jsonDataIn :
        currentCourseValues = jsonDataIn[currentCourseCode]
        currentCourseValues.insert(0, currentCourseCode)
        allCourses.append(currentCourseValues)

    if type(element) != type(int()) :
        elementId = {"Course Code":0, "Course Name":1, "Course Language":2, "Course ETCS":3, "Course Notation":4, "Course Grade":5, "Course Date":6}[element]
    else :
        elementId = element

    allCourses.sort(key=lambda x: x[elementId], reverse=isReverse)

    jsonDataOut = {}
    for currentCourseList in allCourses :
        currentCourseCode = currentCourseList[0]
        currentCourseValues = currentCourseList[1:]
        jsonDataOut[currentCourseCode] = currentCourseValues

    with open(os.path.abspath("Temp/transcriptData.json"), "w") as f:
        json.dump(jsonDataOut, f, indent=4)
