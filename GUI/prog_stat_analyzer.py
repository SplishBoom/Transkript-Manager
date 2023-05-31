from    Utilities   import  calculate_performance, filter_by # -> Utilitiy functions.
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI

class StatAnalyzer(ttk.Frame) :

    def __init__(self, application_container : ttk.Frame, parent : ttk.Frame, root : tk.Tk, current_user_data : dict, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for StatAnalyzer class. Used to initialize main window of the program.
        @Parameters:
            application_container - Required : Container frame of the application. (ttk.Frame) -> Which is used to place the application frame.
            parent                - Required : Parent frame of the application. (ttk.Frame) -> Which is used to set connection to application frame.
            root                  - Required : Root window of the application. (tk.Tk) -> Which is used to set connection between frames.
            current_user_data     - Required : Current user data. (dict) -> Which is used to determine current user data.
            DEBUG                 - Optional : Debug mode flag. (bool) (default : False) -> Which is used to determine whether the application is in debug mode or not.
        @Returns:
            None
        """
        # Initialize main window of the program.
        super().__init__(application_container, *args, **kwargs)

        # Set class variables.
        self.application_container = application_container
        self.parent = parent
        self.DEBUG  = DEBUG
        self.root   = root
        
        # Load user data.
        self.__load_user_data(current_user_data)

        # Load containers.
        self.__load_containers()

        # Load program
        self.__load_scholarship_status()
        self.__load_course_info_status()

    def _get_text(self, text : str) -> str:
        """
        Gets the text from the language dictionary.
        @Parameters:
            text - Required : Text to get from the dictionary. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            translated_text - str : Translated text. (str)
        """
        # Direct wrapper to parent's _get_text method.
        return self.parent._get_text(text, self.parsing_language)

    def __load_containers(self) -> None:
        """
        Loads containers of the main window.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create the main container.
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)
        # Configure the main container.
        self.container.grid_rowconfigure((0,1), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        # Create the program containers.
        self.program_scholarship_status_container = ttk.Frame(self.container)
        self.program_scholarship_status_container.grid(row=0, column=0)

        self.program_course_info_status_container = ttk.Frame(self.container)
        self.program_course_info_status_container.grid(row=1, column=0)

    def __load_user_data(self, given_user_data : dict) -> None:
        """
        Loads user data into class fields.
        @Parameters:
            given_user_data - Required : Given user data. (dict) -> Which is used to load user data into class fields.
        @Returns:
            None
        """
        # Load user data into class fields.
        self.owner_id : str = given_user_data["owner_id"]
        self.parsing_type : str = given_user_data["parsing_type"]
        self.parsing_language : str = given_user_data["parsing_language"]
        self.transcript_manager_date : str = given_user_data["transcript_manager_date"]
        self.transcript_creation_date : str = given_user_data["transcript_creation_date"]
        self.semesters : dict = given_user_data["semesters"]
        self.original_course_list : list = given_user_data["original_course_list"]
        self.filtering : tuple = given_user_data["filtering"]
        self.sorting : tuple = given_user_data["sorting"]
        self.modified_course_list : list = given_user_data["modified_course_list"]
        self.document_name : str = given_user_data["document_name"]
        self.updated_course_list : list = given_user_data["updated_course_list"]
        self.subtracted_course_list : list = given_user_data["subtracted_course_list"]
        self.added_course_list : list = given_user_data["added_course_list"]

        # Update semester data by initialized class variables.
        self.___update_semester_data()

    def ___update_semester_data(self) -> None:
        """
        Updates semester data by initialized class variables.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check for updated courses, then apply changes to semester data.
        updated_course_codes = [course["course_code"] for course in self.updated_course_list]
        for semester in self.semesters :
            current_semester = self.semesters[semester]
            current_course_list = current_semester["course_list"]
            new_course_list = []
            for current_course in current_course_list :
                current_course_code = current_course["course_code"]
                if current_course_code in updated_course_codes :
                    updated_course_data = self.updated_course_list[updated_course_codes.index(current_course_code)]
                    new_course_list.append(updated_course_data)
                else :
                    new_course_list.append(current_course)
            current_semester["course_list"] = new_course_list

        # Check for added courses, then apply changes to the last semester data.
        last_semester_id = f"semester_{len(self.semesters)}"
        self.semesters[last_semester_id]["course_list"].extend(self.added_course_list)

        # Check for subtracted courses, then apply changes to semester data.
        removed_course_codes = [course["course_code"] for course in self.subtracted_course_list]
        for semester in self.semesters :
                
            current_semester = self.semesters[semester]
            current_course_list = current_semester["course_list"]

            new_course_list = []
            for current_course in current_course_list :
                current_course_code = current_course["course_code"]
                if current_course_code in removed_course_codes :
                    continue
                else :
                    new_course_list.append(current_course)

            current_semester["course_list"] = new_course_list

        # Apply filtering to semester data.
        for semester in self.semesters :

            current_semester = self.semesters[semester]
            current_course_list = current_semester["course_list"]

            for current_filter in self.filtering :
                current_course_list = filter_by(current_course_list, current_filter)

            current_semester["course_list"] = current_course_list

    def ___create_scholarship_status_data(self) -> None:
        """
        Creates scholarship status data.
        @Parameters:
            None
        @Returns:
            None
        """
        # Get course list.
        course_list = []
        for semester in self.semesters :
            course_list.extend(self.semesters[semester]["course_list"])

        # Get performance.
        performance = calculate_performance(course_list, skip_retakens=True)
        credits_attempted = performance["credits_attempted"]
        credits_successful = performance["credits_successful"]
        credits_included_in_gpa = performance["credits_included_in_gpa"]
        gpa = performance["gpa"]

        # Calculate scholarship status via expected credits.
        expected_credits = len(self.semesters) * 30

        # Create scholarship status data. By MEF University Scholarship Criteria.
        # Typo -> dict["percentage"] = int
        # Typo -> dict["message"] = str
        # Typo -> dict["note"] = str
        if credits_attempted < expected_credits:
            self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship", "note":"You haven't taken enough courses to apply for scholarship"}
        if credits_included_in_gpa < expected_credits:
            self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship", "note":"You haven't completed enough credits for scholarship"}
        else :
            if 3.75 <= gpa <= 4 :
                self.scholarship_status = {"percentage":50, "message":"You are eligible for a %50 scholarship", "note":"You have a perfect GPA for scholarship"}
            elif 3.60 <= gpa < 3.75 :
                self.scholarship_status = {"percentage":40, "message":"You are eligible for a %40 scholarship", "note":"You have a high GPA for scholarship"}
            elif 3.50 <= gpa < 3.60 :
                self.scholarship_status = {"percentage":25, "message":"You are eligible for a %25 scholarship", "note":"You have a nice GPA for scholarship"}
            elif 3.00 <= gpa < 3.50 :
                self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship", "note":"You have a good GPA for scholarship"}
            elif 2.00 <= gpa < 3.00 :
                self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship", "note":"You have a low GPA for scholarship"}
            elif 0 <= gpa < 2.00 :
                self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship", "note":"You have a very low GPA for scholarship"}
                
    def ___create_course_info_status_data(self) -> None:
        
        # Get course list. Only last taken courses.
        course_list = []
        for semester in self.semesters :
            for course in self.semesters[semester]["course_list"]:
                course_code = course["course_code"]
                if not course_code.endswith("*") :
                    course_list.append(course)

        # Split courses
        grades_must_taken_list = ["F", "W"]
        grades_should_taken_list = ["B-", "C+", "C", "C-", "D+", "D"]

        # Initialize course variables
        self.grades_must_taken = []
        self.grades_should_taken = []

        # Fill course variables
        for course in course_list :
            course_grade = course["course_grade"]
            if course_grade in grades_must_taken_list :
                self.grades_must_taken.append(course)
            elif course_grade in grades_should_taken_list :
                self.grades_should_taken.append(course)

    def __load_scholarship_status(self) -> None:
        """
        Loads scholarship status.
        @Parameters:
            None
        @Returns:
            None
        """
        # Load scholarship status to class fields.
        self.___create_scholarship_status_data()

        # Configure scholarship status container.
        self.program_scholarship_status_container.grid_rowconfigure((0,1), weight=1)
        self.program_scholarship_status_container.grid_columnconfigure(0, weight=1)
        
        # Load scholarship status info label.
        self.scholarship_status_label = ttk.Label(self.program_scholarship_status_container, text=self._get_text("Scholarship Status"))
        self.scholarship_status_label.grid(row=0, column=0)

        # Openup scholarship status treeview.
        self.scholarship_status_treeview = ttk.Treeview(self.program_scholarship_status_container, height=1, show="headings", selectmode="none")
        self.scholarship_status_treeview.grid(row=1, column=0)

        # Configure scholarship status treeview.
        self.scholarship_status_treeview["columns"] = ("_percentage", "_message", "_note")

        self.scholarship_status_treeview.heading("_percentage", text=self._get_text("Percentage"))
        self.scholarship_status_treeview.heading("_message", text=self._get_text("Message"))
        self.scholarship_status_treeview.heading("_note", text=self._get_text("Footnote"))

        self.scholarship_status_treeview.column("_percentage", anchor="center", width=90)
        self.scholarship_status_treeview.column("_message", anchor="center", width=250)
        self.scholarship_status_treeview.column("_note", anchor="center", width=250)

        # Insert scholarship status data to treeview.
        self.scholarship_status_treeview.insert("", "end", values=(self.scholarship_status["percentage"], self._get_text(self.scholarship_status["message"]), self._get_text(self.scholarship_status["note"])))

    def __load_course_info_status(self) -> None:
        """
        Loads course info status.
        @Parameters:
            None
        @Returns:
            None
        """
        # Load course info status to class fields.
        self.___create_course_info_status_data()

        # Create course info status container.
        self.program_course_info_status_container.grid_rowconfigure((0,1,2,3), weight=1)
        self.program_course_info_status_container.grid_columnconfigure((0,1), weight=1)

        # Load treeview for courses must taken and again.
        self.course_info_status_treeview_MUST_TAKEN()
        self.course_info_status_treeview_SHOULD_TAKEN()

    def course_info_status_treeview_MUST_TAKEN(self) -> None:
        """
        Loads course info status treeview for courses must taken again.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create course info status treeview for courses must taken again.
        self.course_info_status_treeview_MUST_TAKEN_info_label = tk.Label(self.program_course_info_status_container, text=self._get_text("Courses Must Taken Again"))
        self.course_info_status_treeview_MUST_TAKEN_info_label.grid(row=0, column=0, columnspan=2)

        # Set a scrollbar for treeview.
        self.course_info_status_treeview_MUST_TAKEN_scrollbar = ttk.Scrollbar(self.program_course_info_status_container, orient="vertical")
        self.course_info_status_treeview_MUST_TAKEN_scrollbar.grid(row=1, column=1, sticky="ns")

        # Openup course info status treeview for courses must taken again.
        maximum_height = 5
        self.course_info_status_treeview_MUST_TAKEN = ttk.Treeview(self.program_course_info_status_container, height=min(len(self.grades_must_taken), maximum_height), show="headings", selectmode="none", yscrollcommand=self.course_info_status_treeview_MUST_TAKEN_scrollbar.set)
        self.course_info_status_treeview_MUST_TAKEN.grid(row=1, column=0)
        # Configure scrollbar.
        self.course_info_status_treeview_MUST_TAKEN_scrollbar.config(command=self.course_info_status_treeview_MUST_TAKEN.yview)

        # Secure scrollbar.
        if len(self.grades_must_taken) <= maximum_height :
            self.course_info_status_treeview_MUST_TAKEN_scrollbar.grid_remove()

        # Configure course info status treeview for courses must taken again.
        if self.grades_must_taken == [] :
            # If no data found, merge columns.
            self.course_info_status_treeview_MUST_TAKEN["columns"] = ("_column")

            self.course_info_status_treeview_MUST_TAKEN.heading("_column", text=self._get_text("No Course Must Taken Again"))
            self.course_info_status_treeview_MUST_TAKEN.column("_column", anchor="center", width=720)
        else :
            # If data found, configure columns.
            self.course_info_status_treeview_MUST_TAKEN["columns"] = ("_code", "_name", "_canguage", "_credit", "_crade", "_crade_point")

            # Set headings.
            self.course_info_status_treeview_MUST_TAKEN.heading("_code", text=self._get_text("Course Code"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_name", text=self._get_text("Course Name"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_canguage", text=self._get_text("Course Language"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_credit", text=self._get_text("Course Credit"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_crade", text=self._get_text("Course Grade"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_crade_point", text=self._get_text("Course Grade Point"))

            # Set columns.
            self.course_info_status_treeview_MUST_TAKEN.column("_code", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_name", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_canguage", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_credit", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_crade", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_crade_point", anchor="center", width=120)

        # Insert course info status data to treeview.
        if not self.grades_must_taken == [] :
            for course in self.grades_must_taken :
                self.course_info_status_treeview_MUST_TAKEN.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]))

    def course_info_status_treeview_SHOULD_TAKEN(self) -> None:
        """
        Loads course info status treeview for courses should taken again.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create course info status treeview for courses should taken again.
        self.course_info_status_treeview_SHOULD_TAKEN_info_label = tk.Label(self.program_course_info_status_container, text=self._get_text("Courses Should Taken Again"))
        self.course_info_status_treeview_SHOULD_TAKEN_info_label.grid(row=2, column=0, columnspan=2)

        # Set a scrollbar for treeview.
        self.course_info_status_treeview_SHOULD_TAKEN_scrollbar = ttk.Scrollbar(self.program_course_info_status_container, orient="vertical")
        self.course_info_status_treeview_SHOULD_TAKEN_scrollbar.grid(row=3, column=1, sticky="ns")

        # Openup course info status treeview for courses should taken again.
        maximum_height = 5
        self.course_info_status_treeview_SHOULD_TAKEN = ttk.Treeview(self.program_course_info_status_container, height=min(len(self.grades_should_taken), maximum_height), show="headings", selectmode="none", yscrollcommand=self.course_info_status_treeview_SHOULD_TAKEN_scrollbar.set)
        self.course_info_status_treeview_SHOULD_TAKEN.grid(row=3, column=0)
        # Configure scrollbar.
        self.course_info_status_treeview_SHOULD_TAKEN_scrollbar.config(command=self.course_info_status_treeview_SHOULD_TAKEN.yview)

        # Secure scrollbar.
        if len(self.grades_should_taken) <= maximum_height :
            self.course_info_status_treeview_SHOULD_TAKEN_scrollbar.grid_remove()

        # Configure course info status treeview for courses should taken again.
        if self.grades_should_taken == [] :
            # If no data found, merge columns.
            self.course_info_status_treeview_SHOULD_TAKEN["columns"] = ("_column")

            self.course_info_status_treeview_SHOULD_TAKEN.heading("_column", text=self._get_text("No Course Should Taken Again"))
            self.course_info_status_treeview_SHOULD_TAKEN.column("_column", anchor="center", width=720)
        else :
            # If data found, configure columns.
            self.course_info_status_treeview_SHOULD_TAKEN["columns"] = ("_code", "_name", "_canguage", "_credit", "_crade", "_crade_point")

            # Set headings.
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_code", text=self._get_text("Course Code"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_name", text=self._get_text("Course Name"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_canguage", text=self._get_text("Course Language"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_credit", text=self._get_text("Course Credit"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_crade", text=self._get_text("Course Grade"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_crade_point", text=self._get_text("Course Grade Point"))

            # Set columns.
            self.course_info_status_treeview_SHOULD_TAKEN.column("_code", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_name", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_canguage", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_credit", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_crade", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_crade_point", anchor="center", width=120)

        # Insert course info status data to treeview.
        if not self.grades_should_taken == [] :
            for course in self.grades_should_taken :
                self.course_info_status_treeview_SHOULD_TAKEN.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]))