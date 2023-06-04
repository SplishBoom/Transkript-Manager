from 	Environment 			import 	UTILITIES_DC, PACKAGES_DC, connect_urls, SELENIUM_DC # -> Environment variables 
from 	bs4 					import 	BeautifulSoup # -> HTML parsing for chrome driver installation
from 	googletrans 			import 	Translator # -> Translation for non hashable texts
from 	win32com.client 		import 	Dispatch # -> OS manipulation
from 	PIL 					import 	Image # -> Image manipulation
import 	gender_guesser.detector as 		gender # -> Gender detection
import 	subprocess # -> OS manipulation
import 	requests # -> Web requests
import 	zipfile # -> Zip file manipulation
import 	socket # -> Internet connection check
import 	os # -> OS manipulation
import 	re # -> Regex manipulation
import 	io # -> IO manipulation

# Initialize a gender detector object.
GENDER_DETECTOR = gender.Detector(case_sensitive=False)

def translate_text(text : str, source_language : str = "en", target_language : str = "tr") -> str:
	"""
	Translates the given text from source language to target language.
	@Parameters:
		text - Required : The text to be translated. (str) -> Used to translate the text
		source_language - Optional : The language of the text. (str) (default = "en") -> Used to translate the text
		target_language - Optional : The language to be translated. (str) (default = "tr") -> Used to translate the text
	@Returns:
		translation.text - The translated text. (str)
	"""
	# Create a translator object (A new one required for each translation because of the caching bug)
	translator = Translator()
	
	try :
		# Try to translate the text
		translation = translator.translate(text, src=source_language, dest=target_language)
		
		# Return the translated text
		return translation.text
	except :
		# If the translation fails, raise an exception
		raise Exception("Error: Translation failed, LOG: " + source_language + " " + target_language + " " + text)

def get_gif_frame_count(gif_file_path : str) -> int:
	"""
	Method, that returns the number of frames in a gif file.
	@Parameters:
		gif_file_path - Required : Path to the gif file. (str) -> Used to get the number of frames
	@Returns:
		number_of_frames - The number of frames in the gif file. (int)
	"""
	# Open the gif file
	with Image.open(gif_file_path) as gif_file:
		# Count the frames
		number_of_frames = 0
		while True:
			try:
				# Seek to the next frame
				gif_file.seek(number_of_frames)
				# Increase the frame count
				number_of_frames += 1
			except EOFError:
				# End of frames
				break

	# Return the number of frames
	return number_of_frames

def authenticate(username : str, password : str) -> bool:
	"""
	Authenticates the user with the given username and password.
	@Parameters:
		username - Required : The username of the user. (str) -> Used to authenticate the user
		password - Required : The password of the user. (str) -> Used to authenticate the user
	@Returns:
		True - If the authentication is successful. (bool)
		False - If the authentication is unsuccessful. (bool)
	"""
	# Load the payload stucture.
	payload = UTILITIES_DC.AUTH_PAYLOAD
	# Fill the payload with the given username and password.
	payload.update(kullanici_adi=username, kullanici_sifre=password)

	# Send the authentication request.
	with requests.Session() as s:
		# Send the authentication request.
		s.post(UTILITIES_DC.AUTH_LOG_URL, data=payload)
		
		# Get the authentication result.
		r = s.get(UTILITIES_DC.AUTH_SEC_URL)

		# Check if the authentication is successful.
		if r.url == UTILITIES_DC.AUTH_SEC_URL:
			# Return True if the authentication is successful.
			return True
		
	# Return False if the authentication is unsuccessful.
	return False

def check_internet_connection() -> bool:
	"""
	Checks if the device is connected to the internet.
	@Parameters:
		None
	@Returns:
		True - If the device is connected to the internet. (bool)
		False - If the device is not connected to the internet. (bool)
	"""
	# Try to connect to the connection test url.
	try :
		requests.get(PACKAGES_DC.CONNECTION_TEST_URL)

		# If the connection is successful, return True.
		return True
	except :
		# If the connection is unsuccessful, return False.
		return False
	
