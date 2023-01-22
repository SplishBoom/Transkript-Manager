from    win32com.client import Dispatch
from    bs4             import BeautifulSoup
import  requests
import  zipfile
import  shutil
import  json
import  os
import  io

WHITE_COLOR = "#{:02x}{:02x}{:02x}".format(255, 255, 255)
BLACK_COLOR = "#{:02x}{:02x}{:02x}".format(0, 0, 0)
RED_COLOR = "#{:02x}{:02x}{:02x}".format(255, 0, 0)
BLUE_COLOR = "#{:02x}{:02x}{:02x}".format(152, 193, 217)
GREEN_COLOR = "#{:02x}{:02x}{:02x}".format(9, 227, 163)
PBLUE_COLOR = "#{:02x}{:02x}{:02x}".format(239, 247, 246)
PINK_COLOR = "#{:02x}{:02x}{:02x}".format(253, 112, 164)
ORANGE_COLOR = "#{:02x}{:02x}{:02x}".format(253, 146, 46)
YELLOW_COLOR = "#{:02x}{:02x}{:02x}".format(217, 243, 78)
PURPLE_COLOR = "#{:02x}{:02x}{:02x}".format(61, 90, 128)
DARK_BACKGROUND_COLOR = "#{:02x}{:02x}{:02x}".format(223, 227, 233)
LIGHT_BACKGROUND2_COLOR = "#{:02x}{:02x}{:02x}".format(232, 240, 254)

def _checkDriver() :
    if not os.path.exists("../Sources/chromedriver.exe") :
        print("ChromeDriver not found !")
        print("Downloading ChromeDriver ...")
    else :
        exit()

    parser = Dispatch("Scripting.FileSystemObject")

    try :
        versionStart = parser.GetFileVersion(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    except :
        try :
            versionStart = parser.GetFileVersion(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        except :
            print("Chrome not found !")
            exit()

    versionStart = versionStart.split(".")[0]

    pathToSave = "Sources"

    downurl = "https://chromedriver.chromium.org/downloads"

    response = requests.get(downurl)

    soup = BeautifulSoup(response.text, "html.parser")

    versions = soup.find_all("a", class_="XqQF9c")

    for currentVersion in versions :

        if currentVersion.text.split(" ")[1].startswith(versionStart) :
            officialVersion = currentVersion.text.split(" ")[1]
            break       

    url = f"https://chromedriver.storage.googleapis.com/{officialVersion}/chromedriver_win32.zip"

    response = requests.get(url)
    zipFile = zipfile.ZipFile(io.BytesIO(response.content))
    zipFile.extractall(pathToSave)

def secureStart(passed=False) :
    neccessaryFolders = ("Assets", "GUI", "Util")

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

    if not os.path.exists(os.path.abspath("Sources")) :
        os.makedirs(os.path.abspath("Sources"))

    if not passed :
        try :
            os.makedirs(os.path.abspath("Data Export"))
        except :
            shutil.rmtree(os.path.abspath("Data Export"))
            os.makedirs(os.path.abspath("Data Export"))

    _checkDriver()
        
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
