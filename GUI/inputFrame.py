from    tkinter     import  ttk
from    PIL         import  Image, ImageTk
from    bs4         import  BeautifulSoup
import  tkinter     as      tk
import  requests

class InputFrame(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.username = tk.StringVar(value="memise")
        self.password = tk.StringVar(value="492v5fwu")
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
        
        loginButton = tk.Button(self, text="Login", font=("Segoe UI", 14, "bold"), foreground="white", background="#27AE60", command=self.checkLogin)

        self.bind("<Return>", self.checkLogin)

        logoLabel.grid(row=0, column=0, sticky="nsew")
        usernameLabel.grid(row=1, column=0, sticky="nsew")
        usernameEntry.grid(row=2, column=0, sticky="nsew")
        passwordLabel.grid(row=3, column=0, sticky="nsew")
        passwordEntry.grid(row=4, column=0, sticky="nsew")
        self.errorMessageLabel.grid(row=5, column=0, sticky="nsew", pady=self.root.generalPadding/1.3)
        loginButton.grid(row=6, column=0, sticky="nsew", ipadx=self.root.generalPadding*2, ipady=self.root.generalPadding/5)

    def checkLogin(self, *event):
        
        if self.username.get() == "" or self.password.get() == "" or self.username.get() == " " or self.password.get() == " " :
            self.errorMessage.set("Please fill in all fields !")
            self.errorMessageLabel.config(foreground="red")
            return
        
        if True :
            logUrl = "https://sis.mef.edu.tr/auth/login/ln/tr"
            secUrl = "https://sis.mef.edu.tr/"

            payload = {
                "kullanici_adi": self.username.get(),
                "kullanici_sifre": self.password.get()
            }
            
            with requests.Session() as s:
                s.post(logUrl, data=payload)
                r = s.get(secUrl)
                soup = BeautifulSoup(r.content, "html.parser")

                if r.url != secUrl:
                    self.errorMessage.set("Wrong username or password !")
                    self.errorMessageLabel.config(foreground="red")
                else :
                    self.errorMessage.set("Login succesfull! Retrieving transcript...")
                    self.errorMessageLabel.config(foreground="green")
                    self.root.retrieveTranscript()