from Utilities import (
    Web, 
    By,
)
import json
from datetime import datetime

def retrieve_transcript(username, password) -> list:

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

    table_elements = client.browser.find_elements(By.TAG_NAME, "table")

    output = []
    for element in table_elements :
        output.append(element.text)

    client.browser.quit()

    return output

def parse_data(output) :

    # remove unnecessary elements
    uni = output.pop(0) # univercity info
    output.pop() # univercity address
    output.pop() # grading system

    if uni.startswith("MEF") :
        sis_language = "en"
    elif uni.startswith("T.C") :
        sis_language = "tr"

    date = output.pop(0) # date"""

    student_info = output.pop(0) # student info
    student_parse = student_info.split("\n")
    if sis_language == "en" :
        keywords = ["Student ID", "National ID"]
    elif sis_language == "tr" :
        keywords = ["Öğrenci Numarası", "TC Kimlik Numarası"]
    student_id = student_parse[0][
        student_parse[0].find(keywords[0]) + len(keywords[0]) + 1 
        :
        student_parse[0].find(keywords[1]) - 1
    ]
    national_id = student_parse[0][
        student_parse[0].find(keywords[1]) + len(keywords[1]) + 1
        :
    ]
    if sis_language == "en" :
        keywords = ["Name", "Surname"]
    elif sis_language == "tr" :
        keywords = ["Adı", "Soyadı"]
    student_name = student_parse[1][
        student_parse[1].find(keywords[0]) + len(keywords[0]) + 1
        :
        student_parse[1].find(keywords[1]) - 1
    ]
    student_surname = student_parse[1][
        student_parse[1].find(keywords[1]) + len(keywords[1]) + 1
        :
    ]
    if sis_language == "en" :
        keywords = ["Faculty / Department", "Program Name"]
    elif sis_language == "tr" :
        keywords = ["Fakülte", "Bölüm"]
    student_faculty = student_parse[2][
        student_parse[2].find(keywords[0]) + len(keywords[0]) + 1
        :
        student_parse[2].find(keywords[1]) - 1
    ]
    student_department = student_parse[2][
        student_parse[2].find(keywords[1]) + len(keywords[1]) + 1
        :
    ]
    if sis_language == "en" :
        keywords = ["Language of Instruction", "Student Status"]
    elif sis_language == "tr" :
        keywords = ["Eğitim Dili", "Öğrencilik Durumu"]
    language_of_instruction = student_parse[3][
        student_parse[3].find(keywords[0]) + len(keywords[0]) + 1
        :
        student_parse[3].find(keywords[1]) - 1
    ]
    student_status = student_parse[3][
        student_parse[3].find(keywords[1]) + len(keywords[1]) + 1
        :
    ]
    semesters = {}
    for index, current_course in enumerate(output) :

        prep = "PREP" in current_course
        semester = current_course.startswith("Semester Credits Attempted") or current_course.startswith("Dönem Alınan Kredi")
        student = "Student ID" in current_course or "Öğrenci Numarası" in current_course

        if prep or semester or student :
            continue

        semester_parse = current_course.split("\n")
        semester_name = semester_parse.pop(0)
        semester_parse.pop(0) # remove junk info (colum names)
        if "Academic Standing" in semester_parse[-1] or "Akademik Durum" in semester_parse[-1] :
            semester_parse.pop() # remove junk info (academic standing)
        cumulative_credits_attempted = semester_parse.pop()
        semester_credits_attempted = semester_parse.pop()
        course_list = semester_parse
        for course_index, course_info in enumerate(course_list) :

            course_info_parse = course_info.split(" ")
            course_code = course_info_parse.pop(0) + " " + course_info_parse.pop(0)
            course_name = " ".join(course_info_parse[:-4])
            course_lang = course_info_parse[-4]
            course_credit = course_info_parse[-3]
            course_grade = course_info_parse[-2]
            course_grade_point = course_info_parse[-1]

            course_list[course_index] = {
                "course_code" : course_code,
                "course_name" : course_name,
                "course_lang" : course_lang,
                "course_credit" : course_credit,
                "course_grade" : course_grade,
                "course_grade_point" : course_grade_point,
            }

        semesters[semester_name] = {
            "course_list" : course_list
        }

    output = {
        "parsing_type" : "online",
        "parsing_language" : sis_language,
        "transcript_manager_date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "transcript_creation_date" : date,
        "student_id" : student_id,
        "national_id" : national_id,
        "student_name" : student_name,
        "student_surname" : student_surname,
        "student_faculty" : student_faculty,
        "student_department" : student_department,
        "language_of_instruction" : language_of_instruction,
        "student_status" : student_status,
        "semesters" : semesters,
    }

    with open(f"{student_name}_online_{sis_language}.json", "w", encoding="utf-8") as file :
        json.dump(output, file, ensure_ascii=False, indent=4)

output = retrieve_transcript(
    username="",
    password="",
)
parse_data(output)