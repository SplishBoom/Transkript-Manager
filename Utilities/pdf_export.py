from Environment import ASSETS_DC, to_turkish

def calculate_performance(course_list):
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

	return {
		"credits_attempted" : credits_attempted,
		"credits_successful" : credits_successful,
		"credits_included_in_gpa" : credits_included_in_gpa,
		"gpa" : gpa
	}

def _get_text(text, parsing_language) :
    if parsing_language == "tr" :
        return to_turkish[text]
    else :
        return text

def generate_pdf(user_info_document : dict, user_data_document : dict, user_photo_path : str, output_file_path : str) :
    
    mef_logo_path = ASSETS_DC.LOGO_PATH

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
    subtracted_course_list = user_data_document["subtracted_course_list"]
    added_course_list = user_data_document["added_course_list"]