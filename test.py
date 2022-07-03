fileName = "icon"
fileExtension = ".ico"
fileFolder = "Assets"

import os

filePath = os.path.abspath(fileFolder+"/"+fileName+fileExtension)

file = open(filePath, "rb")