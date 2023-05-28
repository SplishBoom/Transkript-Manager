from    abc         import ABC, abstractmethod
from    datetime    import datetime
from    Utilities   import Web, By
import  PyPDF2  as  ppdf
import  re
import  json
from urllib.request import urlretrieve as get_photo
from Environment import SELENIUM_DC

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

    def __init__(self, username:str=None, password:str=None, isHidden=True, save_to_file:bool=False, *args, **kwargs) -> None:
        super().__init__()

        self.username = username
        self.password = password

        self.isHidden = isHidden

        self.save_to_file = save_to_file

        self.extracted = None
        self.transcript_data = None

    def _extract_transcript_information(self) -> None:
        """
        Private method for extracting transcript information from the source.
        """

        main_url = SELENIUM_DC.OLEXER_SYSTEM_LOGIN_URL

        client = Web(isHidden=self.isHidden)
        client.open_web_page(main_url)

        username_entry = client.create_element(SELENIUM_DC.OLEXER_USERNAME_ENTRY_XPATH)
        username_entry.send_keys(self.username)

        password_entry = client.create_element(SELENIUM_DC.OLEXER_PASSWORD_ENTRY_XPATH)
        password_entry.send_keys(self.password)

        login_button = client.create_element(SELENIUM_DC.OLEXER_LOGIN_BUTTON_XPATH)
        login_button.click()

        continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
        continue_button.click()
                
        user_photo_label = client.create_element(SELENIUM_DC.OLEXER_USER_PHOTO_LABEL_XPATH)
        user_photo_src = user_photo_label.get_attribute(SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[0])

        get_photo(user_photo_src, SELENIUM_DC.USER_PHOTO_OUTPUT_PATH)

        profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
        profile_selection_label.click()

        drop_down_menu = client.create_element(SELENIUM_DC.OLEXER_DROP_DOWN_MENU_XPATH)
        check_list = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
        flag = False
        for current_element in drop_down_menu.find_elements(by=By.TAG_NAME, value="a") :
            if current_element.text in check_list :
                client.click_on_element(current_element)
                idSelectionMenu = client.create_element(SELENIUM_DC.OLEXER_ID_SELECTION_XPATH)
                for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
                    if element.get_attribute(SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[1]).split("-")[-1].strip() in check_list :
                        client.click_on_element(element)
                        flag = True
                        break
                break
        if flag:
            continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
            client.click_on_element(continue_button)

        transkriptUrl = SELENIUM_DC.OLEXER_TRANSCRIPT_URL
        client.open_web_page(transkriptUrl)

        table_elements = client.browser.find_elements(By.TAG_NAME, SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[2])

        output = []
        for element in table_elements :
            output.append(element.text)

        client.browser.quit()

        self.extracted = output

    def __extract_dynamicly(self, sis_language, keywords, data) :
        """~MMT"""

        if sis_language == "en" :
            keywords = keywords[:2]
        elif sis_language == "tr" :
            keywords = keywords[2:]
        data_1 = data[
            data.find(keywords[0]) + len(keywords[0]) + 1
            :
            data.find(keywords[1]) - 1
        ]
        data_2 = data[
            data.find(keywords[1]) + len(keywords[1]) + 1
            :
        ]
        return data_1, data_2

    def _parse_transcript_information(self) -> None:
        """
        Private method for parsing extracted transcript information from the source.
        """

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
        
        student_school_id, student_national_id = self.__extract_dynamicly(sis_language, ["Student ID", "National ID", "Öğrenci Numarası", "TC Kimlik Numarası"], student_parse[0])
        student_name, student_surname = self.__extract_dynamicly(sis_language, ["Name", "Surname", "Adı", "Soyadı"], student_parse[1])
        student_faculty, student_department = self.__extract_dynamicly(sis_language, ["Faculty / Department", "Program Name", "Fakülte", "Bölüm"], student_parse[2])
        language_of_instruction, student_status = self.__extract_dynamicly(sis_language, ["Language of Instruction", "Student Status", "Eğitim Dili", "Öğrencilik Durumu"], student_parse[3])

        semesters = {}
        semester_no = 1
        original_course_list = []
        for current_course in output :

            prep = "PREP" in current_course
            semester = current_course.startswith("Semester Credits Attempted") or current_course.startswith("Dönem Alınan Kredi")
            student = "Student ID" in current_course or "Öğrenci Numarası" in current_course

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

                if course_code[-1] != "*" :
                    original_course_list.append(course_list[course_index])

            semesters[f"semester_{semester_no}"] = {
                "semester_definition" : semester_definition,
                "course_list" : course_list
            }

            semester_no += 1

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

        if self.save_to_file :
            with open(f"{student_name}_online_{sis_language}.json", "w", encoding="utf-8") as file :
                json.dump(output, file, ensure_ascii=False, indent=4)

        self.transcript_data = output

    def get_transcript_data(self) -> dict :
        """
        Private method for getting transcript data.
        returns:
            transcript_data : dict
        """
        
        self._extract_transcript_information()
        self._parse_transcript_information()

        return self.transcript_data
    
