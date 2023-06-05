from    Environment     import  ASSETS_DC, GUI_DC, to_turkish # -> Environment variables
from    tkinter         import  messagebox # -> Interract with user
import  customtkinter   as      ctk # -> GUI

class CourseRemover(ctk.CTkToplevel) :

    def __init__(self, master : ctk.CTkFrame, modified_course_list : list, existing_course_codes : list, parsing_language : str, selected_course_code : str) -> None:
        """
        Initialize the CourseRemover class. This class is used to remove a course from the course list.
        @Parameters:
            master - Required : The master of the dialog. (ttk.Frame) -> The main window.
            modified_course_list - Required : The modified course list. (list) -> The course list.
            existing_course_codes - Required : The existing course codes. (list) -> The course codes.
            parsing_language - Required : The parsing language. (str) -> The parsing language.
            selected_course_code - Required : The selected course code. (str) -> The course code.
        @Returns:
            None
        """
        # Initialize the Toplevel.
        super().__init__(master)
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        # Set the parsing language.
        self.parsing_language = parsing_language

        # Set the title and the icon.
        self.title(self._get_text("Remove Course"))
        self.iconbitmap(ASSETS_DC.ICON)

        # Set the class variables.
        self.existing_course_codes = existing_course_codes
        self.modified_course_list = modified_course_list
        self.selected_course_code = selected_course_code
        self.result = None

        # Setup the main container.
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container.
        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_columnconfigure((0), weight=1)
        
        # Add an handler on close, for making sure correct data is returned.
        self.protocol("WM_DELETE_WINDOW", self.__clean_exit)
        
        # Create the widgets.
        self.create_widgets()
        
        # Follow the main window.
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def _get_text(self, text : str) -> str:
        """
        Gets the text from the language dictionary.
        @Parameters:
            text - Required : Text to get from the dictionary. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            translated_text - str : Translated text. (str)
        """
        # According to the language, do the translation.
        if self.parsing_language == "tr" :
            return to_turkish[text]
        else :
            return text

    def create_widgets(self) -> None:
        """
        Create the widgets.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create the main container.
        self.widgets_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.widgets_container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container.
        self.widgets_container.grid_rowconfigure((0, 1, 2), weight=1)
        self.widgets_container.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
        self.info_label = ctk.CTkLabel(self.widgets_container, text=self._get_text("Select and Remove Course"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 15, "bold"),
            anchor="center",
        )
        self.info_label.grid(row=0, column=0, columnspan=2)

        self.remover_container = ctk.CTkFrame(self.widgets_container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.remover_container.grid(row=1, column=0, columnspan=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
        self.show_current_addons()

        self.save_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Apply"), command=self.__save,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.save_button.grid(row=2, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

        self.cancel_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Cancel"), command=self.__clean_exit,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.cancel_button.grid(row=2, column=1, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

    def show_current_addons(self) -> None:
        """
        Initialize the widgets of the window.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create the widgets container.
        self.remover_container.grid_rowconfigure((0,1), weight=1)
        self.remover_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Create the widgets.
        self.table_course_code_label = ctk.CTkLabel(self.remover_container, text=self._get_text("Existing Course Code"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 13, "bold"),
            anchor="center",
        )
        self.table_course_code_label.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.binder_variable = ctk.StringVar()
        self.select_course_course_code_combobox = ctk.CTkComboBox(self.remover_container, values=self.existing_course_codes, variable=self.binder_variable,
            justify="center",
            state="readonly",
        ) 
        self.select_course_course_code_combobox.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        # Add an handler for the combobox. To move on.
        self.binder_variable.trace_add("write", self.show_course_items)

        # If there is a selected course code, set it. And initialize the combobox bind.
        if self.selected_course_code is not None :
            self.select_course_course_code_combobox.set(self.selected_course_code)
            self.show_course_items(None)
        
    def show_course_items(self, *args, **kwargs) -> None:
        """
        Shows the course items.
        @Parameters:
            event - Required : The event. (tk.Event) -> The event which is triggered by the combobox.
        @Returns:
            None
        """
        # Configure the container.
        self.table_course_code_label.grid_configure(columnspan=1)
        self.select_course_course_code_combobox.grid_configure(columnspan=1)

        # Create the widgets.
        table_course_name_label = ctk.CTkLabel(self.remover_container, text=self._get_text("Existing Course Name"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 13, "bold"),
            anchor="center",
        )
        table_course_name_label.grid(row=0, column=1, padx=GUI_DC.INNER_PADDING*1.5)

        table_course_lang_label = ctk.CTkLabel(self.remover_container, text=self._get_text("Existing Course Language"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 13, "bold"),
            anchor="center",
        )
        table_course_lang_label.grid(row=0, column=2, padx=GUI_DC.INNER_PADDING*1.5)

        table_course_credit_label = ctk.CTkLabel(self.remover_container, text=self._get_text("Existing Course Credit"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 13, "bold"),
            anchor="center",
        )
        table_course_credit_label.grid(row=0, column=3, padx=GUI_DC.INNER_PADDING*1.5)

        table_course_grade_label = ctk.CTkLabel(self.remover_container, text=self._get_text("Existing Course Grade"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 13, "bold"),
            anchor="center",
        )
        table_course_grade_label.grid(row=0, column=4, padx=GUI_DC.INNER_PADDING*1.5)

        table_course_grade_point_label = ctk.CTkLabel(self.remover_container, text=self._get_text("Existing Course Grade Point"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 13, "bold"),
            anchor="center",
        )
        table_course_grade_point_label.grid(row=0, column=5, padx=GUI_DC.INNER_PADDING*1.5)

        # Get the selected course code.
        use_code = self.select_course_course_code_combobox.get()

        # Get the course items.
        for course in self.modified_course_list :
            if course["course_code"] == use_code :
                self.course_name = ctk.StringVar(value=course["course_name"])
                self.course_lang = ctk.StringVar(value=course["course_lang"])
                self.course_credit = ctk.StringVar(value=course["course_credit"])
                self.course_grade = ctk.StringVar(value=course["course_grade"])
                self.course_grade_point = ctk.StringVar(value=course["course_grade_point"])
                break
        
        # Load the course items. & Configure the widgets.
        self.course_name_entry = ctk.CTkEntry(self.remover_container, textvariable=self.course_name, state="disabled", fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND)
        self.course_name_entry.grid(row=1, column=1, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.course_lang_entry = ctk.CTkEntry(self.remover_container, textvariable=self.course_lang, state="disabled", fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND)
        self.course_lang_entry.grid(row=1, column=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.course_credit_entry = ctk.CTkEntry(self.remover_container, textvariable=self.course_credit, state="disabled", fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND)
        self.course_credit_entry.grid(row=1, column=3, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.course_grade_entry = ctk.CTkEntry(self.remover_container, textvariable=self.course_grade, state="disabled", fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND)
        self.course_grade_entry.grid(row=1, column=4, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.course_grade_point_entry = ctk.CTkEntry(self.remover_container, textvariable=self.course_grade_point, state="disabled", fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND)
        self.course_grade_point_entry.grid(row=1, column=5, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

    def get_result(self) -> dict:
        """
        Returns the result.
        @Parameters:
            None
        @Returns:
            result - Required : The result. (dict)
        @Ultra-Mega-Important-Note:
            song - Must : The stuff (love) -> Uzunlar yanıyor aramızda, bu ışık ikimize fazla ~ Sevgi şelalesinden bir yudum. ~
        """
        # Return the result.
        return self.result

    def __save(self) -> None:
        """
        Saves the result.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check if the course code is selected.
        if self.select_course_course_code_combobox.get() == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please select a course to remove"))
            return

        # Create the deleted course.
        deleted_course = {
            "course_code" : self.select_course_course_code_combobox.get(),
            "course_name" : self.course_name_entry.get(),
            "course_lang" : self.course_lang_entry.get(),
            "course_credit" : self.course_credit_entry.get(),
            "course_grade" : self.course_grade_entry.get(),
            "course_grade_point" : self.course_grade_point_entry.get()
        }

        # Set the result.
        self.result = deleted_course

        # Destroy the window.
        self.destroy()

    def __clean_exit(self) -> None:
        """
        Cleans the exit.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the result to None. (It is None by default.)
        self.result = self.result
        # Destroy the window.
        self.destroy()