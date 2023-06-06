from    urllib.request  import  urlretrieve as get_photo # -> Wrapped utility function for downloading photos from web
from    abc             import  ABC, abstractmethod # -> Abstract class for creating abstract methods
from    Environment     import  SELENIUM_DC # -> Selenium constants
from    datetime        import  datetime # -> Datetime for timestamping
from    Utilities       import  Web, By # -> Web class for web automation
from    PIL             import  Image # -> Image for image processing
import  PyPDF2          as      ppdf # -> PDF reader
import  json # -> JSON for file I/O
import  re # -> Regular expressions for parsing

class Parser(ABC) :

    @abstractmethod
    def _extract_transcript_information(self) -> None:
        """
        Abstract method for extracting transcript information from the source.
        """
        pass

    @abstractmethod
    def _parse_transcript_information(self) -> None:
        """
        Abstract method for extracting transcript information from the source.
        """
        pass

    @abstractmethod
    def get_transcript_data(self) -> dict:
        """
        Abstract method for extracting transcript information from the source.
        @returns:
            transcript_data : dict
        """
        pass

class OnlineParser(Parser) :

    def __init__(self, username : str = None, password : str = None, isHidden : bool = True, save_to_file : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for OnlineParser class.
        @Parameters:
            username - Optional : Username for logging in to the system. (str) (default = None) -> Used to login to the system
            password - Optional : Password for logging in to the system. (str) (default = None) -> Used to login to the system
            isHidden - Optional : Boolean value for hiding the browser. (bool) (default = True) -> Used to hide the browser
            save_to_file - Optional : Boolean value for saving the transcript data to a file. (bool) (default = False) -> Used to save the transcript data to a file
        @Returns:
            None
        """
        # Initialize super class
        super().__init__()

        # Initialize class fields
        self.username = username
        self.password = password

        self.isHidden = isHidden

        self.save_to_file = save_to_file

        self.extracted = None
        self.transcript_data = None

    def _extract_transcript_information(self) -> None:
        """
        Private method for extracting transcript information from the source.
        @Parameters:
            None
        @Returns:
            None
        """

        # Get main url
        main_url = SELENIUM_DC.OLEXER_SYSTEM_LOGIN_URL

        # Initialize web client with main url
        client = Web(isHidden=self.isHidden)
        client.open_web_page(main_url)

        # Get username entry and send username
        username_entry = client.create_element(SELENIUM_DC.OLEXER_USERNAME_ENTRY_XPATH)
        username_entry.send_keys(self.username)

        # Get password entry and send password
        password_entry = client.create_element(SELENIUM_DC.OLEXER_PASSWORD_ENTRY_XPATH)
        password_entry.send_keys(self.password)

        # Get login button and click
        login_button = client.create_element(SELENIUM_DC.OLEXER_LOGIN_BUTTON_XPATH)
        login_button.click()

        # Get continue button and click
        continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
        continue_button.click()
                
        # Get user photo label and source
        user_photo_label = client.create_element(SELENIUM_DC.OLEXER_USER_PHOTO_LABEL_XPATH)
        user_photo_src = user_photo_label.get_attribute(SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[0])

        # Download user photo
        get_photo(user_photo_src, SELENIUM_DC.USER_PHOTO_OUTPUT_PATH)
        # Convert the photo.
        photo = Image.open(SELENIUM_DC.USER_PHOTO_OUTPUT_PATH)
        photo.save(SELENIUM_DC.USER_PHOTO_OUTPUT_PATH, "PNG")

        # Get profile selection label and click to move on.
        profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
        profile_selection_label.click()

        # Iterate through the drop down menu and select the major inside list if exist.
        drop_down_menu = client.create_element(SELENIUM_DC.OLEXER_DROP_DOWN_MENU_XPATH)
        check_list = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
        flag = False
        for current_element in drop_down_menu.find_elements(by=By.TAG_NAME, value="a") :
            # Search for major inside the drop down menu
            if current_element.text in check_list :
                client.click_on_element(current_element)
                # check if major is found
                idSelectionMenu = client.create_element(SELENIUM_DC.OLEXER_ID_SELECTION_XPATH)
                for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
                    if element.get_attribute(SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[1]).split("-")[-1].strip() in check_list :
                        # if also passed the check, click on it, open the system with major and continue
                        client.click_on_element(element)
                        flag = True
                        # break the loop to avoid unnecessary iterations and buggy result
                        break
                break
        if flag:
            # If flag is set, it means the page refreshed with major, so repeat the continue_button process
            continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
            client.click_on_element(continue_button)

        # Open transcript page
        transkriptUrl = SELENIUM_DC.OLEXER_TRANSCRIPT_URL
        client.open_web_page(transkriptUrl)

        # Get transcript table
        table_elements = client.browser.find_elements(By.TAG_NAME, SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[2])

        # Extract data from table
        output = []
        for element in table_elements :
            output.append(element.text)

        # Close the browser
        client.browser.quit()

        # Set extracted data
        self.extracted = output

    def __extract_dynamicly(self, sis_language : str, keywords : list, data : str) -> tuple:
        """
        Private method for extracting transcript information from the source.
        @Parameters:
            sis_language - Required : Language of the SIS system. (str) -> Used to determine the language of the system
            keywords - Required : Keywords for extracting data. (list) -> Used to determine the keywords for extracting data
            data - Required : Data for extracting transcript information. (str) -> Used to determine the data for extracting transcript information
        @Returns:
            data_1 - str : Extracted data from the source.
            data_2 - str : Extracted data from the source.
        @@Contributors:
            @mustafa_mert_tunali
        """
        # Split the data into two parts
        if sis_language == "en" :
            keywords = keywords[:2]
        elif sis_language == "tr" :
            keywords = keywords[2:]
        
        # Search from beginnig to middle.
        data_1 = data[
            data.find(keywords[0]) + len(keywords[0]) + 1
            :
            data.find(keywords[1]) - 1
        ]

        # Search from middle to end.
        data_2 = data[
            data.find(keywords[1]) + len(keywords[1]) + 1
            :
        ]

        # Return the data
        return data_1, data_2

    def _parse_transcript_information(self) -> None:
        """
        Private method for parsing extracted transcript information from the source.
        @Parameters:
            None
        @Returns:
            None
        """

        # Set the output
        output = self.extracted

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
        
        # Extract student information
        student_school_id, student_national_id = self.__extract_dynamicly(sis_language, ["Student ID", "National ID", "Öğrenci Numarası", "TC Kimlik Numarası"], student_parse[0])
        student_name, student_surname = self.__extract_dynamicly(sis_language, ["Name", "Surname", "Adı", "Soyadı"], student_parse[1])
        student_faculty, student_department = self.__extract_dynamicly(sis_language, ["Faculty / Department", "Program Name", "Fakülte", "Bölüm"], student_parse[2])
        language_of_instruction, student_status = self.__extract_dynamicly(sis_language, ["Language of Instruction", "Student Status", "Eğitim Dili", "Öğrencilik Durumu"], student_parse[3])

        # Extract semesters
        semesters = {}
        semester_no = 1
        original_course_list = []
        for current_course in output :

            prep = "PREP" in current_course
            semester = current_course.startswith("Semester Credits Attempted") or current_course.startswith("Dönem Alınan Kredi")
            student = "Student ID" in current_course or "Öğrenci Numarası" in current_course

            # Pass the prep courses when parsing
            if prep or semester or student :
                continue

            semester_parse = current_course.split("\n")
            semester_definition = semester_parse.pop(0)
            semester_parse.pop(0) # remove junk info (colum names)
            if "Academic Standing" in semester_parse[-1] or "Akademik Durum" in semester_parse[-1] :
                semester_parse.pop() # remove junk info (academic standing)
            cumulative_credits_attempted = semester_parse.pop()
            semester_credits_attempted = semester_parse.pop()
            course_list = semester_parse
            # Iterate over courses
            for course_index, course_info in enumerate(course_list) :

                course_info_parse = course_info.split(" ")

                course_code = course_info_parse.pop(0) + " " + course_info_parse.pop(0)
                course_list[course_index] = {
                    "course_code" : course_code,
                    "course_name" : " ".join(course_info_parse[:-4]),
                    "course_lang" : course_info_parse[-4],
                    "course_credit" : course_info_parse[-3],
                    "course_grade" : course_info_parse[-2],
                    "course_grade_point" : course_info_parse[-1],
                }

                # Skip the repeated courses
                if course_code[-1] != "*" :
                    original_course_list.append(course_list[course_index])

            # Update the semester
            semesters[f"semester_{semester_no}"] = {
                "semester_definition" : semester_definition,
                "course_list" : course_list
            }

            # Update the semester no
            semester_no += 1

        # Update the output with parsed data
        output = {
            "parsing_type" : "online",
            "parsing_language" : sis_language,
            "transcript_manager_date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "transcript_creation_date" : date,
            "student_school_id" : student_school_id,
            "student_national_id" : student_national_id,
            "student_name" : student_name,
            "student_surname" : student_surname,
            "student_faculty" : student_faculty,
            "student_department" : student_department,
            "language_of_instruction" : language_of_instruction,
            "student_status" : student_status,
            "semesters" : semesters,
            "original_course_list" : original_course_list
        }

        # Save the output to file if save_to_file is True
        if self.save_to_file :
            with open(f"{student_name}_online_{sis_language}.json", "w", encoding="utf-8") as file :
                json.dump(output, file, ensure_ascii=False, indent=4)

        # Update the transcript data
        self.transcript_data = output

    def get_transcript_data(self) -> dict :
        """
        Private method for getting transcript data.
        @Parameters:
            None
        @Returns:
            dict : Transcript data
        """
        
        # Extract transcript information
        self._extract_transcript_information()
        
        # Parse transcript information
        self._parse_transcript_information()

        # Return the transcript data
        return self.transcript_data
    
class OfflineParser(Parser) :

    def __init__(self, path_to_file : str = None, save_to_file : str = False, *args, **kwargs) -> None:
        """
        Constructor method for OfflineParser class.
        @Parameters:
            path_to_file (str) : Path to the transcript file. (default : None) -> Used to extract transcript information.
            save_to_file (bool) : Save the transcript data to file. (default : False) -> Used to save transcript data to file.
        @Returns:
            None
        """
        # Initialize the super class
        super().__init__()

        # Initialize the class variables
        self.path_to_file = path_to_file

        self.save_to_file = save_to_file

        self.extracted = None
        self.transcript_data = None

    def _extract_transcript_information(self) -> None :
        """
        Private method for extracting transcript information from the source.
        @Parameters:
            None
        @Returns:
            None
        """
        # Read the pdf file
        pdf_file = ppdf.PdfReader(self.path_to_file)

        # Iterate over pages and extract text
        output = []
        for current_page in pdf_file.pages :
            current_page_text = current_page.extract_text()
            current_page_elements = current_page_text.split("\n")
            output.extend(current_page_elements)

        # Update the extracted data
        self.extracted = output

    def _parse_transcript_information(self) -> None:
        """
        Private method for parsing extracted transcript information from the source.
        @Parameters:
            None
        @Returns:
            None
        """
        # Initialize the output
        output = self.extracted
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
        student_school_id = output.pop(0) # student id
        output.pop(0)
        student_national_id = output.pop(0) # national id
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

        # Set splitters for semester seperation
        splitters = [
            "Fall Semester", "Spring Semester", "Summer School", "Fall Dönemi", "Spring Dönemi", "Bahar Dönemi", "Güz Dönemi", "Yaz Okulu"
        ]
        founded_semesters = []
        temp = [output.pop(0)]
        # Iterate over stream data and seperate semesters
        for current_string in output :
            # Get current string
            checker = " ".join(current_string.split(" ")[1:])
            
            # Check if current string is a splitter
            if checker in splitters :
                # Add current semester to founded semesters
                founded_semesters.append(temp)
                temp = [current_string]
            else :
                # Add current string to current semester
                temp.extend([current_string])
        
        # Add the final semester to founded semesters
        founded_semesters.append(temp)

        # clean prep semesters
        clean_index = []
        for semester_index, current_semester in enumerate(founded_semesters) :
            if "Prep" in current_semester :
                clean_index.append(semester_index)

        # remove prep semesters
        for index in reversed(clean_index) :
            founded_semesters.pop(index)

        # Iterate over founded semesters and parse them
        semesters = {}
        semester_no = 1
        original_course_list = []
        for semester_index, current_semester in enumerate(founded_semesters) :
            
            semester_definition = current_semester.pop(0)

            # remove junk info from each semester
            if current_semester[0] == "Course Code" :
                count = 7
            elif current_semester[0] == "Ders Kodu" :
                count = 6
            for i in range(count) :
                current_semester.pop(0)

            # Set feature literals for parsing
            course_list = []
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
                # Check if current string is a splitter
                if current_string == "Semester" or current_string == "Dönem":
                    break
                
                # Check if current string is a course code
                if add_count == 7 :
                    course_list.append(temp)

                    # Check if current course is a repeated course
                    if temp["course_code"][-1] != "*" :
                        original_course_list.append(temp)

                    temp = {}
                    add_count = 1

                # Add current string to temp
                temp[map_hash[add_count]] = current_string
                # Update add count to avoid errors via not founding next course code
                add_count += 1

            # Add the last course to course list
            course_list.append(temp)
            if temp["course_code"][-1] != "*" :
                original_course_list.append(temp)
                        
            # Add current semester to semesters
            semesters[f"semester_{semester_no}"] = {
                "semester_definition" : semester_definition,
                "course_list" : course_list
            }

            # Update semester no
            semester_no += 1
        
        # Set the output by parsed data
        output = {
            "parsing_type" : "offline",
            "parsing_language" : sis_language,
            "transcript_manager_date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "transcript_creation_date" : date,
            "student_school_id" : student_school_id,
            "student_national_id" : student_national_id,
            "student_name" : student_name,
            "student_surname" : student_surname,
            "student_faculty" : student_faculty,
            "student_department" : student_department,
            "language_of_instruction" : language_of_instruction,
            "student_status" : student_status,
            "semesters" : semesters,
            "original_course_list" : original_course_list
        }

        # Save transcript data to file if save_to_file is True
        if self.save_to_file :
            with open(f"{student_name}_offline_{sis_language}.json", "w", encoding="utf-8") as file :
                json.dump(output, file, ensure_ascii=False, indent=4)

        # Set transcript data
        self.transcript_data = output

    def get_transcript_data(self) -> dict :
        """
        Private method for getting transcript data.
        @Parameters:
            None
        @Returns:
            transcript_data (dict) : Transcript data.
        """
        # Extract transcript information
        self._extract_transcript_information()

        # Parse transcript information
        self._parse_transcript_information()

        # Return transcript data
        return self.transcript_data
    
class UserVerifier() :

    def __init__(self, username : str = None, password : str = None, isHidden : bool = True, match_id : str = None, *args, **kwargs) -> None:
        """
        Constructor method for UserVerifier class.
        @Parameters:
            username - Optional : Username for user verification. (str) (default = None) -> Used to connect to the system.
            password - Optional : Password for user verification. (str) (default = None) -> Used to connect to the system.
            isHidden - Optional : Is the browser hidden? (bool) (default = True) -> Used to connect set Web class.
            match_id - Optional : Match id for user verification. (str) (default = None) -> Used to compare with received id.
        @Returns:
            None
        """
        # Set class variables
        self.username = username
        self.password = password

        self.isHidden = isHidden

        self.match_id = match_id
        self.received_id = None

        self.is_user_verified = False

    def _receive_system_id(self) -> None:
        """
        Private method for extracting transcript information from the source.
        @Parameters:
            None
        @Returns:
            None
        """

        # Get main url
        main_url = SELENIUM_DC.OLEXER_SYSTEM_LOGIN_URL

        # Initialize web client with main url
        client = Web(isHidden=self.isHidden)
        client.open_web_page(main_url)

        # Get username entry and send username
        username_entry = client.create_element(SELENIUM_DC.OLEXER_USERNAME_ENTRY_XPATH)
        username_entry.send_keys(self.username)

        # Get password entry and send password
        password_entry = client.create_element(SELENIUM_DC.OLEXER_PASSWORD_ENTRY_XPATH)
        password_entry.send_keys(self.password)

        # Get login button and click
        login_button = client.create_element(SELENIUM_DC.OLEXER_LOGIN_BUTTON_XPATH)
        login_button.click()

        # Get continue button and click
        continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
        continue_button.click()
                
        # Get profile selection label and click to move on.
        profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
        profile_selection_label.click()

        # Iterate through the drop down menu and select the major inside list if exist.
        drop_down_menu = client.create_element(SELENIUM_DC.OLEXER_DROP_DOWN_MENU_XPATH)
        check_list = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
        flag = False
        for current_element in drop_down_menu.find_elements(by=By.TAG_NAME, value="a") :
            # Search for major inside the drop down menu
            if current_element.text in check_list :
                client.click_on_element(current_element)
                # check if major is found
                idSelectionMenu = client.create_element(SELENIUM_DC.OLEXER_ID_SELECTION_XPATH)
                for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
                    if element.get_attribute(SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[1]).split("-")[-1].strip() in check_list :
                        # if also passed the check, click on it, open the system with major and continue
                        client.click_on_element(element)
                        flag = True
                        # break the loop to avoid unnecessary iterations and buggy result
                        break
                break
        if flag:
            # If flag is set, it means the page refreshed with major, so repeat the continue_button process
            continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
            client.click_on_element(continue_button)

        # Get student selection label and click to move on.
        profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
        profile_selection_label.click()

        # Get student info a tag
        student_info_a_tag = client.create_element(SELENIUM_DC.OLEXER_STUDENT_INFO_XPATH)

        # Check if student info a tag is empty, then repeat the process of getting profile selection label and clicking on it. than get student info a tag again.
        if student_info_a_tag.text == "" :
            
            # Get student selection label and click to move on.
            profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
            profile_selection_label.click()

            # Get student info a tag
            student_info_a_tag = client.create_element(SELENIUM_DC.OLEXER_STUDENT_INFO_XPATH)

        # Get student id and set it.
        self.received_id = re.findall(r"\d+", student_info_a_tag.text)[0]

    def _compare_ids(self) -> bool:
        """
        Private method for comparing ids.
        @Parameters:
            None
        @Returns:
            None
        """
        # The above code is implementing a conditional statement in Python. It checks if the
        # `match_id` attribute of an object is `None`. If it is `None`, then it sets the
        # `is_user_verified` attribute of the object to `False`. If `match_id` is not `None`, then it
        # checks if it is equal to the `received_id` attribute of the object. If they are equal, then
        # it sets `is_user_verified` to `True`. Otherwise, it sets `is_user_verified` to `False`.
        if self.match_id == None :
            self.is_user_verified = False
        else :
            if self.match_id == self.received_id :
                self.is_user_verified = True
            else :
                self.is_user_verified = False

    def verify_user(self) -> bool :
        """
        Public method for verifying user.
        @Parameters:
            None
        @Returns:
            self.is_user_verified (bool) : Is user verified? (bool) -> Used to check if user is verified.
        """
        # Receive system id. 
        self._receive_system_id()

        # Compare ids.
        self._compare_ids()
                
        # Return the result.
        return self.is_user_verified