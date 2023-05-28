import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from tkinter import Toplevel
from Environment import ASSETS_DC, to_turkish

from Utilities import (
    calculate_performance,
    filter_by,
    sort_by,
    update_course,
    add_course,
    subtract_course,
)

class GradeUpdater(ttk.Frame) :

    def __init__(self, application_container, parent, root, current_user_data, DEBUG=False, *args, **kwargs):
        super().__init__(application_container, *args, **kwargs)

        self.root = root
        self.parent = parent
        self.application_container = application_container
        self.DEBUG = DEBUG
        
        self.possibleNotations = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W", "S"]
        self.weights = {"A":4.00, "A-":3.70, "B+":3.30, "B":3.00, "B-":2.70, "C+":2.30, "C":2.00, "C-":1.70, "D+":1.30, "D":1.00, "F":0.00}
        
        self.__load_user_data(current_user_data)
        self.__load_output_info(is_init=True)
        self.__update_user_data()

        self.__load_containers()
        self.__load_program_buttons()
        self.__load_program_display()
        self.__load_program_output()

    def __update_user_data(self) :
        self.parent.update_user_data(self.__create_user_data())

    def __load_user_data(self, use_case) :
        self.owner_id : str = use_case["owner_id"]
        self.parsing_type : str = use_case["parsing_type"]
        self.parsing_language : str = use_case["parsing_language"]
        self.transcript_manager_date : str = use_case["transcript_manager_date"]
        self.transcript_creation_date : str = use_case["transcript_creation_date"]
        self.semesters : dict = use_case["semesters"]
        self.original_course_list : list = use_case["original_course_list"]
        self.filtering : list = use_case["filtering"] or []
        self.sorting : dict = use_case["sorting"] or {"sort_key" : None, "should_reverse" : None}
        self.modified_course_list : list = use_case["modified_course_list"]  or self.original_course_list.copy()
        self.document_name : str = use_case["document_name"]
        self.updated_course_list : list = use_case["updated_course_list"] or []
        self.subtracted_course_list : list = use_case["subtracted_course_list"] or []
        self.added_course_list : list = use_case["added_course_list"] or []

    def __load_output_info(self, is_init=False) :

        if is_init :
            original_performance = calculate_performance(self.original_course_list)
            self.original_credits_attempted = tk.IntVar(value=original_performance["credits_attempted"])
            self.original_credits_successful = tk.IntVar(value=original_performance["credits_successful"])
            self.original_credits_included_in_gpa = tk.IntVar(value=original_performance["credits_included_in_gpa"])
            self.original_gpa = tk.DoubleVar(value=original_performance["gpa"])
        
        modified_performance = calculate_performance(self.modified_course_list)
        self.modified_credits_attempted = tk.IntVar(value=modified_performance["credits_attempted"])
        self.modified_credits_successful = tk.IntVar(value=modified_performance["credits_successful"])
        self.modified_credits_included_in_gpa = tk.IntVar(value=modified_performance["credits_included_in_gpa"])
        self.modified_gpa = tk.DoubleVar(value=modified_performance["gpa"])

    def __create_user_data(self) :

        new_document = {
            "owner_id" : self.owner_id,
            "parsing_type" : self.parsing_type,
            "parsing_language" : self.parsing_language,
            "transcript_manager_date" : self.transcript_manager_date,
            "transcript_creation_date" : self.transcript_creation_date,
            "semesters" : self.semesters,
            "original_course_list" : self.original_course_list,
            "filtering" : self.filtering,
            "sorting" : self.sorting,
            "modified_course_list" : self.modified_course_list,
            "document_name" : self.document_name,
            "updated_course_list" : self.updated_course_list,
            "subtracted_course_list" : self.subtracted_course_list,
            "added_course_list" : self.added_course_list
        }
        return new_document

    def _get_text(self, text) :
        return self.parent._get_text(text, self.parsing_language)

    def __load_containers(self) :

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.container.grid_rowconfigure((0,1,2), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.program_buttons_container = ttk.Frame(self.container)
        self.program_buttons_container.grid(row=0, column=0)

        self.program_display_container = ttk.Frame(self.container)
        self.program_display_container.grid(row=1, column=0)

        self.program_output_container = ttk.Frame(self.container)
        self.program_output_container.grid(row=2, column=0)

    def __load_program_buttons(self) :

        self.program_buttons_container.grid_rowconfigure((0,1), weight=1)
        self.program_buttons_container.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        self.filter_button = ttk.Button(self.program_buttons_container, text=self._get_text("Filter Courses"), command=self.__filter)
        self.filter_button.grid(row=0, column=0, columnspan=3)

        self.update_course_button = ttk.Button(self.program_buttons_container, text=self._get_text("Update Course"), command=self.__update_course)
        self.update_course_button.grid(row=0, column=3, columnspan=3)

        self.add_course_button = ttk.Button(self.program_buttons_container, text=self._get_text("Add Course"), command=self.__add_course)
        self.add_course_button.grid(row=0, column=6, columnspan=3)

        self.remove_course_button = ttk.Button(self.program_buttons_container, text=self._get_text("Remove Course"), command=self.__remove_course)
        self.remove_course_button.grid(row=0, column=9, columnspan=3)

        self.sort_by_code_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Code"), command=lambda : self.__sort("course_code"))
        self.sort_by_code_button.grid(row=1, column=0, columnspan=2)

        self.sort_by_name_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Name"), command=lambda : self.__sort("course_name"))
        self.sort_by_name_button.grid(row=1, column=2, columnspan=2)

        self.sort_by_language_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Language"), command=lambda : self.__sort("course_lang"))
        self.sort_by_language_button.grid(row=1, column=4, columnspan=2)

        self.sort_by_credit_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Credit"), command=lambda : self.__sort("course_credit"))
        self.sort_by_credit_button.grid(row=1, column=6, columnspan=2)

        self.sort_by_grade_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Grade"), command=lambda : self.__sort("course_grade"))
        self.sort_by_grade_button.grid(row=1, column=8, columnspan=2)

        self.sort_by_grade_point_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Grade Point"), command=lambda : self.__sort("course_grade_point"))
        self.sort_by_grade_point_button.grid(row=1, column=10, columnspan=2)

        self.sorting_reverse_history = {
            "course_code" : False,
            "course_name" : False,
            "course_lang" : False,
            "course_credit" : False,
            "course_grade" : False,
            "course_grade_point" : False
        }

    def __load_program_display(self) :
        
        self.program_display_container.grid_columnconfigure((0), weight=1)
        self.program_display_container.grid_rowconfigure((0), weight=1)

        self.display_treeview = ttk.Treeview(self.program_display_container, height=15, show="headings", selectmode="browse")
        self.display_treeview.grid(row=0, column=0)

        # set columns
        self.display_treeview["columns"] = ("_code", "_name", "_canguage", "_credit", "_crade", "_crade_point")

        # set headings
        self.display_treeview.heading("_code", text="Course Code")
        self.display_treeview.heading("_name", text="Course Name")
        self.display_treeview.heading("_canguage", text="Course Language")
        self.display_treeview.heading("_credit", text="Course Credit")
        self.display_treeview.heading("_crade", text="Course Grade")
        self.display_treeview.heading("_crade_point", text="Course Grade Point")

        # when headings are clicked, it will be sorted
        self.display_treeview.column("_code", anchor="center", width=120)
        self.display_treeview.column("_name", anchor="center", width=120)
        self.display_treeview.column("_canguage", anchor="center", width=120)
        self.display_treeview.column("_credit", anchor="center", width=120)
        self.display_treeview.column("_crade", anchor="center", width=120)
        self.display_treeview.column("_crade_point", anchor="center", width=120)

        # add data
        self.__update_program_display()

    def __update_program_display(self) :

        # clear all data
        self.display_treeview.delete(*self.display_treeview.get_children())

        # add data
        for course in self.modified_course_list :
            self.display_treeview.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]))
    
    def __load_program_output(self) :
        
        self.program_output_container.grid_rowconfigure((0,1), weight=1)
        self.program_output_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.modes = ["BOTH", "MODIFIED"]
        self.output_mode = "BOTH"

        self.credits_attempted_output_text = tk.StringVar()
        self.credits_successful_output_text = tk.StringVar()
        self.credits_included_in_gpa_output_text = tk.StringVar()
        self.gpa_output_text = tk.StringVar()
        
        self.__update_output_label()
        
        self.credits_attempted_info_label = ttk.Label(self.program_output_container, text=self._get_text("Credits Attempted"))
        self.credits_attempted_info_label.grid(row=0, column=0)
        self.credits_attempted_output_label = ttk.Label(self.program_output_container, textvariable=self.credits_attempted_output_text)
        self.credits_attempted_output_label.grid(row=1, column=0)

        self.credits_successful_info_label = ttk.Label(self.program_output_container, text=self._get_text("Credits Successful"))
        self.credits_successful_info_label.grid(row=0, column=1)
        self.credits_successful_output_label = ttk.Label(self.program_output_container, textvariable=self.credits_successful_output_text)
        self.credits_successful_output_label.grid(row=1, column=1)

        self.credits_included_in_gpa_info_label = ttk.Label(self.program_output_container, text=self._get_text("Credits Included in GPA"))
        self.credits_included_in_gpa_info_label.grid(row=0, column=2)
        self.credits_included_in_gpa_output_label = ttk.Label(self.program_output_container, textvariable=self.credits_included_in_gpa_output_text)
        self.credits_included_in_gpa_output_label.grid(row=1, column=2)

        self.gpa_info_label = ttk.Label(self.program_output_container, text=self._get_text("GPA"))
        self.gpa_info_label.grid(row=0, column=3)
        self.gpa_output_label = ttk.Label(self.program_output_container, textvariable=self.gpa_output_text)
        self.gpa_output_label.grid(row=1, column=3)

        for widget in self.program_output_container.winfo_children() :
            widget.bind("<Button-1>", self.__switch_output_mode)
        self.program_output_container.bind("<Button-1>", self.__switch_output_mode)

    def __switch_output_mode(self, event) :

        if self.output_mode == "BOTH" :
            self.output_mode = "MODIFIED"
        else :
            self.output_mode = "BOTH"

        self.__update_output_label()

    def __update_output_label(self) :

        def ____reconfigure_output_text(modified : tk.StringVar, original : tk.StringVar = None) :
            if original is None :
                return modified.get()
            else :
                return "{} {} {}".format(original.get(), "\u279C", modified.get())
            
        if self.output_mode == "BOTH" :
            self.credits_attempted_output_text.set(____reconfigure_output_text(self.modified_credits_attempted, self.original_credits_attempted))
            self.credits_successful_output_text.set(____reconfigure_output_text(self.modified_credits_successful, self.original_credits_successful))
            self.credits_included_in_gpa_output_text.set(____reconfigure_output_text(self.modified_credits_included_in_gpa, self.original_credits_included_in_gpa))
            self.gpa_output_text.set(____reconfigure_output_text(self.modified_gpa, self.original_gpa))
        elif self.output_mode == "MODIFIED" :
            self.credits_attempted_output_text.set(____reconfigure_output_text(self.modified_credits_attempted))
            self.credits_successful_output_text.set(____reconfigure_output_text(self.modified_credits_successful))
            self.credits_included_in_gpa_output_text.set(____reconfigure_output_text(self.modified_credits_included_in_gpa))
            self.gpa_output_text.set(____reconfigure_output_text(self.modified_gpa))

    def __filter(self) :    
        
        self.filter_button.config(text=self._get_text("Filtering"), state="disabled")

        available_filterings = {"course_lang" : [], "course_credit" : [], "course_grade" : [], "course_grade_point" : []}

        for course in self.modified_course_list :
            current_course_lang = course["course_lang"]
            current_course_credit = course["course_credit"]
            current_course_grade = course["course_grade"]
            current_course_grade_point = course["course_grade_point"]

            if current_course_lang not in available_filterings["course_lang"] :
                available_filterings["course_lang"].append(current_course_lang)
            if current_course_credit not in available_filterings["course_credit"] :
                available_filterings["course_credit"].append(current_course_credit)
            if current_course_grade not in available_filterings["course_grade"] :
                available_filterings["course_grade"].append(current_course_grade)
            if current_course_grade_point not in available_filterings["course_grade_point"] :
                available_filterings["course_grade_point"].append(current_course_grade_point)

        for key in available_filterings :
            available_filterings[key].sort()

        class FilterSelecter(Toplevel) :

            def __init__(self, master, filtering, available_filterings, parsing_language) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Filter Courses"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.result = filtering.copy()
                self.current_filtering = filtering.copy()
                self.available_filterings = available_filterings

                self.container = ttk.Frame(self)
                self.container.grid(row=0, column=0)

                self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

                self.container.grid_rowconfigure((0), weight=1)
                self.container.grid_columnconfigure((0), weight=1)

                self.create_widgets()

                self.grab_set()
                self.focus_set()
                self.wait_window()

            def _get_text(self, text) :
                if self.parsing_language == "tr" :
                    return to_turkish[text]
                else :
                    return text

            def create_widgets(self) :

                self.widgets_container = ttk.Frame(self.container)
                self.widgets_container.grid(row=0, column=0)
                
                self.widgets_container.grid_rowconfigure((0,1,2), weight=1)
                self.widgets_container.grid_columnconfigure((0,1), weight=1)

                self.info_label = ttk.Label(self.widgets_container, text=self._get_text("Select and Remove filters"))
                self.info_label.grid(row=0, column=0, columnspan=2)

                self.filter_change_container = ttk.Frame(self.widgets_container)
                self.filter_change_container.grid(row=1, column=0, columnspan=2)
                self._init_filters()

                self.save_button = ttk.Button(self.widgets_container, text=self._get_text("Apply"), command=self.__save)
                self.save_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.widgets_container, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

            def _init_filters(self) :

                self.row_count = 1 + len(self.current_filtering) + 1 # -> 1 name, n filters, 1 combobox
                self.filter_change_container.grid_rowconfigure(tuple(range(self.row_count)), weight=1)
                self.filter_change_container.grid_columnconfigure((0, 1, 2), weight=1)

                self.filter_by_label = ttk.Label(self.filter_change_container, text=self._get_text("Filter By"))
                self.filter_with_label = ttk.Label(self.filter_change_container, text=self._get_text("Filter With"))
                self.operation_label = ttk.Label(self.filter_change_container, text=self._get_text("Operation"))

                if self.current_filtering == [] :
                    self.filter_by_label.grid(row=0, column=0, columnspan=3)
                else :
                    self.filter_by_label.grid(row=0, column=0)
                    self.filter_with_label.grid(row=0, column=1)
                    self.operation_label.grid(row=0, column=2)

                for grid_row_index, current_filter in enumerate(self.current_filtering) :

                    grid_row_index += 1

                    current_filter_key = current_filter["filter_key"]
                    current_filter_value = current_filter["filter_value"]
                    
                    def ___WRAPS_remove_filter(filter = current_filter) :
                        self.__remove_filter(filter)

                    current_filter_key_label = ttk.Label(self.filter_change_container, text=current_filter_key)
                    current_filter_key_label.grid(row=grid_row_index, column=0)

                    current_filter_value_label = ttk.Label(self.filter_change_container, text=current_filter_value)
                    current_filter_value_label.grid(row=grid_row_index, column=1)

                    remove_filter_button = ttk.Button(self.filter_change_container, text=self._get_text("Remove"), command=___WRAPS_remove_filter)
                    remove_filter_button.grid(row=grid_row_index, column=2)

                self.filter_key_combobox = ttk.Combobox(self.filter_change_container, values=list(available_filterings.keys()), state="readonly")
                self.filter_key_combobox.grid(row=self.row_count-1, column=0)

                self.filter_key_combobox.bind("<<ComboboxSelected>>", self.__load_filter_value_combobox)

            def __load_filter_value_combobox(self, event) :

                self.filter_by_label.grid_forget()
                self.filter_by_label.grid(row=0, column=0)
                self.filter_with_label.grid(row=0, column=1)
                self.operation_label.grid(row=0, column=2)

                self.filter_value_combobox = ttk.Combobox(self.filter_change_container, values=available_filterings[self.filter_key_combobox.get()], state="readonly")
                self.filter_value_combobox.grid(row=self.row_count-1, column=1)

                self.add_filter_button = ttk.Button(self.filter_change_container, text=self._get_text("Add"), command=self.__add_filter)
                self.add_filter_button.grid(row=self.row_count-1, column=2)

            def __add_filter(self) :
                
                # check if the new filter exists
                for current_filter in self.current_filtering :
                    if current_filter["filter_key"] == self.filter_key_combobox.get() and current_filter["filter_value"] == self.filter_value_combobox.get() :
                        messagebox.showerror(self._get_text("Error"), self._get_text("This filter already exists"))
                        return
                    
                # check if the new filter_key or filter_value is empty
                if self.filter_value_combobox.get() == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please select a filter value"))
                    return

                self.current_filtering.append({"filter_key" : self.filter_key_combobox.get(), "filter_value" : self.filter_value_combobox.get()})

                self.filter_key_combobox.destroy()
                self.filter_value_combobox.destroy()
                self.add_filter_button.destroy()

                self._init_filters()

            def __remove_filter(self, current_filter) :
                
                self.current_filtering.remove(current_filter)
                self.filter_change_container.destroy()
                self.filter_change_container = ttk.Frame(self.widgets_container)
                self.filter_change_container.grid(row=1, column=0, columnspan=2)
                self._init_filters()

            def get_result(self) :
                return self.result

            def __save(self) :

                try :
                    if self.filter_value_combobox.get() == "" :
                        messagebox.showerror(self._get_text("Error"), self._get_text("Please select a filter value"))
                        return
                except :
                    pass

                self.result = self.current_filtering
                self.destroy()

            def __clean_exit(self) :
                self.result = self.result
                self.destroy()

        previous_filter_count = len(self.filtering)

        obj = FilterSelecter(self, self.filtering, available_filterings, self.parsing_language)
        self.filtering = obj.get_result()

        current_filter_count = len(self.filtering)

        if current_filter_count < previous_filter_count :
            self.modified_course_list = self.original_course_list.copy()
            for course in self.added_course_list :
                self.modified_course_list = add_course(self.modified_course_list, course)
            for course in self.subtracted_course_list :
                self.modified_course_list = subtract_course(self.modified_course_list, course["course_code"])
            for course in self.updated_course_list :
                self.modified_course_list = update_course(self.modified_course_list, course)
            self.modified_course_list = sort_by(self.modified_course_list, self.sorting)

        for current_filter in self.filtering :
            self.modified_course_list = filter_by(self.modified_course_list, current_filter)

        self.filter_button.config(text=self._get_text("Filter Courses"), state="normal")
        self.__update_user_data()
        self.__load_output_info()
        self.__update_output_label()
        self.__update_program_display()

    def __update_course(self) :
        
        try :
            selected_course_code = self.display_treeview.item(self.display_treeview.selection())["values"][0]
        except :
            selected_course_code = None

        self.update_course_button.config(text=self._get_text("Updating"), state="disabled")

        available_course_codes = []

        for course in self.modified_course_list :
            available_course_codes.append(course["course_code"])

        class CourseUpdater(tk.Toplevel) :

            def __init__(self, master, modified_course_list, available_course_codes, parsing_language, possibleNotations, weights, selected_course_code) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Update Course"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.result = None
                self.available_course_codes = available_course_codes
                self.modified_course_list = modified_course_list
                self.possibleNotations = possibleNotations
                self.weights = weights
                self.selected_course_code = selected_course_code

                self.container = ttk.Frame(self)
                self.container.grid(row=0, column=0)

                self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

                self.container.grid_rowconfigure((0), weight=1)
                self.container.grid_columnconfigure((0), weight=1)

                self.create_widgets()

                self.grab_set()
                self.focus_set()
                self.wait_window()

            def _get_text(self, text) :
                if self.parsing_language == "tr" :
                    return to_turkish[text]
                else :
                    return text

            def create_widgets(self) :

                self.widgets_conainer = ttk.Frame(self.container)
                self.widgets_conainer.grid(row=0, column=0)

                self.widgets_conainer.grid_rowconfigure((0, 1, 2), weight=1)
                self.widgets_conainer.grid_columnconfigure((0, 1), weight=1)

                self.info_label = ttk.Label(self.widgets_conainer, text=self._get_text("Select and Update Course"))
                self.info_label.grid(row=0, column=0, columnspan=2)

                self.updater_container = ttk.Frame(self.widgets_conainer)
                self.updater_container.grid(row=1, column=0, columnspan=2)
                self._init_updates()

                self.save_button = ttk.Button(self.widgets_conainer, text=self._get_text("Apply"), command=self.__save)
                self.save_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.widgets_conainer, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

            def _init_updates(self) :

                self.updater_container.grid_rowconfigure((0,1), weight=1)
                self.updater_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

                self.course_code_label = ttk.Label(self.updater_container, text=self._get_text("Course Code"))
                self.course_code_label.grid(row=0, column=0, columnspan=5)

                self.course_code_combobox = ttk.Combobox(self.updater_container, values=self.available_course_codes, state="readonly")
                self.course_code_combobox.grid(row=1, column=0, columnspan=5)

                self.course_code_combobox.bind("<<ComboboxSelected>>", self.get_new_course_values)
                
                if self.selected_course_code != None :
                    self.course_code_combobox.set(self.selected_course_code)
                    self.get_new_course_values(None)
                    
            def get_new_course_values(self, event) :

                self.course_code_combobox.grid_configure(columnspan=1)
                self.course_code_label.grid_configure(columnspan=1)

                course_code = self.course_code_combobox.get()
                for course in self.modified_course_list :
                    if course["course_code"] == course_code :
                        self.selected_course = course
                        break
                    
                self.new_course_name = tk.StringVar(value=self.selected_course["course_name"])
                self.new_course_lang = tk.StringVar(value=self.selected_course["course_lang"])
                self.new_course_credit = tk.StringVar(value=self.selected_course["course_credit"])
                self.new_course_grade = tk.StringVar(value=self.selected_course["course_grade"])
                self.new_course_grade_point = tk.StringVar(value=self.selected_course["course_grade_point"])

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
                self.new_course_credit_entry = ttk.Entry(self.updater_container, textvariable=self.new_course_credit)
                self.new_course_credit_entry.grid(row=1, column=3)

                course_grade_label = ttk.Label(self.updater_container, text=self._get_text("New Course Grade"))
                course_grade_label.grid(row=0, column=4)
                self.new_course_grade_entry = ttk.Entry(self.updater_container, textvariable=self.new_course_grade)
                self.new_course_grade_entry.grid(row=1, column=4)

                course_grade_point_label = ttk.Label(self.updater_container, text=self._get_text("New Course Grade Point"))
                course_grade_point_label.grid(row=0, column=5)
                self.new_course_grade_point_entry = ttk.Entry(self.updater_container, textvariable=self.new_course_grade_point, state="disabled")
                self.new_course_grade_point_entry.grid(row=1, column=5)

                self.new_course_credit.trace_add("write", self.calculate_new_course_grade_point)
                self.new_course_grade.trace_add("write", self.calculate_new_course_grade_point)

            def calculate_new_course_grade_point(self, *args) :

                try :
                    credit = self.new_course_credit.get()
                    if credit == "" :
                        return
                    else :
                        credit = int(credit)
                    grade = self.new_course_grade.get().upper()
                except :
                    return
                
                if (credit < 0 or credit > 7) or grade not in self.possibleNotations :
                    return
                
                self.new_course_grade.set(grade)

                weight = self.weights[grade]

                grade_point = credit * weight

                self.new_course_grade_point.set(str(grade_point))

            def validate_new_course_data(self) :

                if self.course_code_combobox.get() == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please select a course code"))
                    return False

                if self.new_course_name.get() == "" or self.new_course_lang.get() == "" or self.new_course_credit.get() == "" or self.new_course_grade.get() == "" or self.new_course_grade_point.get() == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please fill all the fields"))
                    return False
                                                
                if self.new_course_grade.get().upper() not in self.possibleNotations :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Invalid grade"))
                    return False
                
                try :
                    pump = self.new_course_credit.get()
                    pump = int(pump)
                    if pump < 0 or pump > 7 :
                        messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be between 0 and 7"))
                        return False
                except :
                    messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be an integer"))
                    return False

                try :
                    pump = self.new_course_grade_point.get()
                    pump = float(pump)
                except :
                    messagebox.showerror(self._get_text("Error"), self._get_text("New Grade Point must be numeric"))
                    return False

                return True

            def get_result(self) :
                return self.result

            def __save(self) :
                
                passed = self.validate_new_course_data()

                if not passed :
                    return

                updated_course = {
                    "course_code" : self.course_code_combobox.get(),
                    "course_name" : self.new_course_name_entry.get(),
                    "course_lang" : self.new_course_lang_entry.get(),
                    "course_credit" : self.new_course_credit_entry.get(),
                    "course_grade" : self.new_course_grade_entry.get().upper(),
                    "course_grade_point" : self.new_course_grade_point_entry.get()
                }

                self.result = updated_course

                self.destroy()

            def __clean_exit(self) :
                self.result = self.result
                self.destroy()

        obj = CourseUpdater(self, self.modified_course_list, available_course_codes, self.parsing_language, self.possibleNotations, self.weights, selected_course_code)
        result = obj.get_result()
        if result is not None :
            self.updated_course_list.append(result)
            self.modified_course_list = update_course(self.modified_course_list, result)

        self.update_course_button.config(text=self._get_text("Update Course"), state="normal")
        self.__update_user_data()
        self.__load_output_info()
        self.__update_output_label()
        self.__update_program_display()

    def __add_course(self) :
        
        self.add_course_button.config(text=self._get_text("Adding"), state="disabled")

        existing_course_codes = [course["course_code"] for course in self.modified_course_list]

        class CourseAdder(tk.Toplevel) :

            def __init__(self, master, existing_course_codes, parsing_language, possibleNotations, weights) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Add Course"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.result = None
                self.existing_course_codes = existing_course_codes
                self.possibleNotations = possibleNotations 
                self.weights = weights

                self.container = ttk.Frame(self)
                self.container.grid(row=0, column=0)

                self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

                self.container.grid_rowconfigure((0), weight=1)
                self.container.grid_columnconfigure((0), weight=1)

                self.create_widgets()

                self.grab_set()
                self.focus_set()
                self.wait_window()

            def _get_text(self, text) :
                if self.parsing_language == "tr" :
                    return to_turkish[text]
                else :
                    return text

            def create_widgets(self) :

                self.add_course_container = ttk.Frame(self.container)
                self.add_course_container.grid(row=0, column=0)

                self.add_course_container.grid_rowconfigure((0, 1, 2), weight=1)
                self.add_course_container.grid_columnconfigure((0, 1), weight=1)

                self.add_course_course_code_label = ttk.Label(self.add_course_container, text=self._get_text("Write and Add Course"))
                self.add_course_course_code_label.grid(row=0, column=0, columnspan=2)

                self.adderer_container = ttk.Frame(self.add_course_container)
                self.adderer_container.grid(row=1, column=0, columnspan=2)
                self.show_current_addons()

                self.save_button = ttk.Button(self.add_course_container, text=self._get_text("Apply"), command=self.__save)
                self.save_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.add_course_container, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

            def show_current_addons(self) :

                self.adderer_container.grid_rowconfigure((0,1), weight=1)
                self.adderer_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

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

                self.new_course_code = tk.StringVar()
                self.new_course_name = tk.StringVar()
                self.new_course_lang = tk.StringVar()
                self.new_course_credit = tk.StringVar()
                self.new_course_grade = tk.StringVar()
                self.new_course_grade_point = tk.StringVar()

                self.new_course_code_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_code)
                self.new_course_code_entry.grid(row=1, column=0)

                self.new_course_name_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_name)
                self.new_course_name_entry.grid(row=1, column=1)

                self.new_course_lang_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_lang)
                self.new_course_lang_entry.grid(row=1, column=2)

                self.new_course_credit_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_credit)
                self.new_course_credit_entry.grid(row=1, column=3)

                self.new_course_grade_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_grade)
                self.new_course_grade_entry.grid(row=1, column=4)

                self.new_course_grade_point_entry = ttk.Entry(self.adderer_container, textvariable=self.new_course_grade_point, state="disabled")
                self.new_course_grade_point_entry.grid(row=1, column=5)

                self.new_course_credit.trace_add("write", self.calculate_new_course_grade_point)
                self.new_course_grade.trace_add("write", self.calculate_new_course_grade_point)

            def calculate_new_course_grade_point(self, *args) :

                try :
                    credit = self.new_course_credit.get()
                    if credit == "" :
                        return
                    else :
                        credit = int(credit)
                    grade = self.new_course_grade.get().upper()
                except :
                    return
                
                if (credit < 0 or credit > 7) or grade not in self.possibleNotations :
                    return
                
                self.new_course_grade.set(grade)

                weight = self.weights[grade]

                grade_point = credit * weight

                self.new_course_grade_point.set(str(grade_point))

            def validate_new_course_data(self) :

                if self.new_course_name.get() == "" or self.new_course_lang.get() == "" or self.new_course_credit.get() == "" or self.new_course_grade.get() == "" or self.new_course_grade_point.get() == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please fill all the fields"))
                    return False
                                                
                if self.new_course_grade.get().upper() not in self.possibleNotations :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Invalid grade"))
                    return False
                
                try :
                    pump = self.new_course_credit.get()
                    pump = int(pump)
                    if pump < 0 or pump > 7 :
                        messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be between 0 and 7"))
                        return False
                except :
                    messagebox.showerror(self._get_text("Error"), self._get_text("New Credit must be an integer"))
                    return False

                try :
                    pump = self.new_course_grade_point.get()
                    pump = float(pump)
                except :
                    messagebox.showerror(self._get_text("Error"), self._get_text("New Grade Point must be numeric"))
                    return False

                if self.new_course_code.get() in self.existing_course_codes :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Course Code already exists"))
                    return False

                return True

            def get_result(self) :
                return self.result

            def __save(self) :
                
                passed = self.validate_new_course_data()

                if not passed :
                    return

                new_course = {
                    "course_code" : self.new_course_code_entry.get(),
                    "course_name" : self.new_course_name_entry.get(),
                    "course_lang" : self.new_course_lang_entry.get(),
                    "course_credit" : self.new_course_credit_entry.get(),
                    "course_grade" : self.new_course_grade_entry.get().upper(),
                    "course_grade_point" : self.new_course_grade_point_entry.get()
                }

                self.result = new_course

                self.destroy()

            def __clean_exit(self) :
                self.result = self.result
                self.destroy()

        obj = CourseAdder(self, existing_course_codes, self.parsing_language, self.possibleNotations, self.weights)
        result = obj.get_result()
        if result is not None :
            self.added_course_list.append(result)
            self.modified_course_list = add_course(self.modified_course_list, result)

        self.add_course_button.config(text=self._get_text("Add Course"), state="normal")
        self.__update_user_data()
        self.__load_output_info()
        self.__update_output_label()
        self.__update_program_display()

    def __remove_course(self) :
        
        try :
            selected_course_code = self.display_treeview.item(self.display_treeview.selection())["values"][0]
        except :
            selected_course_code = None

        self.remove_course_button.config(text=self._get_text("Removing"), state="disabled")

        existing_course_codes = [course["course_code"] for course in self.modified_course_list]

        class CourseRemover(tk.Toplevel) :

            def __init__(self, master, modified_course_list, existing_course_codes, parsing_language, selected_course_code) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Remove Course"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.result = None
                self.existing_course_codes = existing_course_codes
                self.modified_course_list = modified_course_list
                self.selected_course_code = selected_course_code

                self.container = ttk.Frame(self)
                self.container.grid(row=0, column=0)

                self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

                self.container.grid_rowconfigure((0), weight=1)
                self.container.grid_columnconfigure((0), weight=1)

                self.create_widgets()

                self.grab_set()
                self.focus_set()
                self.wait_window()

            def _get_text(self, text) :
                if self.parsing_language == "tr" :
                    return to_turkish[text]
                else :
                    return text

            def create_widgets(self) :

                self.remove_course_container = ttk.Frame(self.container)
                self.remove_course_container.grid(row=0, column=0)

                self.remove_course_container.grid_rowconfigure((0, 1, 2), weight=1)
                self.remove_course_container.grid_columnconfigure((0, 1), weight=1)

                self.remove_course_course_code_label = ttk.Label(self.remove_course_container, text=self._get_text("Select and Remove Course"))
                self.remove_course_course_code_label.grid(row=0, column=0, columnspan=2)

                self.remover_container = ttk.Frame(self.remove_course_container)
                self.remover_container.grid(row=1, column=0, columnspan=2)
                self.show_current_addons()

                self.save_button = ttk.Button(self.remove_course_container, text=self._get_text("Apply"), command=self.__save)
                self.save_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.remove_course_container, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

            def show_current_addons(self) :

                self.remover_container.grid_rowconfigure((0,1), weight=1)
                self.remover_container.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

                self.table_course_code_label = ttk.Label(self.remover_container, text=self._get_text("Existing Course Code"))
                self.table_course_code_label.grid(row=0, column=0, columnspan=5)

                self.select_course_course_code_combobox = ttk.Combobox(self.remover_container, values=self.existing_course_codes, state="readonly")
                self.select_course_course_code_combobox.grid(row=1, column=0, columnspan=5)

                self.select_course_course_code_combobox.bind("<<ComboboxSelected>>", self.show_course_items)

                if self.selected_course_code is not None :
                    self.select_course_course_code_combobox.set(self.selected_course_code)
                    self.show_course_items(None)
                
            def show_course_items(self, event) :

                self.table_course_code_label.grid_configure(columnspan=1)
                self.select_course_course_code_combobox.grid_configure(columnspan=1)

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

                use_code = self.select_course_course_code_combobox.get()

                for course in self.modified_course_list :
                    if course["course_code"] == use_code :
                        self.course_name = tk.StringVar(value=course["course_name"])
                        self.course_lang = tk.StringVar(value=course["course_lang"])
                        self.course_credit = tk.StringVar(value=course["course_credit"])
                        self.course_grade = tk.StringVar(value=course["course_grade"])
                        self.course_grade_point = tk.StringVar(value=course["course_grade_point"])
                        break
                
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

            def get_result(self) :
                return self.result

            def __save(self) :
                
                if self.select_course_course_code_combobox.get() == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please select a course to remove"))
                    return

                deleted_course = {
                    "course_code" : self.select_course_course_code_combobox.get(),
                    "course_name" : self.course_name_entry.get(),
                    "course_lang" : self.course_lang_entry.get(),
                    "course_credit" : self.course_credit_entry.get(),
                    "course_grade" : self.course_grade_entry.get(),
                    "course_grade_point" : self.course_grade_point_entry.get()
                }

                self.result = deleted_course

                self.destroy()

            def __clean_exit(self) :
                self.result = self.result
                self.destroy()

        obj = CourseRemover(self, self.modified_course_list, existing_course_codes, self.parsing_language, selected_course_code)
        result = obj.get_result()
        if result is not None :
            self.subtracted_course_list.append(result)
            self.modified_course_list = subtract_course(self.modified_course_list, result["course_code"])

        self.remove_course_button.config(text=self._get_text("Remove Course"), state="normal")
        self.__update_user_data()
        self.__load_output_info()
        self.__update_output_label()
        self.__update_program_display()

    def __sort(self, key) :
        
        sort_key = key
        should_reverse = self.sorting_reverse_history[sort_key]
        self.sorting_reverse_history[sort_key] = not should_reverse

        self.sorting = {
            "sort_key" : sort_key,
            "should_reverse" : should_reverse
        }

        self.modified_course_list = sort_by(self.modified_course_list, self.sorting)
        self.__update_user_data()
        self.__load_output_info()
        self.__update_output_label()
        self.__update_program_display()
