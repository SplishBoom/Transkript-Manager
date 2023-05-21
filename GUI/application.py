import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import filedialog
import os
from Environment import ASSETS_DC, SELENIUM_DC, to_turkish, connect_pathes
from Utilities import get_gender, generate_pdf
from PIL import Image, ImageTk
import random
from tkinter import messagebox
from tkinter import Toplevel
from datetime import datetime
from tkinter import filedialog

from GUI import AchievementAnalyzer, GradeUpdater, StatAnalyzer

class ApplicationFrame(ttk.Frame) :

    mef_logo_size = (98, 86)
    student_photo_size = (94, 94)
    arrow_size = (20, 20)

    def __init__(self, parent, root, DEBUG=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent
        self.DEBUG = DEBUG

        self.work_dir = os.getcwd()
        self.desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        self.__load_containers()

        self.current_user_info_document, self.current_user_data_document = self.root.get_current_data()
        self.__load_user_info()
        self.__load_user_data()

        if self.parsing_language == "en" :
            self.available_program_modes = ["Achievement Analyzer", "Grade Updater", "Stat Analyzer"]
            self.left_program_mode = tk.StringVar(value="Achievement Analyzer")
            self.current_program_mode = tk.StringVar(value="Grade Updater")
            self.right_program_mode = tk.StringVar(value="Stat Analyzer")
        else :
            self.available_program_modes = ["Başari Analizcisi", "Not Güncelleyici", "Istatistik Analizcisi"]
            self.left_program_mode = tk.StringVar(value="Başari Analizcisi")
            self.current_program_mode = tk.StringVar(value="Not Güncelleyici")
            self.right_program_mode = tk.StringVar(value="Istatistik Analizcisi")
        
        self.__load_user_info_label()
        self.__load_controller()
        self.__load_program_selection()
        self.__load_program()

    def _switch_program_mode(self, new_mode) :
                
        current_mode = self.current_program_mode.get()

        if current_mode == "Achievement Analyzer" or current_mode == "Başari Analizcisi" :
            self.achievement_analyzer_frame.grid_forget()
        elif current_mode == "Grade Updater" or current_mode == "Not Güncelleyici" :
            self.grade_updater_frame.grid_forget()
        elif current_mode == "Stat Analyzer" or current_mode == "Istatistik Analizcisi" :
            self.stat_analyzer_frame.grid_forget()

        if new_mode == "Achievement Analyzer" or new_mode == "Başari Analizcisi" :
            self.achievement_analyzer_frame.grid(row=0, column=0)
        elif new_mode == "Grade Updater" or new_mode == "Not Güncelleyici" :
            self.grade_updater_frame.grid(row=0, column=0)
        elif new_mode == "Stat Analyzer" or new_mode == "Istatistik Analizcisi" :
            self.stat_analyzer_frame.grid(row=0, column=0)

        self.current_program_mode.set(new_mode)
        self.left_program_mode.set(self.available_program_modes[(self.available_program_modes.index(new_mode) - 1) % len(self.available_program_modes)])
        self.right_program_mode.set(self.available_program_modes[(self.available_program_modes.index(new_mode) + 1) % len(self.available_program_modes)])

    def __load_user_info(self) :
        self.language_of_instruction : str = self.current_user_info_document["language_of_instruction"]
        self.student_department : str = self.current_user_info_document["student_department"]
        self.student_faculty : str = self.current_user_info_document["student_faculty"]
        self.student_name : str = self.current_user_info_document["student_name"]
        self.student_school_id : str = self.current_user_info_document["student_school_id"]
        self.student_national_id : str = self.current_user_info_document["_id"]
        self.student_status : str = self.current_user_info_document["student_status"]
        self.student_surname : str = self.current_user_info_document["student_surname"]
        
        self.student_gender = get_gender(name=self.student_name)

    def __load_user_data(self, use_specific=None) :
        if use_specific is None :
            use_case = self.current_user_data_document
        else :
            use_case = use_specific

        self.owner_id : str = use_case["owner_id"]
        self.parsing_type : str = use_case["parsing_type"]
        self.parsing_language : str = use_case["parsing_language"]
        self.transcript_manager_date : str = use_case["transcript_manager_date"]
        self.transcript_creation_date : str = use_case["transcript_creation_date"]
        self.semesters : dict = use_case["semesters"]
        self.original_course_list : list = use_case["original_course_list"]
        self.filtering : tuple = use_case["filtering"]
        self.sorting : tuple = use_case["sorting"]
        self.modified_course_list : list = use_case["modified_course_list"] or self.original_course_list
        self.document_name : str = use_case["document_name"]
        self.subtracted_course_list : list = use_case["subtracted_course_list"]
        self.added_course_list : list = use_case["added_course_list"]

    def update_user_data_from_grade_updater(self, updated_user_data) :
        self.__load_user_data(use_specific=updated_user_data)

    def _get_text(self, text) :
        if self.parsing_language == "tr" :
            return to_turkish[text]
        else :
            return text

    def __load_containers(self) :

        try :
            self.container.grid_forget()
        except :
            pass

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.container.grid_rowconfigure((0,1,2,3), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.user_info_label_container = ttk.Frame(self.container)
        self.user_info_label_container.grid(row=0, column=0)

        self.controllers_container = ttk.Frame(self.container)
        self.controllers_container.grid(row=1, column=0)

        self.program_selection_container = ttk.Frame(self.container)
        self.program_selection_container.grid(row=2, column=0)

        self.program_container = ttk.Frame(self.container)
        self.program_container.grid(row=3, column=0)

    def __load_user_info_label(self) :

        def ___change_user_photo(*args, **kwargs) :
            self.current_user_photo_path = random.choice(list(ASSETS_DC.GENDERS_PHOTO_PATH.values()))
            self.student_photo = ImageTk.PhotoImage(Image.open(self.current_user_photo_path).resize(self.student_photo_size, Image.ANTIALIAS))
            self.student_photo_label.configure(image=self.student_photo)

        self.user_info_label_container.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.user_info_label_container.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        self.logo_image = ImageTk.PhotoImage(Image.open(ASSETS_DC.LOGO_PATH).resize(self.mef_logo_size, Image.ANTIALIAS))
        mef_logo_label = ttk.Label(self.user_info_label_container, image=self.logo_image)
        mef_logo_label.grid(row=0, column=0, columnspan=4)

        self.document_name_label = ttk.Label(self.user_info_label_container, text=self.document_name)
        self.document_name_label.grid(row=0, column=4, columnspan=4)

        self.current_user_photo_path = ASSETS_DC.GENDERS_PHOTO_PATH[self.student_gender]
        self.student_photo = ImageTk.PhotoImage(Image.open(self.current_user_photo_path).resize(self.student_photo_size, Image.ANTIALIAS))
        self.student_photo_label = ttk.Label(self.user_info_label_container, image=self.student_photo)
        self.student_photo_label.grid(row=0, column=8, columnspan=4)
        self.student_photo_label.bind("<Button-1>", ___change_user_photo)

        student_id_label = ttk.Label(self.user_info_label_container, text=self._get_text("Student ID"))
        student_id_label.grid(row=1, column=0, columnspan=3)
        student_id_label_value = ttk.Label(self.user_info_label_container, text=self.student_school_id)
        student_id_label_value.grid(row=1, column=3, columnspan=3)

        national_id_label = ttk.Label(self.user_info_label_container, text=self._get_text("National ID"))
        national_id_label.grid(row=1, column=6, columnspan=3)
        national_id_label_value = ttk.Label(self.user_info_label_container, text=self.student_national_id)
        national_id_label_value.grid(row=1, column=9, columnspan=3)

        student_name_label = ttk.Label(self.user_info_label_container, text=self._get_text("Name"))
        student_name_label.grid(row=2, column=0, columnspan=3)
        student_name_label_value = ttk.Label(self.user_info_label_container, text=self.student_name)
        student_name_label_value.grid(row=2, column=3, columnspan=3)

        student_surname_label = ttk.Label(self.user_info_label_container, text=self._get_text("Surname"))
        student_surname_label.grid(row=2, column=6, columnspan=3)
        student_surname_label_value = ttk.Label(self.user_info_label_container, text=self.student_surname)
        student_surname_label_value.grid(row=2, column=9, columnspan=3)

        faculty_department_label = ttk.Label(self.user_info_label_container, text=self._get_text("Faculty / Department"))
        faculty_department_label.grid(row=3, column=0, columnspan=3)
        faculty_department_label_value = ttk.Label(self.user_info_label_container, text=self.student_faculty)
        faculty_department_label_value.grid(row=3, column=3, columnspan=3)

        program_name_label = ttk.Label(self.user_info_label_container, text=self._get_text("Program Name"))
        program_name_label.grid(row=3, column=6, columnspan=3)
        program_name_label_value = ttk.Label(self.user_info_label_container, text=self.student_department)
        program_name_label_value.grid(row=3, column=9, columnspan=3)

        language_of_instruction_label = ttk.Label(self.user_info_label_container, text=self._get_text("Language of Instruction"))
        language_of_instruction_label.grid(row=4, column=0, columnspan=3)
        language_of_instruction_label_value = ttk.Label(self.user_info_label_container, text=self.language_of_instruction)
        language_of_instruction_label_value.grid(row=4, column=3, columnspan=3)

        student_status_label = ttk.Label(self.user_info_label_container, text=self._get_text("Student Status"))
        student_status_label.grid(row=4, column=6, columnspan=3)
        student_status_label_value = ttk.Label(self.user_info_label_container, text=self.student_status)
        student_status_label_value.grid(row=4, column=9, columnspan=3)

    def __load_controller(self) :

        self.controllers_container.grid_rowconfigure((0), weight=1)
        self.controllers_container.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        self.load_db_data_button = ttk.Button(self.controllers_container, text=self._get_text("Load Data"), command=self.__load_db_data)
        self.load_db_data_button.grid(row=0, column=0)

        self.save_db_data_button = ttk.Button(self.controllers_container, text=self._get_text("Save Data"), command=self.__save_db_data)
        self.save_db_data_button.grid(row=0, column=1)

        self.exit_button = ttk.Button(self.controllers_container, text=self._get_text("Exit"), command=self.root.terminate)
        self.exit_button.grid(row=0, column=2)

        self.reset_button = ttk.Button(self.controllers_container, text=self._get_text("Reset"), command=self.__reset)
        self.reset_button.grid(row=0, column=3)

        self.restart_button = ttk.Button(self.controllers_container, text=self._get_text("Restart"), command=self.root._switch_to_login)
        self.restart_button.grid(row=0, column=4)

        self.export_button = ttk.Button(self.controllers_container, text=self._get_text("Export Data"), command=self.__export)
        self.export_button.grid(row=0, column=5)

    def __load_program_selection(self) :

        self.program_selection_container.grid_rowconfigure((0), weight=1)
        self.program_selection_container.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.left_arrow_photo_path = ASSETS_DC.LEFT_ARROW_PATH
        self.left_arrow_image = ImageTk.PhotoImage(Image.open(self.left_arrow_photo_path).resize(self.arrow_size, Image.ANTIALIAS))
        self.left_arrow_button = ttk.Button(self.program_selection_container, image=self.left_arrow_image, command=lambda : self.__change_mode_index("decrease"))
        self.left_arrow_button.grid(row=0, column=0)

        self.left_program_info_label = ttk.Label(self.program_selection_container, textvariable=self.left_program_mode, state="disabled")
        self.left_program_info_label.grid(row=0, column=1)

        self.current_program_info_label = ttk.Label(self.program_selection_container, textvariable=self.current_program_mode)
        self.current_program_info_label.grid(row=0, column=2)

        self.right_program_info_label = ttk.Label(self.program_selection_container, textvariable=self.right_program_mode, state="disabled")
        self.right_program_info_label.grid(row=0, column=3)

        self.right_arrow_photo_path = ASSETS_DC.RIGHT_ARROW_PATH
        self.right_arrow_image = ImageTk.PhotoImage(Image.open(self.right_arrow_photo_path).resize(self.arrow_size, Image.ANTIALIAS))
        self.right_arrow_button = ttk.Button(self.program_selection_container, image=self.right_arrow_image, command=lambda : self.__change_mode_index("increase"))
        self.right_arrow_button.grid(row=0, column=4)

    def __load_program(self) :

        self.program_container.grid_rowconfigure(0, weight=1)
        self.program_container.grid_columnconfigure(0, weight=1)

        self.grade_updater_frame = GradeUpdater(self.program_container, self, self.root, DEBUG=self.DEBUG, current_user_data_document=self.current_user_data_document)
        self.grade_updater_frame.grid(row=0, column=0)

        self.achievement_analyzer_frame = AchievementAnalyzer(self.program_container, self, self.root, DEBUG=self.DEBUG)

        self.stat_analyzer_frame = StatAnalyzer(self.program_container, self, self.root, DEBUG=self.DEBUG)

    def __load_db_data(self, *args, **kwargs) :
        
        self.load_db_data_button.config(text=self._get_text("Loading Data"), state="disabled")

        class DataLoader(Toplevel) :

            def __init__(self, master, options, parsing_language) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Load Data"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.options = options

                self.selected_option = tk.StringVar(self)

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

            def get_selected_option(self) :
                return self.selected_option.get()

            def create_widgets(self) :
                
                self.options_label = ttk.Label(self.container, text=self._get_text("Select a document to load"))
                self.options_label.grid(row=0, column=0, columnspan=2)

                self.options_combobox = ttk.Combobox(self.container, textvariable=self.selected_option, values=self.options)
                self.options_combobox.grid(row=1, column=0, columnspan=2)

                self.load_button = ttk.Button(self.container, text=self._get_text("Load"), command=self.__load)
                self.load_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.container, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

            def __load(self) :
                self.destroy()

            def __clean_exit(self) :
                self.selected_option.set("")
                self.destroy()

        expected_owner_id = self.student_national_id

        document_list = list(self.root.db_client.user_data.get_available_documents(expected_owner_id))

        if document_list == [] :
            messagebox.showerror(self._get_text("Error"), self._get_text("No data found for this user"))
            self.load_db_data_button.config(text=self._get_text("Load Data"), state="normal")
            return

        available_documents = {}
        for document in document_list :
            available_documents[document["document_name"]] = document

        options = list(available_documents.keys())

        data_loader = DataLoader(self.root, options, self.parsing_language)
        selected_option = data_loader.get_selected_option()

        if selected_option == "" :
            self.load_db_data_button.config(text=self._get_text("Load Data"), state="normal")
            return
        
        selected_user_data_document = available_documents[selected_option]
             
        self.root.set_current_data(user_data_document=selected_user_data_document)

        self.__load_user_data(use_specific=selected_user_data_document)

        self.__reset()

    def __save_db_data(self, *args, **kwargs) :

        self.save_db_data_button.config(text=self._get_text("Saving Data"), state="disabled")

        class DataSaver(Toplevel) :

            def __init__(self, master, existing_document_names, parsing_language) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Save Data"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.existing_document_names = existing_document_names
                self.new_document_name = tk.StringVar(self)

                self.container = ttk.Frame(self)
                self.container.grid(row=0, column=0)

                self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

                self.container.grid_rowconfigure((0), weight=1)
                self.container.grid_columnconfigure((0), weight=1)

                self.create_widgets()

                self.grab_set()
                self.focus_set()
                self.wait_window()

            def get_new_document_name(self) :
                return self.new_document_name.get()

            def _get_text(self, text) :
                if self.parsing_language == "tr" :
                    return to_turkish[text]
                else :
                    return text

            def create_widgets(self) :

                self.new_document_name_label = ttk.Label(self.container, text=self._get_text("Enter a name for the document"))
                self.new_document_name_label.grid(row=0, column=0, columnspan=2)

                self.new_document_name_entry = ttk.Entry(self.container, textvariable=self.new_document_name)
                self.new_document_name_entry.grid(row=1, column=0, columnspan=2)

                self.save_button = ttk.Button(self.container, text=self._get_text("Save"), command=self.__save)
                self.save_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.container, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

            def __save(self) :

                new_document_name = self.get_new_document_name()

                if new_document_name == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please enter a name for the document"))
                    return

                if new_document_name in self.existing_document_names :
                    messagebox.showerror(self._get_text("Error"), self._get_text("A document with this name already exists"))
                    return

                self.destroy()

            def __clean_exit(self) :
                self.new_document_name.set("")
                self.destroy()

        expected_owner_id = self.student_national_id

        document_list = list(self.root.db_client.user_data.get_available_documents(expected_owner_id))

        existing_document_names = []
        for document in document_list :
            existing_document_names.append(document["document_name"])

        data_saver = DataSaver(self.root, existing_document_names, self.parsing_language)
        new_document_name = data_saver.get_new_document_name()

        if new_document_name == "" :
            self.save_db_data_button.config(text=self._get_text("Save Data"), state="normal")
            return
        
        self.document_name = new_document_name

        new_user_data_document = {
            "owner_id" : self.owner_id,
            "parsing_type" : self.parsing_type,
            "parsing_language" : self.parsing_language,
            "transcript_manager_date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
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

        self.root.db_client.user_data.push_init(new_user_data_document)

        self.save_db_data_button.config(text=self._get_text("Save Data"), state="normal")

    def __reset(self, *args, **kwargs) :
        
        self.reset_button.config(text=self._get_text("Resetting"), state="disabled")
        
        self.root.restart_application()
    
    def __export(self, *args, **kwargs) :

        self.export_button.config(text=self._get_text("Exporting Data"), state="disabled")

        if not self.DEBUG :
            output_file_folder = filedialog.askdirectory(initialdir = self.work_dir, title = self._get_text("Select Output Folder"))
        else :
            output_file_folder = filedialog.askdirectory(initialdir = self.desktop_path, title = self._get_text("Select Output Folder"))

        if output_file_folder is not None and output_file_folder != "" and output_file_folder != " " :
            output_file_path = connect_pathes(output_file_folder, self.document_name + ".pdf")

            generate_pdf(
                user_info_document = self.current_user_info_document, 
                user_data_document = self.current_user_data_document, 
                user_photo_path = self.current_user_photo_path,
                output_file_path = output_file_path
            )

        self.export_button.config(text=self._get_text("Export Data"), state="normal")
            
    def __change_mode_index(self, operation, *args, **kwargs) :
        
        current_mode = self.current_program_mode.get()
        current_modes_index = self.available_program_modes.index(current_mode)

        if operation == "increase" :
            if current_modes_index == len(self.available_program_modes) - 1 :
                new_mode_index = 0
            else :
                new_mode_index = current_modes_index + 1
        elif operation == "decrease" :
            if current_modes_index == 0 :
                new_mode_index = len(self.available_program_modes) - 1
            else :
                new_mode_index = current_modes_index - 1
        else :
            raise Exception("Invalid Operation")
        
        new_mode = self.available_program_modes[new_mode_index]
        
        self._switch_program_mode(new_mode)
