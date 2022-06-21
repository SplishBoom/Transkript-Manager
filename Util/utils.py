import  os
import shutil
import json
import requests

def secureStart() :
    os.system("cls")
    
    neccessaryFolders = ("Assets", "GUI", "Sources", "Util")

    for folder in neccessaryFolders:
        if not os.path.exists(folder):
            print("Folder " + folder + " not found. Terminating application...")
            exit()

    """try :
        os.makedirs("Temp")
    except :
        shutil.rmtree("Temp")
        os.makedirs("Temp")"""
        
def secureFinish() :

    unncessaryFolders = ("Temp", "Util/__pycache__", "GUI/__pycache__")

    for unncessaryFolder in unncessaryFolders:
        try :
            shutil.rmtree(unncessaryFolder)
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

    with open("Temp/transcriptData.json", "r") as f:
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

    with open("Temp/transcriptData.json", "w") as f:
        json.dump(jsonDataOut, f, indent=4)