def get_connection_details() -> tuple:
	"""
	Returns the connection details of the device.
	@Parameters:
		None
	@Returns:
		hostname - The hostname of the device. (str)
		address - The IP address of the device. (str)
		port - The port of the device. (str)
		ssid - The SSID of the device. (str)
	"""
	# Get the connection details.
	hostname = socket.gethostname()
	address = socket.gethostbyname(hostname)
	port = socket.getservbyname("http", "tcp")
	try :
		# Get the SSID of the device. Handle an exception if the device is connected to the internet via ethernet.
		ssid = subprocess.check_output('netsh wlan show interfaces | findstr SSID', shell=True).decode('utf-8').split(':')[1].strip()
		ssid = ssid[ssid.find(":")+1:ssid.find("\n")-1]
	except :
		# If the device is connected to the internet via ethernet, set the SSID to "~Ethernet".
		ssid = "~Ethernet"

	# Return the connection details.
	return (
		hostname, 
		address, 
		port, 
		ssid
	)

def download_chrome_driver() -> tuple:
	"""
	Downloads the chrome driver.
	@Parameters:
		None
	@Returns:
		True, Path- If the download is successful. (tuple)
		False, Error - If the download is unsuccessful. (tuple)
	"""
	def get_chrome_version() -> str:
		"""
		Returns the chrome version.
		@Parameters:
			None
		@Returns:
			version_base - The chrome version. (str)
		"""
		# Dispatch the file system object.
		parser = Dispatch("Scripting.FileSystemObject")

		# Get the chrome version.
		try :
			version = parser.GetFileVersion(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
		except :
			try :
				version = parser.GetFileVersion(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
			except :
				return None

		# Get the chrome version base.
		version_base = version.split(".")[0]

		# Return the chrome version base.
		return version_base

	# Get the chrome version base.
	version_base = get_chrome_version()

	# Check if the chrome version base is None.
	if version_base is None :
		return (False, "Couldn't find acceptable chrome version, please check your chrome installation.")

	# Get the version from base.
	version_base = version_base.split(".")[0]

	# Download the chrome driver.
	download_page_response = requests.get(PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_URL)

	# Parse the download page.
	parsed_page = BeautifulSoup(download_page_response.text, "html.parser")

	# Get the official version.
	all_versions = parsed_page.find_all("a", class_="XqQF9c")

	# Check if the official version is found.
	for current_version in all_versions :

		if current_version.text.split(" ")[1].startswith(version_base) :
			# If the official version is found, break the loop.
			official_version = current_version.text.split(" ")[1]
			break       

	# Set the file download url.
	file_download_url = connect_urls(PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_PARTITION["base"], official_version, PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_PARTITION["args"])

	# Download the chrome driver.
	download_response = requests.get(file_download_url)

	# Get zip file.
	zipFile = zipfile.ZipFile(io.BytesIO(download_response.content))

	# Extract the zip file to location.
	zipFile.extractall(PACKAGES_DC.EXTRACTION_SITE)

	# Return the status.
	return (True, SELENIUM_DC.CHROME_DRIVER_PATH)

def validate_transcript(path_to_pdf_file : str) -> bool:
	"""
	Validates the transcript.
	@Parameters:
		path_to_pdf_file - Required : The path to the transcript. (str) -> [Example: "C:/Users/username/Desktop/transcript.pdf"]
	@Returns:
		True - If the transcript is valid. (bool)
		False - If the transcript is invalid. (bool)
	"""
	# Check if the path to the transcript is empty.
	if path_to_pdf_file is None or path_to_pdf_file == "" :
		return False
	
	# Check if the path to the transcript is a pdf.
	if not path_to_pdf_file.endswith(".pdf") :
		return False
	
	# Check if the path to the transcript exists.
	if not os.path.exists(path_to_pdf_file) :
		return False
	
	# Check if the path to the transcript is readable.
	try :
		with open(path_to_pdf_file, "rb") as pdf_file :
			pdf_file.read()
	except :
		return False
	
	# If all passed, return True.
	return True

def get_gender(name : str = None, country : str = "turkey") -> str:
	"""
	Gets the gender of the user by comparing the names.
	@Parameters:
		name - Optional : The name of the user. (str) (default = None) -> used for gender detection
		country - Optional : The country of the user (str) (default = "turkey") -> used to set parameter into object.
	@Returns:
		gender (str) gender of the user.
	"""
	# Check if the name is None.
	if name is not None :
		# Set up a translation map.
		transmap = str.maketrans("ıüöçşğİÜÖÇŞĞ", "iuocsgIUOCSG")
        
		# Clean the name.
		name = name.lower()
		name = name.split(" ")[0]
		name = name.translate(transmap)
		name = name.capitalize()

		# Remove the non-alphabetic characters.
		name = re.sub(r"[^a-zA-Z]+", "", name)
	
		# Detect and return gender.
		return GENDER_DETECTOR.get_gender(name=name, country=country)
	else :
		# If not passed, return None.
		return None

def push_dpi() -> None:
	"""
	Pushes the DPI awareness.
	@Parameters:
		None
	@Returns:
		None
	"""
	# Try to push the DPI awareness.
	try:
		from ctypes import windll
		# Try to push the DPI awareness.
		windll.shcore.SetProcessDpiAwareness(1)
	except:
		# If failed, pass.
		pass

def _validate_input_key(key : str) -> None:
	"""
	Validates the input key.
	@Parameters:
		key - Required : The key to validate. (str) -> [Example: "course_code"]
	@Returns:
		None
	"""
	if key not in ["course_code", "course_name", "course_lang", "course_credit", "course_grade", "course_grade_point"]:
		# If key is not found, than raise an error. This is because this can not be outside of the scope by initial call.
		raise ValueError("Invalid sort key")
		
def sort_by(given_course_list : list, sorting : dict) -> list:
	"""
	Sorts the given course list by given sorting key.
	@Parameters:
		given_course_list - Required : The course list to sort. (list) -> Used to sort the course list.
		sorting - Required : The sorting key. (dict) -> Used to sort the course list.
	@Returns:
		course_list (list) sorted course list.
	"""
	# Get values.
	sort_key = sorting["sort_key"]
	should_reverse = sorting["should_reverse"]
	
	# Check if sort key is None.
	if sort_key is None:
		return given_course_list.copy()
	
	# Validate the input key.
	_validate_input_key(sort_key)

	# Copy the course list.
	course_list = given_course_list.copy()
	
	# Special case for course_grade_point.
	if sort_key == "course_grade_point":
		# Sort the course list.
		course_list.sort(key=lambda x: float(x[sort_key]), reverse=should_reverse)
	else :
		# Sort the course list.
		course_list.sort(key=lambda x: x[sort_key], reverse=should_reverse)

	# Return the sorted course list.
	return course_list

def filter_by(given_course_list : list, filtering : dict) -> list:
	"""
	Filters the given course list by given filtering key.
	@Parameters:
		given_course_list - Required : The course list to filter. (list) -> Used to filter the course list.
		filtering - Required : The filtering key. (dict) -> Used to filter the course list.
	@Returns:
		course_list (list) filtered course list.
	"""
	# Get values.
	filter_key = filtering["filter_key"]
	filter_value = filtering["filter_value"]
	
	# Validate the input key.
	_validate_input_key(filter_key)

	# Copy the course list.
	course_list = given_course_list.copy()

	# Special case for course_grade_point.
	if filter_key == "course_grade_point":
		# Filter the course list.
		course_list = list(filter(lambda x: float(x[filter_key]) == float(filter_value), course_list))
	else :
		# Filter the course list.
		course_list = list(filter(lambda x: x[filter_key] == filter_value, course_list))
	
	# Return the filtered course list.
	return course_list

def add_course(given_course_list : list, course : dict) -> list:
	"""
	Adds the given course to the given course list.
	@Parameters:
		given_course_list - Required : The course list to add. (list) -> Used to add the course to the course list.
		course - Required : The course to add. (dict) -> Used to add the course to the course list.
	@Returns:
		course_list (list) course list with added course.
	"""
	# Get values.
	course_code = course["course_code"]
	course_name = course["course_name"]
	course_lang = course["course_lang"]
	course_credit = course["course_credit"]
	course_grade = course["course_grade"]
	course_grade_point = course["course_grade_point"]

	# Copy the course list.
	course_list = given_course_list.copy()

	# Check if course code is already exists.
	result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
	
	# If yes, than add a number to the end of the course code. Until it is unique.
	n = 1
	while result:
		course_code = course_code + " (" + str(n) + ")"
		result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
		n += 1

	# Create the new course.
	new_course ={
		"course_code": course_code,
		"course_name": course_name,
		"course_lang": course_lang,
		"course_credit": course_credit,
		"course_grade": course_grade,
		"course_grade_point": course_grade_point
	}

	# Add the new course to the course list.
	course_list.append(new_course)

	# Return the appended course list.
	return course_list

def subtract_course(given_course_list : list, course_code : str) -> list:
	"""
	Subtracts the given course from the given course list.
	@Parameters:
		given_course_list - Required : The course list to subtract. (list) -> Used to subtract the course from the course list.
		course_code - Required : The course code to subtract. (str) -> Used to subtract the course from the course list.
	@Returns:
		course_list (list) course list with subtracted course.
	"""
	# Copy the course list.
	course_list = given_course_list.copy()

	# Filter the course list.
	result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})
	
	# If the course code is not found, return the original course list.
	if not result:
		return course_list
	else:
		# If the course code is found, remove the course from the course list.
		course_list = list(filter(lambda x: x["course_code"] != course_code, course_list))

		# Return the subtracted course list.
		return course_list

