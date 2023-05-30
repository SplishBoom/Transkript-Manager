import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import PhotoImage
import os
from Environment import ASSETS_DC, SELENIUM_DC, connect_pathes, to_turkish
from Utilities import UserVerifier, get_gender, generate_pdf, translate_text, authenticate, get_gif_frame_count
from rembg import remove as remove_background
import threading
import random
from tkinter import messagebox
from tkinter import Toplevel
from datetime import datetime
from tkinter import filedialog
import threading
import copy
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

        current_user_info_document, current_user_data_document = self.root.get_current_data()
        self.__load_user_data(current_user_data_document)
        self.__load_user_info(current_user_info_document)
        self.__update_user_authitication()

        if self.parsing_language == "en" :
            self.available_program_modes = ["Stat Analyzer", "Grade Updater", "Achievement Analyzer"]
            self.left_program_mode = tk.StringVar(value="Stat Analyzer")
            self.current_program_mode = tk.StringVar(value="Grade Updater")
            self.right_program_mode = tk.StringVar(value="Achievement Analyzer")
        else :
            self.available_program_modes = ["Istatistik Analizcisi", "Not Güncelleyici", "Başari Analizcisi"]
            self.left_program_mode = tk.StringVar(value="Istatistik Analizcisi")
            self.current_program_mode = tk.StringVar(value="Not Güncelleyici")
            self.right_program_mode = tk.StringVar(value="Başari Analizcisi")
        
        self.__load_user_info_label()
        self.__load_controller()
        self.__load_program_selection()
        self.__load_program()

    def __update_user_authitication(self) :
        self.is_user_authenticated = self.root.get_authication_status()

    def _switch_program_mode(self, new_mode) :
                
        current_mode = self.current_program_mode.get()

        current_user_data = self.__create_user_data()

        if current_mode == "Stat Analyzer" or current_mode == "Istatistik Analizcisi" :
            self.stat_analyzer_frame.grid_forget()
            self.stat_analyzer_frame = None
        elif current_mode == "Grade Updater" or current_mode == "Not Güncelleyici" :
            self.grade_updater_frame.grid_forget()
        elif current_mode == "Achievement Analyzer" or current_mode == "Başari Analizcisi" :
            self.achievement_analyzer_frame.grid_forget()
            self.achievement_analyzer_frame = None

        if new_mode == "Stat Analyzer" or new_mode == "Istatistik Analizcisi" :
            self.stat_analyzer_frame = StatAnalyzer(self.program_container, self, self.root, current_user_data, DEBUG=self.DEBUG)
            self.stat_analyzer_frame.grid(row=0, column=0)
        elif new_mode == "Grade Updater" or new_mode == "Not Güncelleyici" :
            self.grade_updater_frame.grid(row=0, column=0)
        elif new_mode == "Achievement Analyzer" or new_mode == "Başari Analizcisi" :
            self.achievement_analyzer_frame = AchievementAnalyzer(self.program_container, self, self.root, current_user_data, DEBUG=self.DEBUG)
            self.achievement_analyzer_frame.grid(row=0, column=0)

        self.current_program_mode.set(new_mode)
        self.left_program_mode.set(self.available_program_modes[(self.available_program_modes.index(new_mode) - 1) % len(self.available_program_modes)])
        self.right_program_mode.set(self.available_program_modes[(self.available_program_modes.index(new_mode) + 1) % len(self.available_program_modes)])

    def update_user_data(self, new_user_data) :

        self.__load_user_data(new_user_data)

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

    def __create_user_data(self) :

        new_document = {
            "owner_id" : self.owner_id,
            "parsing_type" : self.parsing_type,
            "parsing_language" : self.parsing_language,
            "transcript_manager_date" : self.transcript_manager_date,
            "transcript_creation_date" : self.transcript_creation_date,
            "semesters" : copy.deepcopy(self.semesters),
            "original_course_list" : copy.deepcopy(self.original_course_list),
            "filtering" : copy.deepcopy(self.filtering),
            "sorting" : copy.deepcopy(self.sorting),
            "modified_course_list" : copy.deepcopy(self.modified_course_list),
            "document_name" : self.document_name,
            "updated_course_list" : copy.deepcopy(self.updated_course_list),
            "subtracted_course_list" : copy.deepcopy(self.subtracted_course_list),
            "added_course_list" : copy.deepcopy(self.added_course_list)
        }
        return new_document

    def __load_user_info(self, use_case) :
        
        self.language_of_instruction : str = use_case["language_of_instruction"]
        self.student_department : str = use_case["student_department"]
        self.student_faculty : str = use_case["student_faculty"]
        self.student_name : str = use_case["student_name"]
        self.student_school_id : str = use_case["student_school_id"]
        self.student_national_id : str = use_case["_id"]
        self.student_status : str = use_case["student_status"]
        self.student_surname : str = use_case["student_surname"]
        
        if self.parsing_language == "tr" :
            self.student_faculty = translate_text(self.student_faculty)
            self.student_department = translate_text(self.student_department)
            self.student_status = translate_text(self.student_status)
            self.language_of_instruction = translate_text(self.language_of_instruction)
        if self.parsing_language == "en" :
            self.student_faculty = translate_text(self.student_faculty, "tr", "en")
            self.student_department = translate_text(self.student_department, "tr", "en")
            self.student_status = translate_text(self.student_status, "tr", "en")
            self.language_of_instruction = translate_text(self.language_of_instruction, "tr", "en")

        self.student_gender = get_gender(name=self.student_name)

    def __create_user_info(self) :

        new_document = {
            "_id" : self.student_national_id,
            "student_name" : self.student_name,
            "student_surname" : self.student_surname,
            "student_school_id" : self.student_school_id,
            "student_department" : self.student_department,
            "student_faculty" : self.student_faculty,
            "student_status" : self.student_status,
            "language_of_instruction" : self.language_of_instruction
        }
        return new_document

    def _get_text(self, text, parsing_language=None) :
        return self.root.get_text(text, parsing_language or self.parsing_language)

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

            available_photo_list = list(ASSETS_DC.GENDERS_PHOTO_PATH.values())

            index_of_current_photo = available_photo_list.index(self.current_user_photo_path)
            index_of_next_photo = (index_of_current_photo + 1) % len(available_photo_list)

            self.current_user_photo_path = available_photo_list[index_of_next_photo]
            self.student_photo = ImageTk.PhotoImage(Image.open(self.current_user_photo_path).resize(self.student_photo_size, Image.ANTIALIAS))
            self.student_photo_label.configure(image=self.student_photo)
            self.student_photo_label.image = self.student_photo

        def __load_original_photo() :

            def job() :
                self.student_photo_label.unbind("<Button-1>")
                self.current_user_photo_path = SELENIUM_DC.USER_PHOTO_OUTPUT_PATH
                self.student_photo = ImageTk.PhotoImage(remove_background(Image.open(self.current_user_photo_path).resize(self.student_photo_size, Image.ANTIALIAS), alpha_matting=True))
                self.student_photo_label.configure(image=self.student_photo)
                self.student_photo_label.image = self.student_photo

            threading.Thread(target=job).start()

        self.user_info_label_container.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.user_info_label_container.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        self.logo_image = ImageTk.PhotoImage(Image.open(ASSETS_DC.LOGO_PATH).resize(self.mef_logo_size, Image.ANTIALIAS))
        mef_logo_label = ttk.Label(self.user_info_label_container, image=self.logo_image)
        mef_logo_label.grid(row=0, column=0, columnspan=4, rowspan=2)

        self.document_name_label = ttk.Label(self.user_info_label_container, text=self.document_name)
        self.document_name_label.grid(row=0, column=4, columnspan=4)

        self.document_date_label = ttk.Label(self.user_info_label_container, text=self.transcript_creation_date)
        self.document_date_label.grid(row=1, column=4, columnspan=4)

        self.current_user_photo_path = ASSETS_DC.GENDERS_PHOTO_PATH[self.student_gender]
        self.student_photo = ImageTk.PhotoImage(Image.open(self.current_user_photo_path).resize(self.student_photo_size, Image.ANTIALIAS))
        self.student_photo_label = ttk.Label(self.user_info_label_container, image=self.student_photo)
        self.student_photo_label.grid(row=0, column=8, columnspan=4, rowspan=2)
        self.student_photo_label.bind("<Button-1>", ___change_user_photo)
        if os.path.exists(SELENIUM_DC.USER_PHOTO_OUTPUT_PATH) :
            __load_original_photo()

        student_id_label = ttk.Label(self.user_info_label_container, text=self._get_text("Student ID"))
        student_id_label.grid(row=2, column=0, columnspan=3)
        student_id_label_value = ttk.Label(self.user_info_label_container, text=self.student_school_id)
        student_id_label_value.grid(row=2, column=3, columnspan=3)

        national_id_label = ttk.Label(self.user_info_label_container, text=self._get_text("National ID"))
        national_id_label.grid(row=2, column=6, columnspan=3)
        national_id_label_value = ttk.Label(self.user_info_label_container, text=self.student_national_id)
        national_id_label_value.grid(row=2, column=9, columnspan=3)

        student_name_label = ttk.Label(self.user_info_label_container, text=self._get_text("Name"))
        student_name_label.grid(row=3, column=0, columnspan=3)
        student_name_label_value = ttk.Label(self.user_info_label_container, text=self.student_name)
        student_name_label_value.grid(row=3, column=3, columnspan=3)

        student_surname_label = ttk.Label(self.user_info_label_container, text=self._get_text("Surname"))
        student_surname_label.grid(row=3, column=6, columnspan=3)
        student_surname_label_value = ttk.Label(self.user_info_label_container, text=self.student_surname)
        student_surname_label_value.grid(row=3, column=9, columnspan=3)

        faculty_department_label = ttk.Label(self.user_info_label_container, text=self._get_text("Faculty / Department"))
        faculty_department_label.grid(row=4, column=0, columnspan=3)
        faculty_department_label_value = ttk.Label(self.user_info_label_container, text=self.student_faculty)
        faculty_department_label_value.grid(row=4, column=3, columnspan=3)

        program_name_label = ttk.Label(self.user_info_label_container, text=self._get_text("Program Name"))
        program_name_label.grid(row=4, column=6, columnspan=3)
        program_name_label_value = ttk.Label(self.user_info_label_container, text=self.student_department)
        program_name_label_value.grid(row=4, column=9, columnspan=3)

        language_of_instruction_label = ttk.Label(self.user_info_label_container, text=self._get_text("Language of Instruction"))
        language_of_instruction_label.grid(row=5, column=0, columnspan=3)
        language_of_instruction_label_value = ttk.Label(self.user_info_label_container, text=self.language_of_instruction)
        language_of_instruction_label_value.grid(row=5, column=3, columnspan=3)

        student_status_label = ttk.Label(self.user_info_label_container, text=self._get_text("Student Status"))
        student_status_label.grid(row=5, column=6, columnspan=3)
        student_status_label_value = ttk.Label(self.user_info_label_container, text=self.student_status)
        student_status_label_value.grid(row=5, column=9, columnspan=3)

    def __load_controller(self) :

        self.controllers_container.grid_rowconfigure((0), weight=1)
        self.controllers_container.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        self.load_db_data_button = ttk.Button(self.controllers_container, text=self._get_text("Load Data"), command=self.__load_db_data)
        self.load_db_data_button.grid(row=0, column=0)

        self.save_db_data_button = ttk.Button(self.controllers_container, text=self._get_text("Save Data"), command=self.__save_db_data)
        self.save_db_data_button.grid(row=0, column=1)

        self.exit_button = ttk.Button(self.controllers_container, text=self._get_text("Exit"), command=self.root.terminate)
        self.exit_button.grid(row=0, column=2)

        self.reset_button = ttk.Button(self.controllers_container, text=self._get_text("Refresh"), command=self.__reset)
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

        current_user_data = self.__create_user_data()

        self.grade_updater_frame = GradeUpdater(self.program_container, self, self.root, current_user_data, DEBUG=self.DEBUG)
        self.grade_updater_frame.grid(row=0, column=0)

        self.achievement_analyzer_frame = None
        
        self.stat_analyzer_frame = None

    def __load_db_data(self, *args, **kwargs) :
        
        self.load_db_data_button.config(text=self._get_text("Loading Data"), state="disabled")

        self.__check_authentication()

        if not self.is_user_authenticated :
            self.load_db_data_button.config(text=self._get_text("Load Data"), state="enabled")
            return

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

                selected_option = self.selected_option.get()

                if selected_option == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Please select a document"))
                    return
                
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

        self.__load_user_data(selected_user_data_document)

        self.__reset()

    def __save_db_data(self, *args, **kwargs) :

        self.save_db_data_button.config(text=self._get_text("Saving Data"), state="disabled")

        self.__check_authentication()

        if not self.is_user_authenticated :
            self.save_db_data_button.config(text=self._get_text("Save Data"), state="enabled")
            return

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
                
                if new_document_name == "Untitled Document" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("This name is reserved, please enter another name"))
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
            "updated_course_list" : self.updated_course_list,
            "subtracted_course_list" : self.subtracted_course_list,
            "added_course_list" : self.added_course_list
        }

        user_info_document = self.__create_user_info()

        self.root.db_client.user_info.push_init(user_info_document)
        self.root.db_client.user_data.push_init(new_user_data_document)

        self.root.set_current_data(user_info_document, new_user_data_document)

        self.save_db_data_button.config(text=self._get_text("Save Data"), state="normal")

        self.__reset()

    def __reset(self, *args, **kwargs) :
        
        self.reset_button.config(text=self._get_text("Refreshing"), state="disabled")
        
        self.root.restart_application()
    
    def __export(self, *args, **kwargs) :

        self.export_button.config(text=self._get_text("Exporting Data"), state="disabled")

        if not self.DEBUG :
            output_file_folder = filedialog.askdirectory(initialdir = self.work_dir, title = self._get_text("Select Output Folder"))
        else :
            output_file_folder = filedialog.askdirectory(initialdir = self.desktop_path, title = self._get_text("Select Output Folder"))

        if output_file_folder is not None and output_file_folder != "" and output_file_folder != " " :
            output_file_path = connect_pathes(output_file_folder, self.document_name + ".pdf")

            current_user_info_document = self.__create_user_info()
            current_user_data_document = self.__create_user_data()

            generate_pdf(
                user_info_document = current_user_info_document, 
                user_data_document = current_user_data_document, 
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

    def __check_authentication(self) :

        if self.is_user_authenticated == True :
            return True

        class Verifier(tk.Toplevel) :

            def __init__(self, master, match_id, parsing_language) :
                super().__init__(master)

                self.parsing_language = parsing_language

                self.title(self._get_text("Unauthorized Access Verification"))
                self.iconbitmap(ASSETS_DC.ICON)

                self.match_id = match_id
                self.result = False

                self.container = ttk.Frame(self)
                self.container.grid(row=0, column=0)

                self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

                self.container.grid_rowconfigure((0), weight=1)
                self.container.grid_columnconfigure((0), weight=1)

                self.create_widgets()

                self.grab_set()
                self.focus_set()
                self.wait_window()

            def create_widgets(self) :

                self.widgets_container = ttk.Frame(self.container)
                self.widgets_container.grid(row=0, column=0)

                self.widgets_container.grid_rowconfigure((0, 1, 2, 3), weight=1)
                self.widgets_container.grid_columnconfigure((0, 1), weight=1)

                self.info_label = ttk.Label(self.widgets_container, text=self._get_text("Enter your credentials to authorize"))
                self.info_label.grid(row=0, column=0, columnspan=2)

                self.login_container = ttk.Frame(self.widgets_container)
                self.login_container.grid(row=1, column=0, columnspan=2)
                self.__init_login()

                self.login_button = ttk.Button(self.widgets_container, text=self._get_text("Apply"), command=self.__login)
                self.login_button.grid(row=2, column=0)

                self.cancel_button = ttk.Button(self.widgets_container, text=self._get_text("Cancel"), command=self.__clean_exit)
                self.cancel_button.grid(row=2, column=1)

                self.gif_frame_count = get_gif_frame_count(ASSETS_DC.LOADING_ANIMATION_PATH)
                self.gif_frames = [PhotoImage(file=ASSETS_DC.LOADING_ANIMATION_PATH, format = 'gif -index %i' %(i)) for i in range(self.gif_frame_count)]
                self.output_loading_label = ttk.Label(self.widgets_container)
                
            def __start_loading_animation(self) :
                self.output_loading_label.grid(row=3, column=0, columnspan=2)
                self.animation_id = self.after(0, self.__animate_loading, 0)

            def __animate_loading(self, frame_index) :
                if not self.thread.is_alive() :
                    self.after(0, self.__stop_loading_animation)
                    return
                if frame_index == self.gif_frame_count :
                    frame_index = 0
                self.current_frame = self.gif_frames[frame_index]
                self.output_loading_label.configure(image=self.current_frame)
                self.animation_id = self.after(20, self.__animate_loading, frame_index + 1)
                
            def __stop_loading_animation(self) :
                
                self.after_cancel(self.animation_id)
                self.output_loading_label.grid_remove()
                
                if self.result == True :
                    self.__clean_exit()
                else :
                    messagebox.showerror(self._get_text("Error"), self._get_text("The entered user does not have the required permissions"))
                    self.login_button.config(state="normal", text=self._get_text("Apply"))
                    # clear entries
                    self.username_entry.delete(0, "end")
                    self.password_entry.delete(0, "end")

            def __init_login(self) :

                self.login_container.grid_rowconfigure((0, 1), weight=1)
                self.login_container.grid_columnconfigure((0, 1), weight=1)

                self.username_label = ttk.Label(self.login_container, text=self._get_text("Username"))
                self.username_label.grid(row=0, column=0)
                self.username_entry = ttk.Entry(self.login_container)
                self.username_entry.grid(row=0, column=1)

                self.password_label = ttk.Label(self.login_container, text=self._get_text("Password"))
                self.password_label.grid(row=1, column=0)
                self.password_entry = ttk.Entry(self.login_container, show="*")
                self.password_entry.grid(row=1, column=1)

            def __load_thread(self) :

                def start_auth() :
                    
                    verifier = UserVerifier(username=self.username_entry.get(), password=self.password_entry.get(), match_id=self.match_id)
                    self.result = verifier.verify_user()

                self.thread = threading.Thread(target=start_auth, daemon=True)
                self.thread.start()

            def __login(self) :

                self.login_button.config(text=self._get_text("Processing"), state="disabled")

                username = self.username_entry.get()
                password = self.password_entry.get()

                if username == "" or password == "" :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Username or Password is Empty"))
                    self.login_button.config(text=self._get_text("Login"), state="normal")
                    return
                
                auth = authenticate(username, password)

                if auth == False :
                    messagebox.showerror(self._get_text("Error"), self._get_text("Username or Password is Incorrect"))
                    self.login_button.config(text=self._get_text("Login"), state="normal")
                    return
                
                self.__start_loading_animation()
                self.__load_thread()

            def _get_text(self, text) :
                if self.parsing_language == "tr" :
                    return to_turkish[text]
                else :
                    return text
            
            def __clean_exit(self) :
                self.result = self.result
                self.destroy()
            
            def get_result(self) :
                return self.result

        obj = Verifier(self, self.student_school_id, self.parsing_language)
        result = obj.get_result()

        self.is_user_authenticated = result
        self.root.set_authication_status(result)