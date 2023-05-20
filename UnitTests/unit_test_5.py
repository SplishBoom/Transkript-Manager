"""
UT : data functions
"""

import json

current_user_info_document_mongo_export_path = ""
current_user_data_document_mongo_export_path = ""

with open(current_user_info_document_mongo_export_path, "r") as f:
    current_user_info_document = json.load(f)

with open(current_user_data_document_mongo_export_path, "r") as f:
    current_user_data_document = json.load(f)

language_of_instruction = current_user_info_document["language_of_instruction"]
student_department = current_user_info_document["student_department"]
student_faculty = current_user_info_document["student_faculty"]
student_name = current_user_info_document["student_name"]
student_school_id = current_user_info_document["student_school_id"]
student_national_id = current_user_info_document["_id"]
student_status = current_user_info_document["student_status"]
student_surname = current_user_info_document["student_surname"]

owner_id = current_user_data_document["owner_id"]
parsing_type = current_user_data_document["parsing_type"]
parsing_language = current_user_data_document["parsing_language"]
transcript_manager_date = current_user_data_document["transcript_manager_date"]
transcript_creation_date = current_user_data_document["transcript_creation_date"]
semesters = current_user_data_document["semesters"]
original_course_list = current_user_data_document["original_course_list"]
filtering = current_user_data_document["filtering"]
sorting = current_user_data_document["sorting"]
modified_course_list = current_user_data_document["modified_course_list"]
document_name = current_user_data_document["document_name"]
subtracted_course_list = current_user_data_document["subtracted_course_list"]
added_course_list = current_user_data_document["added_course_list"]


def _validate_inpu_key(key):
    if key not in ["course_code", "course_name", "course_lang", "course_credit", "course_grade", "course_grade_point"]:
        raise ValueError("Invalid sort key")
        
def sort_by(given_course_list, sort_key, should_reverse=False):
    _validate_inpu_key(sort_key)
    course_list = given_course_list.copy()
    course_list.sort(key=lambda x: x[sort_key], reverse=should_reverse)
    return course_list

def filter_by(given_course_list, filter_key, filter_value):
    _validate_inpu_key(filter_key)
    course_list = given_course_list.copy()
    course_list = list(filter(lambda x: x[filter_key] == filter_value, course_list))
    return course_list

def add_course(given_course_list, course_code, course_name, course_lang, course_credit, course_grade, course_grade_point):
    course_list = given_course_list.copy()
    result = filter_by(course_list, "course_code", course_code)
    n = 1
    while result:
        course_code = course_code + " (" + str(n) + ")"
        result = filter_by(course_list, "course_code", course_code)
        n += 1
    new_course ={
        "course_code": course_code,
        "course_name": course_name,
        "course_lang": course_lang,
        "course_credit": course_credit,
        "course_grade": course_grade,
        "course_grade_point": course_grade_point
    }
    course_list.append(new_course)
    return course_list

def subtract_course(given_course_list, course_code):
    course_list = given_course_list.copy()
    result = filter_by(course_list, "course_code", course_code)
    if not result:
        return course_list
    else:
        course_list = list(filter(lambda x: x["course_code"] != course_code, course_list))
        return course_list

def update_course(given_course_list, course_code, course_name, course_lang, course_credit, course_grade, course_grade_point):
    # The code is defining a function that takes a list of dictionaries as input and filters the list
    # based on a given course code. If the course code is not found in the list, the original list is
    # returned. If the course code is found, the function removes the dictionary with that course code
    # from the list and adds a new dictionary with the given course information. The updated list is
    # then returned.
    course_list = given_course_list.copy()
    result = filter_by(course_list, "course_code", course_code)
    if not result:
        return course_list
    else:
        course_list = list(filter(lambda x: x["course_code"] != course_code, course_list))
        course_list = add_course(course_list, course_code, course_name, course_lang, course_credit, course_grade, course_grade_point)
        return course_list

def calculate_gpa(course_list):
    """
    This function calculates the GPA based on the given course list.
    """

    credits_attempted = 0
    credits_successful = 0
    credits_included_in_gpa = 0
    gpa = 0

    for course in course_list:
        course_credit : int = int(course["course_credit"])
        course_grade : str = course["course_grade"]
        course_grade_point : float = float(course["course_grade_point"])

        credits_attempted += course_credit

        if course_grade in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D"]:
            credits_successful += course_credit
            credits_included_in_gpa += course_credit
            gpa += course_grade_point
        elif course_grade in ["S"]:
            credits_successful += course_credit
        elif course_grade == "F" or course_grade == "U":
            credits_included_in_gpa += course_credit
            gpa += course_grade_point
        elif course_grade == "I":
            continue
        elif course_grade == "W":
            credits_attempted -= course_credit
        elif course_grade == "N/A":
            continue

    if credits_included_in_gpa == 0:
        gpa = 0
    else :
        gpa = gpa / credits_included_in_gpa
    
    gpa = round(gpa, 2)

    return (
        credits_attempted,
        credits_successful,
        credits_included_in_gpa,
        gpa
    )


course_list = semesters["semester_1"]["course_list"]

course_list = sort_by(course_list, "course_code")
course_list = sort_by(course_list, "course_grade")
course_list = sort_by(course_list, "course_grade", should_reverse=True)

course_list = semesters["semester_5"]["course_list"]

course_list = filter_by(course_list, "course_lang", "EN")
course_list_2 = filter_by(course_list, "course_grade", "A")

filtering = [
    ("course_lang", "EN"),
    ("course_grade", "A"),
    ("course_code", "COMP 110")
]
sorting = [
    ("course_code", False),
    ("course_grade", True),
]