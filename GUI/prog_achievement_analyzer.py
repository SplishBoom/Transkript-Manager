from    Utilities                           import  calculate_performance, generate_gradient_colors, filter_by # -> Utility functions
from    tkinter                             import  Label as TkinterLabel, Frame as TkinterFrame # -> Manipulate matplotlib widgets.
from    matplotlib.backends.backend_tkagg   import  FigureCanvasTkAgg, NavigationToolbar2Tk # -> Packing plot and setting toolbar
from    Environment                         import  GUI_DC # -> Environment variables
from    matplotlib.figure                   import  Figure # -> Plotting and creating figure
import  customtkinter                       as      ctk # -> Custom tkinter library

class AchievementAnalyzer(ctk.CTkFrame) :

    def __init__(self, application_container : ctk.CTkFrame, parent : ctk.CTkFrame, root : ctk.CTk, current_user_data : dict, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for AchievementAnalyzer class. Used to initialize main window of the program.
        @Parameters:
            application_container - Required : Container frame of the application. (ttk.Frame) -> Which is used to place the application frame.
            parent                - Required : Parent frame of the application. (ttk.Frame) -> Which is used to set connection to application frame.
            root                  - Required : Root window of the application. (tk.Tk) -> Which is used to set connection between frames.
            current_user_data     - Required : Current user data. (dict) -> Which is used to determine current user data.
            DEBUG                 - Optional : Debug mode flag. (bool) (default : False) -> Which is used to determine whether the application is in debug mode or not.
        @Returns:
            None
        """
        # Initialize main window of the program
        super().__init__(application_container, *args, **kwargs)

        # Set class variables
        self.application_container = application_container
        self.parent = parent
        self.root   = root
        self.DEBUG  = DEBUG
        
        # Load user data
        self.__load_user_data(current_user_data)

        # Load containers
        self.__load_containers()

        # Load program
        self.__load_program_plot()

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
        # Set the initial configuration, to make expandable affect on window.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main container
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure main container
        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        # Create program container
        self.program_plot_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.program_plot_container.grid(row=0, column=0, sticky="nsew")

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

    def ___create_course_based_plot_data(self) -> None:
        """
        Creates course based plot data.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set possible grades
        self.all_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W", "S", "N/A"]
        
        # Initialize course based plot data
        self.course_based_plot_data = {
            "course_grade" : [],
            "course_index" : [],
            "course_code" : []
        }

        # Iterate over modified course list
        for course_index, course in enumerate(self.modified_course_list):
            course_grade = course["course_grade"]
            course_index = course_index + 1
            course_code = course["course_code"]

            # Update course_grade to its corresponding index in reversed all_grades
            reversed_index = len(self.all_grades) - self.all_grades.index(course_grade) - 1

            # Append course based plot data
            self.course_based_plot_data["course_grade"].append(reversed_index)
            self.course_based_plot_data["course_index"].append(course_index)
            self.course_based_plot_data["course_code"].append(course_code)
            
    def ___create_semester_based_plot_data(self) -> None:
        """
        Creates semester based plot data.
        @Parameters:
            None
        @Returns:
            None
        """
        # Initialize semester based plot data
        self.semester_based_plot_data = {
            "semester_grade" : [],
            "semester_index" : [],
            "semester_name" : []
        }

        # Openup a temporary semester
        dummy_semester = {
            "semester_definition" : "Temp Semester",
            "course_list" : self.added_course_list.copy()
        }
        # Append temporary semester to semesters when it is not empty
        if dummy_semester["course_list"] != [] :
            self.semesters["Temp Semester"] = dummy_semester

        # Get updated course list, and apply updates to semester course lists.
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

        # Remove subtracted courses from semester course lists.
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

        # Iterate over semesters, apply filtering.
        for semester in self.semesters :

            current_semester = self.semesters[semester]
            current_course_list = current_semester["course_list"]

            for current_filter in self.filtering :
                current_course_list = filter_by(current_course_list, current_filter)

            current_semester["course_list"] = current_course_list
          
        # Main loop for semester based plot data
        for semester_index, semester in enumerate(self.semesters) :

            # Get current semester data
            current_semester = self.semesters[semester]
            current_course_list = current_semester["course_list"]

            # Calculate semester performance
            semester_performance = calculate_performance(current_course_list)
            semester_grade = semester_performance["gpa"]
            semester_index = semester_index + 1
            semester_name = " ".join(current_semester["semester_definition"].split(" ")[0:2])
            
            # If the transcript is old, this will handle the translation.
            try :
                semester_year, semester_semester = semester_name.split(" ")
                semester_name = semester_year + " " + self._get_text(semester_semester)
            except :
                pass

            # Append semester based plot data
            self.semester_based_plot_data["semester_grade"].append(semester_grade)
            self.semester_based_plot_data["semester_index"].append(semester_index)
            self.semester_based_plot_data["semester_name"].append(semester_name)

    def __load_program_plot(self) -> None:
        """
        Loads program plot.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure program plot container
        self.program_plot_container.grid_rowconfigure((0), weight=1)
        self.program_plot_container.grid_columnconfigure((0,2), weight=1)
        self.program_plot_container.grid_columnconfigure((1), weight=0)

        # Create program based plot data & load program based plot
        self.___create_semester_based_plot_data()
        self.___load_semester_based_plot()

        # Put a seperator between program based plot and course based plot
        seperator = ctk.CTkFrame(self.program_plot_container, width=20, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        seperator.grid(row=0, column=1, sticky="nsew")

        # Create course based plot data & load course based plot
        self.___create_course_based_plot_data()
        self.___load_course_based_plot()

    def ___load_semester_based_plot(self) -> None:
        """
        Loads semester based plot using class variables.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set up main container and packable frame for navigation toolbar packing
        self.semester_based_plot_container = ctk.CTkFrame(self.program_plot_container)
        self.semester_based_plot_container.grid(row=0, column=0, sticky="nsew")
        self.sbp_packable_frame = ctk.CTkFrame(self.semester_based_plot_container)
        self.sbp_packable_frame.pack(fill="both", expand=True)

        # Create semester based plot figure and configure it
        self.semester_based_plot_figure = Figure(figsize=(5, 5), dpi=100, tight_layout=True)
        self.semester_based_plot_figure.subplots_adjust(left=0.12, right=0.97, bottom=0.135, top=0.93)
        self.semester_based_plot_figure.patch.set_facecolor(GUI_DC.LIGHT_BACKGROUND)
        self.semester_based_plot_figure.patch.set_alpha(0.5)

        # Create semester based plot
        self.semester_based_plot = self.semester_based_plot_figure.add_subplot(111)
        self.semester_based_plot.set_title(self._get_text("Semester Based Performance"))
        self.semester_based_plot.set_ylabel(self._get_text("Grade Point Average"))
        self.semester_based_plot.set_facecolor("#F0F0F0")
        self.semester_based_plot.grid(color="#FFFFFF", linestyle="-", linewidth=1)
        self.semester_based_plot.set_axisbelow(True)

        # Create gradient colors
        num_colors = len(self.semester_based_plot_data["semester_grade"])
        gradient_colors = generate_gradient_colors(num_colors)

        # Plot semester based plot as bar chart
        self.semester_based_plot.bar(
            self.semester_based_plot_data["semester_index"], 
            self.semester_based_plot_data["semester_grade"], 
            color=gradient_colors, 
            edgecolor="black"
        )

        # Setup x & y limits, ticks and labels
        self.semester_based_plot.set_xlim(0, len(self.semester_based_plot_data["semester_index"]) + 1)
        self.semester_based_plot.set_ylim(0, 4.0)

        self.semester_based_plot.set_xticks(self.semester_based_plot_data["semester_index"])
        self.semester_based_plot.set_xticklabels(labels=self.semester_based_plot_data["semester_name"], rotation=25, ha="right", fontsize=8)

        # Setup the canvas and pack it.
        self.semester_based_plot_canvas = FigureCanvasTkAgg(self.semester_based_plot_figure, self.sbp_packable_frame)
        self.semester_based_plot_canvas.draw()
        self.semester_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)
    
        # Setup the toolbar and pack it.
        self.semester_based_plot_toolbar = NavigationToolbar2Tk(self.semester_based_plot_canvas, self.sbp_packable_frame)
        # Set the coloring
        self.semester_based_plot_toolbar.configure(background=GUI_DC.DARK_BACKGROUND)
        # Find the wanted widgets and pack them. Remove the rest.
        desired_widgets = []
        for child in self.semester_based_plot_toolbar.winfo_children():
            if not (isinstance(child, TkinterLabel) or isinstance(child, TkinterFrame)):
                desired_widgets.append(child)
            child.pack_forget()
        # RePack the desired widgets.
        for widget in desired_widgets:
            widget.configure(bg=GUI_DC.LIGHT_BACKGROUND, cursor="hand2")
            widget.pack(fill="both", expand=True, side="left", padx=1, pady=1)

        self.semester_based_plot_toolbar.update()
        self.semester_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)
     
    def ___load_course_based_plot(self) -> None:
        """
        Loads course based plot using class variables.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set up main container and packable frame for navigation toolbar packing
        self.course_based_plot_container = ctk.CTkFrame(self.program_plot_container)
        self.course_based_plot_container.grid(row=0, column=2, sticky="nsew")
        self.cbp_packable_frame = ctk.CTkFrame(self.course_based_plot_container)
        self.cbp_packable_frame.pack(fill="both", expand=True)

        # Create course based plot figure and configure it
        self.course_based_plot_figure = Figure(figsize=(5, 5), dpi=100, tight_layout=True)
        self.course_based_plot_figure.subplots_adjust(left=0.12, right=0.97, bottom=0.135, top=0.93)
        self.course_based_plot_figure.patch.set_facecolor(GUI_DC.LIGHT_BACKGROUND)
        self.course_based_plot_figure.patch.set_alpha(0.5)

        # Create course based plot
        self.course_based_plot = self.course_based_plot_figure.add_subplot(111)
        self.course_based_plot.set_title(self._get_text("Course Based Performance"))
        self.course_based_plot.set_ylabel(self._get_text("Grade Notation"))
        self.course_based_plot.set_facecolor("#F0F0F0")
        self.course_based_plot.grid(color="#FFFFFF", linestyle="-", linewidth=1)
        self.course_based_plot.set_axisbelow(True)

        # Create gradient colors
        num_colors = len(self.course_based_plot_data["course_grade"])
        gradient_colors = generate_gradient_colors(num_colors)

        # Plot course based plot as scatter plot
        self.course_based_plot.scatter(
            self.course_based_plot_data["course_index"],
            self.course_based_plot_data["course_grade"], 
            color=gradient_colors, 
            edgecolor="black"
        )

        # Setup x & y limits, ticks and labels
        x_padding = 1
        self.course_based_plot.set_xlim(0.5 - x_padding, len(self.course_based_plot_data["course_index"]) + 0.5 + x_padding)
        self.course_based_plot.set_xticks(self.course_based_plot_data["course_index"])
        self.course_based_plot.set_xticklabels(labels=self.course_based_plot_data["course_code"], rotation=55, ha="right", fontsize=6)
        
        all_grade_indices = list(reversed(range(len(self.all_grades))))
        self.course_based_plot.set_yticks(all_grade_indices)
        self.course_based_plot.set_yticklabels(self.all_grades)

        # Setup the canvas and pack it.
        self.course_based_plot_canvas = FigureCanvasTkAgg(self.course_based_plot_figure, self.cbp_packable_frame)
        self.course_based_plot_canvas.draw()
        self.course_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Setup the toolbar and pack it.
        self.course_based_plot_toolbar = NavigationToolbar2Tk(self.course_based_plot_canvas, self.cbp_packable_frame)
        # Set the coloring
        self.course_based_plot_toolbar.configure(background=GUI_DC.DARK_BACKGROUND)
        # Find the wanted widgets and pack them. Remove the rest.
        desired_widgets = []
        for child in self.course_based_plot_toolbar.winfo_children():
            if not (isinstance(child, TkinterLabel) or isinstance(child, TkinterFrame)):
                desired_widgets.append(child)
            child.pack_forget()
        # RePack the desired widgets.
        for widget in desired_widgets:
            widget.configure(bg=GUI_DC.LIGHT_BACKGROUND, cursor="hand2")
            widget.pack(fill="both", expand=True, side="left", padx=1, pady=1)

        self.course_based_plot_toolbar.update()
        self.course_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)