class OfflineParser(Parser) :

    def __init__(self, path_to_file:str=None, save_to_file:str=False, *args, **kwargs) -> None:
        super().__init__()

        self.path_to_file = path_to_file

        self.save_to_file = save_to_file

        self.extracted = None
        self.transcript_data = None

    def _extract_transcript_information(self) -> None :
        """
        Private method for extracting transcript information from the source.
        """
        
        pdf_file = ppdf.PdfReader(self.path_to_file)

        output = []
        for current_page in pdf_file.pages :
            current_page_text = current_page.extract_text()
            current_page_elements = current_page_text.split("\n")
            output.extend(current_page_elements)

        self.extracted = output

    def _parse_transcript_information(self) -> None:
        """
        Private method for parsing extracted transcript information from the source.
        """
        
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

        splitters = [
            "Fall Semester", "Spring Semester", "Summer School", "Fall Dönemi", "Spring Dönemi", "Bahar Dönemi", "Güz Dönemi", "Yaz Okulu"
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
        founded_semesters.append(temp)

        # clean prep semesters
        clean_index = []
        for semester_index, current_semester in enumerate(founded_semesters) :
            if "Prep" in current_semester :
                clean_index.append(semester_index)

        for index in reversed(clean_index) :
            founded_semesters.pop(index)

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
                if current_string == "Semester" or current_string == "Dönem":
                    break
                
                if add_count == 7 :
                    course_list.append(temp)

                    if temp["course_code"][-1] != "*" :
                        original_course_list.append(temp)

                    temp = {}
                    add_count = 1

                temp[map_hash[add_count]] = current_string
                add_count += 1

            course_list.append(temp)
            if temp["course_code"][-1] != "*" :
                original_course_list.append(temp)
                        
            semesters[f"semester_{semester_no}"] = {
                "semester_definition" : semester_definition,
                "course_list" : course_list
            }
            semester_no += 1
        
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

        self.transcript_data = output

        if self.save_to_file :
            with open(f"{student_name}_offline_{sis_language}.json", "w", encoding="utf-8") as file :
                json.dump(output, file, ensure_ascii=False, indent=4)

    def get_transcript_data(self) -> dict :
        """
        Private method for getting transcript data.
        returns:
            transcript_data : dict
        """

        self._extract_transcript_information()
        self._parse_transcript_information()

        return self.transcript_data
    
class UserVerifier() :

    def __init__(self, username:str=None, password:str=None, isHidden=True, match_id=None, *args, **kwargs) -> None:
        super().__init__()

        self.username = username
        self.password = password

        self.isHidden = isHidden

        self.match_id = match_id
        self.received_id = None

        self.is_user_verified = False

    def _receive_system_id(self) -> None:
        """
        Private method for extracting transcript information from the source.
        """

        main_url = SELENIUM_DC.OLEXER_SYSTEM_LOGIN_URL

        client = Web(isHidden=self.isHidden)
        client.open_web_page(main_url)

        username_entry = client.create_element(SELENIUM_DC.OLEXER_USERNAME_ENTRY_XPATH)
        username_entry.send_keys(self.username)

        password_entry = client.create_element(SELENIUM_DC.OLEXER_PASSWORD_ENTRY_XPATH)
        password_entry.send_keys(self.password)

        login_button = client.create_element(SELENIUM_DC.OLEXER_LOGIN_BUTTON_XPATH)
        login_button.click()

        continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
        continue_button.click()
                
        profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
        profile_selection_label.click()

        drop_down_menu = client.create_element(SELENIUM_DC.OLEXER_DROP_DOWN_MENU_XPATH)
        check_list = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
        flag = False
        for current_element in drop_down_menu.find_elements(by=By.TAG_NAME, value="a") :
            if current_element.text in check_list :
                client.click_on_element(current_element)
                idSelectionMenu = client.create_element(SELENIUM_DC.OLEXER_ID_SELECTION_XPATH)
                for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
                    if element.get_attribute(SELENIUM_DC.OLEXER_SOURCE_ATTRIBUTE_TAGS[1]).split("-")[-1].strip() in check_list :
                        client.click_on_element(element)
                        flag = True
                        break
                break
        if flag:
            continue_button = client.create_element(SELENIUM_DC.OLEXER_CONTINUE_BUTTON_XPATH)
            client.click_on_element(continue_button)

        profile_selection_label = client.create_element(SELENIUM_DC.OLEXER_PROFILE_SELECTION_XPATH)
        profile_selection_label.click()

        student_info_a_tag = client.create_element(SELENIUM_DC.OLEXER_STUDENT_INFO_XPATH)

        self.received_id = re.findall(r"\d+", student_info_a_tag.text)[0]

    def _compare_ids(self) -> bool:
        
        if self.match_id == None :
            self.is_user_verified = False
        else :
            if self.match_id == self.received_id :
                self.is_user_verified = True
            else :
                self.is_user_verified = False

    def verify_user(self) -> None :
        """
        Public method for verifying user.
        """

        self._receive_system_id()
        self._compare_ids()
                
        return self.is_user_verified