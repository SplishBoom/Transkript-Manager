from    Environment     import  ASSETS_DC, GUI_DC, to_turkish # -> Environment variables
from    tkinter         import  messagebox # -> User interaction
import  customtkinter   as      ctk # -> Custom tkinter widgets

class DataLoader(ctk.CTkToplevel) :

    def __init__(self, master : ctk.CTkFrame, options : tuple, parsing_language : str) -> None:
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
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure((0), weight=1)

        # Set the parsing language.
        self.parsing_language = parsing_language

        # Set the title and icon of the window.
        self.title(self._get_text("Load Data"))
        self.iconbitmap(ASSETS_DC.ICON)

        # Set the class variables.
        self.options = options
        self.selected_option = ctk.StringVar(self)

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
        # Create the widgets container.
        self.widgets_container = ctk.CTkFrame(self.container, fg_color=GUI_DC.DARK_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND)
        self.widgets_container.grid(row=0, column=0, sticky="nsew")
        # Configure the widgets container.
        self.widgets_container.grid_rowconfigure((0, 1, 2), weight=1)
        self.widgets_container.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
        self.options_label = ctk.CTkLabel(self.widgets_container, text=self._get_text("Select a document to load"),
            fg_color=GUI_DC.DARK_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            text_color=GUI_DC.LIGHT_TEXT_COLOR,
            font=("Arial", 15, "bold"),
            anchor="center",
        )
        self.options_label.grid(row=0, column=0, columnspan=2)

        self.options_combobox = ctk.CTkComboBox(self.widgets_container, variable=self.selected_option, values=self.options,
            justify="center",
            state="readonly",
        )
        self.options_combobox.grid(row=1, column=0, columnspan=2, padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)

        self.load_button = ctk.CTkButton(self.widgets_container, text=self._get_text("Load"), command=self.__load,
            fg_color=GUI_DC.LIGHT_BACKGROUND,
            bg_color=GUI_DC.DARK_BACKGROUND,
            hover_color=GUI_DC.SECONDARY_LIGHT_BACKGROUND,
            text_color=GUI_DC.DARK_TEXT_COLOR,
            text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
            anchor="center",
            font=("Arial", 12, "bold")
        )
        self.load_button.grid(row=2, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

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