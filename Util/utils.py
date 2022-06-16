import  os
import shutil

import requests

def secureStart() :
    neccessaryFolders = ("Assets", "GUI", "Sources", "Util")

    for folder in neccessaryFolders:
        if not os.path.exists(folder):
            print("Folder " + folder + " not found. Terminating application...")
            exit()

    if os.path.exists("Temp"):
        shutil.rmtree("Temp")
        os.makedirs("Temp")

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