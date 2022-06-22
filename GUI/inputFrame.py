from    PIL         import  Image, ImageTk
from    Util        import  authenticate
from    tkinter     import  PhotoImage
from    tkinter     import  ttk
import  tkinter     as      tk
import  threading

class InputFrame(ttk.Frame):
    
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.root = root

        self.gifFrames = [PhotoImage(file='Assets/loader3.gif',format = 'gif -index %i' %(i)) for i in range(150)]
        self.isDone = False

        self.username = tk.StringVar(value="")
        self.password = tk.StringVar(value="")
        self.errorMessage = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.logoImg = ImageTk.PhotoImage(Image.open("Assets\mefLogo.png").resize((194, 126), Image.ANTIALIAS))
        logoLabel = ttk.Label(self, image=self.logoImg, padding=(self.root.generalPadding), anchor="center")

        usernameLabel = ttk.Label(self, text="User Name", font=("Segoe UI", 13, "bold"), foreground="#4E5963")
        usernameEntry = ttk.Entry(self, font=("Segoe UI", 11, "bold"), foreground="gray38", textvariable=self.username)

        passwordLabel = ttk.Label(self, text="Password", font=("Segoe UI", 13, "bold"), foreground="#4E5963")
        passwordEntry = ttk.Entry(self, show="*", font=("Segoe UI", 11, "bold"), foreground="gray38", textvariable=self.password)
        
        self.errorMessageLabel = ttk.Label(self, textvariable=self.errorMessage, font=("Segoe UI", 9, "bold"), foreground="red", anchor="center")
        
        self.loginButton = tk.Button(self, text="Login", font=("Segoe UI", 14, "bold"), foreground="white", background="#27AE60", command=self.checkLogin, disabledforeground="gray90")

        self.gifLabel = ttk.Label(self, padding=(self.root.generalPadding), anchor="center")

        self.root.bind("<Return>", self.checkLogin)

        logoLabel.grid(row=0, column=0, sticky="nsew")
        usernameLabel.grid(row=1, column=0, sticky="nsew")
        usernameEntry.grid(row=2, column=0, sticky="nsew")
        passwordLabel.grid(row=3, column=0, sticky="nsew")
        passwordEntry.grid(row=4, column=0, sticky="nsew")
        self.errorMessageLabel.grid(row=5, column=0, sticky="nsew", pady=self.root.generalPadding/1.3)
        self.loginButton.grid(row=6, column=0, sticky="nsew")

    def checkLogin(self, *event):
        
        if self.username.get() == "" or self.password.get() == "" or self.username.get() == " " or self.password.get() == " " :
            self.updateErrorMessage("Please fill in all fields !", "red")
            self.root.after(500, self.clearErrorMessage)
            return
        
        isLoginSuccesfull = authenticate(self.username.get(), self.password.get())

        if isLoginSuccesfull :
            self.updateErrorMessage("Login succesfull! Retrieving transcript...", "green")
            self.loginButton.config(state="disabled")
            self.loginButton.config(text="Logged in")
            self.startRetrievalAndReportUser()
        else :
            self.updateErrorMessage("Wrong username or password !", "red")
            self.root.after(750, self.clearErrorMessage)
            
    def updateErrorMessage(self, message, messageColor) :
        self.errorMessage.set(message)
        self.errorMessageLabel.config(foreground=messageColor)

    def clearErrorMessage(self) : 
        self.errorMessage.set("")

    def showGif(self, frameIndex) :

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
        
        self.root.after(20, self.showGif, frameIndex)

    def startRetrievalAndReportUser(self) :

        self.root.after(0, self.showGif, 0)

        retrievalT = threading.Thread(target=self.root.retrieveTranscriptData, args=(self.username.get(), self.password.get(), True))
        retrievalT.start()