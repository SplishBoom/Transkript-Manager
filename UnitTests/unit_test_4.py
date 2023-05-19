"""
UT : safe_start() and safe_end() test
"""

from Utilities import safe_start, safe_end

if __name__ == '__main__':
    try :
        safe_start()
        """
            DRIVER CODE HERE
        """
        safe_end()
        print("Unit test 4 passed")
    except Exception as e :
        print(e)
        print("Unit test 4 failed")
        