from Utilities import (
    Web, 
    By,
)
from Constants import (
    password,
    username,
)

main_url = "file:///C:/GithubProjects/transkript-manager/Data/online%20turkish.html"
main_url = "https://sis.mef.edu.tr/auth/login"

client = Web(isHidden=False)
client.open_web_page(main_url)

username_entry = client.create_element("//*[@id=\"kullanici_adi\"]")
username_entry.send_keys(username)

password_entry = client.create_element("//*[@id=\"kullanici_sifre\"]")
password_entry.send_keys(password)

login_button = client.create_element("//*[@id=\"loginForm\"]/div[2]/div[3]/button")
login_button.click()

continue_button = client.create_element("/html/body/div[3]/input")
continue_button.click()

profile_selection_label = client.create_element("/html/body/div[2]/div/div[3]/ul/li")
profile_selection_label.click()

drop_down_menu = client.create_element("/html/body/div[2]/div/div[3]/ul/li/ul")
check_list = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
flag = False
for current_element in drop_down_menu.find_elements(by=By.TAG_NAME, value="a") :
    if current_element.text in check_list :
        client.click_on_element(current_element)
        idSelectionMenu = client.create_element("//*[@id=\"yetkiDegistir\"]/div/ul")
        for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
            if element.get_attribute("text").split("-")[-1].strip() in check_list :
                client.click_on_element(element)
                flag = True
                break
        break
if flag:
    continue_button = client.create_element("/html/body/div[3]/input")
    client.click_on_element(continue_button)

transkriptUrl = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
client.open_web_page(transkriptUrl)

transkriptText = client.browser.find_element(By.TAG_NAME, "body").text

client.browser.quit()

with open("output.txt", "w", encoding="utf-8") as file :
    file.write(transkriptText)