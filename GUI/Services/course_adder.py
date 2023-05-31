from    Environment import  ASSETS_DC, to_turkish # -> Environment variables
from    tkinter     import  messagebox # -> Interract with user
from    tkinter     import  Toplevel # -> Create new window
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI

class CourseAdder(Toplevel) :

    def __init__(self, master : ttk.Frame, existing_course_codes : list, parsing_language : str, possibleNotations : list, weights : dict, possibleCredits : list) -> None:
        """
        Constructor of CourseAdder class. This class is used to add new courses to the program.
        @Parameters:
            master - Required : The master frame of the window. (ttk.Frame) -> This is the main window of the program.
            existing_course_codes - Required : The list of existing course codes. (list) -> This is used to check if the course code is already in use.
            parsing_language - Required : The language of the program. (str) -> This is used to get the text from the language dictionary.
            possibleNotations - Required : The list of possible notations. (list) -> This is used to check if the notation is valid.
            weights - Required : The dictionary of weights. (dict) -> This is used to calculate the grade point.
            possibleCredits - Required : The list of possible credits. (list) -> This is used to check if the credit is valid.
        @Returns:
            None
        """
        # Initialize the Toplevel window.
        super().__init__(master)

        # Set the parsing language.
        self.parsing_language = parsing_language

        # Set the title and icon of the window.
        self.title(self._get_text("Add Course"))
        self.iconbitmap(ASSETS_DC.ICON)

        # Set the class variables.
        self.existing_course_codes = existing_course_codes
        self.possibleNotations = possibleNotations 
        self.possibleCredits = possibleCredits
        self.weights = weights
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
        Creates the widgets of the window.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create the main container.
        self.add_course_container = ttk.Frame(self.container)
        self.add_course_container.grid(row=0, column=0)
        # Configure the main container.
        self.add_course_container.grid_rowconfigure((0, 1, 2), weight=1)
        self.add_course_container.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
        self.add_course_course_code_label = ttk.Label(self.add_course_container, text=self._get_text("Write and Add Course"))
        self.add_course_course_code_label.grid(row=0, column=0, columnspan=2)

        self.adderer_container = ttk.Frame(self.add_course_container)
        self.adderer_container.grid(row=1, column=0, columnspan=2)
        self.show_current_addons()

        self.save_button = ttk.Button(self.add_course_container, text=self._get_text("Apply"), command=self.__save)
        self.save_button.grid(row=2, column=0)

        self.cancel_button = ttk.Button(self.add_course_container, text=self._get_text("Cancel"), command=self.__clean_exit)
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
        self.adderer_container.grid_rowconfigure((0,1), weight=1)
        self.adderer_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Create the widgets.
        table_course_code_label = ttk.Label(self.adderer_container, text=self._get_text("New Course Code"))
        table_course_code_label.grid(row=0, column=0)

        table_course_name_label = ttk.Label(self.adderer_container, text=self._get_text("New Course Name"))
        table_course_name_label.grid(row=0, column=1)

        table_course_lang_label = ttk.Label(self.adderer_container, text=self._get_text("New Course Language"))
        table_course_lang_label.grid(row=0, column=2)

        table_course_credit_label = ttk.Label(self.adderer_container, text=self._get_text("New Course Credit"))
        table_course_credit_label.grid(row=0, column=3)

        table_course_grade_label = ttk.Label(self.adderer_container, text=self._get_text("New Course Grade"))
        table_course_grade_label.grid(row=0, column=4)

        table_course_grade_point_label = ttk.Label(self.adderer_container, text=self._get_text("New Course Grade Point"))
        table_course_grade_point_label.grid(row=0, column=5)

        # Setup the class variables.
        self.new_course_code = tk.StringVar()
        self.new_course_name = tk.StringVar()
        self.new_course_lang = tk.StringVar()
        self.new_course_credit = tk.StringVar()
        self.new_course_grade = tk.StringVar()
        self.new_course_grade_point = tk.StringVar()

        # Create entries and comboboxes.
        self.new_course_code_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_code)
        self.new_course_code_entry.grid(row=1, column=0)

        self.new_course_name_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_name)
        self.new_course_name_entry.grid(row=1, column=1)

        self.new_course_lang_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_lang)
        self.new_course_lang_entry.grid(row=1, column=2)

        # Use combobox for non validations.
        self.new_course_credit_combobox = ttk.Combobox(self.adderer_container, textvariable=self.new_course_credit, values=self.possibleCredits, state="readonly")
        self.new_course_credit_combobox.grid(row=1, column=3)

        # Use combobox for non validations.
        self.new_course_grade_combobox = ttk.Combobox(self.adderer_container, textvariable=self.new_course_grade, values=self.possibleNotations, state="readonly")
        self.new_course_grade_combobox.grid(row=1, column=4)

        # Set the grade point entry to disabled to prevent direct input.
        self.new_course_grade_point_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_grade_point, state="disabled")
        self.new_course_grade_point_entry.grid(row=1, column=5)

        # Handle changes.
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
        grade_point = credit * weight

        # Set the grade point.
        self.new_course_grade_point.set(str(grade_point))

    def validate_new_course_data(self) -> bool:
        """
        Validate the data of the new course.
        @Parameters:
            None
        @Returns:
            bool: True if the data is valid, False otherwise.
        """
        # Check for empty fields.
        if self.new_course_name.get() == "" or self.new_course_lang.get() == "" or self.new_course_credit.get() == "" or self.new_course_grade.get() == "" or self.new_course_grade_point.get() == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please fill all the fields"))
            return False

        # Check for validation. Grade must be in the possible notations.                    
        if self.new_course_grade.get().upper() not in self.possibleNotations :
            messagebox.showerror(self._get_text("Error"), self._get_text("Invalid grade"))
            return False
        
        # Check for validation. Credit must be between 0 and 7.
        try :
            pump = self.new_course_credit.get()
            pump = int(pump)
            if pump < 0 or pump > 7 :
                messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be between 0 and 7"))
                return False
        except :
            messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be an integer"))
            return False

        # Check for validation. Grade point must be numeric.
        try :
            pump = self.new_course_grade_point.get()
            pump = float(pump)
        except :
            messagebox.showerror(self._get_text("Error"), self._get_text("New Grade Point must be numeric"))
            return False

        # Check for validation. Course code must be unique.
        if self.new_course_code.get() in self.existing_course_codes :
            messagebox.showerror(self._get_text("Error"), self._get_text("Course Code already exists"))
            return False

        # Return True if all the validations are passed.
        return True

    def get_result(self) -> dict:
        """
        Get the result of the dialog.
        @Parameters:
            None
        @Returns:
            dict: The result of the dialog.
        """
        # Return the result.
        return self.result

    def __save(self) -> None:
        """
        Save the new course.
        @Parameters:
            None
        @Returns:
            None
        """
        # Validate the data.
        passed = self.validate_new_course_data()

        # If not passed, return.
        if not passed :
            return

        # Create the new course. Via class fields.
        new_course = {
            "course_code" : self.new_course_code_entry.get(),
            "course_name" : self.new_course_name_entry.get(),
            "course_lang" : self.new_course_lang_entry.get(),
            "course_credit" : self.new_course_credit_combobox.get(),
            "course_grade" : self.new_course_grade_combobox.get().upper(),
            "course_grade_point" : self.new_course_grade_point_entry.get()
        }

        # Set the result.
        self.result = new_course

        # Destroy the dialog.
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