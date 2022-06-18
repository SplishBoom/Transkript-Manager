from    selenium.webdriver.chrome.service  import Service
from    selenium.webdriver.chrome.options  import Options
from    selenium.webdriver.common.by       import By
from    selenium                           import webdriver

def retrieveData(username, password, isHidden=False):

    mainUrl = "https://sis.mef.edu.tr/auth/login"

    class Web :

        def __init__(self, driverOptions, driverPath="Sources\chromedriver.exe") :
            self.browser = webdriver.Chrome(service=Service(executable_path=driverPath), options=driverOptions)

        def openWebPage(self,url) :
            self.browser.get(url)

        def createElement(self,xPath) :
            if type(xPath) == str :
                createdElement = None
                while (createdElement == None) :
                    try :
                        createdElement = self.browser.find_element(By.XPATH, xPath)
                    except :
                        continue
                return createdElement
            else :
                createdElement = None
                while (createdElement == None) :
                    for xpath in xPath :
                        try :
                            createdElement = self.browser.find_element(By.XPATH, xPath)
                            break
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

    leftMenuButton = client.createElement("//*[@id=\"left-menu7\"]")
    leftMenuButton.click()

    transkriptUrl = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
    client.openWebPage(transkriptUrl)

    transkriptText = client.browser.find_element(By.TAG_NAME, "body").text

    client.browser.quit()

    with open ("Temp/transkripText.txt", "w", encoding="utf-8") as file :
        file.write(transkriptText)
        