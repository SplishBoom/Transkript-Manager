import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.colors as mcolors
from Utilities import calculate_performance, generate_gradient_colors

class AchievementAnalyzer(ttk.Frame) :

    def __init__(self, application_container, parent, root, current_user_data, DEBUG=False, *args, **kwargs):
        super().__init__(application_container, *args, **kwargs)

        self.root = root
        self.parent = parent
        self.application_container = application_container
        self.DEBUG = DEBUG
        
        self.__load_user_data(current_user_data)

        self.__load_containers()

        self.__load_program_plot()

    def __load_containers(self) :

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        self.program_plot_container = ttk.Frame(self.container)
        self.program_plot_container.grid(row=0, column=0)

    def __load_user_data(self, use_case) :
        
        self.owner_id : str = use_case["owner_id"]
        self.parsing_type : str = use_case["parsing_type"]
        self.parsing_language : str = use_case["parsing_language"]
        self.transcript_manager_date : str = use_case["transcript_manager_date"]
        self.transcript_creation_date : str = use_case["transcript_creation_date"]
        self.semesters : dict = use_case["semesters"].copy()
        self.original_course_list : list = use_case["original_course_list"].copy()
        self.filtering : tuple = use_case["filtering"].copy()
        self.sorting : tuple = use_case["sorting"].copy()
        self.modified_course_list : list = use_case["modified_course_list"].copy()
        self.document_name : str = use_case["document_name"]
        self.updated_course_list : list = use_case["updated_course_list"].copy()
        self.subtracted_course_list : list = use_case["subtracted_course_list"].copy()
        self.added_course_list : list = use_case["added_course_list"].copy()

    def ___create_course_based_plot_data(self):

        self.all_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", "I", "W", "S", "N/A"]
        
        self.course_based_plot_data = {
            "course_grade" : [],
            "course_index" : [],
            "course_code" : []
        }

        for course_index, course in enumerate(self.modified_course_list):
            course_grade = course["course_grade"]
            course_index = course_index + 1
            course_code = course["course_code"]

            # Update course_grade to its corresponding index in reversed all_grades
            reversed_index = len(self.all_grades) - self.all_grades.index(course_grade) - 1
            self.course_based_plot_data["course_grade"].append(reversed_index)
            self.course_based_plot_data["course_index"].append(course_index)
            self.course_based_plot_data["course_code"].append(course_code)
            
    def ___create_semester_based_plot_data(self) :

        self.semester_based_plot_data = {
            "semester_grade" : [],
            "semester_index" : [],
            "semester_name" : []
        }

        dummy_semester = {
            "semester_definition" : "Temp Semester",
            "course_list" : self.added_course_list.copy()
        }
        if dummy_semester["course_list"] != [] :
            self.semesters["Temp Semester"] = dummy_semester

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
          
        for semester_index, semester in enumerate(self.semesters) :

            current_semester = self.semesters[semester]
            current_course_list = current_semester["course_list"]

            semester_performance = calculate_performance(current_course_list)
            semester_grade = semester_performance["gpa"]
            semester_index = semester_index + 1
            semester_name = " ".join(current_semester["semester_definition"].split(" ")[0:2])

            self.semester_based_plot_data["semester_grade"].append(semester_grade)
            self.semester_based_plot_data["semester_index"].append(semester_index)
            self.semester_based_plot_data["semester_name"].append(semester_name)

    def __load_program_plot(self) :

        self.program_plot_container.grid_rowconfigure((0), weight=1)
        self.program_plot_container.grid_columnconfigure((0,1), weight=1)

        self.___create_semester_based_plot_data()
        self.___load_semester_based_plot()

        self.___create_course_based_plot_data()
        self.___load_course_based_plot()

    def ___load_semester_based_plot(self):

        self.semester_based_plot_container = ttk.Frame(self.program_plot_container)
        self.semester_based_plot_container.grid(row=0, column=0, sticky="nsew")
        self.sbp_packable_frame = ttk.Frame(self.semester_based_plot_container)
        self.sbp_packable_frame.pack(fill="both", expand=True)

        self.semester_based_plot_figure = Figure(figsize=(5, 5), dpi=100)
        self.semester_based_plot_figure.subplots_adjust(left=0.12, right=0.97, bottom=0.135, top=0.93)
        self.semester_based_plot_figure.patch.set_facecolor("#F0F0F0")
        self.semester_based_plot_figure.patch.set_alpha(0.5)

        self.semester_based_plot = self.semester_based_plot_figure.add_subplot(111)
        self.semester_based_plot.set_title("Semester Based Performance")
        self.semester_based_plot.set_ylabel("Grade Point Average")
        self.semester_based_plot.set_facecolor("#F0F0F0")
        self.semester_based_plot.grid(color="#FFFFFF", linestyle="-", linewidth=1)
        self.semester_based_plot.set_axisbelow(True)

        num_colors = len(self.semester_based_plot_data["semester_grade"])
        gradient_colors = generate_gradient_colors(num_colors)

        self.semester_based_plot.bar(
            self.semester_based_plot_data["semester_index"], 
            self.semester_based_plot_data["semester_grade"], 
            color=gradient_colors, 
            edgecolor="black"
        )

        self.semester_based_plot.set_xlim(0, len(self.semester_based_plot_data["semester_index"]) + 1)
        self.semester_based_plot.set_ylim(0, 4.0)

        self.semester_based_plot.set_xticks(self.semester_based_plot_data["semester_index"])
        self.semester_based_plot.set_xticklabels(labels=self.semester_based_plot_data["semester_name"], rotation=25, ha="right", fontsize=8)

        self.semester_based_plot_canvas = FigureCanvasTkAgg(self.semester_based_plot_figure, self.sbp_packable_frame)
        self.semester_based_plot_canvas.draw()
        self.semester_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.semester_based_plot_toolbar = NavigationToolbar2Tk(self.semester_based_plot_canvas, self.sbp_packable_frame)
        self.semester_based_plot_toolbar.update()
        self.semester_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)
     
    def ___load_course_based_plot(self):
        self.course_based_plot_container = ttk.Frame(self.program_plot_container)
        self.course_based_plot_container.grid(row=0, column=1, sticky="nsew")
        self.cbp_packable_frame = ttk.Frame(self.course_based_plot_container)
        self.cbp_packable_frame.pack(fill="both", expand=True)

        self.course_based_plot_figure = Figure(figsize=(5, 5), dpi=100)
        self.course_based_plot_figure.subplots_adjust(left=0.12, right=0.97, bottom=0.135, top=0.93)
        self.course_based_plot_figure.patch.set_facecolor("#F0F0F0")
        self.course_based_plot_figure.patch.set_alpha(0.5)

        self.course_based_plot = self.course_based_plot_figure.add_subplot(111)
        self.course_based_plot.set_title("Course Based Performance")
        self.course_based_plot.set_ylabel("Grade Notation")
        self.course_based_plot.set_facecolor("#F0F0F0")
        self.course_based_plot.grid(color="#FFFFFF", linestyle="-", linewidth=1)
        self.course_based_plot.set_axisbelow(True)

        num_colors = len(self.course_based_plot_data["course_grade"])
        gradient_colors = generate_gradient_colors(num_colors)

        self.course_based_plot.scatter(
            self.course_based_plot_data["course_index"],
            self.course_based_plot_data["course_grade"], 
            color=gradient_colors, 
            edgecolor="black"
        )

        x_padding = 1
        self.course_based_plot.set_xlim(
            0.5 - x_padding, 
            len(self.course_based_plot_data["course_index"]) + 0.5 + x_padding
        )
        self.course_based_plot.set_xticks(self.course_based_plot_data["course_index"])
        self.course_based_plot.set_xticklabels(labels=self.course_based_plot_data["course_code"], rotation=55, ha="right", fontsize=6)
        
        all_grade_indices = list(reversed(range(len(self.all_grades))))
        self.course_based_plot.set_yticks(all_grade_indices)
        self.course_based_plot.set_yticklabels(self.all_grades)

        self.course_based_plot_canvas = FigureCanvasTkAgg(self.course_based_plot_figure, self.cbp_packable_frame)
        self.course_based_plot_canvas.draw()
        self.course_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.course_based_plot_toolbar = NavigationToolbar2Tk(self.course_based_plot_canvas, self.cbp_packable_frame)
        self.course_based_plot_toolbar.update()
        self.course_based_plot_canvas.get_tk_widget().pack(fill="both", expand=True)
