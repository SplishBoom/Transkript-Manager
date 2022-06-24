from    selenium.webdriver.chrome.service  import Service
from    selenium.webdriver.chrome.options  import Options
from    selenium.webdriver.common.by       import By
from    selenium                           import webdriver
import  os

def retrieveData(username, password, isHidden=False):

    mainUrl = "https://sis.mef.edu.tr/auth/login"

    class Web :

        def __init__(self, driverOptions, driverPath="Sources\chromedriver.exe") :
            self.browser = webdriver.Chrome(service=Service(executable_path=driverPath), options=driverOptions)

        def openWebPage(self,url) :
            self.browser.get(url)

        def createElement(self,xPath) :
            createdElement = None
            while (createdElement == None) :
                try :
                    createdElement = self.browser.find_element(By.XPATH, xPath)
                except :
                    continue
            return createdElement

        def clickOnElement(self, element) :
            while (True) :
                try :
                    element.click()
                    break
                except :
                    continue

        def checkIdSelection(self, dropdownXPATH=None, idSelectionXPATH=None) :
            dropDownMenu = self.createElement(dropdownXPATH)
            
            checkList = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
            flag = False
            for dpElement in dropDownMenu.find_elements(by=By.TAG_NAME, value="a") :
                
                if dpElement.text in checkList :
                    
                    self.clickOnElement(dpElement)

                    idSelectionMenu = self.createElement(idSelectionXPATH)

                    for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
                        if element.get_attribute("text").split("-")[-1].strip() in checkList :

                            self.clickOnElement(element)
                            flag = True
                            break
                    break
                    
            if flag:
                continueButton = self.createElement("/html/body/div[3]/input")
                self.clickOnElement(continueButton)

    if isHidden :
        driverOptions = Options()
        driverOptions.add_argument("--headless")
    else :
        driverOptions = Options()

    client = Web(driverOptions)

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

    with open (os.path.abspath("transcriptText.txt"), "w", encoding="utf-8") as file :
        file.write(transkriptText)
