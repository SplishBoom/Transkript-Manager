from Utilities import (
    Web, 
    By,
)
import json

file_link = "file:///C:/GithubProjects/transkript-manager/Data/online/online%20english.html"

client = Web(isHidden=False)
client.open_web_page(file_link)

table_elements = client.browser.find_elements(By.TAG_NAME, "table")

jj = {}
for num, element in enumerate(table_elements) :
    jj[num] = element.text

client.browser.quit()


with open("output.json", "w", encoding="utf-8") as file :
    json.dump(jj, file, indent=4, ensure_ascii=False)