def update_course(given_course_list : list, course : dict) -> list:
	"""
	Updates the given course in the given course list.
	@Parameters:
		given_course_list - Required : The course list to update. (list) -> Used to update the course in the course list.
		course - Required : The course to update. (dict) -> Used to update the course in the course list.
	@Returns:
		course_list (list) course list with updated course.
	"""
	# Get value.
	course_code = course["course_code"]

	# Copy the course list.
	course_list = given_course_list.copy()
	
	# Filter the course list. If the course code is not found, return the original course list.
	result = filter_by(course_list, {"filter_key":"course_code", "filter_value":course_code})

	# If the course code is not found, return the original course list.
	if not result:
		# Return the original course list.
		return course_list
	else:
		# If the course code is found, update the course in the course list.
		index_of_course = course_list.index(result[0])
		
		# Remove the old course.
		course_list.pop(index_of_course)

		# Insert the new course.
		course_list.insert(index_of_course, course)

		# Return the updated course list.
		return course_list

def calculate_performance(course_list : list, skip_retakens : bool = False) -> dict:
	"""
	Calculates the GPA, credits attempted, credits successful and credits included in GPA based on the given course list.
	@Parameters:
		course_list - Required : The course list to calculate performance. (list) -> Used to calculate the performance of the course list.
		skip_retakens - Optional : Skip retaken courses. (bool) -> Used to skip retaken courses.
	@Returns:
		credits_attempted (int) total credits attempted.
		credits_successful (int) total credits successful.
		credits_included_in_gpa (int) total credits included in gpa.
		gpa (float) gpa.
	"""

	# Initialize variables.
	credits_attempted = 0
	credits_successful = 0
	credits_included_in_gpa = 0
	gpa = 0

	# Iterate over the course list.
	for course in course_list:

		# Skip retaken courses.
		if skip_retakens:
			if course["course_code"].endswith("*"):
				continue

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

