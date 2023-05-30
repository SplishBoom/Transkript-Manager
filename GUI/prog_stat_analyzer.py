import tkinter as tk
from Utilities import calculate_performance
from tkinter import ttk

class StatAnalyzer(ttk.Frame) :

    def __init__(self, application_container, parent, root, current_user_data, DEBUG=False, *args, **kwargs):
        super().__init__(application_container, *args, **kwargs)

        self.root = root
        self.parent = parent
        self.application_container = application_container
        self.DEBUG = DEBUG
        
        self.__load_user_data(current_user_data)

        self.__load_containers()

        self.__load_scholarship_status()
        self.__load_course_info_status()

    def _get_text(self, text) :
        return self.parent._get_text(text, self.parsing_language)

    def __load_containers(self) :

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.container.grid_rowconfigure((0,1), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        self.program_scholarship_status_container = ttk.Frame(self.container)
        self.program_scholarship_status_container.grid(row=0, column=0)

        self.program_course_info_status_container = ttk.Frame(self.container)
        self.program_course_info_status_container.grid(row=1, column=0)

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
        self.updated_course_list : list = use_case["updated_course_list"]
        self.subtracted_course_list : list = use_case["subtracted_course_list"]
        self.added_course_list : list = use_case["added_course_list"]

        self.___update_semester_data()

    def ___update_semester_data(self) :

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

        last_semester_id = f"semester_{len(self.semesters)}"
        self.semesters[last_semester_id]["course_list"].extend(self.added_course_list)

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

    def ___create_scholarship_status_data(self):

        course_list = []
        for semester in self.semesters :
            course_list.extend(self.semesters[semester]["course_list"])

        performance = calculate_performance(course_list, skip_retakens=True)
        credits_attempted = performance["credits_attempted"]
        credits_successful = performance["credits_successful"]
        credits_included_in_gpa = performance["credits_included_in_gpa"]
        gpa = performance["gpa"]

        expected_credits = len(self.semesters) * 30

        if credits_attempted < expected_credits:
            self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship.", "note":"You haven't taken enough courses to apply for scholarship"}
        if credits_included_in_gpa < expected_credits:
            self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship.", "note":"You haven't completed enough credits for scholarship"}
        else :
            if 3.75 <= gpa <= 4 :
                self.scholarship_status = {"percentage":50, "message":"You are eligible for a %50 scholarship.", "note":"You have a perfect GPA for scholarship"}
            elif 3.60 <= gpa < 3.75 :
                self.scholarship_status = {"percentage":40, "message":"You are eligible for a %40 scholarship.", "note":"You have a high GPA for scholarship"}
            elif 3.50 <= gpa < 3.60 :
                self.scholarship_status = {"percentage":25, "message":"You are eligible for a %25 scholarship.", "note":"You have a nice GPA for scholarship"}
            elif 3.00 <= gpa < 3.50 :
                self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship.", "note":"You have a good GPA for scholarship"}
            elif 2.00 <= gpa < 3.00 :
                self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship.", "note":"You have a low GPA for scholarship"}
            elif 0 <= gpa < 2.00 :
                self.scholarship_status = {"percentage":0, "message":"You are not eligible for a scholarship.", "note":"You have a very low GPA for scholarship"}
                
    def ___create_course_info_status_data(self) :
        
        course_list = []
        for semester in self.semesters :
            for course in self.semesters[semester]["course_list"]:
                course_code = course["course_code"]
                if not course_code.endswith("*") :
                    course_list.append(course)

        all_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W", "S", "N/A"]

        grades_must_taken_list = ["F", "W"]
        grades_should_taken_list = ["B-", "C+", "C", "C-", "D+", "D"]

        self.grades_must_taken = []
        self.grades_should_taken = []

        for course in course_list :
            course_grade = course["course_grade"]
            if course_grade in grades_must_taken_list :
                self.grades_must_taken.append(course)
            elif course_grade in grades_should_taken_list :
                self.grades_should_taken.append(course)

    def __load_scholarship_status(self) :
        
        self.___create_scholarship_status_data()

        self.program_scholarship_status_container.grid_rowconfigure((0,1), weight=1)
        self.program_scholarship_status_container.grid_columnconfigure(0, weight=1)

        self.scholarship_status_label = ttk.Label(self.program_scholarship_status_container, text=self._get_text("Scholarship Status"))
        self.scholarship_status_label.grid(row=0, column=0)

        self.scholarship_status_treeview = ttk.Treeview(self.program_scholarship_status_container, height=1, show="headings", selectmode="none")
        self.scholarship_status_treeview.grid(row=1, column=0)

        self.scholarship_status_treeview["columns"] = ("_percentage", "_message", "_note")

        self.scholarship_status_treeview.heading("_percentage", text=self._get_text("Percentage"))
        self.scholarship_status_treeview.heading("_message", text=self._get_text("Message"))
        self.scholarship_status_treeview.heading("_note", text=self._get_text("Footnote"))

        self.scholarship_status_treeview.column("_percentage", anchor="center", width=90)
        self.scholarship_status_treeview.column("_message", anchor="center", width=250)
        self.scholarship_status_treeview.column("_note", anchor="center", width=250)

        self.scholarship_status_treeview.insert("", "end", values=(self.scholarship_status["percentage"], self.scholarship_status["message"], self.scholarship_status["note"]))

    def __load_course_info_status(self):

        self.___create_course_info_status_data()

        self.program_course_info_status_container.grid_rowconfigure((0,1,2,3), weight=1)
        self.program_course_info_status_container.grid_columnconfigure(0, weight=1)

        self.course_info_status_treeview_MUST_TAKEN()
        self.course_info_status_treeview_SHOULD_TAKEN()

    def course_info_status_treeview_MUST_TAKEN(self) :
        
        self.course_info_status_treeview_MUST_TAKEN_info_label = tk.Label(self.program_course_info_status_container, text=self._get_text("Courses Must Taken Again"))
        self.course_info_status_treeview_MUST_TAKEN_info_label.grid(row=0, column=0)

        maximum_height = 5
        self.course_info_status_treeview_MUST_TAKEN = ttk.Treeview(self.program_course_info_status_container, height=min(len(self.grades_must_taken), maximum_height), show="headings", selectmode="none")
        self.course_info_status_treeview_MUST_TAKEN.grid(row=1, column=0)

        if self.grades_must_taken == [] :
            self.course_info_status_treeview_MUST_TAKEN["columns"] = ("_column")

            self.course_info_status_treeview_MUST_TAKEN.heading("_column", text=self._get_text("No Course Must Taken Again"))
            self.course_info_status_treeview_MUST_TAKEN.column("_column", anchor="center", width=720)
        else :
            self.course_info_status_treeview_MUST_TAKEN["columns"] = ("_code", "_name", "_canguage", "_credit", "_crade", "_crade_point")

            self.course_info_status_treeview_MUST_TAKEN.heading("_code", text=self._get_text("Course Code"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_name", text=self._get_text("Course Name"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_canguage", text=self._get_text("Course Language"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_credit", text=self._get_text("Course Credit"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_crade", text=self._get_text("Course Grade"))
            self.course_info_status_treeview_MUST_TAKEN.heading("_crade_point", text=self._get_text("Course Grade Point"))

            self.course_info_status_treeview_MUST_TAKEN.column("_code", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_name", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_canguage", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_credit", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_crade", anchor="center", width=120)
            self.course_info_status_treeview_MUST_TAKEN.column("_crade_point", anchor="center", width=120)

        if not self.grades_must_taken == [] :
            for course in self.grades_must_taken :
                self.course_info_status_treeview_MUST_TAKEN.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]))

    def course_info_status_treeview_SHOULD_TAKEN(self) :

        self.course_info_status_treeview_SHOULD_TAKEN_info_label = tk.Label(self.program_course_info_status_container, text=self._get_text("Courses Should Taken Again"))
        self.course_info_status_treeview_SHOULD_TAKEN_info_label.grid(row=2, column=0)

        maximum_height = 5
        self.course_info_status_treeview_SHOULD_TAKEN = ttk.Treeview(self.program_course_info_status_container, height=min(len(self.grades_should_taken), maximum_height), show="headings", selectmode="none")
        self.course_info_status_treeview_SHOULD_TAKEN.grid(row=3, column=0)

        if self.grades_should_taken == [] :
            self.course_info_status_treeview_SHOULD_TAKEN["columns"] = ("_column")

            self.course_info_status_treeview_SHOULD_TAKEN.heading("_column", text=self._get_text("No Course Should Taken Again"))
            self.course_info_status_treeview_SHOULD_TAKEN.column("_column", anchor="center", width=720)
        else :
            self.course_info_status_treeview_SHOULD_TAKEN["columns"] = ("_code", "_name", "_canguage", "_credit", "_crade", "_crade_point")

            self.course_info_status_treeview_SHOULD_TAKEN.heading("_code", text=self._get_text("Course Code"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_name", text=self._get_text("Course Name"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_canguage", text=self._get_text("Course Language"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_credit", text=self._get_text("Course Credit"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_crade", text=self._get_text("Course Grade"))
            self.course_info_status_treeview_SHOULD_TAKEN.heading("_crade_point", text=self._get_text("Course Grade Point"))

            self.course_info_status_treeview_SHOULD_TAKEN.column("_code", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_name", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_canguage", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_credit", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_crade", anchor="center", width=120)
            self.course_info_status_treeview_SHOULD_TAKEN.column("_crade_point", anchor="center", width=120)

        if not self.grades_should_taken == [] :
            for course in self.grades_should_taken :
                self.course_info_status_treeview_SHOULD_TAKEN.insert("", "end", values=(course["course_code"], course["course_name"], course["course_lang"], course["course_credit"], course["course_grade"], course["course_grade_point"]))