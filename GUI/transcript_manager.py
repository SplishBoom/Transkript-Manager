from    Environment     import  GUI_DC, ASSETS_DC, to_turkish # -> Environment variables
from    GUI             import  LoginFrame, ApplicationFrame # -> GUI
from    Utilities       import  MongoClient, OfflineParser # -> Database and parsing
import  customtkinter   as      ctk # -> GUI

class TranscriptManager(ctk.CTk) :

    def __init__(self, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor of the TranscriptManager. Initializes the driver code.
        @Parameters:
            DEBUG - Optional : Debug mode. (bool) -> Which is used to determine if the application is in debug mode.
        @Return:
            None
        """
        # Initialize the Tkinter window.
        super().__init__(*args, **kwargs)

        # Set the theme of the application.
        ctk.set_appearance_mode("dark")

        # Set the title and icon of the window.
        self.title(GUI_DC.TITLE)
        self.iconbitmap(ASSETS_DC.ICON)

        # Set the main windows colors.
        self.configure(fg_color = GUI_DC.DARK_BACKGROUND, bg_color = GUI_DC.DARK_BACKGROUND)

        # Set class variables.
        self.DEBUG = DEBUG
        self.db_client = MongoClient()
        self.user_info_document = None
        self.user_data_document = None
        self.is_user_authenticated = False

        # Configure window's gridding.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Setup the main container.
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=0, column=0, padx=GUI_DC.GENERAL_PADDING, pady=GUI_DC.GENERAL_PADDING)
        # Configure the main container.
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        if not self.DEBUG :
            # Load the initial frame.
            self.login_frame = LoginFrame(self.main_container, self, self.DEBUG)
            # Grid the initial frame.
            self.login_frame.grid(row=0, column=0, stick="nsew")

            # Push up the DPI for the application.
            #push_dpi()
        else :
            # DEBUG MODE NO COMMENT
            parser = OfflineParser(path_to_file=r"C:\GithubProjects\transkript-manager\Data\emir.pdf")
            data = parser.get_transcript_data()
            user_info_document, user_data_document = self.db_client.documentisize(data)
            #self.db_client.user_info.push_init(user_info_document)
            #self.db_client.user_data.push_init(user_data_document)
            self.set_current_data(user_info_document, user_data_document)

            is_user_authenticated = user_data_document["parsing_type"] != "offline"

            self.set_authication_status(is_user_authenticated)

            self.application_frame = ApplicationFrame(self.main_container, self, self.DEBUG)
            self.application_frame.grid(row=0, column=0, stick="nsew")

            self.after(100000, self.destroy)

        # Set the termination protocol. To avoid the terminal crash.
        self.protocol("WM_DELETE_WINDOW", self.terminate)

    def _switch_to_application(self) -> None:
        """
        Switches the current frame to the application frame.
        @Parameters:
            None
        @Return:
            None
        """
        # Remove the login frame.
        self.login_frame.grid_forget()
        self.login_frame = None
        # Load the application frame.
        self.application_frame = ApplicationFrame(self.main_container, self, self.DEBUG)
        self.application_frame.grid(row=0, column=0, stick="nsew")

    def restart_application(self) -> None:
        """
        Restarts the application.
        @Parameters:
            None
        @Return:
            None
        """
        # Remove the application frame.
        self.application_frame.grid_forget()
        self.application_frame = None
        # Load the application frame.
        self.application_frame = ApplicationFrame(self.main_container, self, self.DEBUG)
        self.application_frame.grid(row=0, column=0, stick="nsew")

    def _switch_to_login(self) -> None:
        """
        Switches the current frame to the login frame.
        @Parameters:
            None
        @Return:
            None
        """
        # Remove the application frame.
        self.application_frame.grid_forget()
        self.application_frame = None
        # Load the login frame.
        self.login_frame = LoginFrame(self.main_container, self, self.DEBUG)
        self.login_frame.grid(row=0, column=0, stick="nsew")

    def set_current_data(self, user_info_document : dict = None, user_data_document : dict = None) -> None:
        """
        Sets the current data of the user. It detects the None situation and sets the data accordingly.
        @Parameters:
            user_info_document - Optional : The user info document. (dict) (default = None) -> Which is used to determine the user info document.
            user_data_document - Optional : The user data document. (dict) (default = None) -> Which is used to determine the user data document.
        @Return:
            None
        """
        # Update the user_info_document and user_data_document. If they are not None.
        if user_info_document is not None :
            self.user_info_document = user_info_document
        if user_data_document is not None :
            self.user_data_document = user_data_document

    def get_current_data(self) -> tuple:
        """
        Gets the current data of the user.
        @Parameters:
            None
        @Return:
            tuple (
                user_info_document - The user info document. (dict) -> Which is used to determine the user info document.
                user_data_document - The user data document. (dict) -> Which is used to determine the user data document.
            )
        """
        # Return the user_info_document and user_data_document.
        return self.user_info_document, self.user_data_document

    def set_authication_status(self, status : bool) -> None:
        """
        Sets the authication status of the user.
        @Parameters:
            status - Required : The authication status. (bool) -> Which is used to determine the authication status.
        @Return:
            None
        """
        # Update the authication status.
        self.authication_status = status

    def get_authication_status(self) -> bool:
        """
        Gets the authication status of the user.
        @Parameters:
            None
        @Return:
            status - The authication status. (bool) -> Which is used to determine the authication status.
        """
        # Return the authication status.
        return self.authication_status

    def get_text(self, text : str, parsing_language : str) -> str:
        """
        Gets the text in the parsing language.
        @Wrapping:
            This method is wrapped by other frames via parents or root object directly!
        @Parameters:
            text - Required : The text to be parsed. (str) -> Which is used to determine the text to be parsed.
            parsing_language - Required : The parsing language. (str) -> Which is used to determine the parsing language.
        @Return:
            text - The parsed text. (str) -> Which is used to determine the parsed text.
        """
        # Return the parsed text.
        if parsing_language == "tr" :
            return to_turkish[text]
        else :
            return text

    def terminate(self) -> None:
        """
        Terminates the application.
        @Parameters:
            None
        @Return:
            None
        """
        self.destroy()
