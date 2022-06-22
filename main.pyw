from    Util    import secureStart, secureFinish
from    GUI     import Application

if __name__ == "__main__":
    
    debug = False

    secureStart(debug)

    app = Application(debug=debug)
    app.mainloop()

    secureFinish(debug)