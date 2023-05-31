from    Utilities   import  get_gif_frame_count, authenticate, validate_transcript # -> Utilitiy functions
from    Utilities   import  OfflineParser, OnlineParser # -> Utilitiy classes
from    PIL         import  Image, ImageTk # -> Image processing
from    tkinter     import  PhotoImage # -> Image processing
from    tkinter     import  filedialog # -> Ask file path
from    Environment import  ASSETS_DC # -> Environment variables
from    tkinter     import  ttk # -> GUI
import  tkinter     as      tk # -> GUI
import  os # -> Get current working directory
import  time # -> Simulate a long process
import  threading # -> Split long processes into threads

class LoginFrame(ttk.Frame) :

    # Data Fields
    mef_uni_logo_size  = (192, 126)

    def __init__(self, parent : ttk.Frame, root : tk.Tk, DEBUG : bool = False, *args, **kwargs) -> None:
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
        self.username = tk.StringVar(value="")
        self.password = tk.StringVar(value="")
        self.path_to_transcript = tk.StringVar(value="")
        self.name_of_transcript = tk.StringVar(value="Select Transcript")
        self.execution_mode = tk.StringVar(value="online")
        self.work_dir = os.getcwd()
        self.desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        # Initialize widget containers.
        self.__load_containers()

        # # Load widgets.
        self.__load_mef_label()
        self.__load_online_login()
        self.__load_output()

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
            if self.execution_mode.get() == "online" :
                parser = OnlineParser(username=self.username.get(), password=self.password.get())
            elif self.execution_mode.get() == "offline" :
                parser = OfflineParser(path_to_file=self.path_to_transcript.get())
                if not self.DEBUG :
                    time.sleep(2.3) # Simulate a long process by fake sleeping for 3 seconds.
                else :
                    pass

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

    def __handle_login(self, *args, **kwargs) -> None:
        """
        Method to handle the login process.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check the execution mode. (online or offline) Than, get the correctness of the login parameters. Also disable buttons to prevent multiple login attempts.
        if self.execution_mode.get() == "online" :
            self.online_login_button.config(state="disabled", text="Processing")
            self.online_login_label_button.config(state="disabled")
            isAllowed = authenticate(username=self.username.get(), password=self.password.get())
        elif self.execution_mode.get() == "offline" :
            self.offline_login_button.config(state="disabled", text="Processing")
            self.offline_login_label_button.config(state="disabled")
            isAllowed = validate_transcript(self.path_to_transcript.get())
        else :
            raise ValueError("Invalid Execution Mode")

        # If the login parameters are correct, start the loading animation and load the thread.
        if isAllowed :
            self.__start_loading_animation()
            self.__load_thread()
        else :
            # If the login parameters are incorrect, show the error message and fix the buttons. So, user can try again. Use after to show animation effect on buttons.
            if self.execution_mode.get() == "online" :
                self.online_login_button.config(text="Wrong Credentials")
                self.after(500, lambda : self.online_login_button.config(state="normal", text="Login"))
                self.after(500, lambda : self.online_login_label_button.config(state="normal"))
            elif self.execution_mode.get() == "offline" :
                self.offline_login_button.config(text="Invalid Transcript")
                self.after(500, lambda : self.offline_login_button.config(state="normal", text="Login"))
                self.after(500, lambda : self.offline_login_label_button.config(state="normal"))
            else :
                raise ValueError("Invalid Execution Mode")

    def __handle_ask_file_dialog(self, *args, **kwargs) -> None:
        """
        Method to handle the ask file dialog.
        @Parameters:
            None
        @Returns:
            None
        """

        # DEBUG MODE NO COMMENT
        if not self.DEBUG :
            input_file_path = filedialog.askopenfile(initialdir = self.work_dir, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])
        else :
            input_file_path = filedialog.askopenfile(initialdir = self.desktop_path, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])

        # Check if the file is selected.
        if input_file_path is not None and input_file_path != "" and input_file_path != " " :
            # Set the path to transcript and name of transcript.
            self.path_to_transcript.set(input_file_path.name)
            self.name_of_transcript.set(os.path.basename(input_file_path.name))

    def __switch_login_mode(self, *args, **kwargs) -> None:
        """
        Method to switch the login mode.
        @Parameters:
            None
        @Returns:
            None
        """
        # Check the execution mode and switch it. Apply remove and grid methods to the containers. than, load the login containers back.
        if self.execution_mode.get() == "online" :
            self.execution_mode.set("offline")
            self.online_login_container.grid_remove()
            self.offline_login_container.grid(row=1, column=0)
            self.__load_offline_login()
        else :
            self.execution_mode.set("online")
            self.offline_login_container.grid_remove()
            self.online_login_container.grid(row=1, column=0)
            self.__load_online_login()

    def __load_containers(self) -> None:
        """
        Method to load the main containers.
        @Parameters:
            None
        @Returns:
            None
        """
        # Create the main container.
        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)
        # Configure the main container.
        self.container.grid_rowconfigure((0,1,2), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create the sub containers.
        self.mef_label_container = ttk.Frame(self.container)
        self.mef_label_container.grid(row=0, column=0)

        self.online_login_container = ttk.Frame(self.container)
        self.online_login_container.grid(row=1, column=0)

        self.offline_login_container = ttk.Frame(self.container)

        self.output_container = ttk.Frame(self.container)
        self.output_container.grid(row=2, column=0)

    def __load_mef_label(self) -> None:
        """
        Method to load the mef label.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the mef label container.
        self.mef_label_container.grid_rowconfigure(0, weight=1)
        self.mef_label_container.grid_columnconfigure(0, weight=1)

        # Load the mef label.
        self.mef_logo_image = ImageTk.PhotoImage(Image.open(ASSETS_DC.LOGO_PATH).resize(self.mef_uni_logo_size, Image.ANTIALIAS))
        self.mef_logo_label = ttk.Label(self.mef_label_container, image=self.mef_logo_image)
        self.mef_logo_label.grid(row=0, column=0)

    def __load_online_login(self) -> None:
        """
        Method to load the online login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the online login container.
        self.online_login_container.grid_rowconfigure((0,1,3), weight=1)
        self.online_login_container.grid_columnconfigure((0,1), weight=1)

        # Create the online login widgets.
        self.online_login_label_button = ttk.Button(self.online_login_container, text="Online Login", command=self.__switch_login_mode)
        self.online_login_label_button.grid(row=0, column=0, columnspan=2)

        self.online_login_username_label = ttk.Label(self.online_login_container, text="Username")
        self.online_login_username_label.grid(row=1, column=0)
        self.online_login_username_entry = ttk.Entry(self.online_login_container, textvariable=self.username)
        self.online_login_username_entry.grid(row=1, column=1)

        self.online_login_password_label = ttk.Label(self.online_login_container, text="Password")
        self.online_login_password_label.grid(row=2, column=0)
        self.online_login_password_entry = ttk.Entry(self.online_login_container, textvariable=self.password, show="*")
        self.online_login_password_entry.grid(row=2, column=1)

        self.online_login_button = ttk.Button(self.online_login_container, text="Login", command=self.__handle_login)
        self.online_login_button.grid(row=3, column=0, columnspan=2)

    def __load_offline_login(self) -> None:
        """
        Method to load the offline login widgets and wires logic.
        @Parameters:
            None
        @Returns:
            None
        """
        # Configure the offline login container.
        self.offline_login_container.grid_rowconfigure((0,1,2), weight=1)
        self.offline_login_container.grid_columnconfigure(0, weight=1)

        # Create the offline login widgets.
        self.offline_login_label_button = ttk.Button(self.offline_login_container, text="Offline Login", command=self.__switch_login_mode)
        self.offline_login_label_button.grid(row=0, column=0)

        self.offline_open_file_button = ttk.Button(self.offline_login_container, textvariable=self.name_of_transcript, command=self.__handle_ask_file_dialog)
        self.offline_open_file_button.grid(row=1, column=0)

        self.offline_login_button = ttk.Button(self.offline_login_container, text="Login", command=self.__handle_login)
        self.offline_login_button.grid(row=2, column=0)

    def __load_output(self) -> None:
        """
        Method to load the output widgets. Used for gif animation
        @Parameters:
            None
        @Returns:
            None
        """
        # Get the number of frames in the gif file.
        self.gif_frame_count = get_gif_frame_count(ASSETS_DC.LOADING_ANIMATION_PATH)

        # Load each embeddable frame of the gif.
        self.gif_frames = [PhotoImage(file=ASSETS_DC.LOADING_ANIMATION_PATH, format = 'gif -index %i' %(i)) for i in range(self.gif_frame_count)]

        # Configure the output container.
        self.output_container.grid_rowconfigure(0, weight=1)
        self.output_container.grid_columnconfigure(0, weight=1)

        # Create the output widgets. But don't grid them yet. Until login handler is called.
        self.output_loading_label = ttk.Label(self.output_container)

    def __start_loading_animation(self) -> None:
        """
        Method to start the loading animation.
        @Parameters:
            None
        @Returns:
            None
        """
        # Grids the loading gif's label.
        self.output_loading_label.grid(row=0, column=0)
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
        self.output_loading_label.configure(image=self.current_frame)

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
        self.output_loading_label.grid_remove()
        # Switch to the application.
        self.root._switch_to_application()