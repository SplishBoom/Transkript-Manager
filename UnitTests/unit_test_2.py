"""
UT : GUI --> Login
"""

from GUI import TranscriptManager

if __name__ == "__main__" :

    try :
        TranscriptManager().mainloop()
    except Exception as e :
        print(e)
        print("Unit test 2 failed")