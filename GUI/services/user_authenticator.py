from    Utilities   import  UserVerifier, authenticate, get_gif_frame_count # -> Utility functions
from    Environment import  ASSETS_DC, to_turkish # -> Environment variables
from    tkinter     import  messagebox # -> Ask file path
from    tkinter     import  PhotoImage # Embed images
from    tkinter     import  Toplevel # -> Create a pop up window
from    tkinter     import  ttk # -> GUI
import  threading # -> Run the authentication in a different thread

class UserAuthenticator(Toplevel) :

    def __init__(self, master : ttk.Frame, match_id : str, parsing_language : str) -> None:
        """
        Constructor of the Authenticator class. Asks user to enter their credentials to authorize.
        @Parameters:
            master - Required : Container frame of the toplevel window. (ttk.Frame) -> Which is used to place the toplevel window.
            match_id - Required : Match ID to authorize. (str) -> Which is used to authorize the user.
            parsing_language - Required : Language of the parsing. (str) -> Which is used to get the text from the language dictionary for translation.
        @Return:
            None
        """
        # Initialize the Toplevel window.
        super().__init__(master)

        # Set the parsing language.
        self.parsing_language = parsing_language

        # Set the title and icon of the window.
        self.title(self._get_text("Unauthorized Access Verification"))
        self.iconbitmap(ASSETS_DC.ICON)

        # Set the class variables.
        self.match_id = match_id
        self.result = False

        # Setup the main container.
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)
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

    def create_widgets(self) -> None:
        """
        Creates the widgets of the window.
        @Parameters:
            None
        @Return:
            None
        """
        # Create the widgets container.
        self.widgets_container = ttk.Frame(self.container)
        self.widgets_container.grid(row=0, column=0)
        # Configure the widgets container.
        self.widgets_container.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.widgets_container.grid_columnconfigure((0, 1), weight=1)

        # Create the widgets.
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
        
    def __start_loading_animation(self) -> None:
        """
        Starts the loading animation.
        @Parameters:
            None
        @Return:
            None
        """
        # Grids the loading gif's label.
        self.output_loading_label.grid(row=3, column=0, columnspan=2)
        # Initialize the animation.
        self.animation_id = self.after(0, self.__animate_loading, 0)

    def __animate_loading(self, frame_index : int) -> None:
        """
        Animates the loading gif.
        @Parameters:
            frame_index - Required : Index of the frame to be displayed. (int) -> Which is used to get the frame from the frames list.
        @Return:
            None
        """
        # Check if the thread is alive. Than stop the program.
        if not self.thread.is_alive() :
            self.after(0, self.__stop_loading_animation)
            return
        
        # Check if the frame index is equal to the frame count. Than reset the frame index.
        if frame_index == self.gif_frame_count :
            frame_index = 0

        # Set the current frame.
        self.current_frame = self.gif_frames[frame_index]
        self.output_loading_label.configure(image=self.current_frame)

        # Animate the next frame.
        self.animation_id = self.after(20, self.__animate_loading, frame_index + 1)
        
    def __stop_loading_animation(self) -> None:
        """
        Stops the loading animation.
        @Parameters:
            None
        @Return:
            None
        """
        # Stop the animation.
        self.after_cancel(self.animation_id)
        self.output_loading_label.grid_remove()
        
        # If result is true, than destroy the window.
        if self.result == True :
            self.__clean_exit()
        else :
            # When the result is false, than enable the login button. Show an error message and clear the entries. So the user can try again.
            messagebox.showerror(self._get_text("Error"), self._get_text("The entered user does not have the required permissions"))
            self.login_button.config(state="normal", text=self._get_text("Apply"))

            # Clear the entries.
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

    def __init_login(self) -> None:
        """
        Initializes the login widgets.
        @Parameters:
            None
        @Return:
            None
        """
        # Configure the login container.
        self.login_container.grid_rowconfigure((0, 1), weight=1)
        self.login_container.grid_columnconfigure((0, 1), weight=1)

        # Create the login widgets.
        self.username_label = ttk.Label(self.login_container, text=self._get_text("Username"))
        self.username_label.grid(row=0, column=0)
        self.username_entry = ttk.Entry(self.login_container)
        self.username_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_container, text=self._get_text("Password"))
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(self.login_container, show="*")
        self.password_entry.grid(row=1, column=1)

    def __load_thread(self) -> None:
        """
        Loads the thread.
        @Parameters:
            None
        @Return:
            None
        """
        def start_auth() -> None:
            """
            Starts the authentication on a core thread.
            @Parameters:
                None
            @Return:
                None
            """
            # Create the verifier object.
            verifier = UserVerifier(username=self.username_entry.get(), password=self.password_entry.get(), match_id=self.match_id)
            # Verify the user. than set the result.
            self.result = verifier.verify_user()

        # Create the thread.
        self.thread = threading.Thread(target=start_auth, daemon=True)
        # Start the thread.
        self.thread.start()

    def __login(self) -> None:
        """
        Starts the login process.
        @Parameters:
            None
        @Return:
            None
        """
        # Disable the login button and set the text to processing. So the user can't click the button again.
        self.login_button.config(text=self._get_text("Processing"), state="disabled")

        # Get the username and password.
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username or password is empty. Than show an error message and enable the login button.
        if username == "" or password == "" :
            messagebox.showerror(self._get_text("Error"), self._get_text("Username or Password is Empty"))
            self.login_button.config(text=self._get_text("Login"), state="normal")
            return
        
        # Authenticate the user credentials with the system
        auth = authenticate(username, password)

        # Check if the authentication is false. Than show an error message and enable the login button. So the user can try again.
        if auth == False :
            messagebox.showerror(self._get_text("Error"), self._get_text("Username or Password is Incorrect"))
            self.login_button.config(text=self._get_text("Login"), state="normal")
            return
        
        # If nothin is wrong, than start the retrieving process.
        self.__start_loading_animation()
        self.__load_thread()

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
    
    def __clean_exit(self) -> None:
        """
        Cleans the selected option and destroys the window.
        @Parameters:
            None
        @Return:
            None
        """
        # Save the result.
        self.result = self.result
        # Destroy the window.
        self.destroy()
    
    def get_result(self) -> bool:
        """
        Gets the result of the login process.
        @Parameters:
            None
        @Return:
            result - bool : Result of the login process. (bool) -> True if the login process is successful. False if the login process is unsuccessful.
        """
        # Return the result.
        return self.result
