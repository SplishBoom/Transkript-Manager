import  os
import shutil

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