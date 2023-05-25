from PIL import Image
import requests
from Environment import UTILITIES_DC, PACKAGES_DC, connect_urls, SELENIUM_DC
import socket
import subprocess
import os
import platform
import re
from    bs4         import BeautifulSoup
import  io
from win32com.client import Dispatch
import gender_guesser.detector as gender
import  zipfile
from googletrans import Translator

GENDER_DETECTOR = gender.Detector(case_sensitive=False)

def translate_text(text:str, source_language:str="en", target_language:str="tr") -> str:

	translator = Translator()
	
	try :
		translation = translator.translate(text, src=source_language, dest=target_language)
		return translation.text
	except :
		raise Exception("Error: Translation failed, LOG: " + source_language + " " + target_language + " " + text)

def get_gif_frame_count(gif_file_path:str) -> int:
	"""
	Method, that returns the number of frames in a gif file.
	@Params
		gif_file_path : str - (Required) The path to the gif file.
	@Returns
		number_of_frames : int - The number of frames in the gif file.
	"""

	with Image.open(gif_file_path) as gif_file:
		number_of_frames = 0
		while True:
			try:
				gif_file.seek(number_of_frames)
				number_of_frames += 1
			except EOFError:
				break

	return number_of_frames

def authenticate(username, password) :

	payload = UTILITIES_DC.AUTH_PAYLOAD
	payload.update(kullanici_adi=username, kullanici_sifre=password)

	with requests.Session() as s:
		s.post(UTILITIES_DC.AUTH_LOG_URL, data=payload)
		r = s.get(UTILITIES_DC.AUTH_SEC_URL)

		if r.url == UTILITIES_DC.AUTH_SEC_URL:
			return True

	return False

def check_internet_connection() :
	try :
		requests.get(PACKAGES_DC.CONNECTION_TEST_URL)
		return True
	except :
		return False
	
def get_connection_details() :
	hostname = socket.gethostname()
	address = socket.gethostbyname(hostname)
	port = socket.getservbyname("http", "tcp")
	try :
		ssid = subprocess.check_output('netsh wlan show interfaces | findstr SSID', shell=True).decode('utf-8').split(':')[1].strip()
		ssid = ssid[ssid.find(":")+1:ssid.find("\n")-1]
	except :
		ssid = "~Ethernet"

	return (hostname, address, port, ssid)

def download_chrome_driver() -> tuple:

	def get_chrome_version() -> str:

		parser = Dispatch("Scripting.FileSystemObject")

		try :
			version = parser.GetFileVersion(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
		except :
			try :
				version = parser.GetFileVersion(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
			except :
				return None

		version_base = version.split(".")[0]

		return version_base

	version_base = get_chrome_version()

	if version_base is None :
		return (False, "Couldn't find acceptable chrome version, please check your chrome installation.")

	version_base = version_base.split(".")[0]

	download_page_response = requests.get(PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_URL)

	parsed_page = BeautifulSoup(download_page_response.text, "html.parser")

	all_versions = parsed_page.find_all("a", class_="XqQF9c")

	for current_version in all_versions :

		if current_version.text.split(" ")[1].startswith(version_base) :
			official_version = current_version.text.split(" ")[1]
			break       

	file_download_url = connect_urls(PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_PARTITION["base"], official_version, PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_PARTITION["args"])

	download_response = requests.get(file_download_url)
	zipFile = zipfile.ZipFile(io.BytesIO(download_response.content))
	zipFile.extractall(PACKAGES_DC.EXTRACTION_SITE)

	return (True, SELENIUM_DC.CHROME_DRIVER_PATH)

def validate_transcript(path_to_pdf_file) :
	
	if path_to_pdf_file is None or path_to_pdf_file == "" :
		return False
	
	if not path_to_pdf_file.endswith(".pdf") :
		return False
	
	if not os.path.exists(path_to_pdf_file) :
		return False
	
	try :
		with open(path_to_pdf_file, "rb") as pdf_file :
			pdf_file.read()
	except :
		return False
	
	return True

def get_gender(name : str =None, country="turkey") :	
	
	if name is not None :
		transmap = str.maketrans("ıüöçşğİÜÖÇŞĞ", "iuocsgIUOCSG")
        
		name = name.lower()
		name = name.split(" ")[0]
		name = name.translate(transmap)
		name = name.capitalize()

		name = re.sub(r"[^a-zA-Z]+", "", name)
	
		return GENDER_DETECTOR.get_gender(name=name, country=country)
	else :
		return None

def push_dpi() :

	try:
		from ctypes import windll
		windll.shcore.SetProcessDpiAwareness(1)
	except:
		pass

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
	if sort_key == "course_grade_point":
		course_list.sort(key=lambda x: float(x[sort_key]), reverse=should_reverse)
	else :
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
		index_of_course = course_list.index(result[0])
		course_list.pop(index_of_course)
		course_list.insert(index_of_course, course)
		return course_list

def calculate_performance(course_list, skip_retakens=False):
	"""
	This function calculates the GPA based on the given course list.
	"""

	credits_attempted = 0
	credits_successful = 0
	credits_included_in_gpa = 0
	gpa = 0

	for course in course_list:

		if skip_retakens:
			if course["course_code"].endswith("*"):
				continue

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