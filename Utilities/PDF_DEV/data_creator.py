from DIRECT_EXECUTION import (
    sort_by,
    filter_by,
    add_course,
    subtract_course,
    update_course,
    calculate_performance
)
import json

def load_data() :

    with open(r"DIRECT_EXECUTION\user_info_in.json", "r", encoding="utf-8") as f:
        user_info_document = json.load(f)
    with open(r"DIRECT_EXECUTION\user_data_in.json", "r", encoding="utf-8") as f:
        user_data_document = json.load(f)

    return (
        user_info_document,
        user_data_document
    )

def save_data(user_info_document, user_data_document) :

    with open(r"DIRECT_EXECUTION\user_info_out.json", "w", encoding="utf-8") as f:
        json.dump(user_info_document, f, indent=4)
    with open(r"DIRECT_EXECUTION\user_data_out.json", "w", encoding="utf-8") as f:
        json.dump(user_data_document, f, indent=4)


if __name__ == "__main__" :
        
    if True : # LOAD INITIAL DATA
        user_info_document, user_data_document = load_data()

        language_of_instruction = user_info_document["language_of_instruction"]
        student_department = user_info_document["student_department"]
        student_faculty = user_info_document["student_faculty"]
        student_name = user_info_document["student_name"]
        student_school_id = user_info_document["student_school_id"]
        student_national_id = user_info_document["_id"]
        student_status = user_info_document["student_status"]
        student_surname = user_info_document["student_surname"]
        
        owner_id = user_data_document["owner_id"]
        parsing_type = user_data_document["parsing_type"]
        parsing_language = user_data_document["parsing_language"]
        transcript_manager_date = user_data_document["transcript_manager_date"]
        transcript_creation_date = user_data_document["transcript_creation_date"]
        semesters = user_data_document["semesters"]
        original_course_list = user_data_document["original_course_list"]
        filtering = user_data_document["filtering"]
        sorting = user_data_document["sorting"]
        modified_course_list = user_data_document["modified_course_list"]
        document_name = user_data_document["document_name"]
        updated_course_list = user_data_document["updated_course_list"]
        subtracted_course_list = user_data_document["subtracted_course_list"]
        added_course_list = user_data_document["added_course_list"]

    if True : # SETUP
        
        filtering = [
            {
                "filter_key" : "course_lang",
                "filter_value" : "EN",
            },
            {
                "filter_key" : "course_grade",
                "filter_value" : "A",
            },
        ]

        sorting = {
            "sort_key" : "course_grade",
            "should_reverse" : True,
        }

        courses_to_subtract = [
            {
                "course_code" : "COMP 100",
                "course_name" : "Introduction to Computer Engineering",
                "course_lang" : "en",
                "course_credit" : 3,
                "course_grade" : "A",
                "course_grade_point" : 4.0,
            },
            {
                "course_code" : "COMP 109",
                "course_name" : "Introduction to Computer Engineering Lab",
                "course_lang" : "en",
                "course_credit" : 1,
                "course_grade" : "A",
                "course_grade_point" : 4.0,
            },
        ]

        courses_to_add = [
            {
                "course_code" : "DENEME 100",
                "course_name" : "Deneme deneme 1 1 1 1",
                "course_lang" : "en",
                "course_credit" : 99,
                "course_grade" : "X",
                "course_grade_point" : 99.9,
            },
            {
                "course_code" : "DENEME 101",
                "course_name" : "Deneme deneme 2 2 2 2",
                "course_lang" : "en",
                "course_credit" : 99,
                "course_grade" : "X",
                "course_grade_point" : 99.9,
            }
        ]

        courses_to_update = [
            {
                "course_code" : "MATH 115",
                "course_name" : "BAM BAM BİRAM BAM Bİ RAM BAM",
                "course_lang" : "en",
                "course_credit" : 2,
                "course_grade" : "A",
                "course_grade_point" : 1.0,
            },
            {
                "course_code" : "EE 203",
                "course_name" : "SERKAN ELEKTALAR KOLTUGUN ALTINDA KALIP BENI ARA",
                "course_lang" : "ARABIC",
                "course_credit" : 10,
                "course_grade" : "F",
                "course_grade_point" : 99.9,
            }
        ]
    
    if True : # EXECUTE
        
        for current_filter in filtering :
            modified_course_list = filter_by(modified_course_list, current_filter)

        modified_course_list = sort_by(modified_course_list, sorting)

        for current_course in courses_to_subtract :
            modified_course_list = subtract_course(modified_course_list, current_course["course_code"])
            subtracted_course_list.append(current_course)

        for current_course in courses_to_add :
            modified_course_list = add_course(modified_course_list, current_course)
            added_course_list.append(current_course)

        for current_course in courses_to_update :
            modified_course_list = update_course(modified_course_list, current_course)
            updated_course_list.append(current_course)

    if True : # SAVE DATA

        user_data_document["filtering"] = filtering
        user_data_document["sorting"] = sorting
        user_data_document["modified_course_list"] = modified_course_list
        user_data_document["updated_course_list"] = updated_course_list
        user_data_document["subtracted_course_list"] = subtracted_course_list
        user_data_document["added_course_list"] = added_course_list

        save_data(user_info_document, user_data_document)