from    Utilities       import  get_gif_frame_count, authenticate, validate_transcript # -> Utilitiy functions
from    Utilities       import  OfflineParser, OnlineParser # -> Utilitiy classes
from    PIL             import  Image # -> Image processing
from    Environment     import  ASSETS_DC, GUI_DC # -> Environment variables
import  customtkinter   as      ctk # -> GUI
import  threading # -> Split long processes into threads
import  time # -> Simulate a long process
import  os # -> Get current working directory

class LoginFrame(ctk.CTkFrame) :

    def __init__(self, parent : ctk.CTkFrame, root : ctk.CTk, DEBUG : bool = False, *args, **kwargs) -> None:
        """
        Constructor method for LoginFrame class. Used to initialize main window of the login.
        @Parameters:
            parent - Required : Container frame of the login. (ttk.Frame) -> Which is used to place the login frame.
            root   - Required : Root window of the login. (tk.Tk) -> Which is used to set connection between frames.
            DEBUG  - Optional : Debug mode flag. (bool) (default : False) -> Which is used to determine whether the login is in debug mode or not.
        @Returns:
            None
        """
        # Initialize main frame
        super().__init__(parent, *args, **kwargs)

        # Initialize variables
        self.parent = parent
        self.root   = root
        self.DEBUG  = DEBUG
        self.username = ctk.StringVar(value=None)
        self.password = ctk.StringVar(value=None)
        self.path_to_transcript = ctk.StringVar(value=None)
        self.name_of_transcript = ctk.StringVar(value=None)
        self.work_dir = os.getcwd()
        self.desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        # Initialize widget containers.
        self.__load_containers()

        # # Load widgets.
        self.__load_mef_label()
        self.__load_input_field()

    def __load_containers(self) -> None:
        """
        Method to load the main containers.
        @Parameters:
            None
        @Returns:
            None
        """
        # Set the initial configuration, to make expandable affect on window.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Create the main container.
        self.container = ctk.CTkFrame(self, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.DARK_BACKGROUND, corner_radius=25)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Configure the main container.
        self.container.grid_rowconfigure((0,1), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create the sub containers.
        self.mef_label_container = ctk.CTkFrame(self.container)
        self.mef_label_container.grid(row=0, column=0)

        self.input_field_container = ctk.CTkFrame(self.container)
        self.input_field_container.grid(row=1, column=0)

        # Iterate over containers, and configure them.
        for container in self.container.winfo_children() :
            container.configure(fg_color=GUI_DC.LIGHT_BACKGROUND, border_color=GUI_DC.BORDER_COLOR, border_width=2, corner_radius=25, bg_color = GUI_DC.LIGHT_BACKGROUND)
            container.grid_configure(padx=GUI_DC.GENERAL_PADDING, pady=GUI_DC.GENERAL_PADDING, sticky="nsew")


    def __load_mef_label(self) -> None:
        """
        Method to load the mef label.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the mef label container.
        self.mef_label_container.grid_rowconfigure((0,1,2), weight=1)
        self.mef_label_container.grid_columnconfigure(0, weight=1)

        # Load the mef label.
        ctk.CTkFrame(self.mef_label_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=0, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)
        self.mef_logo_image = ctk.CTkImage(dark_image=Image.open(ASSETS_DC.LOGO_PATH), light_image=Image.open(ASSETS_DC.LOGO_PATH), size=GUI_DC.LOGIN_MEF_LOGO_SIZE)
        self.mef_logo_label = ctk.CTkLabel(self.mef_label_container, image=self.mef_logo_image, text=None, anchor="center")
        self.mef_logo_label.grid(row=1, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING)
        ctk.CTkFrame(self.mef_label_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=2, column=0, pady=GUI_DC.INNER_PADDING, padx=GUI_DC.INNER_PADDING)

    def __load_input_field(self) -> None:
        """
        Method to load the online & offline login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the input field container.
        self.input_field_container.grid_rowconfigure((0,1,2), weight=1)
        self.input_field_container.grid_columnconfigure((0), weight=1)

        # Create the tabview widget for the input field.
        ctk.CTkFrame(self.input_field_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=0, column=0, pady=GUI_DC.INNER_PADDING//2, padx=GUI_DC.INNER_PADDING)
        ctk.CTkTabview._segmented_button_border_width = 4
        ctk.CTkTabview._button_height = 30
        ctk.CTkTabview._top_button_overhang = 9
        self.tab_view = ctk.CTkTabview(self.input_field_container, 
                                       fg_color=GUI_DC.DARK_BACKGROUND, 
                                       bg_color=GUI_DC.LIGHT_BACKGROUND,
                                       text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                       text_color_disabled=GUI_DC.MEDIUM_TEXT_COLOR,
                                       segmented_button_fg_color=GUI_DC.DARK_BACKGROUND,
                                       segmented_button_selected_color=GUI_DC.BUTTON_LIGHT_BLUE,
                                       segmented_button_selected_hover_color=GUI_DC.BUTTON_LIGHT_BLUE_HOVER,
                                       segmented_button_unselected_color=GUI_DC.DARK_BACKGROUND,
                                       segmented_button_unselected_hover_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                       corner_radius=25,
                                       width=0,
                                       height=317
        )
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=GUI_DC.INNER_PADDING, pady=GUI_DC.INNER_PADDING)
        ctk.CTkFrame(self.input_field_container, width=0, height=0, fg_color=GUI_DC.LIGHT_BACKGROUND, bg_color=GUI_DC.LIGHT_BACKGROUND).grid(row=2, column=0, pady=GUI_DC.INNER_PADDING//2, padx=GUI_DC.INNER_PADDING)
        # Add the tabs
        self.online_tab = self.tab_view.add("Online Login")
        self.offline_tab = self.tab_view.add("Offline Login")

        # Set the current tab to online login.
        self.tab_view.set("Online Login")

        # Load the online login widgets into the tab.
        self.___load_online_login()
        # Load the offline login widgets into the tab.
        self.___load_offline_login()

    def ___load_online_login(self) -> None:
        """
        Method to load the online login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the online login container.
        self.online_tab.grid_rowconfigure((0,1,3,4,5,6), weight=1)
        self.online_tab.grid_columnconfigure((0), weight=1)

        # Create the online login widgets.
        self.offline_status_label = ctk.CTkLabel(self.online_tab, text="Username",
                                                        fg_color=GUI_DC.DARK_BACKGROUND,
                                                        bg_color=GUI_DC.DARK_BACKGROUND,
                                                        text_color=GUI_DC.LIGHT_BACKGROUND,
                                                        font=("Arial", 12, "bold")
        )
        self.offline_status_label.grid(row=0, column=0, sticky="w", padx=15)
        self.online_login_username_entry = ctk.CTkEntry(self.online_tab, textvariable=self.username,
                                                        fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                                        bg_color=GUI_DC.DARK_BACKGROUND,
                                                        border_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                                        placeholder_text="username",
                                                        placeholder_text_color=GUI_DC.DARK_TEXT_COLOR,
                                                        text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_username_entry.grid(row=1, column=0, sticky="we", padx=15)
        
        # Dummy label for spacing. *** The pady is not working propely on customtkinter, so this is a workaround. ***
        ctk.CTkLabel(self.online_tab, height=0, text=None).grid(row=2, column=0)

        self.online_login_password_label = ctk.CTkLabel(self.online_tab, text="Password",
                                                        fg_color=GUI_DC.DARK_BACKGROUND,
                                                        bg_color=GUI_DC.DARK_BACKGROUND,
                                                        text_color=GUI_DC.LIGHT_BACKGROUND,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_password_label.grid(row=3, column=0, sticky="w", padx=15)
        self.online_login_password_entry = ctk.CTkEntry(self.online_tab, textvariable=self.password, show="*",
                                                        fg_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                                        bg_color=GUI_DC.DARK_BACKGROUND,
                                                        border_color=GUI_DC.SECONDARY_DARK_BACKGROUND,
                                                        placeholder_text="password",
                                                        placeholder_text_color=GUI_DC.DARK_TEXT_COLOR,
                                                        text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                                        font=("Arial", 12, "bold")
        )
        self.online_login_password_entry.grid(row=4, column=0, sticky="we", padx=15)

        ctk.CTkLabel(self.online_tab, height=0, text=None).grid(row=5, column=0)

        self.online_login_button = ctk.CTkButton(self.online_tab, text="Login", command=self.__handle_login, 
                                                 fg_color=GUI_DC.BUTTON_LIGHT_GREEN, 
                                                 hover_color=GUI_DC.BUTTON_LIGHT_GREEN_HOVER, 
                                                 border_color=GUI_DC.LIGHT_BACKGROUND, 
                                                 bg_color=GUI_DC.DARK_BACKGROUND, 
                                                 corner_radius=50,
                                                 text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                                 text_color_disabled=GUI_DC.DARK_TEXT_COLOR,
                                                 font=("Arial", 14, "bold")
        )
        self.online_login_button.grid(row=6, column=0, pady=12)

    def ___load_offline_login(self) -> None:
        """
        Method to load the offline login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the offline login container.
        self.offline_tab.grid_rowconfigure((0,1,2), weight=1)
        self.offline_tab.grid_columnconfigure(0, weight=1)

        # Create the offline login widgets.
        self.offline_open_file_button = ctk.CTkButton(self.offline_tab, text=self.name_of_transcript.get() or "Select Transcript", command=self.__handle_ask_file_dialog,
                                                      fg_color=GUI_DC.BUTTON_LIGHT_BLUE,
                                                      hover_color=GUI_DC.BUTTON_LIGHT_BLUE_HOVER,
                                                      border_color=GUI_DC.LIGHT_BACKGROUND,
                                                      bg_color=GUI_DC.DARK_BACKGROUND,
                                                      corner_radius=50,
                                                      text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                                      text_color_disabled=GUI_DC.DARK_TEXT_COLOR,
                                                      font=("Arial", 14, "bold"),
        )
        self.offline_open_file_button.grid(row=0, column=0, pady=12)

        self.offline_status_label = ctk.CTkLabel(self.offline_tab, text="Offline Mode Available",
                                                        fg_color=GUI_DC.DARK_BACKGROUND,
                                                        bg_color=GUI_DC.DARK_BACKGROUND,
                                                        text_color=GUI_DC.BUTTON_LIGHT_GREEN,
                                                        font=("Arial", 12, "bold")
        )
        self.offline_status_label.grid(row=1, column=0, sticky="we", padx=15)

        self.offline_login_button = ctk.CTkButton(self.offline_tab, text="Login", command=self.__handle_login, 
                                                  fg_color=GUI_DC.BUTTON_LIGHT_GREEN, 
                                                  hover_color=GUI_DC.BUTTON_LIGHT_GREEN_HOVER, 
                                                  border_color=GUI_DC.LIGHT_BACKGROUND, 
                                                  bg_color=GUI_DC.DARK_BACKGROUND, 
                                                  corner_radius=50,
                                                  text_color=GUI_DC.LIGHT_TEXT_COLOR,
                                                  text_color_disabled=GUI_DC.DARK_TEXT_COLOR,
                                                  font=("Arial", 14, "bold")
        )
        self.offline_login_button.grid(row=2, column=0, pady=12)


    def __handle_ask_file_dialog(self, *args, **kwargs) -> None:
        """
        Method to handle the ask file dialog.
        @Parameters:
            None
        @Returns:
            None
        """

        # Disable the buttons to prevent multiple file selection.
        self.offline_open_file_button.configure(state="disabled", text="Processing")

        # DEBUG MODE NO COMMENT
        if not self.DEBUG :
            input_file_path = ctk.filedialog.askopenfile(initialdir = self.work_dir, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])
        else :
            input_file_path = ctk.filedialog.askopenfile(initialdir = self.desktop_path, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])

        # Set literal for user interraction
        file_selected = False

        # Check if the file is selected.
        if input_file_path is not None and input_file_path != "" and input_file_path != " " :
            # Set the path to transcript and name of transcript.
            self.path_to_transcript.set(input_file_path.name)
            self.name_of_transcript.set(os.path.basename(input_file_path.name))
            # Update statement
            file_selected = True

        # Fix the buttons. So, user can try again.
        if not file_selected :
            self.offline_open_file_button.configure(text="No File Selected", fg_color=GUI_DC.BUTTON_LIGHT_RED, text_color_disabled=GUI_DC.LIGHT_TEXT_COLOR)
            self.after(500, lambda : self.offline_open_file_button.configure(state="normal", text=self.name_of_transcript.get() or "Select Transcript", fg_color=GUI_DC.BUTTON_LIGHT_BLUE, text_color_disabled=GUI_DC.DARK_TEXT_COLOR))
        else :
            self.offline_open_file_button.configure(state="normal", text=self.name_of_transcript.get() or "Select Transcript")

    def __handle_login(self, *args, **kwargs) -> None:
        """
        Method to handle the login process.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check the execution mode. (online or offline) Than, get the correctness of the login parameters. Also disable buttons to prevent multiple login attempts.
        if self.tab_view.get() == "Online Login" :
            self.online_login_button.configure(state="disabled", text="Processing")
            self.online_login_username_entry.configure(state="disabled")
            self.online_login_password_entry.configure(state="disabled")
            if (self.username.get() is None or self.username.get() == "" or self.username.get() == " ") or (self.password.get() is None or self.password.get() == "" or self.password.get() == " ") :
                isAllowed = False
            else :            
                isAllowed = authenticate(username=self.username.get(), password=self.password.get())
        elif self.tab_view.get() == "Offline Login" :
            self.offline_login_button.configure(state="disabled", text="Processing")
            self.offline_open_file_button.configure(state="disabled")
            if self.path_to_transcript.get() is None or self.path_to_transcript.get() == "" or self.path_to_transcript.get() == " " :
                isAllowed = False
            else :
                isAllowed = validate_transcript(self.path_to_transcript.get())
        else :
            raise ValueError("Invalid Execution Mode")

        # If the login parameters are correct, start the loading animation and load the thread.
        if isAllowed :
            self.tab_view.configure(state="disabled")
            self.__start_loading_animation()
            self.__load_thread()
        else :
            # If the login parameters are incorrect, show the error message and fix the buttons. So, user can try again. Use after to show animation effect on buttons.
            if self.tab_view.get() == "Online Login" :
                self.online_login_username_entry.configure(state="normal")
                self.online_login_password_entry.configure(state="normal")
                self.online_login_button.configure(text="Wrong Credentials", fg_color=GUI_DC.BUTTON_LIGHT_RED, text_color_disabled=GUI_DC.LIGHT_TEXT_COLOR)
                self.after(500, lambda : self.online_login_button.configure(state="normal", text="Login", fg_color=GUI_DC.BUTTON_LIGHT_GREEN, text_color_disabled=GUI_DC.DARK_TEXT_COLOR))
            elif self.tab_view.get() == "Offline Login" :
                self.offline_open_file_button.configure(state="normal")
                self.offline_login_button.configure(text="Invalid Transcript", fg_color=GUI_DC.BUTTON_LIGHT_RED, text_color_disabled=GUI_DC.LIGHT_TEXT_COLOR)
                self.after(500, lambda : self.offline_login_button.configure(state="normal", text="Login", fg_color=GUI_DC.BUTTON_LIGHT_GREEN, text_color_disabled=GUI_DC.DARK_TEXT_COLOR))
            else :
                raise ValueError("Invalid Execution Mode")

    def __load_thread(self) -> None:
        """
        Method to load the thread for the login process.
        @Parameters:
            None
        @Returns:
            None
        """
        def start_parse() -> None:
            """
            Method to start the parsing process on core thread.
            @Parameters:
                None
            @Returns:
                None
            """
            # Create parser object according to the execution mode.
            if self.tab_view.get() == "Online Login" :
                parser = OnlineParser(username=self.username.get(), password=self.password.get())
            elif self.tab_view.get() == "Offline Login" :
                parser = OfflineParser(path_to_file=self.path_to_transcript.get())
                if not self.DEBUG :
                    time.sleep(2.3) # Simulate a long process by fake sleeping for 3 seconds.
                else :
                    pass
            else :
                raise ValueError("Invalid Execution Mode")

            # Parse the transcript.
            data = parser.get_transcript_data()

            # Create user info and user data documents.
            user_info_document, user_data_document = self.root.db_client.documentisize(data)
            
            # Uncomment the following lines if you want to push the data to the database at each login. (Not recommended) (INIT PUSH)
            #self.root.db_client.user_info.push_init(user_info_document)
            #self.root.db_client.user_data.push_init(user_data_document)

            # Set the current data to the root.
            self.root.set_current_data(user_info_document, user_data_document)

            # Set the authentication status to the root.
            is_user_authenticated = user_data_document["parsing_type"] != "offline"
            self.root.set_authication_status(is_user_authenticated)

        # Load the thread.
        self.thread = threading.Thread(target=start_parse, daemon=True)
        # Start the thread.
        self.thread.start()


    def __start_loading_animation(self) -> None:
        """
        Method to start the loading animation.
        @Parameters:
            None
        @Returns:
            None
        """

        # Get the pressed login button.
        if self.tab_view.get() == "Online Login" :
            self.pressed_button : ctk.CTkButton = self.online_login_button
        elif self.tab_view.get() == "Offline Login" :
            self.pressed_button : ctk.CTkButton = self.offline_login_button
        else :
            raise ValueError("Invalid Execution Mode")
        
        # Reconfigure the pressed button.
        self.pressed_button.configure(state="disabled", text=None, command=None, fg_color=GUI_DC.LIGHT_BACKGROUND)

        # Get the number of frames in the gif file.
        self.gif_frame_count = get_gif_frame_count(ASSETS_DC.LOADING_ANIMATION_PATH)

        # Load each embeddable frame of the gif.
        self.gif_frames = []
        for frame in range(self.gif_frame_count):
            
            # Get the current frame.
            current_pil_image = Image.open(ASSETS_DC.LOADING_ANIMATION_PATH)
            current_pil_image.seek(frame)
            
            # Append it in to the frame list.
            current_gif_object = ctk.CTkImage(light_image=current_pil_image, dark_image=current_pil_image, size=GUI_DC.LOGIN_GIF_SIZE)
            self.gif_frames.append(current_gif_object)

        # Initialize the animation.
        self.animation_id = self.root.after(0, self.__animate_loading, 0)

    def __animate_loading(self, frame_index : int) -> None:
        """
        Method to animate the loading gif.
        @Parameters:
            frame_index - Required : Index of the frame to be displayed. (int) -> Which is used to get the frame from the frames list.
        @Returns:
            None
        """
        # Check if the thread is alive. Than stop the program.
        if not self.thread.is_alive() :
            self.root.after(0, self.__stop_loading_animation)
            return

        # Check if the frame index is equal to the frame count. Than reset the frame index.
        if frame_index == self.gif_frame_count :
            frame_index = 0
        
        # Set the current frame.
        self.current_frame = self.gif_frames[frame_index]

        # Set text to None, the ctk currently does not update itself when the image is changed without a text.
        self.pressed_button.configure(image=self.current_frame, text=None)

        # Animate the next frame.
        self.animation_id = self.root.after(20, self.__animate_loading, frame_index + 1)
        
    def __stop_loading_animation(self) -> None:
        """
        Method to stop the loading animation.
        @Parameters:
            None
        @Returns:
            None
        """
        # Cancel the animation.
        self.root.after_cancel(self.animation_id)

        # Switch to the application.
        self.root._switch_to_application()