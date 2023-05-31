from    Environment                         import SELENIUM_DC # -> Environment variables
from    selenium                            import webdriver # -> Webdriver utilization
from    selenium.webdriver.chrome.service   import Service # -> Service settlement
from    selenium.webdriver.chrome.options   import Options # -> Initialization options
from    selenium.webdriver.common.by        import By # -> Tag definer
import  os # -> OS manipulation

class Web :

    def __init__(self, driver_path = None, isHidden = True) -> None:
        """
        Constructor, that initializes selenium browser.
        @Parameters:
            driver_path - Optional : Path to the driver. (str) (default = None) -> Used to initialize the browser
            isHidden    - Optional : If the browser is hidden or not. (bool) (default = True) -> Used to initialize the browser
        @Returns:
            None
        """
        # Check if not path is given, load the default one from dataclass
        if driver_path == None :
            driver_path = SELENIUM_DC.CHROME_DRIVER_PATH

        # Change the permission of the driver for linux
        os.chmod(driver_path, 755)

        # Initalize & Load the Service and Options
        self.service = Service(executable_path=driver_path,)
        self.options = Options()

        # Add the arguments to the options
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--log-level=3")
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # If the browser is hidden, add the headless argument
        if isHidden :
            self.options.add_argument("--headless")
            
        # Initialize the browser
        self.browser = webdriver.Chrome(service=self.service, options=self.options)

        # Maximize the browser, for better view on non headless mode and better workout on headless mode
        self.browser.maximize_window()

    def open_web_page(self, url : str) -> None:
        """
        Public Class Method, that opens a web page.
        @Parameters:
            url - Required : Url of the web page. (str) -> Used to open the web page
        @Returns:
            None
        """
        # Open the web page
        self.browser.get(url)

    def go_back(self) -> None:
        """
        Public Class Method, that goes back to the previous page.
        @Parameters:
            None
        @Returns:
            None
        """
        # Go back to the previous page
        self.browser.back()

    def terminate_client(self) -> None:
        """
        Public Class Method, that terminates the browser.
        @Parameters:
            None
        @Returns:
            None
        """
        # Terminate the browser
        self.browser.quit()

    def create_element(self, xPath : str) -> None:
        """
        Public Class Method, that creates an element. With certain quarantees likewise the loop.
        @Parameters:
            xPath - Required : XPath of the element. (str) -> Used to create the element
        @Returns:
            None
        """
        createdElement = None
        # While the element is not created, try to create it until it is created
        while (createdElement == None) :
            try :
                createdElement = self.browser.find_element(By.XPATH, xPath)
            except :
                continue
        # Return the created element
        return createdElement

    def click_on_element(self, element : object) -> None:
        """
        Public Class Method, that clicks on an element. With certain quarantees likewise the loop.
        @Parameters:
            element - Required : Element to be clicked. (object) -> Used to click on the element
        @Returns:
            None
        """
        # While the element is not clicked, try to click it until it is clicked
        while (True) :
            try :
                element.click()
                break
            except :
                continue