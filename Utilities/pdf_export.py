from Environment import	ASSETS_DC, to_turkish # -> Environment variables

def calculate_performance(course_list : list) -> dict:
	"""
	The function calculates the GPA, credits attempted, credits successful and credits included in GPA based on the given course list.
	@Parameters:
		course_list - Required : List of dict courses (list) -> Used to calculate GPA
	@Returns:
		(dict) : Dictionary of calculated GPA, credits attempted, credits successful and credits included in GPA
	"""

	# Initialize variables
	credits_attempted = 0
	credits_successful = 0
	credits_included_in_gpa = 0
	gpa = 0

	# Iterate over courses
	for course in course_list:
		# Get course variables
		course_credit : int = int(course["course_credit"])
		course_grade : str = course["course_grade"]
		course_grade_point : float = float(course["course_grade_point"])

		# Update credits attempted for each course seen
		credits_attempted += course_credit

		# Start calculating GPA
		if course_grade in ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D"]:
			# If course is successful, update credits successful and credits included in GPA
			credits_successful += course_credit
			credits_included_in_gpa += course_credit
			gpa += course_grade_point
		elif course_grade in ["S"]:
			# If course is passed, update credits successful only
			credits_successful += course_credit
		elif course_grade == "F" or course_grade == "U":
			# If course is failed, update credits included in GPA
			credits_included_in_gpa += course_credit
			gpa += course_grade_point
		elif course_grade == "I":
			# If course is incomplete, do not do anything
			continue
		elif course_grade == "W":
			# If course is withdrawn, update credits attempted only
			credits_attempted -= course_credit
		elif course_grade == "N/A":
			# If course is not taken, do not do anything
			continue

	# To double check for division by zero error
	if credits_included_in_gpa == 0:
		gpa = 0
	else :
		gpa = gpa / credits_included_in_gpa
	
	# Round GPA to 2 decimal places
	gpa = round(gpa, 2)

	# Return calculated values
	return {
		"credits_attempted" : credits_attempted,
		"credits_successful" : credits_successful,
		"credits_included_in_gpa" : credits_included_in_gpa,
		"gpa" : gpa
	}

def _get_text(text : str, parsing_language : str) -> str:
    """
	This function returns the text in the given language.
	@Parameters:
		text - Required : The text to be translated. (str) -> Used to be translated.
		parsing_language - Required : The language of the text. (str) -> Used to find the language of the text.
	@Returns:
		translated_text - The translated text. (str)
	"""
	# If the language is Turkish, return the Turkish version of the text.
    if parsing_language == "tr" :
        return to_turkish[text]
    else :
		# Else, return the English version of the text.
        return text

def generate_pdf(user_info_document : dict, user_data_document : dict, user_photo_path : str, output_file_path : str) -> None:
    """
	This function generates the PDF file of the transcript.
	@Parameters:
		user_info_document - Required : The user info document. (dict) -> Used to get the user info.
		user_data_document - Required : The user data document. (dict) -> Used to get the user data.
		user_photo_path - Required : The path of the user photo. (str) -> Used to get the user photo.
		output_file_path - Required : The path of the output file. (str) -> Used to save the PDF file.
	@Returns:
		None
	"""
    
	# Load the photo path for mef logo
    mef_logo_path = ASSETS_DC.LOGO_PATH

	# get the user info literals
    language_of_instruction = user_info_document["language_of_instruction"]
    student_department = user_info_document["student_department"]
    student_faculty = user_info_document["student_faculty"]
    student_name = user_info_document["student_name"]
    student_school_id = user_info_document["student_school_id"]
    student_national_id = user_info_document["_id"]
    student_status = user_info_document["student_status"]
    student_surname = user_info_document["student_surname"]

	# get the user data literals
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