from    PIL         import  Image, ImageTk
from    Util        import  authenticate
from    tkinter     import  PhotoImage
from    tkinter     import  ttk
import  tkinter     as      tk
import  threading
import  json
import  os

class InputFrame(ttk.Frame):
    
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.root = root

        self["style"] = "InputFrame.TFrame"

        self.configure(relief="flat", borderwidth=10)

        fileName = "loader"
        fileExtension = ".gif"
        fileFolder = "Assets"
        filePath = os.path.abspath(fileFolder+"/"+fileName+fileExtension)
        self.gifFrames = [PhotoImage(file=filePath, format = 'gif -index %i' %(i)) for i in range(150)]
        
        self.isDone = False
        self.autoLogin = False
        self.loadedFromPayload = False

        self._loadPayload()
        self.errorMessage = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        fileName = "mefLogo"
        fileExtension = ".png"
        fileFolder = "Assets"
        filePath = os.path.abspath(fileFolder+"/"+fileName+fileExtension)
        self.logoImg = ImageTk.PhotoImage(Image.open(filePath).resize((194, 126), Image.ANTIALIAS))
        logoLabel = ttk.Label(self, image=self.logoImg, padding=(self.root.generalPadding), anchor="center", cursor="heart", style="InputFrameLabel.TLabel")

        usernameLabel = ttk.Label(self, text="User Name", font=("Segoe UI", 13, "bold"), foreground="#4E5963", style="InputFrameLabel.TLabel")
        usernameEntry = ttk.Entry(self, font=("Segoe UI", 11, "bold"), foreground="gray38", textvariable=self._username)

        passwordLabel = ttk.Label(self, text="Password", font=("Segoe UI", 13, "bold"), foreground="#4E5963", style="InputFrameLabel.TLabel")
        passwordEntry = ttk.Entry(self, show="*", font=("Segoe UI", 11, "bold"), foreground="gray38", textvariable=self._password)
        
        self.errorMessageLabel = ttk.Label(self, textvariable=self.errorMessage, font=("Segoe UI", 9, "bold"), foreground="red", anchor="center", style="InputFrameLabel.TLabel")
        
        self.loginButton = tk.Button(self, text="Login", font=("Segoe UI", 14, "bold"), foreground="white", background="#27AE60", command=self._checkLogin, disabledforeground="gray90", cursor="exchange")

        self.gifLabel = ttk.Label(self, padding=(self.root.generalPadding), anchor="center", style="InputFrameLabel.TLabel")

        self.root.bind("<Return>", self._checkLogin)
        
        logoLabel.grid(row=0, column=0, sticky="ew")
        usernameLabel.grid(row=1, column=0, sticky="ew")
        usernameEntry.grid(row=2, column=0, sticky="ew")
        passwordLabel.grid(row=3, column=0, sticky="ew")
        passwordEntry.grid(row=4, column=0, sticky="ew")
        self.errorMessageLabel.grid(row=5, column=0, sticky="ew", pady=self.root.generalPadding/1.3)
        self.loginButton.grid(row=6, column=0, sticky="ew")

        if self.autoLogin :
            print("Auto login is enabled, logging in automatically...")
            self.after(150, self._checkLogin)

    def _loadPayload(self) :
        
        try :
            with open(os.path.abspath("Sources/payload.json"), "r", encoding="utf-8") as payloadFile :
                payload = json.load(payloadFile)

            self._username = tk.StringVar(value=payload["username"])
            self._password = tk.StringVar(value=payload["password"])

            print("Payload loaded successfully. Your credentials are entered automatically.")

            self.autoLogin = payload["autoLogin"]

            self.loadedFromPayload = True
        except :
            print("Could not load ./Sources/payload file, you have to enter your credentials manually.")
            self._username = tk.StringVar(value="")
            self._password = tk.StringVar(value="")

    def _checkLogin(self, *event):
        
        if self._username.get() == "" or self._password.get() == "" or self._username.get() == " " or self._password.get() == " " :
            if self.loadedFromPayload :
                self._updateErrorMessage("Please check payload file !", "red")
            else :
                self._updateErrorMessage("Please fill in all fields !", "red")
            self.root.after(500, self._clearErrorMessage)
            return
        
        isLoginSuccesfull = authenticate(self._username.get(), self._password.get())

        if isLoginSuccesfull :
            if self.loadedFromPayload :
                self._updateErrorMessage("Payload succesfull! Retrieving transcript...", "green")
            else :
                self._updateErrorMessage("Login succesfull! Retrieving transcript...", "green")
            self.loginButton.config(state="disabled")
            self.loginButton.config(text="Logged in")
            self._startRetrievalAndReportUser()
        else :
            if self.loadedFromPayload :
                self._updateErrorMessage("Please check payload file !", "red")
            else :
                self._updateErrorMessage("Wrong username or password !", "red")
            self.root.after(750, self._clearErrorMessage)
            
    def _updateErrorMessage(self, message, messageColor) :
        self.errorMessage.set(message)
        self.errorMessageLabel.config(foreground=messageColor)

    def _clearErrorMessage(self) : 
        self.errorMessage.set("")

    def _showGif(self, frameIndex) :

        if self.isDone :
            return

        self.currentFrame = self.gifFrames[frameIndex]
        frameIndex += 1

        if frameIndex == 1 :
            self.gifLabel.configure(image=self.currentFrame)
            self.gifLabel.grid(row=7, column=0, sticky="nsew")
        elif frameIndex == 150 :
            frameIndex = 0
    
        self.gifLabel.configure(image=self.currentFrame)
        
        self.root.after(20, self._showGif, frameIndex)

    def _startRetrievalAndReportUser(self) :

        self.root.after(0, self._showGif, 0)

        retrievalT = threading.Thread(target=self.root.retrieveTranscriptData, args=(self._username.get(), self._password.get(), True))
        retrievalT.start()