def generate_gradient_colors(num_colors : int, start_color : tuple = (0, 0, 1), end_color : tuple = (1, 0, 0)) -> list:
	"""
	Generates a list of gradient colors.
	@Parameters:
		num_colors - Required : Number of colors to generate. (int) -> Used to generate the number of colors.
		start_color - Optional : Start color of the gradient. (tuple) -> Used to generate the gradient colors.
		end_color - Optional : End color of the gradient. (tuple) -> Used to generate the gradient colors.
	@Returns:
		gradient_colors (list) list of gradient colors.
	"""
	# Initialize variables.
	gradient_colors = []
	# Iterate over the number of colors.
	for i in range(num_colors):
		# Calculate the gradient color. R = R1 + (i / (n - 1)) * (R2 - R1), G = G1 + (i / (n - 1)) * (G2 - G1), B = B1 + (i / (n - 1)) * (B2 - B1)
		try : 
			r = start_color[0] + (i / (num_colors - 1)) * (end_color[0] - start_color[0])
			g = start_color[1] + (i / (num_colors - 1)) * (end_color[1] - start_color[1])
			b = start_color[2] + (i / (num_colors - 1)) * (end_color[2] - start_color[2])
		except ZeroDivisionError:
			r = start_color[0] + (i / (num_colors)) * (end_color[0] - start_color[0])
			g = start_color[1] + (i / (num_colors)) * (end_color[1] - start_color[1])
			b = start_color[2] + (i / (num_colors)) * (end_color[2] - start_color[2])
			
		# Append the gradient color.
		gradient_colors.append((r, g, b))

	# Return the gradient colors.
	return gradient_colors