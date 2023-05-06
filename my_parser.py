from    abc         import ABC, abstractmethod
from    datetime    import datetime
from    Utilities   import Web, By
import  PyPDF2  as  ppdf
import  json

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
    def _get_transcript_data(self) -> dict:
        """
        Abstract method for extracting transcript information from the source.
        @returns:
            transcript_data : dict
        """
        pass

class OnlineParser(Parser) :

    def __init__(self, username:str=None, password:str=None, save_to_file:bool=False, *args, **kwargs) -> None:
        super().__init__()

        self.username = username
        self.password = password

        self.save_to_file = save_to_file

        self.extracted = None
        self.transcript_data = None

    def _extract_transcript_information(self) -> None:
        """
        Private method for extracting transcript information from the source.
        """

        main_url = "https://sis.mef.edu.tr/auth/login"

        client = Web(isHidden=True)
        client.open_web_page(main_url)

        username_entry = client.create_element("//*[@id=\"kullanici_adi\"]")
        username_entry.send_keys(self.username)

        password_entry = client.create_element("//*[@id=\"kullanici_sifre\"]")
        password_entry.send_keys(self.password)

        login_button = client.create_element("//*[@id=\"loginForm\"]/div[2]/div[3]/button")
        login_button.click()

        continue_button = client.create_element("/html/body/div[3]/input")
        continue_button.click()

        profile_selection_label = client.create_element("/html/body/div[2]/div/div[3]/ul/li")
        profile_selection_label.click()

        drop_down_menu = client.create_element("/html/body/div[2]/div/div[3]/ul/li/ul")
        check_list = ["Diğer Kimlikler", "Other IDs", "Anadal", "Major"]
        flag = False
        for current_element in drop_down_menu.find_elements(by=By.TAG_NAME, value="a") :
            if current_element.text in check_list :
                client.click_on_element(current_element)
                idSelectionMenu = client.create_element("//*[@id=\"yetkiDegistir\"]/div/ul")
                for element in idSelectionMenu.find_elements(by=By.TAG_NAME, value="a") :
                    if element.get_attribute("text").split("-")[-1].strip() in check_list :
                        client.click_on_element(element)
                        flag = True
                        break
                break
        if flag:
            continue_button = client.create_element("/html/body/div[3]/input")
            client.click_on_element(continue_button)

        transkriptUrl = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
        client.open_web_page(transkriptUrl)

        table_elements = client.browser.find_elements(By.TAG_NAME, "table")

        output = []
        for element in table_elements :
            output.append(element.text)

        client.browser.quit()

        self.extracted = output

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
        if sis_language == "en" :
            keywords = ["Student ID", "National ID"]
        elif sis_language == "tr" :
            keywords = ["Öğrenci Numarası", "TC Kimlik Numarası"]
        student_id = student_parse[0][
            student_parse[0].find(keywords[0]) + len(keywords[0]) + 1 
            :
            student_parse[0].find(keywords[1]) - 1
        ]
        national_id = student_parse[0][
            student_parse[0].find(keywords[1]) + len(keywords[1]) + 1
            :
        ]
        if sis_language == "en" :
            keywords = ["Name", "Surname"]
        elif sis_language == "tr" :
            keywords = ["Adı", "Soyadı"]
        student_name = student_parse[1][
            student_parse[1].find(keywords[0]) + len(keywords[0]) + 1
            :
            student_parse[1].find(keywords[1]) - 1
        ]
        student_surname = student_parse[1][
            student_parse[1].find(keywords[1]) + len(keywords[1]) + 1
            :
        ]
        if sis_language == "en" :
            keywords = ["Faculty / Department", "Program Name"]
        elif sis_language == "tr" :
            keywords = ["Fakülte", "Bölüm"]
        student_faculty = student_parse[2][
            student_parse[2].find(keywords[0]) + len(keywords[0]) + 1
            :
            student_parse[2].find(keywords[1]) - 1
        ]
        student_department = student_parse[2][
            student_parse[2].find(keywords[1]) + len(keywords[1]) + 1
            :
        ]
        if sis_language == "en" :
            keywords = ["Language of Instruction", "Student Status"]
        elif sis_language == "tr" :
            keywords = ["Eğitim Dili", "Öğrencilik Durumu"]
        language_of_instruction = student_parse[3][
            student_parse[3].find(keywords[0]) + len(keywords[0]) + 1
            :
            student_parse[3].find(keywords[1]) - 1
        ]
        student_status = student_parse[3][
            student_parse[3].find(keywords[1]) + len(keywords[1]) + 1
            :
        ]
        semesters = {}
        for index, current_course in enumerate(output) :

            prep = "PREP" in current_course
            semester = current_course.startswith("Semester Credits Attempted") or current_course.startswith("Dönem Alınan Kredi")
            student = "Student ID" in current_course or "Öğrenci Numarası" in current_course

            if prep or semester or student :
                continue

            semester_parse = current_course.split("\n")
            semester_name = semester_parse.pop(0)
            semester_parse.pop(0) # remove junk info (colum names)
            if "Academic Standing" in semester_parse[-1] or "Akademik Durum" in semester_parse[-1] :
                semester_parse.pop() # remove junk info (academic standing)
            cumulative_credits_attempted = semester_parse.pop()
            semester_credits_attempted = semester_parse.pop()
            course_list = semester_parse
            for course_index, course_info in enumerate(course_list) :

                course_info_parse = course_info.split(" ")
                course_code = course_info_parse.pop(0) + " " + course_info_parse.pop(0)
                course_name = " ".join(course_info_parse[:-4])
                course_lang = course_info_parse[-4]
                course_credit = course_info_parse[-3]
                course_grade = course_info_parse[-2]
                course_grade_point = course_info_parse[-1]

                course_list[course_index] = {
                    "course_code" : course_code,
                    "course_name" : course_name,
                    "course_lang" : course_lang,
                    "course_credit" : course_credit,
                    "course_grade" : course_grade,
                    "course_grade_point" : course_grade_point,
                }

            semesters[semester_name] = {
                "course_list" : course_list
            }

        output = {
            "parsing_type" : "online",
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
            "semesters" : semesters,
        }

        if self.save_to_file :
            with open(f"{student_name}_online_{sis_language}.json", "w", encoding="utf-8") as file :
                json.dump(output, file, ensure_ascii=False, indent=4)

        self.transcript_data = output

    def _get_transcript_data(self) -> dict :
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

        self.transcript_data = output

        if self.save_to_file :
            with open(f"{student_name}_offline_{sis_language}.json", "w", encoding="utf-8") as file :
                json.dump(output, file, ensure_ascii=False, indent=4)

    def _get_transcript_data(self) -> dict :
        """
        Private method for getting transcript data.
        returns:
            transcript_data : dict
        """

        self._extract_transcript_information()
        self._parse_transcript_information()

        return self.transcript_data

if __name__ == "__main__" :

    fp = " path "
    username = " c "
    password = " c "

    parser = OnlineParser(username=username, password=password, save_to_file=True)
    parser.get_transcript_data()

    parser = OfflineParser(path_to_file=fp, save_to_file=True)
    parser.get_transcript_data()