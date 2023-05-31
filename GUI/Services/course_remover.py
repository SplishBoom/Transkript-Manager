from    Environment import  ASSETS_DC, to_turkish # -> Environment variables
from    tkinter     import  messagebox # -> Interract with user
from    tkinter     import  Toplevel # -> Create new window
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI

class CourseRemover(Toplevel) :

    def __init__(self, master : ttk.Frame, modified_course_list : list, existing_course_codes : list, parsing_language : str, selected_course_code : str) -> None:
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
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)
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
        self.remove_course_container = ttk.Frame(self.container)
        self.remove_course_container.grid(row=0, column=0)
        # Configure the main container.
        self.remove_course_container.grid_rowconfigure((0, 1, 2), weight=1)
        self.remove_course_container.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
        self.remove_course_course_code_label = ttk.Label(self.remove_course_container, text=self._get_text("Select and Remove Course"))
        self.remove_course_course_code_label.grid(row=0, column=0, columnspan=2)

        self.remover_container = ttk.Frame(self.remove_course_container)
        self.remover_container.grid(row=1, column=0, columnspan=2)
        self.show_current_addons()

        self.save_button = ttk.Button(self.remove_course_container, text=self._get_text("Apply"), command=self.__save)
        self.save_button.grid(row=2, column=0)

        self.cancel_button = ttk.Button(self.remove_course_container, text=self._get_text("Cancel"), command=self.__clean_exit)
        self.cancel_button.grid(row=2, column=1)

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
        self.table_course_code_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Code"))
        self.table_course_code_label.grid(row=0, column=0, columnspan=5)

        self.select_course_course_code_combobox = ttk.Combobox(self.remover_container, values=self.existing_course_codes, state="readonly")
        self.select_course_course_code_combobox.grid(row=1, column=0, columnspan=5)

        # Add an handler for the combobox. To move on.
        self.select_course_course_code_combobox.bind("<<ComboboxSelected>>", self.show_course_items)

        # If there is a selected course code, set it. And initialize the combobox bind.
        if self.selected_course_code is not None :
            self.select_course_course_code_combobox.set(self.selected_course_code)
            self.show_course_items(None)
        
    def show_course_items(self, event : tk.Event) -> None:
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
        table_course_name_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Name"))
        table_course_name_label.grid(row=0, column=1)

        table_course_lang_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Language"))
        table_course_lang_label.grid(row=0, column=2)

        table_course_credit_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Credit"))
        table_course_credit_label.grid(row=0, column=3)

        table_course_grade_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Grade"))
        table_course_grade_label.grid(row=0, column=4)

        table_course_grade_point_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Grade Point"))
        table_course_grade_point_label.grid(row=0, column=5)

        # Get the selected course code.
        use_code = self.select_course_course_code_combobox.get()

        # Get the course items.
        for course in self.modified_course_list :
            if course["course_code"] == use_code :
                self.course_name = tk.StringVar(value=course["course_name"])
                self.course_lang = tk.StringVar(value=course["course_lang"])
                self.course_credit = tk.StringVar(value=course["course_credit"])
                self.course_grade = tk.StringVar(value=course["course_grade"])
                self.course_grade_point = tk.StringVar(value=course["course_grade_point"])
                break
        
        # Load the course items. & Configure the widgets.
        self.course_name_entry = ttk.Entry(self.remover_container, textvariable=self.course_name, state="disabled")
        self.course_name_entry.grid(row=1, column=1)

        self.course_lang_entry = ttk.Entry(self.remover_container, textvariable=self.course_lang, state="disabled")
        self.course_lang_entry.grid(row=1, column=2)

        self.course_credit_entry = ttk.Entry(self.remover_container, textvariable=self.course_credit, state="disabled")
        self.course_credit_entry.grid(row=1, column=3)

        self.course_grade_entry = ttk.Entry(self.remover_container, textvariable=self.course_grade, state="disabled")
        self.course_grade_entry.grid(row=1, column=4)

        self.course_grade_point_entry = ttk.Entry(self.remover_container, textvariable=self.course_grade_point, state="disabled")
        self.course_grade_point_entry.grid(row=1, column=5)

    def get_result(self) -> dict:
        """
        Returns the result.
        @Parameters:
            None
        @Returns:
            result - Required : The result. (dict)
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