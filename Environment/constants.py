from os import path
from dataclasses import dataclass

def connect_pathes(*pathes): return path.join(*pathes)
def connect_urls(*urls): return "/".join(urls)

PROJECT_DIRECTORY = path.dirname(path.dirname(path.abspath(__file__)))

ASSETS_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Assets")
ENVIRONMENT_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Environment")
GUI_FOLDER = connect_pathes(PROJECT_DIRECTORY, "GUI")
SOURCES_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Sources")
TEMP_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Temp")
UTILITIES_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Utilities")

@dataclass
class ExecutionDC:
    PRE_EXISTING_CHECKLIST_MUST: list
    PRE_EXISTING_CHECKLIST_RELATIVE: list
    POST_CACHE_CLEANUP_LIST: list
    POST_CLEANUP_LIST: list

@dataclass
class AssetsDC:
    LOADING_ANIMATION_PATH : str
    LOGO_PATH : str
    ICON : str
    GENDERS_PHOTO_PATH : dict
    LEFT_ARROW_PATH : str
    RIGHT_ARROW_PATH : str

@dataclass
class SeleniumDC:
    CHROME_DRIVER_PATH : str
    USER_PHOTO_OUTPUT_PATH : str
    OLEXER_SYSTEM_LOGIN_URL : str
    OLEXER_USERNAME_ENTRY_XPATH : str
    OLEXER_PASSWORD_ENTRY_XPATH : str
    OLEXER_LOGIN_BUTTON_XPATH : str
    OLEXER_CONTINUE_BUTTON_XPATH : str
    OLEXER_USER_PHOTO_LABEL_XPATH : str
    OLEXER_SOURCE_ATTRIBUTE_TAGS : list
    OLEXER_PROFILE_SELECTION_XPATH : str
    OLEXER_DROP_DOWN_MENU_XPATH : str
    OLEXER_ID_SELECTION_XPATH : str
    OLEXER_TRANSCRIPT_URL : str

@dataclass
class PackagesDC:
    CHROME_DRIVER_DOWNLOAD_URL : str
    CONNECTION_TEST_URL : str
    CHROME_DRIVER_DOWNLOAD_PARTITION : dict
    EXTRACTION_SITE : str

@dataclass
class UtilitiesDC:
    AUTH_LOG_URL : str
    AUTH_SEC_URL : str
    AUTH_PAYLOAD : dict

@dataclass
class DatabaseDC:
    CONNECTION_STRING : str
    DATABASE_NAME : str
    COLLECTION_NAMES : dict

@dataclass
class GUIDC:
    TITLE : str

