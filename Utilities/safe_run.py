from    Environment import EXECUTION_DC, PACKAGES_DC, SELENIUM_DC
from    Environment import connect_urls
from    sys         import platform
import  requests
import  colorama
import  shutil
import  os
from Utilities import check_internet_connection, get_connection_details, download_chrome_driver

log_style = {
    "ASCII" : {
        "PROCCESS" : "\n***LOGGER (⌐■_■)",
        "SUCCESS"  : "\t\t|\n\t\t|__LOGGER (～￣▽￣)～ ->",
        "FAILURE"  : "\t\t|\n\t\t|__LOGGER (ﾉ ﾟｰﾟ)ﾉ ->",
    },
    "CONSOLE" : {
        "PROCCESS" : "***LOG",
        "SUCCESS"  : "     |_LOG",
        "FAILURE"  : "     |_LOG",
    }
}
ASCII_LOG = log_style["CONSOLE"]

"""
EXECUTION_DC = ExecutionDC(
    PRE_EXISTING_CHECKLIST_MUST = [ASSETS_FOLDER, CONSTANTS_FOLDER, GUI_FOLDER, UTILITIES_FOLDER],
    PRE_EXISTING_CHECKLIST_RELATIVE = [SOURCES_FOLDER, TEMP_FOLDER],
    POST_CACHE_CLEANUP_LIST = [CONSTANTS_FOLDER, GUI_FOLDER, UTILITIES_FOLDER],
    POST_CLEANUP_LIST = [SOURCES_FOLDER, TEMP_FOLDER]
)

"""

def safe_start() -> None:
    
    def __checkout_pre_existing_checklist_must() -> None:
        # Check for folders that must exist. If not, terminate the application.
        print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for required modules...", colorama.Fore.RESET)
        pre_existing_checklist_must_STATUS = []
        for current_folder_path in EXECUTION_DC.PRE_EXISTING_CHECKLIST_MUST :
            if not os.path.exists(current_folder_path) :
                pre_existing_checklist_must_STATUS.append(os.path.basename(current_folder_path))
        if pre_existing_checklist_must_STATUS :
            print(colorama.Fore.RED, ASCII_LOG["FAILURE"], f"The following modules are missing -> {pre_existing_checklist_must_STATUS}", colorama.Fore.RESET)
            exit()
        else :
            print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All required modules approved -> {[os.path.basename(fname) for fname in EXECUTION_DC.PRE_EXISTING_CHECKLIST_MUST]}", colorama.Fore.RESET)

    def __checkout_pre_existing_checklist_relative() -> None:
        # Check for folders that should exist. If not, create them. If yes, clean them.
        print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for relative packs...", colorama.Fore.RESET)
        pre_existing_checklist_relative_STATUS = []
        for current_folder_path in EXECUTION_DC.PRE_EXISTING_CHECKLIST_RELATIVE :
            if not os.path.exists(current_folder_path) :
                pre_existing_checklist_relative_STATUS.append(os.path.basename(current_folder_path))
                os.mkdir(current_folder_path)
        if pre_existing_checklist_relative_STATUS :
            print(colorama.Fore.BLUE, ASCII_LOG["SUCCESS"], f"The following packs created -> {pre_existing_checklist_relative_STATUS}", colorama.Fore.RESET)
        else :
            print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"All relative packs approved -> {[os.path.basename(fname) for fname in EXECUTION_DC.PRE_EXISTING_CHECKLIST_RELATIVE]}", colorama.Fore.RESET)
    
    def __checkout_internet_connection() -> None:
        # Check for internet connection. If not, terminate the application.
        print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for internet connection...", colorama.Fore.RESET)    
        retrieval = check_internet_connection()
        if retrieval : 
            print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Internet connection established -> {get_connection_details()}", colorama.Fore.RESET)
        else :
            print(colorama.Fore.RED, ASCII_LOG["ERROR"], f"Internet connection failrue", colorama.Fore.RESET)
            exit()

    def __checkout_chrome_driver() -> None:
        # Check for chrome driver. If not, download it.
        print(colorama.Fore.YELLOW, ASCII_LOG["PROCCESS"], f"Checking for chrome driver...", colorama.Fore.RESET)
        if not os.path.exists(SELENIUM_DC.CHROME_DRIVER_PATH) :
            print(colorama.Fore.BLUE, ASCII_LOG["SUCCESS"], f"Chrome driver not found. Downloading...", colorama.Fore.RESET)
            is_download_successfull, message = download_chrome_driver()
            if is_download_successfull :
                print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Chrome driver downloaded successfully -> {message}", colorama.Fore.RESET)
            else :
                print(colorama.Fore.RED, ASCII_LOG["FAILURE"], f"Chrome driver download failed -> {message}", colorama.Fore.RESET)
                exit()
        else :
            print(colorama.Fore.GREEN, ASCII_LOG["SUCCESS"], f"Chrome driver found -> {SELENIUM_DC.CHROME_DRIVER_PATH}", colorama.Fore.RESET)

    __checkout_pre_existing_checklist_must()
    __checkout_pre_existing_checklist_relative()
    __checkout_internet_connection()
    __checkout_chrome_driver()

def safe_end() -> None:
    pass