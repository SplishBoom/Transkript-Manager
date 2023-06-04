from    Utilities       import  calculate_performance, filter_by # -> Utilitiy functions.
from    Environment     import  GUI_DC # -> Environment variables
import  customtkinter   as      ctk # -> GUI.

class StatAnalyzer(ctk.CTkFrame) :

    def __init__(self, application_container : ctk.CTkFrame, parent : ctk.CTkFrame, root : ctk.CTk, current_user_data : dict, DEBUG : bool = False, *args, **kwargs) -> None:
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

    def __load_containers(self) -> None:
        """
        Loads containers of the main window.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the initial configuration, to make expandable affect on window.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the main container.
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container.
        self.container.grid_rowconfigure((0,1), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        # Create the program containers.
        self.scholarship_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.scholarship_container.grid(row=0, column=0, sticky="nsew")

        self.course_info_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.course_info_container.grid(row=1, column=0, sticky="nsew")

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
        self.scholarship_container.grid_rowconfigure((0,1), weight=1)
        self.scholarship_container.grid_columnconfigure((0,1,2), weight=1)

        # Load scholarship status info label.
        self.info_label = ctk.CTkLabel(self.scholarship_container, text=self._get_text("Scholarship Status"),
            fg_color = GUI_DC.DARK_BACKGROUND,
            bg_color = GUI_DC.DARK_BACKGROUND,
            text_color = GUI_DC.LIGHT_TEXT_COLOR,
            font = ("Arial", 20, "bold"),
            anchor = "center",
            corner_radius =  25
        )
        self.info_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING//2)
    
        # Load info widgets
        self.percentage_label = ctk.CTkLabel(self.scholarship_container, text=self.scholarship_status["percentage"],
            fg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
            bg_color = GUI_DC.DARK_BACKGROUND,
            text_color = GUI_DC.LIGHT_TEXT_COLOR,
            font = ("Arial", 13, "bold"),
            anchor = "center",
            corner_radius =  50
        )
        self.percentage_label.grid(row=1, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING)

        self.message_label = ctk.CTkLabel(self.scholarship_container, text=self._get_text(self.scholarship_status["message"]),
            fg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
            bg_color = GUI_DC.DARK_BACKGROUND,
            text_color = GUI_DC.LIGHT_TEXT_COLOR,
            font = ("Arial", 13, "bold"),
            anchor = "center",
            corner_radius =  50
        )
        self.message_label.grid(row=1, column=1, sticky="nsew", padx=GUI_DC.INNER_PADDING)

        self.note_label = ctk.CTkLabel(self.scholarship_container, text=self._get_text(self.scholarship_status["note"]),
            fg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
            bg_color = GUI_DC.DARK_BACKGROUND,
            text_color = GUI_DC.LIGHT_TEXT_COLOR,
            font = ("Arial", 13, "bold"),
            anchor = "center",
            corner_radius =  50
        )
        self.note_label.grid(row=1, column=2, sticky="nsew", padx=GUI_DC.INNER_PADDING)

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
        self.course_info_container.grid_rowconfigure((0), weight=1)
        self.course_info_container.grid_columnconfigure((0), weight=1)

        # Set a tabview for switching between course info status.
        ctk.CTkTabview._segmented_button_border_width = 4
        ctk.CTkTabview._button_height = 30
        ctk.CTkTabview._top_button_overhang = 9
        self.tab_view = ctk.CTkTabview(self.course_info_container, 
                                       fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, 
                                       bg_color=GUI_DC.DARK_BACKGROUND,
                                       text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                       text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
                                       segmented_button_fg_color=GUI_DC.DARK_BACKGROUND,
                                       segmented_button_selected_color=GUI_DC.BUTTON_LIGHT_DBLUE_HOVER,
                                       segmented_button_selected_hover_color=GUI_DC.BUTTON_LIGHT_DBLUE_HOVER,
                                       segmented_button_unselected_color=GUI_DC.DARK_BACKGROUND,
                                       segmented_button_unselected_hover_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                       corner_radius=25,
                                       width=300,
                                       height=250,
                                       border_width=0
        )
        self.tab_view.grid(row=0, column=0, sticky="nsew")

        # Set tab names.
        self.must_taken_courses_tab_name = "Critical Courses" if self.parsing_language == "en" else "Kritik Kurslar"
        self.should_taken_courses_tab_name = "Complimentary Courses" if self.parsing_language == "en" else "Tamamlayici Kurslar"

        # Add tabs.
        self.must_taken_courses_tab = self.tab_view.add(self.must_taken_courses_tab_name)
        self.should_taken_courses_tab = self.tab_view.add(self.should_taken_courses_tab_name)

        # Configure tabs.
        self.must_taken_courses_tab.grid_rowconfigure((0), weight=1)
        self.must_taken_courses_tab.grid_columnconfigure((0), weight=1)
        self.should_taken_courses_tab.grid_rowconfigure((0), weight=1)
        self.should_taken_courses_tab.grid_columnconfigure((0), weight=1)

        # Set the current tab to initial course info.
        self.tab_view.set(self.must_taken_courses_tab_name)

        # Load course info status info label.
        self._load_must_taken_courses()
        self._load_should_taken_courses()


    def _load_must_taken_courses(self) -> None:
        """
        Loads course must_taken courses with bubble image.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create a hold container.
        self.must_taken_container = ctk.CTkFrame(self.must_taken_courses_tab, fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, bg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, corner_radius=25)
        self.must_taken_container.grid(row=0, column=0, sticky="nsew")
        
        # Set the inital values and calculate the row and column count.
        courses_in_a_column = 6
        number_of_must_courses = len(self.grades_must_taken)
        row_count = (number_of_must_courses - 1) // courses_in_a_column + 1
        row_count = max(row_count, 1)
        
        # Used inital values to configure the grid.
        self.must_taken_container.grid_rowconfigure(tuple(range(row_count)), weight=1)
        self.must_taken_container.grid_columnconfigure((0), weight=1)
        
        # Check if there is a no course situation.
        if len(self.grades_must_taken) == 0 :
            # If yes, show a congrat message and leave.
            self.congrats_label = ctk.CTkLabel(self.must_taken_container, text=self._get_text("Congrats! You don't have any course to take again."),
                fg_color = GUI_DC.BUTTON_LIGHT_GREEN,
                bg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
                text_color = GUI_DC.DARK_TEXT_COLOR,
                font = ("Arial", 18, "italic"),
                anchor = "center",
                corner_radius =  25
            )
            self.congrats_label.grid(row=0, column=0, sticky="nsew")
        else :
            # Otherwise, put the available courses on the grid. Start by creating a row for each 5 elements.
            data_row_frames = []
            for i in range(row_count) :
                new_frame = ctk.CTkFrame(self.must_taken_container, fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, bg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, corner_radius=25)
                new_frame.grid(row=i, column=0, sticky="nsew")
                # Store the rows (frames) for later use.
                data_row_frames.append(new_frame)

            # Iterate over all courses, than apply //5 operation and put 5 element maximum in a row at each.
            for i in range(number_of_must_courses) :
                # Get course name and grade.
                course_code = self.grades_must_taken[i]["course_code"]
                course_grade = self.grades_must_taken[i]["course_grade"]
                
                # Set a show message.
                course_info = f"{course_code}\n\n{course_grade}"
                
                # Find the index of the current row.
                row_index = i // courses_in_a_column

                # Create a label with optimized parameters. (Bubble Effect !)
                course_info_label = ctk.CTkLabel(data_row_frames[row_index], text=course_info,
                    fg_color = GUI_DC.BUTTON_LIGHT_RED,
                    bg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
                    text_color = GUI_DC.DARK_TEXT_COLOR,
                    font = ("Arial", 13, "bold"),
                    anchor = "center",
                    corner_radius =  50,
                    width=50,
                    height=50
                )
                # Pack the label. | Grid is not used, it is not easy to automatically center widgets with setted column. Ex columspan=3 this should be an argument but there are 4 courses, and etc.
                course_info_label.pack(side="left", expand=True, fill="y", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
   
    def _load_should_taken_courses(self) -> None:
        """
        Loads course should_tak courses with bubble image.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create a hold container.
        self.should_taken_container = ctk.CTkFrame(self.should_taken_courses_tab, fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, bg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, corner_radius=25)
        self.should_taken_container.grid(row=0, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
        
        # Set the inital values and calculate 
        courses_in_a_column = 6
        number_of_must_courses = len(self.grades_should_taken)
        row_count = (number_of_must_courses - 1) // courses_in_a_column + 1
        row_count = max(row_count, 1)
        
        # Used inital values to configure the grid.
        self.should_taken_container.grid_rowconfigure(tuple(range(row_count)), weight=1)
        self.should_taken_container.grid_columnconfigure((0), weight=1)
        
        # Check if there is a no course situation.
        if len(self.grades_should_taken) == 0 :
            # If yes, show a congrat message and leave.
            self.congrats_label = ctk.CTkLabel(self.should_taken_container, text=self._get_text("Congrats! You don't have any course to take again."),
                fg_color = GUI_DC.BUTTON_LIGHT_GREEN,
                bg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
                text_color = GUI_DC.DARK_TEXT_COLOR,
                font = ("Arial", 18, "italic"),
                anchor = "center",
                corner_radius =  25
            )
            self.congrats_label.grid(row=0, column=0, sticky="nsew")
        else :
            # Otherwise, put the available courses on the  Start by creating a row for each 5 elements.
            data_row_frames = []
            for i in range(row_count) :
                new_frame = ctk.CTkFrame(self.should_taken_container, fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, bg_color=GUI_DC.SECONDARY_DARK_BACKGROUND, corner_radius=25)
                new_frame.grid(row=i, column=0, sticky="nsew")
                # Store the rows (frames) for
                data_row_frames.append(new_frame)

            # Iterate over all courses, than apply //5 operation and put 5 element maximum in a row at each.
            for i in range(number_of_must_courses) :
                # Get course name and grade.
                course_code = self.grades_should_taken[i]["course_code"]
                course_grade = self.grades_should_taken[i]["course_grade"]
                
                # Set a show message.
                course_info = f"{course_code}\n\n{course_grade}"
                
                # Find the index of the current row.
                row_index = i // courses_in_a_column

                # Create a label with optimized parameters. (Bubble Effect !)
                course_info_label = ctk.CTkLabel(data_row_frames[row_index], text=course_info,
                    fg_color = GUI_DC.BUTTON_LIGHT_BLUE,
                    bg_color = GUI_DC.SECONDARY_DARK_BACKGROUND,
                    text_color = GUI_DC.DARK_TEXT_COLOR,
                    font = ("Arial", 13, "bold"),
                    anchor = "center",
                    corner_radius =  50,
                    width=50,
                    height=50
                )
                # Pack the label. | Grid is not used, it is not easy to automatically center widgets with setted column. Ex columspan=3 this should be an argument but there are 4 courses, and etc.
                course_info_label.pack(side="left", expand=True, fill="y", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)


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