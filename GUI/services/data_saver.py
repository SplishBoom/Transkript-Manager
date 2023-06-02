from    Environment     import  ASSETS_DC, GUI_DC, to_turkish # -> Environment variables
from    tkinter         import  messagebox # -> User interaction
import  customtkinter   as      ctk # -> Custom tkinter widgets

class DataSaver(ctk.CTkToplevel) :

    def __init__(self, master : ctk.CTkFrame, existing_document_names : list, parsing_language : str) -> None:
        """
        Constructor of the DataLoader class. Asks user to select a filename to save.
        @Parameters:
            master - Required : Container frame of the toplevel window. (ttk.Frame) -> Which is used to place the toplevel window.
            existing_document_names - Required : Existing document names. (list) -> Which is used to check if the name is already exists.
            parsing_language - Required : Language of the parsing. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            None
        """
        # Initialize the Toplevel window.
        super().__init__(master)
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        # Set the parsing language.
        self.parsing_language = parsing_language
        
        # Set the title and icon of the window.
        self.title(self._get_text("Save Data"))
        self.iconbitmap(ASSETS_DC.ICON)
        
        # Set the class variables.
        self.existing_document_names = existing_document_names
        self.new_document_name = ctk.StringVar(self)

        # Setup the main container.
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container.
        self.container.grid_rowconfigure((0), weight=1)
        self.container.grid_columnconfigure((0), weight=1)

        # Add an handler on close, for making sure correct data is returned.
        self.protocol("WM_DELETE_WINDOW", self.__clean_exit)

        # Create the widgets.
        self.create_widgets()

        # Follow the main window.
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def get_new_document_name(self) -> str:
        """
        Returns the new document name.
        @Parameters:
            None
        @Return:
            new_document_name - str : New document name. (str) -> Which is used to save the data.
        """
        # Return the new document name.
        return self.new_document_name.get()

    def _get_text(self, text : str) -> str:
        """
        Gets the text from the language dictionary.
        @Parameters:
            text - Required : Text to get from the dictionary. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            translated_text - str : Translated text. (str)
        """
        # According to the language, do the translation.
        if self.parsing_language == "tr" :
            return to_turkish[text]
        else :
            return text

    def create_widgets(self) -> None:
        """
        Creates the widgets of the toplevel window.
        @Parameters:
            None
        @Return:
            None
        """
        # Create the widgets container.
        self.widgets_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.widgets_container.grid(row=0, column=0, sticky="nsew")
        # Configure the widgets container.
        self.widgets_container.grid_rowconfigure((0, 1, 2), weight=1)
        self.widgets_container.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
        self.new_document_name_label = ctk.CTkLabel(self.widgets_container, text=self._get_text("Enter a name for the document"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 15, "bold"),
            anchor="center",
        )
        self.new_document_name_label.grid(row=0, column=0, columnspan=2)

        self.new_document_name_entry = ctk.CTkEntry(self.widgets_container, textvariable=self.new_document_name,

        )
        self.new_document_name_entry.grid(row=1, column=0, columnspan=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.save_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Save"), command=self.__save,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.save_button.grid(row=2, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

        self.cancel_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Cancel"), command=self.__clean_exit,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.cancel_button.grid(row=2, column=1, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

    def __save(self) -> None:
        """
        Saves the data.
        @Parameters:
            None
        @Return:
            None
        """
        # Get the new document name.
        new_document_name = self.get_new_document_name()

        # Check if the new document name is valid.
        if new_document_name == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please enter a name for the document"))
            return
        if new_document_name in self.existing_document_names :
            messagebox.showerror(self._get_text("Error"), self._get_text("A document with this name already exists"))
            return
        if new_document_name == "Transcript Document" :
            messagebox.showerror(self._get_text("Error"), self._get_text("This name is reserved, please enter another name"))
            return

        # Clean the window.
        self.destroy()

    def __clean_exit(self) -> None:
        """
        Cleans the selected option and destroys the window.
        @Parameters:
            None
        @Return:
            None
        """
        # Clean the new_document_name. To avoid returning wrong data.
        self.new_document_name.set("")
        # Destroy the window.
        self.destroy()