import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import filedialog
import os
from Environment import ASSETS_DC, SELENIUM_DC

class ApplicationFrame(ttk.Frame) :

    def __init__(self, parent, root, DEBUG=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.DEBUG = DEBUG

        self.current_user_info_document = self.root.user_info_document
        self.current_user_data_document = self.root.user_data_document

        print(self.current_user_info_document["student_department"])
        print(self.current_user_data_document["filtering"])



        self.__load_containers()

        self.__load_user_info_label()

    def __load_containers(self) :

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.container.grid_rowconfigure((0,1,2), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.user_info_label = ttk.Frame(self.container)
        self.user_info_label.grid(row=0, column=0)

    def __load_user_info_label(self) :
        pass