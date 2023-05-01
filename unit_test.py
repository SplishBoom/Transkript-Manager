from Utilities import Web, By

language = "turkish"
mode = "online"

main_url = "file:///C:/GithubProjects/transkript-manager/Data/online%20turkish.html"

client = Web(isHidden=False)
client.open_web_page(main_url)

inputField = client.create_element("//*[@id=\"kullanici_adi\"]")
inputField.send_keys("memise")

passwordField = client.create_element("//*[@id=\"kullanici_sifre\"]")
passwordField.send_keys("Ee67456133140!")

loginButton = client.create_element("//*[@id=\"loginForm\"]/div[2]/div[3]/button")
loginButton.click()

continueButton = client.create_element("/html/body/div[3]/input")
continueButton.click()

profileSelection = client.create_element("/html/body/div[2]/div/div[3]/ul/li")
profileSelection.click()

dropDownMenu = client.create_element("/html/body/div[2]/div/div[3]/ul/li/ul")
checkList = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
flag = False
for dpElement in dropDownMenu.find_elements(by=By.TAG_NAME, value="a") :
    if dpElement.text in checkList :
        client.click_on_element(dpElement)
        idSelectionMenu = client.create_element("//*[@id=\"yetkiDegistir\"]/div/ul")
        for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
            if element.get_attribute("text").split("-")[-1].strip() in checkList :
                client.click_on_element(element)
                flag = True
                break
        break
if flag:
    continueButton = client.create_element("/html/body/div[3]/input")
    client.click_on_element(continueButton)

transkriptUrl = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
client.openWebPage(transkriptUrl)

transkriptText = client.browser.find_element(By.TAG_NAME, "body").text

client.browser.quit()

with open("output.txt", "w", encoding="utf-8") as file :
    file.write(transkriptText)