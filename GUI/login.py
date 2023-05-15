import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import filedialog
import os
from Utilities import get_gif_frame_count, authenticate, validate_transcript
from Utilities import (
    OfflineParser,
    OnlineParser
)
import time
import threading

class LoginFrame(ttk.Frame) :

    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root

        self.username = tk.StringVar(value="")
        self.password = tk.StringVar(value="")
        self.path_to_transcript = tk.StringVar(value="")
        self.name_of_transcript = tk.StringVar(value="Select Transcript")
        self.execution_mode = tk.StringVar(value="online")

        self.work_dir = os.getcwd()
        self.desktop_path = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        self.__load_containers()

        self.__load_mef_label()
        self.__load_online_login()
        self.__load_output()

    def __online_thread(self) :

        def job() :
            parser = OnlineParser(username=self.username.get(), password=self.password.get())
            data = parser.get_transcript_data()
            user_info_document, user_data_document = self.root.db_client.documentisize(data)
            self.root.db_client.user_info.push_init(user_info_document)
            self.root.db_client.user_data.push_init(user_data_document)

        self.thread = threading.Thread(target=job, daemon=True)
        self.thread.start()

    def __ofline_thread(self) :

        def job() :
            time.sleep(3) # Simulate a long process by fake sleeping for 3 seconds.
            parser = OfflineParser(path_to_file=self.path_to_transcript.get())
            data = parser.get_transcript_data()
            user_info_document, user_data_document = self.root.db_client.documentisize(data)
            self.root.db_client.user_info.push_init(user_info_document)
            self.root.db_client.user_data.push_init(user_data_document)

        self.thread = threading.Thread(target=job, daemon=True)
        self.thread.start()
        
    def __handle_online_login(self, *args, **kwargs) :
        
        self.online_login_button.config(state="disabled", text="Processing")
        self.online_login_label_button.config(state="disabled")

        isCredentialsCorrect = authenticate(username=self.username.get(), password=self.password.get())

        if isCredentialsCorrect :
            self.__start_loading_animation()
            self.__online_thread()
        else :
            self.online_login_button.config(text="Wrong Credentials")
            self.after(500, lambda : self.online_login_button.config(state="normal", text="Login"))
            self.after(500, lambda : self.online_login_label_button.config(state="normal"))

    def __handle_offline_login(self, *args, **kwargs) :

        self.offline_login_button.config(state="disabled", text="Processing")
        self.offline_login_label_button.config(state="disabled")

        isTranscriptValid = validate_transcript(self.path_to_transcript.get())

        if isTranscriptValid :
            self.__start_loading_animation()
            self.__ofline_thread()
        else :
            self.offline_login_button.config(text="Invalid Transcript")
            self.after(500, lambda : self.offline_login_button.config(state="normal", text="Login"))
            self.after(500, lambda : self.offline_login_label_button.config(state="normal"))

    def __handle_ask_file_dialog(self, *args, **kwargs) :

        input_file_path = filedialog.askopenfile(initialdir = self.work_dir, title = "Select Transcript", filetypes = [('pdf files only', '*.pdf')])
        
        if input_file_path is not None :
            self.path_to_transcript.set(input_file_path.name)
            self.name_of_transcript.set(os.path.basename(input_file_path.name))

    def __switch_login_mode(self, *args, **kwargs) :
        
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

    def __load_containers(self) :

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0)

        self.container.grid_rowconfigure((0,1,2), weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.mef_label_container = ttk.Frame(self.container)
        self.mef_label_container.grid(row=0, column=0)

        self.online_login_container = ttk.Frame(self.container)
        self.online_login_container.grid(row=1, column=0)

        self.offline_login_container = ttk.Frame(self.container)

        self.output_container = ttk.Frame(self.container)
        self.output_container.grid(row=2, column=0)

    def __load_mef_label(self) :
        
        self.mef_label_container.grid_rowconfigure(0, weight=1)
        self.mef_label_container.grid_columnconfigure(0, weight=1)

        self.mef_logo_image = ImageTk.PhotoImage(Image.open("Assets\mef logo.png").resize((192, 126), Image.ANTIALIAS))
        self.mef_logo_label = ttk.Label(self.mef_label_container, image=self.mef_logo_image)
        self.mef_logo_label.grid(row=0, column=0)

    def __load_online_login(self) :
        
        self.online_login_container.grid_rowconfigure((0,1,3), weight=1)
        self.online_login_container.grid_columnconfigure((0,1), weight=1)

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

        self.online_login_button = ttk.Button(self.online_login_container, text="Login", command=self.__handle_online_login)
        self.online_login_button.grid(row=3, column=0, columnspan=2)

    def __load_offline_login(self) :
        
        self.offline_login_container.grid_rowconfigure((0,1,2), weight=1)
        self.offline_login_container.grid_columnconfigure(0, weight=1)

        self.offline_login_label_button = ttk.Button(self.offline_login_container, text="Offline Login", command=self.__switch_login_mode)
        self.offline_login_label_button.grid(row=0, column=0)

        self.offline_open_file_button = ttk.Button(self.offline_login_container, textvariable=self.name_of_transcript, command=self.__handle_ask_file_dialog)
        self.offline_open_file_button.grid(row=1, column=0)

        self.offline_login_button = ttk.Button(self.offline_login_container, text="Login", command=self.__handle_offline_login)
        self.offline_login_button.grid(row=2, column=0)

    def __load_output(self) :
        
        self.gif_frame_count = get_gif_frame_count("Assets\loader.gif")

        self.gif_frames = [PhotoImage(file="Assets\loader.gif", format = 'gif -index %i' %(i)) for i in range(self.gif_frame_count)]

        self.output_container.grid_rowconfigure(0, weight=1)
        self.output_container.grid_columnconfigure(0, weight=1)

        self.output_loading_label = ttk.Label(self.output_container)

    def __start_loading_animation(self) :
        
        self.output_loading_label.grid(row=0, column=0)

        self.animation_id = self.root.after(0, self.__animate_loading, 0)

    def __animate_loading(self, frame_index) :

        if not self.thread.is_alive() :
            self.root.after(0, self.__stop_loading_animation)
            return

        if frame_index == self.gif_frame_count :
            frame_index = 0
        
        self.current_frame = self.gif_frames[frame_index]
        self.output_loading_label.configure(image=self.current_frame)

        self.update()

        self.animation_id = self.root.after(20, self.__animate_loading, frame_index + 1)

    def __stop_loading_animation(self) :
        self.root.after_cancel(self.animation_id)
        self.output_loading_label.grid_remove()

        self.root._switch_to_interface()