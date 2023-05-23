def _validate_input_key(key):
	if key not in ["course_code", "course_name", "course_lang", "course_credit", "course_grade", "course_grade_point"]:
		raise ValueError("Invalid sort key")
		
def sort_by(given_course_list, sorting):
	sort_key = sorting["sort_key"]
	should_reverse = sorting["should_reverse"]
	if sort_key is None:
		return given_course_list.copy()
	_validate_input_key(sort_key)
	course_list = given_course_list.copy()
	course_list.sort(key=lambda x: x[sort_key], reverse=should_reverse)
	return course_list

def filter_by(given_course_list, filtering):
	filter_key = filtering["filter_key"]
	filter_value = filtering["filter_value"]
	_validate_input_key(filter_key)
	course_list = given_course_list.copy()
	course_list = list(filter(lambda x: x[filter_key] == filter_value, course_list))
	return course_list

def add_course(given_course_list, course):

	course_code = course["course_code"]
	course_name = course["course_name"]
	course_lang = course["course_lang"]
	course_credit = course["course_credit"]
	course_grade = course["course_grade"]
	course_grade_point = course["course_grade_point"]

	course_list = given_course_list.copy()
	result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
	n = 1
	while result:
		course_code = course_code + " (" + str(n) + ")"
		result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
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
	result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
	if not result:
		return course_list
	else:
		course_list = list(filter(lambda x: x["course_code"] != course_code, course_list))
		return course_list

def update_course(given_course_list, course):
	# The code is defining a function that takes a list of dictionaries as input and filters the list
	# based on a given course code. If the course code is not found in the list, the original list is
	# returned. If the course code is found, the function removes the dictionary with that course code
	# from the list and adds a new dictionary with the given course information. The updated list is
	# then returned.
	course_code = course["course_code"]

	course_list = given_course_list.copy()
	result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
	if not result:
		return course_list
	else:
		course_list = list(filter(lambda x: x["course_code"] != course_code, course_list))
		course_list = add_course(course_list, course)
		return course_list

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