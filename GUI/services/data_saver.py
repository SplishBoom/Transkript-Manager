from    Environment import  ASSETS_DC, to_turkish # -> Environment variables
from    tkinter     import  messagebox # -> Ask file path
from    tkinter     import  Toplevel # -> Create a pop up window
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI

class DataSaver(Toplevel) :

    def __init__(self, master : ttk.Frame, existing_document_names : list, parsing_language : str) -> None:
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

        # Set the parsing language.
        self.parsing_language = parsing_language
        
        # Set the title and icon of the window.
        self.title(self._get_text("Save Data"))
        self.iconbitmap(ASSETS_DC.ICON)
        
        # Set the class variables.
        self.existing_document_names = existing_document_names
        self.new_document_name = tk.StringVar(self)

        # Setup the main container.
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        # Configure the container.
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
        # Create the widgets.
        self.new_document_name_label = ttk.Label(self.container, text=self._get_text("Enter a name for the document"))
        self.new_document_name_label.grid(row=0, column=0, columnspan=2)

        self.new_document_name_entry = ttk.Entry(self.container, textvariable=self.new_document_name)
        self.new_document_name_entry.grid(row=1, column=0, columnspan=2)

        self.save_button = ttk.Button(self.container, text=self._get_text("Save"), command=self.__save)
        self.save_button.grid(row=2, column=0)

        self.cancel_button = ttk.Button(self.container, text=self._get_text("Cancel"), command=self.__clean_exit)
        self.cancel_button.grid(row=2, column=1)

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