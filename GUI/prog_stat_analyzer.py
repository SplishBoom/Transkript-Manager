import tkinter as tk
from tkinter import ttk

class StatAnalyzer(ttk.Frame) :

    def __init__(self, application_container, parent, root, current_user_data, DEBUG=False, *args, **kwargs):
        super().__init__(application_container, *args, **kwargs)

        self.root = root
        self.parent = parent
        self.application_container = application_container
        self.DEBUG = DEBUG

        label = ttk.Label(self, text="Stat Analyzer")
        label.grid(row=0, column=0)