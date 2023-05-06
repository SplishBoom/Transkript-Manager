import PyPDF2 as ppdf

import json
from datetime import datetime

def retrieve_transcript(path_to_file) -> list:

    pdf_file = ppdf.PdfReader(path_to_file)

    output = []
    for current_page in pdf_file.pages :
        current_page_text = current_page.extract_text()
        current_page_elements = current_page_text.split("\n")
        output.extend(current_page_elements)

    return output

def parse_data(output) :

    # remove unnecessary elements
    if "T.C" in output[0] :
        output.pop(0) # T.C
        sis_language = "tr"
    else :
        sis_language = "en"
    output.pop(0) # univercity info
    output.pop(0) # univercity info
    for i in range(31) :
        output.pop() # removing unneccessary elements

    date = output.pop(0) # date

    output.pop(0)
    student_id = output.pop(0) # student id
    output.pop(0)
    national_id = output.pop(0) # national id
    output.pop(0)
    student_name = output.pop(0) # student name
    output.pop(0)
    student_surname = output.pop(0) # student surname
    output.pop(0)
    student_faculty = output.pop(0) # student department
    output.pop(0)
    student_department = output.pop(0) # student program
    output.pop(0)
    language_of_instruction = output.pop(0) # language of instruction
    output.pop(0)
    student_status = output.pop(0) # student status

    splitters = [
        "Fall Semester", "Spring Semester", "Summer School", "Fall Dönemi", "Spring Dönemi"
    ]
    founded_semesters = []
    temp = [output.pop(0)]
    for current_string in output :
        checker = " ".join(current_string.split(" ")[1:])

        if checker in splitters :
            founded_semesters.append(temp)
            temp = [current_string]
        else :
            temp.extend([current_string])

    # clean prep semesters
    clean_index = []
    for semester_index, current_semester in enumerate(founded_semesters) :
        if "Prep" in current_semester :
            clean_index.append(semester_index)

    for index in reversed(clean_index) :
        founded_semesters.pop(index)
    
    semesters = {}
    for semester_index, current_semester in enumerate(founded_semesters) :
        
        semester_name = current_semester.pop(0)

        # remove junk info from each semester
        if current_semester[0] == "Course Code" :
            count = 7
        elif current_semester[0] == "Ders Kodu" :
            count = 6
        for i in range(count) :
            current_semester.pop(0)

        courses = []
        temp = {}
        add_count = 1
        map_hash = {
            1 : "course_code",
            2 : "course_name",
            3 : "course_lang",
            4 : "course_credit",
            5 : "course_grade",
            6 : "course_grade_point"
        }
        for current_string in current_semester :
            if current_string == "Semester" or current_string == "Dönem":
                break
            
            if add_count == 7 :
                courses.append(temp)
                temp = {}
                add_count = 1

            temp[map_hash[add_count]] = current_string
            add_count += 1

        courses.append(temp)

        semesters[semester_name] = {
            "course_list" : courses
        }
            
    output = {
        "parsing_type" : "offline",
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
        "semesters" : semesters
    }

    with open(f"{student_name}_offline_{sis_language}.json", "w", encoding="utf-8") as file :
        json.dump(output, file, ensure_ascii=False, indent=4)