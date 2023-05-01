from    selenium.webdriver.chrome.service  import Service
from    selenium.webdriver.chrome.options  import Options
from    selenium.webdriver.common.by       import By
from    selenium                           import webdriver
import  os

def retrieveData(username, password, isHidden=False):

    mainUrl = "https://sis.mef.edu.tr/auth/login"

    if isHidden :
        driverOptions = Options()
        driverOptions.add_argument("--headless")
    else :
        driverOptions = Options()

    fileName = "chromedriver"
    fileExtension = ".exe"
    fileFolder = "Sources"
    filePath = os.path.abspath(fileFolder+"/"+fileName+fileExtension)
    os.chmod(filePath, 755)
    client = Web(driverOptions, driverPath=filePath)

    client.openWebPage(mainUrl)

    inputField = client.createElement("//*[@id=\"kullanici_adi\"]")
    inputField.send_keys(username)

    passwordField = client.createElement("//*[@id=\"kullanici_sifre\"]")
    passwordField.send_keys(password)

    loginButton = client.createElement("//*[@id=\"loginForm\"]/div[2]/div[3]/button")
    loginButton.click()

    continueButton = client.createElement("/html/body/div[3]/input")
    continueButton.click()
    
    profileSelection = client.createElement("/html/body/div[2]/div/div[3]/ul/li")
    profileSelection.click()

    client.checkIdSelection(dropdownXPATH="/html/body/div[2]/div/div[3]/ul/li/ul", idSelectionXPATH="//*[@id=\"yetkiDegistir\"]/div/ul")

    leftMenuButton = client.createElement("//*[@id=\"left-menu7\"]")
    leftMenuButton.click()

    transkriptUrl = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
    client.openWebPage(transkriptUrl)

    transkriptText = client.browser.find_element(By.TAG_NAME, "body").text

    client.browser.quit()

    with open (os.path.abspath("Temp/transcriptText.txt"), "w", encoding="utf-8") as file :
        file.write(transkriptText)
