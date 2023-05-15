import tkinter as tk
from tkinter import ttk
import os
from GUI import LoginFrame
from Utilities import MongoClient

class Application(tk.Tk) :

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.db_client = MongoClient(connection_string="mongodb://localhost:27017", db_name="trman")

        self.title("Transcript Manager")

        self.application_container = ttk.Frame(self)
        self.application_container.grid(row=0, column=0)

        self.application_container.grid_rowconfigure(0, weight=1)
        self.application_container.grid_columnconfigure(0, weight=1)

        self.login_frame = LoginFrame(self.application_container, self)
        self.login_frame.grid(row=0, column=0)


    def _switch_to_interface(self) :

        self.login_frame.grid_forget()

        self.interface_frame = ttk.Frame(self.application_container)
        self.interface_frame.grid(row=0, column=0)
