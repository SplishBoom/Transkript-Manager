from    Environment import  ASSETS_DC, to_turkish # -> Environment variables
from    tkinter     import  messagebox # -> Interract with user
from    tkinter     import  Toplevel # -> Create new window
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI

class CourseUpdater(Toplevel) :

    def __init__(self, master : ttk.Frame, modified_course_list : list, available_course_codes : list, parsing_language : str, possibleNotations : list, weights : dict, possibleCredits : list, selected_course_code : str) -> None:
        """
        Constructor method for CourseUpdater class. This class is used to update course information.
        @Parameters:
            master - Required : Parent widget of this class. (ttk.Frame) -> Which is the main window.
            modified_course_list - Required : Modified course list. (list) -> List of dict courses.
            available_course_codes - Required : Available course codes. (list) -> Course codes that can be selected.
            parsing_language - Required : Parsing language. (str) -> "tr" or "en"
            possibleNotations - Required : Possible notations. (list) -> List of possible notations.
            weights - Required : Weights of notations. (dict) -> Dict of notation weights.
            possibleCredits - Required : Possible credits. (list) -> List of possible credits.
            selected_course_code - Required : Selected course code. (str) -> Course code that is selected by user.
        @Returns:
            None
        """
        # Initialize Toplevel class
        super().__init__(master)

        # Set program language
        self.parsing_language = parsing_language

        # Set the title and the icon.
        self.title(self._get_text("Update Course"))
        self.iconbitmap(ASSETS_DC.ICON)

        # Set class variables
        self.available_course_codes = available_course_codes
        self.selected_course_code = selected_course_code
        self.modified_course_list = modified_course_list
        self.possibleNotations = possibleNotations
        self.possibleCredits = possibleCredits
        self.weights = weights
        self.result = None

        # Create the main container
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)
        # Configure the main container
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
        Creates the widgets.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the widget container.
        self.widgets_conainer = ttk.Frame(self.container)
        self.widgets_conainer.grid(row=0, column=0)
        # Configure the widget container.
        self.widgets_conainer.grid_rowconfigure((0, 1, 2), weight=1)
        self.widgets_conainer.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
        self.info_label = ttk.Label(self.widgets_conainer, text=self._get_text("Select and Update Course"))
        self.info_label.grid(row=0, column=0, columnspan=2)

        self.updater_container = ttk.Frame(self.widgets_conainer)
        self.updater_container.grid(row=1, column=0, columnspan=2)
        self._init_updates()

        self.save_button = ttk.Button(self.widgets_conainer, text=self._get_text("Apply"), command=self.__save)
        self.save_button.grid(row=2, column=0)

        self.cancel_button = ttk.Button(self.widgets_conainer, text=self._get_text("Cancel"), command=self.__clean_exit)
        self.cancel_button.grid(row=2, column=1)

    def _init_updates(self) -> None:
        """
        Initializes the update widgets.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the updater container.
        self.updater_container.grid_rowconfigure((0,1), weight=1)
        self.updater_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Create the widgets.
        self.course_code_label = ttk.Label(self.updater_container, text=self._get_text("Course Code"))
        self.course_code_label.grid(row=0, column=0, columnspan=5)

        self.course_code_combobox = ttk.Combobox(self.updater_container, values=self.available_course_codes, state="readonly")
        self.course_code_combobox.grid(row=1, column=0, columnspan=5)

        # Add an handler for the combobox. To move on.
        self.course_code_combobox.bind("<<ComboboxSelected>>", self.get_new_course_values)

        # If there is a selected course code, set it. And initialize the combobox bind.
        if self.selected_course_code != None :
            self.course_code_combobox.set(self.selected_course_code)
            self.get_new_course_values(None)
            
    def get_new_course_values(self, event : tk.Event) -> None:
        """
        Gets the new course values.
        @Parameters:
            event - Required : Event. (tk.Event) -> Event that is triggered by the combobox.
        @Returns:
            None
        """
        # Configure the container.
        self.course_code_combobox.grid_configure(columnspan=1)
        self.course_code_label.grid_configure(columnspan=1)

        # Get the selected course.
        course_code = self.course_code_combobox.get()
        for course in self.modified_course_list :
            if course["course_code"] == course_code :
                self.selected_course = course
                break
            
        # Set the new course values.
        self.new_course_name = tk.StringVar(value=self.selected_course["course_name"])
        self.new_course_lang = tk.StringVar(value=self.selected_course["course_lang"])
        self.new_course_credit = tk.StringVar(value=self.selected_course["course_credit"])
        self.new_course_grade = tk.StringVar(value=self.selected_course["course_grade"])
        self.new_course_grade_point = tk.StringVar(value=self.selected_course["course_grade_point"])

        # Create the widgets. Use the new course values.
        course_name_label = ttk.Label(self.updater_container, text=self._get_text("New Course Name"))
        course_name_label.grid(row=0, column=1)
        self.new_course_name_entry = ttk.Entry(self.updater_container, textvariable=self.new_course_name)
        self.new_course_name_entry.grid(row=1, column=1)

        course_lang_label = ttk.Label(self.updater_container, text=self._get_text("New Course Language"))
        course_lang_label.grid(row=0, column=2)
        self.new_course_lang_entry = ttk.Entry(self.updater_container, textvariable=self.new_course_lang)
        self.new_course_lang_entry.grid(row=1, column=2)

        course_credit_label = ttk.Label(self.updater_container, text=self._get_text("New Course Credit"))
        course_credit_label.grid(row=0, column=3)
        # Use combobox for non validations.
        self.new_course_credit_combobox = ttk.Combobox(self.updater_container, values=self.possibleCredits, state="readonly", textvariable=self.new_course_credit)
        self.new_course_credit_combobox.grid(row=1, column=3)

        course_grade_label = ttk.Label(self.updater_container, text=self._get_text("New Course Grade"))
        course_grade_label.grid(row=0, column=4)
        # Use combobox for non validations.
        self.new_course_grade_combobox = ttk.Combobox(self.updater_container, values=self.possibleNotations, state="readonly", textvariable=self.new_course_grade)
        self.new_course_grade_combobox.grid(row=1, column=4)

        course_grade_point_label = ttk.Label(self.updater_container, text=self._get_text("New Course Grade Point"))
        course_grade_point_label.grid(row=0, column=5)
        # Disable the entry. To prevent direct input.
        self.new_course_grade_point_entry = ttk.Entry(self.updater_container, textvariable=self.new_course_grade_point, state="disabled")
        self.new_course_grade_point_entry.grid(row=1, column=5)

        # Add an handler for the new course credit and grade. To calculate the new course grade point.
        self.new_course_credit.trace_add("write", self.calculate_new_course_grade_point)
        self.new_course_grade.trace_add("write", self.calculate_new_course_grade_point)

    def calculate_new_course_grade_point(self, *args, **kwargs) -> None:
        """
        Calculate the grade point of the new course.
        @Parameters:
            None
        @Returns:
            None
        """
        # Handle the direct input case, check for validation at first.
        try :
            credit = self.new_course_credit.get()
            if credit == "" :
                return
            else :
                credit = int(credit)
            grade = self.new_course_grade.get().upper()
        except :
            return
        
        # Check for validation.
        if (credit < 0 or credit > 7) or grade not in self.possibleNotations :
            return

        # Get the weight of the grade.
        weight = self.weights[grade]

        # Calculate the grade point.
        grade_point = round(credit * weight, 2)

        # Set the grade point.
        self.new_course_grade_point.set(str(grade_point))

    def validate_new_course_data(self) -> bool:
        """
        Validates the new course data.
        @Parameters:
            None
        @Returns:
            bool - True if the data is valid, False otherwise.
        """
        # Check for validation. Check if the course code is selected.
        if self.course_code_combobox.get() == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please select a course code"))
            return False

        # Check for validation. Check if any of the fields is empty.
        if self.new_course_name.get() == "" or self.new_course_lang.get() == "" or self.new_course_credit.get() == "" or self.new_course_grade.get() == "" or self.new_course_grade_point.get() == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please fill all the fields"))
            return False
                                        
        # Check for validation. Check if the course grade is valid.
        if self.new_course_grade.get().upper() not in self.possibleNotations :
            messagebox.showerror(self._get_text("Error"), self._get_text("Invalid grade"))
            return False
        
        # Check for validation. Check if the course credit is valid. & Numeric.
        try :
            pump = self.new_course_credit.get()
            pump = int(pump)
            if pump < 0 or pump > 7 :
                messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be between 0 and 7"))
                return False
        except :
            messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be an integer"))
            return False

        # Check for validation. Check if the course grade point is valid. & Numeric.
        try :
            pump = self.new_course_grade_point.get()
            pump = float(pump)
        except :
            messagebox.showerror(self._get_text("Error"), self._get_text("New Grade Point must be numeric"))
            return False

        # Return True if all the validations are passed.
        return True

    def get_result(self) -> dict:
        """
        Returns the result of the updater.
        @Parameters:
            None
        @Returns:
            dict - The updated course.
        """
        # Return the result.
        return self.result

    def __save(self) -> None:
        """
        Saves the updated course.
        @Parameters:
            None
        @Returns:
            None
        """
        # Validate the new course data.
        passed = self.validate_new_course_data()

        # Return if not passed.
        if not passed :
            return

        # Set the updated course by class fields.
        updated_course = {
            "course_code" : self.course_code_combobox.get(),
            "course_name" : self.new_course_name_entry.get(),
            "course_lang" : self.new_course_lang_entry.get(),
            "course_credit" : self.new_course_credit_combobox.get(),
            "course_grade" : self.new_course_grade_combobox.get().upper(),
            "course_grade_point" : self.new_course_grade_point_entry.get()
        }

        # Set the result.
        self.result = updated_course

        # Destroy the window.
        self.destroy()

    def __clean_exit(self) -> None:
        """
        Clean exit from the dialog.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the result to None. (It is None by default.)
        self.result = self.result
        # Destroy the dialog.
        self.destroy()