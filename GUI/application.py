from    Util        import WHITE_COLOR, BLACK_COLOR, RED_COLOR, BLUE_COLOR, GREEN_COLOR, PBLUE_COLOR, PINK_COLOR, ORANGE_COLOR, YELLOW_COLOR, PURPLE_COLOR, DARK_BACKGROUND_COLOR, LIGHT_BACKGROUND2_COLOR
from    GUI         import ControllFrame, DisplayFrame, InfoFrame, InputFrame, ResultFrame
from    Util        import retrieveData, segmentAndCreateJsons
from    tkinter     import ttk
import  tkinter     as     tk
import  os

class Application(tk.Tk):
    
    def __init__(self, debug=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        self.generalPadding = 10
        
        style = ttk.Style()

        style.theme_use("clam")
        
        self.innerColor = PBLUE_COLOR

        style.configure("ContainerFrame.TFrame", background=BLUE_COLOR)
        
        style.configure("InputFrame.TFrame", background=DARK_BACKGROUND_COLOR)
        style.configure("InputFrameLabel.TLabel", background=DARK_BACKGROUND_COLOR)

        style.configure("InfoFrame.TFrame", background=self.innerColor)
        style.configure("InfoFrameLabel.TLabel", background=self.innerColor, font=("Segoe UI", 12, "bold"), foreground=BLACK_COLOR)
        
        style.configure("ControllFrame.TFrame", background=BLUE_COLOR)
        style.configure("ControllFrameSortButton.TButton", font=("Segoe UI", 11, "bold"), cursor="circle", relief="flat", borderwidth=0)
        style.configure("ControllFrameSettButton.TButton", font=("Segoe UI", 11, "bold"), cursor="circle", relief="flat", borderwidth=0)
        style.configure("ControllFrameDummyButton.TButton", font=("Segoe UI", 11, "bold"), cursor="arrow", relief="flat", borderwidth=0)
        style.map("ControllFrameDummyButton.TButton", 
                foreground=[("pressed", BLUE_COLOR), ("active", BLUE_COLOR), ("!active", BLUE_COLOR)], 
                background=[("pressed", BLUE_COLOR), ("active", BLUE_COLOR), ("!active", BLUE_COLOR)])
        style.map("ControllFrameSortButton.TButton", 
                foreground=[("pressed", WHITE_COLOR), ("active", WHITE_COLOR), ("!active", BLACK_COLOR)], 
                background=[("pressed", PINK_COLOR), ("active", ORANGE_COLOR), ("!active", GREEN_COLOR)])
        style.map("ControllFrameSettButton.TButton",
                foreground=[("pressed", WHITE_COLOR), ("active", WHITE_COLOR), ("!active", BLACK_COLOR)],
                background=[("pressed", ORANGE_COLOR), ("active", PINK_COLOR), ("!active", PINK_COLOR)])

        style.configure("DisplayFrame.TFrame", background=BLUE_COLOR)
        style.configure("DisplayFrameChangedCombobox.TCombobox", foreground=YELLOW_COLOR, fieldbackground=BLACK_COLOR)
        style.configure("DisplayFrameSortedCombobox.TCombobox", foreground=BLACK_COLOR, fieldbackground=GREEN_COLOR)
        style.configure("DisplayFrameNormalCombobox.TCombobox", foreground=BLACK_COLOR, fieldbackground=self.innerColor)

        style.configure("ResultFrame.TFrame", background=self.innerColor)
        style.configure("ResultFrameInfoLabel.TLabel", background=self.innerColor, font=("Arial", 11, "bold"), anchor="center")
        style.configure("ResultFrameDynamicLabel.TLabel", background=self.innerColor, font=("Arial", 15, "bold"), anchor="center")
        
        self.configure(background=PURPLE_COLOR)
        self.configure(padx=self.generalPadding, pady=self.generalPadding)

        self.iconbitmap(os.path.abspath("Assets/icon.ico"))

        self.title("Transcript Manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure   (0, weight=1)

        self.container = ttk.Frame(self, padding=(self.generalPadding,))
        self.container.grid(row=0, column=0)
        self.container["style"] = "ContainerFrame.TFrame"

        if debug :
            self.switchToManager()
        else :
            self.inputSection = InputFrame(self.container, self)
            self.inputSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

        self.rotateApplicationWindow()

    def retrieveTranscriptData(self, username, password, statue) :
        retrieveData(username, password, statue)
        self.inputSection.isDone = True
        self.segmentateTranscriptData()

    def segmentateTranscriptData(self):
        segmentAndCreateJsons()
        self.switchToManager()

    def switchToManager(self, *event):
        try :
            self.inputSection.grid_forget()
        except :
            pass
        
        self.infoSection = InfoFrame(self.container, self)
        self.infoSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

        self.controllSection = ControllFrame(self.container, self)
        self.controllSection.grid(row=1, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding/2)

        self.displaySection = DisplayFrame(self.container, self)
        self.displaySection.grid(row=2, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

        self.resultSection = ResultFrame(self.container, self)
        self.resultSection.grid(row=3, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding/2)

        self.rotateApplicationWindow()

    def closeProgram(self) :
        self.destroy()

    def restartProgram(self) :
        self.infoSection.grid_forget()
        self.controllSection.grid_forget()
        self.displaySection.grid_forget()
        self.resultSection.grid_forget()

        self.inputSection = InputFrame(self.container, self)
        self.inputSection.grid(row=0, column=0, sticky="nsew", padx=self.generalPadding/2, pady=self.generalPadding/2, ipadx=self.generalPadding*2, ipady=self.generalPadding*2)

    def rotateApplicationWindow(self) :
        self.update()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2), int(self.winfo_screenheight()/2 - self.winfo_reqheight()/2)))