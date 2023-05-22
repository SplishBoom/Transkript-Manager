import tkinter as tk
from tkinter import ttk

from Utilities import calculate_performance

class GradeUpdater(ttk.Frame) :

    def __init__(self, application_container, parent, root, current_user_data, DEBUG=False, *args, **kwargs):
        super().__init__(application_container, *args, **kwargs)

        self.root = root
        self.parent = parent
        self.application_container = application_container
        self.DEBUG = DEBUG
        
        self.__load_user_data(current_user_data)

        self.__load_containers()
        self.__load_program_buttons()

    def __load_user_data(self, use_case) :
        self.owner_id : str = use_case["owner_id"]
        self.parsing_type : str = use_case["parsing_type"]
        self.parsing_language : str = use_case["parsing_language"]
        self.transcript_manager_date : str = use_case["transcript_manager_date"]
        self.transcript_creation_date : str = use_case["transcript_creation_date"]
        self.semesters : dict = use_case["semesters"]
        self.original_course_list : list = use_case["original_course_list"]
        self.filtering : tuple = use_case["filtering"]
        self.sorting : tuple = use_case["sorting"]
        self.modified_course_list : list = use_case["modified_course_list"]
        self.document_name : str = use_case["document_name"]
        self.subtracted_course_list : list = use_case["subtracted_course_list"]
        self.added_course_list : list = use_case["added_course_list"]        

        

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

        self.program_display_container = tk.Canvas(self.container)
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

        self.sort_by_code_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Code"), command=lambda : self.__sort("code"))
        self.sort_by_code_button.grid(row=1, column=0, columnspan=2)

        self.sort_by_name_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Name"), command=lambda : self.__sort("name"))
        self.sort_by_name_button.grid(row=1, column=2, columnspan=2)

        self.sort_by_language_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Language"), command=lambda : self.__sort("language"))
        self.sort_by_language_button.grid(row=1, column=4, columnspan=2)

        self.sort_by_credit_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Credit"), command=lambda : self.__sort("credit"))
        self.sort_by_credit_button.grid(row=1, column=6, columnspan=2)

        self.sort_by_grade_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Grade"), command=lambda : self.__sort("grade"))
        self.sort_by_grade_button.grid(row=1, column=8, columnspan=2)

        self.sort_by_grade_point_button = ttk.Button(self.program_buttons_container, text=self._get_text("Sort by Grade Point"), command=lambda : self.__sort("grade_point"))
        self.sort_by_grade_point_button.grid(row=1, column=10, columnspan=2)

    def __filter(self) :    
        pass        

    def __update_course(self) :
        pass

    def __add_course(self) :
        pass

    def __remove_course(self) :
        pass

    def __sort(self, key) :
        pass