EXECUTION_DC = ExecutionDC(
    PRE_EXISTING_CHECKLIST_MUST = [ASSETS_FOLDER, ENVIRONMENT_FOLDER, GUI_FOLDER, UTILITIES_FOLDER],
    PRE_EXISTING_CHECKLIST_RELATIVE = [SOURCES_FOLDER, TEMP_FOLDER],
    POST_CACHE_CLEANUP_LIST = [ENVIRONMENT_FOLDER, GUI_FOLDER, UTILITIES_FOLDER],
    POST_CLEANUP_LIST = [TEMP_FOLDER],
)
ASSETS_DC = AssetsDC(
    LOADING_ANIMATION_PATH = connect_pathes(ASSETS_FOLDER, "animated", "loader.gif"),
    LOGO_PATH = connect_pathes(ASSETS_FOLDER, "mef", "logo.png"),
    ICON = connect_pathes(ASSETS_FOLDER, "ui", "icon.ico"),
    GENDERS_PHOTO_PATH = {
        "andy" : connect_pathes(ASSETS_FOLDER, "user", "andy.png"),
        "female" : connect_pathes(ASSETS_FOLDER, "user", "female.png"),
        "male" : connect_pathes(ASSETS_FOLDER, "user", "male.png"),
        "mostly_female" : connect_pathes(ASSETS_FOLDER, "user", "mostly_female.png"),
        "mostly_male" : connect_pathes(ASSETS_FOLDER, "user", "mostly_male.png"),
        "unknown" : connect_pathes(ASSETS_FOLDER, "user", "unknown.png"),
    },
    LEFT_ARROW_PATH = connect_pathes(ASSETS_FOLDER, "ui", "left_arrow.png"),
    RIGHT_ARROW_PATH = connect_pathes(ASSETS_FOLDER, "ui", "right_arrow.png"),
)
SELENIUM_DC = SeleniumDC(
    CHROME_DRIVER_PATH = connect_pathes(SOURCES_FOLDER, "chromedriver.exe"),
    USER_PHOTO_OUTPUT_PATH = connect_pathes(TEMP_FOLDER, "user_photo.png"),
    OLEXER_SYSTEM_LOGIN_URL = "https://sis.mef.edu.tr/auth/login",
    OLEXER_USERNAME_ENTRY_XPATH = "//*[@id=\"kullanici_adi\"]",
    OLEXER_PASSWORD_ENTRY_XPATH = "//*[@id=\"kullanici_sifre\"]",
    OLEXER_LOGIN_BUTTON_XPATH = "//*[@id=\"loginForm\"]/div[2]/div[3]/button",
    OLEXER_CONTINUE_BUTTON_XPATH = "/html/body/div[3]/input",
    OLEXER_USER_PHOTO_LABEL_XPATH = "/html/body/div[2]/div/div[3]/ul/li/a/img",
    OLEXER_SOURCE_ATTRIBUTE_TAGS = ["src", "text", "table"],
    OLEXER_PROFILE_SELECTION_XPATH = "/html/body/div[2]/div/div[3]/ul/li",
    OLEXER_DROP_DOWN_MENU_XPATH = "/html/body/div[2]/div/div[3]/ul/li/ul",
    OLEXER_ID_SELECTION_XPATH = "//*[@id=\"yetkiDegistir\"]/div/ul",
    OLEXER_TRANSCRIPT_URL = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
)
PACKAGES_DC = PackagesDC(
    CHROME_DRIVER_DOWNLOAD_URL = "https://chromedriver.chromium.org/downloads",
    CONNECTION_TEST_URL = "https://www.google.com",
    CHROME_DRIVER_DOWNLOAD_PARTITION = {"base":"https://chromedriver.storage.googleapis.com", "args":"chromedriver_win32.zip"},
    EXTRACTION_SITE = SOURCES_FOLDER
)
UTILITIES_DC = UtilitiesDC(
    AUTH_LOG_URL = "https://sis.mef.edu.tr/auth/login/ln/tr",
    AUTH_SEC_URL = "https://sis.mef.edu.tr/",
    AUTH_PAYLOAD = {"kullanici_adi": None, "kullanici_sifre": None}
)
DATABASE_DC = DatabaseDC(
    CONNECTION_STRING = "mongodb://localhost:27017/",
    DATABASE_NAME = "trman",
    COLLECTION_NAMES = {"__user_info_collection_define" : "user_info", "__user_data_collection_define" : "user_data"}
)
GUI_DC = GUIDC(
    TITLE = "Transcript Manager",
)

log_style = {
    "ASCII" : {
        "PROCCESS" : "\n***LOGGER (⌐■_■)",
        "SUCCESS"  : "\t\t|\n\t\t|__LOGGER (～￣▽￣)～ ->",
        "FAILURE"  : "\t\t|\n\t\t|__LOGGER (ﾉ ﾟｰﾟ)ﾉ ->",
        "ERROR"    : "\t\t|\n\t\t|__LOGGER (╯ °□°）╯ ->"
    },
    "CONSOLE" : {
        "PROCCESS" : "***LOG",
        "SUCCESS"  : "     |_LOG",
        "FAILURE"  : "     |_LOG",
        "ERROR"    : "     |_LOG"
    }
}
ASCII_LOG = log_style["CONSOLE"]

DEBUG = True