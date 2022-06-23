from sqlalchemy import false
from sympy import true
from    Util    import secureStart, secureFinish
from    GUI     import Application

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

if __name__ == "__main__":
    debug = False
    
    secureStart(debug)

    app = Application(debug=debug)
    app.mainloop()

    secureFinish(debug)