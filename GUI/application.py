from    GUI             import  AchievementAnalyzer, GradeUpdater, StatAnalyzer # -> Program frames
from    GUI             import  UserAuthenticator, DataLoader, DataSaver # -> Service frames
from    Utilities       import  get_gender, generate_pdf, translate_text # -> Utilitiy functions
from    Environment     import  ASSETS_DC, SELENIUM_DC, GUI_DC # -> Environment variables
from    PIL             import  Image # -> Image processing
from    tkinter         import  messagebox # -> Interact with user
from    datetime        import  datetime # -> Get current date
import  customtkinter   as      ctk # -> GUI
import  copy # -> Copy objects without reference
import  os # -> Get current working directory

class ApplicationFrame(ctk.CTkFrame) :

    def __init__(self, parent : ctk.CTkFrame, root : ctk.CTk, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for ApplicationFrame class. Used to initialize main window of the application.
        @Parameters:
            parent - Required : Container frame of the application. (ttk.Frame) -> Which is used to place the application frame.
            root   - Required : Root window of the application. (tk.Tk) -> Which is used to set connection between frames.
            DEBUG  - Optional : Debug mode flag. (bool) (default : False) -> Which is used to determine whether the application is in debug mode or not.
        @Returns:
            None
        """
        # Initialize main frame.
        super().__init__(parent, *args, **kwargs)

        # Initialize variables.
        self.parent = parent
        self.root   = root
        self.DEBUG  = DEBUG
        self.work_dir = os.getcwd()
        self.desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        # Initialize widget containers.
        self.__load_containers()

        # Initialize user data.
        current_user_info_document, current_user_data_document = self.root.get_current_data()
        self.__load_user_data(current_user_data_document)
        self.__load_user_info(current_user_info_document)
        self.__update_user_authitication()

        # Load widgets.
        self.__load_user_info_label()
        self.__load_controller()
        self.__load_programs()

    def __load_containers(self) -> None:
        """
        Loads containers into class fields.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the initial configuration, to make expandable affect on window.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # If already exists, forget the container.
        try :
            self.container.grid_forget()
        except :
            pass
        # Create main container for ApplicationFrame.
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure main container.
        self.container.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create containers for ApplicationFrame widgets
        ctk.CTkFrame(self.container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=0, column=0, pady=GUI_DC.GENERAL_PADDING//2, padx=GUI_DC.GENERAL_PADDING)
        self.user_info_label_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.LIGHT_BACKGROUND, border_color=GUI_DC.BORDER_COLOR, border_width=2, corner_radius=25)
        self.user_info_label_container.grid(row=1, column=0, sticky="nsew", padx=GUI_DC.GENERAL_PADDING)
        ctk.CTkFrame(self.container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=2, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.GENERAL_PADDING)
        self.controllers_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.LIGHT_BACKGROUND, border_color=GUI_DC.BORDER_COLOR, border_width=2, corner_radius=25)
        self.controllers_container.grid(row=3, column=0, sticky="nsew", padx=GUI_DC.GENERAL_PADDING)
        ctk.CTkFrame(self.container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=4, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.GENERAL_PADDING)
        self.program_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.LIGHT_BACKGROUND, border_color=GUI_DC.BORDER_COLOR, border_width=2, corner_radius=25)
        self.program_container.grid(row=5, column=0, sticky="nsew", padx=GUI_DC.GENERAL_PADDING)
        ctk.CTkFrame(self.container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=6, column=0, pady=GUI_DC.GENERAL_PADDING//2, padx=GUI_DC.GENERAL_PADDING)


    def __load_user_info_label(self) -> None:
        """
        Loads user info label on application frame.
        @Parameters:
            None
        @Returns:
            None
        """
        def ___change_user_photo(*args, **kwargs) -> None:
            """
            Changes user photo. In every click.
            @Parameters:
                None
            @Returns:
                None
            """
            # Get photo list from available photos. Normally data is dict [key : photo_name, value : photo_path]
            available_photo_list = list(self.available_photos.values())
            # Get index of current and next photo.
            index_of_current_photo = available_photo_list.index(self.current_user_photo_path)
            index_of_next_photo = (index_of_current_photo + 1) % len(available_photo_list)
            # Change current user photo
            self.current_user_photo_path = available_photo_list[index_of_next_photo]
            self.student_photo = ctk.CTkImage(light_image=Image.open(self.current_user_photo_path), dark_image=Image.open(self.current_user_photo_path), size=GUI_DC.STUDENT_PHOTO_SIZE)
            self.student_photo_label.configure(image=self.student_photo, text=None) # Text attirbute added for ctk bug.
            self.student_photo_label.image = self.student_photo

        # Configure user info label container.
        self.user_info_label_container.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.user_info_label_container.grid_columnconfigure((0), weight=1)

        # Split into two parts
        ctk.CTkFrame(self.user_info_label_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=0, column=0, pady=GUI_DC.INNER_PADDING//1.5, padx=GUI_DC.INNER_PADDING)
        self.assets_container = ctk.CTkFrame(self.user_info_label_container, fg_color=GUI_DC.LIGHT_BACKGROUND)
        self.assets_container.grid(row=1, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING)
        ctk.CTkFrame(self.user_info_label_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=2, column=0, padx=GUI_DC.INNER_PADDING//1.5, pady=GUI_DC.INNER_PADDING)
        self.texts_container = ctk.CTkFrame(self.user_info_label_container, fg_color=GUI_DC.LIGHT_BACKGROUND)
        self.texts_container.grid(row=3, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING)
        ctk.CTkFrame(self.user_info_label_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=4, column=0, pady=GUI_DC.INNER_PADDING//1.5, padx=GUI_DC.INNER_PADDING)
        
        # Configure assets container.
        self.assets_container.grid_rowconfigure((0), weight=1)
        self.assets_container.grid_columnconfigure((0,1,2), weight=1)
        # Create mef uni logo label.
        self.logo_image = ctk.CTkImage(light_image=Image.open(ASSETS_DC.LOGO_PATH), dark_image=Image.open(ASSETS_DC.LOGO_PATH), size=GUI_DC.APP_MEF_LOGO_SIZE)
        mef_logo_label = ctk.CTkLabel(self.assets_container, image=self.logo_image, text=None)
        mef_logo_label.grid(row=0, column=0, sticky="nsew")

        # Create document name label.
        self.document_info_label = ctk.CTkLabel(self.assets_container, text=self.document_name+2*"\n"+self.transcript_creation_date)
        self.document_info_label.grid(row=0, column=1, sticky="nsew")

        # Create student photo label.
        # If online login approved, than add the user photo to available photos. To show it on the label.
        self.available_photos = ASSETS_DC.GENDERS_PHOTO_PATH
        if os.path.exists(SELENIUM_DC.USER_PHOTO_OUTPUT_PATH) :
            self.available_photos["user_photo"] = SELENIUM_DC.USER_PHOTO_OUTPUT_PATH
            self.current_user_photo_path = SELENIUM_DC.USER_PHOTO_OUTPUT_PATH
        else :
            self.current_user_photo_path = ASSETS_DC.GENDERS_PHOTO_PATH[self.student_gender]
        self.student_photo = ctk.CTkImage(light_image=Image.open(self.current_user_photo_path), dark_image=Image.open(self.current_user_photo_path), size=GUI_DC.STUDENT_PHOTO_SIZE)
        self.student_photo_label = ctk.CTkLabel(self.assets_container, image=self.student_photo, text=None)
        self.student_photo_label.grid(row=0, column=2, sticky="nsew")
        self.student_photo_label.bind("<Button-1>", ___change_user_photo)

        # Configure labels.
        for acurrent_asset_label in self.assets_container.winfo_children() :
            acurrent_asset_label.configure(
                fg_color=GUI_DC.LIGHT_BACKGROUND,
                bg_color=GUI_DC.LIGHT_BACKGROUND,
                text_color=GUI_DC.DARK_TEXT_COLOR,
                font=("Arial", 17, "bold"),
                anchor="center",
            )

        # Configure texts container.
        self.texts_container.grid_rowconfigure((0,1), weight=1)
        self.texts_container.grid_columnconfigure((0,1,2,3), weight=1)
        # Create student id, national id, name, surname, faculty, department, program, language of instruction, and status labels.
        #student_id_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Student ID"))
        #student_id_label.grid(row=0, column=0)
        student_id_label_value = ctk.CTkLabel(self.texts_container, text=self.student_school_id)
        student_id_label_value.grid(row=0, column=0)

        #national_id_label = ctk.CTkLabel(self.texts_container, text=self._get_text("National ID"))
        #national_id_label.grid(row=0, column=2)
        national_id_label_value = ctk.CTkLabel(self.texts_container, text=self.student_national_id)
        national_id_label_value.grid(row=0, column=1)

        #student_name_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Name"))
        #student_name_label.grid(row=0, column=4)
        student_name_label_value = ctk.CTkLabel(self.texts_container, text=self.student_name)
        student_name_label_value.grid(row=0, column=2)

        #student_surname_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Surname"))
        #student_surname_label.grid(row=0, column=6)
        student_surname_label_value = ctk.CTkLabel(self.texts_container, text=self.student_surname)
        student_surname_label_value.grid(row=0, column=3)

        #faculty_department_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Faculty / Department"))
        #faculty_department_label.grid(row=1, column=0)
        faculty_department_label_value = ctk.CTkLabel(self.texts_container, text=self.student_faculty.split(" / ")[0])
        faculty_department_label_value.grid(row=1, column=0)

        #program_name_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Program Name"))
        #program_name_label.grid(row=1, column=2)
        program_name_label_value = ctk.CTkLabel(self.texts_container, text=self.student_department)
        program_name_label_value.grid(row=1, column=1)

        #language_of_instruction_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Language of Instruction"))
        #language_of_instruction_label.grid(row=1, column=4)
        language_of_instruction_label_value = ctk.CTkLabel(self.texts_container, text=self.language_of_instruction)
        language_of_instruction_label_value.grid(row=1, column=2)

        #student_status_label = ctk.CTkLabel(self.texts_container, text=self._get_text("Student Status"))
        #student_status_label.grid(row=1, column=6)
        student_status_label_value = ctk.CTkLabel(self.texts_container, text=self.student_status)
        student_status_label_value.grid(row=1, column=3)

        # Configure labels.
        for acurrent_text_label in self.texts_container.winfo_children() :
            acurrent_text_label.configure(
                fg_color=GUI_DC.LIGHT_BACKGROUND,
                bg_color=GUI_DC.LIGHT_BACKGROUND,
                text_color=GUI_DC.DARK_TEXT_COLOR,
                font=("Arial", 13, "bold"),
                anchor="center",
                corner_radius=25,
            )
            acurrent_text_label.grid_configure(sticky="nsew")
    
    def __load_controller(self) -> None:
        """
        This method creates the controller container and its widgets.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure controller container.
        self.controllers_container.grid_rowconfigure((0,1,2), weight=1)
        self.controllers_container.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        # Create controller buttons.
        self.load_db_data_button = ctk.CTkButton(self.controllers_container, text=self._get_text("Load Data"), command=self.__load_db_data, fg_color = GUI_DC.BUTTON_LIGHT_PURPLE, hover_color = GUI_DC.BUTTON_LIGHT_PURPLE_HOVER)
        self.load_db_data_button.grid(row=0, column=0)

        self.save_db_data_button = ctk.CTkButton(self.controllers_container, text=self._get_text("Save Data"), command=self.__save_db_data, fg_color = GUI_DC.BUTTON_LIGHT_YELLOW, hover_color = GUI_DC.BUTTON_LIGHT_YELLOW_HOVER)
        self.save_db_data_button.grid(row=0, column=1)

        self.exit_button = ctk.CTkButton(self.controllers_container, text=self._get_text("Exit"), command=self.root.terminate, fg_color = GUI_DC.BUTTON_LIGHT_ORANGE, hover_color = GUI_DC.BUTTON_LIGHT_ORANGE_HOVER)
        self.exit_button.grid(row=0, column=2)

        self.restart_button = ctk.CTkButton(self.controllers_container, text=self._get_text("Restart"), command=self.root._switch_to_login, fg_color = GUI_DC.BUTTON_LIGHT_PINK, hover_color = GUI_DC.BUTTON_LIGHT_PINK_HOVER)
        self.restart_button.grid(row=0, column=3)

        self.reset_button = ctk.CTkButton(self.controllers_container, text=self._get_text("Refresh"), command=self.__reset, fg_color = GUI_DC.BUTTON_LIGHT_DBLUE, hover_color = GUI_DC.BUTTON_LIGHT_DBLUE_HOVER)
        self.reset_button.grid(row=0, column=4)

        self.export_button = ctk.CTkButton(self.controllers_container, text=self._get_text("Export Data"), command=self.__export, fg_color = GUI_DC.BUTTON_LIGHT_DGREEN, hover_color = GUI_DC.BUTTON_LIGHT_DGREEN_HOVER)
        self.export_button.grid(row=0, column=5)
    
        for current_button in self.controllers_container.winfo_children() :
            current_button.configure(
                bg_color=GUI_DC.LIGHT_BACKGROUND,
                corner_radius=25,
                text_color=GUI_DC.LIGHT_TEXT_COLOR,
                text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
                font=("Arial", 13, "bold"),
            )
            current_button.grid_configure(padx=GUI_DC.GENERAL_PADDING, pady=GUI_DC.GENERAL_PADDING, sticky="nsew")

    def __load_programs(self) -> None:
        """
        This method creates the program selection container and its widgets.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure program selection container.
        self.program_container.grid_rowconfigure((0,1,2), weight=1)
        self.program_container.grid_columnconfigure((0), weight=1)

        # Create the tabview widget for the input field.
        ctk.CTkFrame(self.program_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=0, column=0, pady=GUI_DC.INNER_PADDING//2, padx=GUI_DC.INNER_PADDING)
        ctk.CTkTabview._segmented_button_border_width = 4
        ctk.CTkTabview._button_height = 30
        ctk.CTkTabview._top_button_overhang = 9
        self.tab_view = ctk.CTkTabview(self.program_container, 
                                       fg_color=GUI_DC.DARK_BACKGROUND, 
                                       bg_color=GUI_DC.LIGHT_BACKGROUND,
                                       text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                       text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
                                       segmented_button_fg_color=GUI_DC.DARK_BACKGROUND,
                                       segmented_button_selected_color=GUI_DC.BUTTON_LIGHT_BLUE,
                                       segmented_button_selected_hover_color=GUI_DC.BUTTON_LIGHT_BLUE_HOVER,
                                       segmented_button_unselected_color=GUI_DC.DARK_BACKGROUND,
                                       segmented_button_unselected_hover_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                       corner_radius=25,
                                       width=1100,
                                       height=550,
                                       border_width=0
        )
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
        ctk.CTkFrame(self.program_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=2, column=0, pady=GUI_DC.INNER_PADDING//2, padx=GUI_DC.INNER_PADDING)

        # Set tab names.
        self.stat_analyzer_tab_name = "Stat Analyzer" if self.parsing_language == "en" else "Istatistik Analizcisi"
        self.grade_updater_tab_name = "Grade Updater" if self.parsing_language == "en" else "Not Guncelleyici"
        self.achievement_analyzer_tab_name = "Achievement Analyzer" if self.parsing_language == "en" else "Basari Analizcisi"

        # Add tabs.
        self.stat_analyzer_tab = self.tab_view.add(self.stat_analyzer_tab_name)
        self.grade_updater_tab = self.tab_view.add(self.grade_updater_tab_name)
        self.achievement_analyzer_tab = self.tab_view.add(self.achievement_analyzer_tab_name)

        # Configure tabs.
        self.stat_analyzer_tab.grid_rowconfigure(0, weight=1)
        self.stat_analyzer_tab.grid_columnconfigure(0, weight=1)
        self.grade_updater_tab.grid_rowconfigure(0, weight=1)
        self.grade_updater_tab.grid_columnconfigure(0, weight=1)
        self.achievement_analyzer_tab.grid_rowconfigure(0, weight=1)
        self.achievement_analyzer_tab.grid_columnconfigure(0, weight=1)

        # Set the current tab to initial program.
        self.tab_view.set(self.grade_updater_tab_name)

        # Configure binding.
        self.tab_view.configure(command=self.___switch_program_mode)

        # Load the program.
        current_user_data = self.__create_user_data() # Get latest current user data.
        self.current_program_frame_name = self.grade_updater_tab_name
        self.grade_updater_frame = GradeUpdater(self.grade_updater_tab, self, self.root, current_user_data, DEBUG=self.DEBUG)
        self.grade_updater_frame.grid(row=0, column=0, sticky="nsew")

        self.stat_analyzer_frame = None
        self.achievement_analyzer_frame = None


    def __update_user_authitication(self) -> None:
        """
        Updates user authentication status.
        @Parameters:
            None
        @Returns:
            None
        """
        # Load user authentication status into class field.
        self.is_user_authenticated = self.root.get_authication_status()

    def update_user_data(self, new_user_data : dict) -> None:
        """
        Updates classes user data. By creating new user data.
        @Parameters:
            new_user_data - Required : New user data. (dict) -> Which is used to update classes user data.
        @Returns:
            None
        """
        # Load new user data.
        self.__load_user_data(new_user_data)

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
        self.sorting : dict = given_user_data["sorting"]
        self.modified_course_list : list = given_user_data["modified_course_list"]
        self.document_name : str = given_user_data["document_name"]
        self.updated_course_list : list = given_user_data["updated_course_list"]
        self.subtracted_course_list : list = given_user_data["subtracted_course_list"]
        self.added_course_list : list = given_user_data["added_course_list"]

    def __create_user_data(self) -> dict:
        """
        Creates user data from class fields.
        @Parameters:
            None
        @Returns:
            new_user_data - Required : New user data. (dict) -> Which is created from class fields.
        """
        # Create new user data from class fields.
        new_user_data = {
            "owner_id" : self.owner_id,
            "parsing_type" : self.parsing_type,
            "parsing_language" : self.parsing_language,
            "transcript_manager_date" : self.transcript_manager_date,
            "transcript_creation_date" : self.transcript_creation_date,
            "semesters" : copy.deepcopy(self.semesters),
            "original_course_list" : copy.deepcopy(self.original_course_list),
            "filtering" : copy.deepcopy(self.filtering),
            "sorting" : copy.deepcopy(self.sorting),
            "modified_course_list" : copy.deepcopy(self.modified_course_list),
            "document_name" : self.document_name,
            "updated_course_list" : copy.deepcopy(self.updated_course_list),
            "subtracted_course_list" : copy.deepcopy(self.subtracted_course_list),
            "added_course_list" : copy.deepcopy(self.added_course_list)
        }
        # Return new user data.
        return new_user_data

    def __load_user_info(self, given_user_info : dict) -> None:
        """
        Loads user info into class fields.
        @Parameters:
            given_user_info - Required : Use case. (dict) -> Which is used to load user info into class fields.
        @Returns:
            None
        """
        # Load user info into class fields. (Which are non-translatable.)
        self.language_of_instruction : str = given_user_info["language_of_instruction"]
        self.student_department : str = given_user_info["student_department"]
        self.student_faculty : str = given_user_info["student_faculty"]
        self.student_name : str = given_user_info["student_name"]
        self.student_school_id : str = given_user_info["student_school_id"]
        self.student_national_id : str = given_user_info["_id"]
        self.student_status : str = given_user_info["student_status"]
        self.student_surname : str = given_user_info["student_surname"]
        
        # Load rest of user info into class fields. (Which are translatable.)
        if self.parsing_language == "tr" :
            self.student_faculty = translate_text(self.student_faculty)
            self.student_department = translate_text(self.student_department)
            self.student_status = translate_text(self.student_status)
            self.language_of_instruction = translate_text(self.language_of_instruction)
        if self.parsing_language == "en" :
            self.student_faculty = translate_text(self.student_faculty, "tr", "en")
            self.student_department = translate_text(self.student_department, "tr", "en")
            self.student_status = translate_text(self.student_status, "tr", "en")
            self.language_of_instruction = translate_text(self.language_of_instruction, "tr", "en")

        # Get the gender of the student by using their name.
        self.student_gender = get_gender(name=self.student_name)

    def __create_user_info(self) -> dict:
        """
        Creates user info from class fields.
        @Parameters:
            None
        @Returns:
            new_user_info - Required : New user info. (dict) -> Which is created from class fields.
        """
        # Create new user info from class fields.
        new_user_info = {
            "_id" : self.student_national_id,
            "student_name" : self.student_name,
            "student_surname" : self.student_surname,
            "student_school_id" : self.student_school_id,
            "student_department" : self.student_department,
            "student_faculty" : self.student_faculty,
            "student_status" : self.student_status,
            "language_of_instruction" : self.language_of_instruction
        }
        # Return new user info.
        return new_user_info


    def _get_text(self, text : str, parsing_language : str = None) -> str:
        """
        Gets the text from the given text.
        @Parameters:
            text - Required : Text. (str) -> Which is used to get the text from.
            parsing_language - Optional : Parsing language. (str) (default : None) -> Which is used to get the text in the given language.
        @Returns:
            self.root.get_text(text, parsing_language or self.parsing_language) - Required : Text. (str) -> Which is gotten from the given text.
        """
        # Wrap to root's get_text method. Then return the result.
        return self.root.get_text(text, parsing_language or self.parsing_language)

    def __check_authentication(self) -> bool:
        """
        This method checks the user authentication status. If the user is not authenticated, it asks the user to authenticate. If the user is authenticated, it returns True.
        @Parameters:
            None
        @Returns:
            result - Required : Authentication result. (bool) -> True if the user is authenticated, False if not.
        """
        # If the user is already authenticated, return True.
        if self.is_user_authenticated == True :
            return True

        # Ask the user to authenticate.
        obj = UserAuthenticator(self, self.student_school_id, self.parsing_language)
        result = obj.get_result()

        # Set the authentication status.
        self.is_user_authenticated = result
        self.root.set_authication_status(result)

    def ___switch_program_mode(self, *args, **kwargs) -> None:
        """
        This method binds the program selection tabs. And initializes outer program on switch.
        @Parameters:
            None
        @Returns:
            None
        """
        # Get the name of the name mode.
        new_mode_name = self.tab_view.get()

        # Get the latest user data.
        current_user_data = self.__create_user_data()

        # Firstly remove the current program frame.
        if self.current_program_frame_name == self.stat_analyzer_tab_name :
            self.stat_analyzer_frame.grid_remove()
            self.stat_analyzer_frame.destroy()
        elif self.current_program_frame_name == self.grade_updater_tab_name :
            self.grade_updater_frame.grid_remove()
        elif self.current_program_frame_name == self.achievement_analyzer_tab_name :
            self.achievement_analyzer_frame.grid_remove()
            self.achievement_analyzer_frame.destroy()
        else :
            raise Exception("Unknown program frame name.")
        
        # Then grid the new program frame.
        if new_mode_name == self.stat_analyzer_tab_name :
            self.stat_analyzer_frame = StatAnalyzer(self.stat_analyzer_tab, self, self.root, current_user_data, DEBUG=self.DEBUG)
            self.stat_analyzer_frame.grid(row=0, column=0, sticky="nsew")
            self.current_program_frame_name = self.stat_analyzer_tab_name
        elif new_mode_name == self.grade_updater_tab_name :
            self.grade_updater_frame.grid(row=0, column=0, sticky="nsew")
            self.current_program_frame_name = self.grade_updater_tab_name
        elif new_mode_name == self.achievement_analyzer_tab_name :
            self.achievement_analyzer_frame = AchievementAnalyzer(self.achievement_analyzer_tab, self, self.root, current_user_data, DEBUG=self.DEBUG)
            self.achievement_analyzer_frame.grid(row=0, column=0, sticky="nsew")
            self.current_program_frame_name = self.achievement_analyzer_tab_name
        else :
            raise Exception("Unknown program frame name.")

    def __load_db_data(self, *args, **kwargs) -> None:
        """
        This method loads the database data to the program. If neccessary requirements are met.
        @Parameters:
            None
        @Returns:
            None
        """
        # Disable the button to prevent multiple clicks.
        self.load_db_data_button.configure(text=self._get_text("Loading"), state="disabled")

        # Check if the user is authenticated.
        self.__check_authentication()

        # If not authenticated, fix the button and cancel operation.
        if not self.is_user_authenticated :
            self.load_db_data_button.configure(text=self._get_text("Auth Eror"), fg_color=GUI_DC.BUTTON_LIGHT_RED)
            self.after(500, lambda : self.load_db_data_button.configure(text=self._get_text("Load Data"), fg_color=GUI_DC.BUTTON_LIGHT_PURPLE, state="normal"))
            return

        # Initialize the match data.
        expected_owner_id = self.student_national_id
        document_list = list(self.root.db_client.user_data.get_available_documents(expected_owner_id))

        # If no data found, fix the button and cancel operation.
        if document_list == [] :
            messagebox.showerror(self._get_text("Error"), self._get_text("No data found for this user"))
            self.load_db_data_button.configure(text=self._get_text("No Data"), fg_color=GUI_DC.BUTTON_LIGHT_RED)
            self.after(500, lambda : self.load_db_data_button.configure(text=self._get_text("Load Data"), fg_color=GUI_DC.BUTTON_LIGHT_PURPLE, state="normal"))
            return

        # If data found, load the available data.
        available_documents = {}
        for document in document_list :
            available_documents[document["document_name"]] = document

        # Ask the user to select a data.
        options = list(available_documents.keys())
        data_loader = DataLoader(self.root, options, self.parsing_language)
        selected_option = data_loader.get_selected_option()

        # If no data selected, fix the button and cancel operation.
        if selected_option == "" :
            self.load_db_data_button.configure(text=self._get_text("No Selection"), fg_color=GUI_DC.BUTTON_LIGHT_RED)
            self.after(500, lambda : self.load_db_data_button.configure(text=self._get_text("Load Data"), fg_color=GUI_DC.BUTTON_LIGHT_PURPLE, state="normal"))
            return
        
        # If data selected, load the data.
        selected_user_data_document = available_documents[selected_option]
        self.root.set_current_data(user_data_document=selected_user_data_document)
        self.__load_user_data(selected_user_data_document)

        # Reset the ApplicationFrame to take effect. Also fix the button.
        self.load_db_data_button.configure(text=self._get_text("Loaded"), fg_color=GUI_DC.BUTTON_LIGHT_GREEN)
        self.after(500, self.__reset)

    def __save_db_data(self, *args, **kwargs) -> None:
        """
        This method saves the database data to the program. If neccessary requirements are met.
        @Parameters:
            None
        @Returns:
            None
        """
        # Disable the button to prevent multiple clicks.
        self.save_db_data_button.configure(text=self._get_text("Saving"), state="disabled")

        # Check if the user is authenticated.
        self.__check_authentication()

        # If not authenticated, fix the button and cancel operation.
        if not self.is_user_authenticated :
            self.save_db_data_button.configure(text=self._get_text("Auth Eror"), fg_color=GUI_DC.BUTTON_LIGHT_RED)
            self.after(500, lambda : self.save_db_data_button.configure(text=self._get_text("Save Data"), fg_color=GUI_DC.BUTTON_LIGHT_YELLOW, state="normal"))
            return

        # Initialize the match data.
        expected_owner_id = self.student_national_id
        document_list = list(self.root.db_client.user_data.get_available_documents(expected_owner_id))

        # Collect the existing document names.
        existing_document_names = []
        for document in document_list :
            existing_document_names.append(document["document_name"])

        # Ask the user to select a new document name.
        data_saver = DataSaver(self.root, existing_document_names, self.parsing_language)
        new_document_name = data_saver.get_new_document_name()

        # If no document name selected, fix the button and cancel operation.
        if new_document_name == "" :
            self.save_db_data_button.configure(text=self._get_text("No Input"), fg_color=GUI_DC.BUTTON_LIGHT_RED)
            self.after(500, lambda : self.save_db_data_button.configure(text=self._get_text("Save Data"), fg_color=GUI_DC.BUTTON_LIGHT_YELLOW, state="normal"))
            return
        
        # If document name selected, save the data.
        self.document_name = new_document_name

        # Update the porgram execution date.
        self.program_execution_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Create the user data & info documents.
        new_user_data_document = self.__create_user_data()
        user_info_document = self.__create_user_info()

        # Push the documents to the database.
        self.root.db_client.user_info.push_init(user_info_document)
        self.root.db_client.user_data.push_init(new_user_data_document)

        # Set the current data. For root to remember.
        self.root.set_current_data(user_info_document, new_user_data_document)

        # Fix the button and reset the ApplicationFrame to take effect.
        self.save_db_data_button.configure(text=self._get_text("Saved"), fg_color=GUI_DC.BUTTON_LIGHT_GREEN)
        self.after(500, self.__reset)

    def __reset(self, *args, **kwargs) -> None:
        """
        This method resets the ApplicationFrame. This means, only "current_data" and "authication_status" will be kept by root. All programs will initialized again including this ApplicationFrame.
        @Parameters:
            None
        @Returns:
            None
        """
        # Disable the button to prevent multiple clicks.
        self.reset_button.configure(text=self._get_text("Refreshing"), state="disabled")
        # Reset the ApplicationFrame. By restarting the application.
        self.root.restart_application()
    
    def __export(self, *args, **kwargs) -> None:
        """
        This method exports the current data to a pdf file by taking output path as filedialog.
        @Parameters:
            None
        @Returns:
            None
        """
        # Disable the button to prevent multiple clicks.
        self.export_button.configure(text=self._get_text("Exporting"), state="disabled")

        # Get the output file path.
        output_file_folder = ctk.filedialog.asksaveasfilename(initialdir=self.desktop_path, initialfile=self.document_name, defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])

        # Set a flag to check whether the export is successful or not.
        is_exported = False

        # Check if the user selected a folder.
        if output_file_folder is not None and output_file_folder != "" and output_file_folder != " " :
            # If selected, create the output file path.
            output_file_path = output_file_folder

            # Create the user data & info documents.
            current_user_info_document = self.__create_user_info()
            current_user_data_document = self.__create_user_data()

            # Export the data. By direct call to utility method generate_pdf.
            try :
                generate_pdf(
                    user_info_document = current_user_info_document, 
                    user_data_document = current_user_data_document, 
                    user_photo_path = self.current_user_photo_path,
                    mef_logo_path = ASSETS_DC.LOGO_PATH,
                    output_file_path = output_file_path
                )
                # Update the flag.
                is_exported = True
            except Exception as e :
                # Update the flag.
                is_exported = False
                print("An undefined error occured on \"Data Export\", please contact with the developer.")

        # Fix the button and reset the ApplicationFrame to take effect. If not selected or selected, it does not matter.
        if is_exported :
            self.export_button.configure(text=self._get_text("Exported"), fg_color=GUI_DC.BUTTON_LIGHT_GREEN)
            self.after(500, lambda : self.export_button.configure(text=self._get_text("Export Data"), fg_color=GUI_DC.BUTTON_LIGHT_DGREEN, state="normal"))
        else :
            self.export_button.configure(text=self._get_text("Not Exported"), fg_color=GUI_DC.BUTTON_LIGHT_RED)
            self.after(500, lambda : self.export_button.configure(text=self._get_text("Export Data"), fg_color=GUI_DC.BUTTON_LIGHT_DGREEN, state="normal"))