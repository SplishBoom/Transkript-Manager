from    Environment import  ASSETS_DC, to_turkish # -> Environment variables
from    tkinter     import  messagebox # -> Ask file path
from    tkinter     import  Toplevel # -> Create a pop up window
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI

class DataLoader(Toplevel) :

    def __init__(self, master : ttk.Frame, options : tuple, parsing_language : str) -> None:
        """
        Constructor of the DataLoader class. Asks user to select a file to load.
        @Parameters:
            master - Required : Container frame of the toplevel window. (ttk.Frame) -> Which is used to place the toplevel window.
            options - Required : Options received from database (tuple) -> Which is used to create a combobox. For data selection. 
            parsing_language - Required : Language of the parsing. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            None
        """
        # Initialize the Toplevel window.
        super().__init__(master)

        # Set the parsing language.
        self.parsing_language = parsing_language

        # Set the title and icon of the window.
        self.title(self._get_text("Load Data"))
        self.iconbitmap(ASSETS_DC.ICON)

        # Set the class variables.
        self.options = options
        self.selected_option = tk.StringVar(self)

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

    def get_selected_option(self) -> str:
        """
        Gets the selected option from the combobox.
        @Parameters:
            None
        @Return:
            selected_option - str : Selected option from the combobox. (str)
        """
        # Return the selected option.
        return self.selected_option.get()

    def create_widgets(self) -> None:
        """
        Creates the widgets of the toplevel window.
        @Parameters:
            None
        @Return:
            None
        """
        # Create the widgets.
        self.options_label = ttk.Label(self.container, text=self._get_text("Select a document to load"))
        self.options_label.grid(row=0, column=0, columnspan=2)

        self.options_combobox = ttk.Combobox(self.container, textvariable=self.selected_option, values=self.options)
        self.options_combobox.grid(row=1, column=0, columnspan=2)

        self.load_button = ttk.Button(self.container, text=self._get_text("Load"), command=self.__load)
        self.load_button.grid(row=2, column=0)

        self.cancel_button = ttk.Button(self.container, text=self._get_text("Cancel"), command=self.__clean_exit)
        self.cancel_button.grid(row=2, column=1)

    def __load(self) -> None:
        """
        Loads the selected option from the combobox.
        @Parameters:
            None
        @Return:
            None
        """
        # Get the selected option.
        selected_option = self.selected_option.get()

        # If no option is selected, show an error message.
        if selected_option == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Please select a document"))
            return
        
        # Set the selected option.
        self.destroy()

    def __clean_exit(self) -> None:
        """
        Cleans the selected option and destroys the window.
        @Parameters:
            None
        @Return:
            None
        """
        # Clean the selected option. To avoid returning wrong data.
        self.selected_option.set("")
        # Destroy the window.
        self.destroy()
