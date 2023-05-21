import tkinter as tk
from tkinter import ttk
import os
from GUI import LoginFrame, ApplicationFrame
from Utilities import MongoClient, push_dpi, OfflineParser
from Environment import GUI_DC, ASSETS_DC

class TranscriptManager(tk.Tk) :

    def __init__(self, DEBUG=False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.DEBUG = DEBUG

        if not self.DEBUG :
            push_dpi()

        self.title(GUI_DC.TITLE)
        self.iconbitmap(ASSETS_DC.ICON)

        self.db_client = MongoClient()
        self.user_info_document = None
        self.user_data_document = None

        self.main_container = ttk.Frame(self)
        self.main_container.grid(row=0, column=0)

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        if not self.DEBUG :
            self.login_frame = LoginFrame(self.main_container, self, self.DEBUG) 
            self.login_frame.grid(row=0, column=0)
        else :
            parser = OfflineParser(path_to_file=r"C:\GithubProjects\transkript-manager\Data\emir.pdf")
            data = parser.get_transcript_data()
            user_info_document, user_data_document = self.db_client.documentisize(data)
            self.db_client.user_info.push_init(user_info_document)
            self.db_client.user_data.push_init(user_data_document)
            self.set_current_data(user_info_document, user_data_document)
            self.application_frame = ApplicationFrame(self.main_container, self, self.DEBUG)
            self.application_frame.grid(row=0, column=0)

            self.after(100000, self.destroy)

        self.protocol("WM_DELETE_WINDOW", self.terminate)

    def _switch_to_application(self) :
        self.login_frame.grid_forget()
        self.login_frame = None

        self.application_frame = ApplicationFrame(self.main_container, self, self.DEBUG)
        self.application_frame.grid(row=0, column=0)

    def _switch_to_login(self) :
        self.application_frame.grid_forget()
        self.application_frame = None

        self.login_frame = LoginFrame(self.main_container, self, self.DEBUG)
        self.login_frame.grid(row=0, column=0)

    def set_current_data(self, user_info_document=None, user_data_document=None) :
        if user_info_document is not None :
            self.user_info_document = user_info_document
        if user_data_document is not None :
            self.user_data_document = user_data_document

    def terminate(self) :
        self.destroy()
