from os import path
from dataclasses import dataclass

def connect_pathes(*pathes): return path.join(*pathes)

PROJECT_DIRECTORY = path.dirname(path.dirname(path.abspath(__file__)))

ASSETS_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Assets")
CONSTANTS_FOLDER = connect_pathes(PROJECT_DIRECTORY, "Constants")
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
    MAN_PP : str
    WOMAN_PP : str

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
    OLEXER_PROFILE_SELECTION_XPATH : str
    OLEXER_DROP_DOWN_MENU_XPATH : str
    OLEXER_ID_SELECTION_XPATH : str
    OLEXER_TRANSCRIPT_URL : str
    
@dataclass
class PackagesDC:
    CHROME_DRIVER_DOWNLOAD_URL : str
    CONNECTION_TEST_URL : str
    CHROME_DRIVER_DOWNLOAD_PARTITION : dict

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

EXECUTION_DC = ExecutionDC(
    PRE_EXISTING_CHECKLIST_MUST = [ASSETS_FOLDER, CONSTANTS_FOLDER, GUI_FOLDER, UTILITIES_FOLDER],
    PRE_EXISTING_CHECKLIST_RELATIVE = [SOURCES_FOLDER, TEMP_FOLDER],
    POST_CACHE_CLEANUP_LIST = [CONSTANTS_FOLDER, GUI_FOLDER, UTILITIES_FOLDER],
    POST_CLEANUP_LIST = [SOURCES_FOLDER, TEMP_FOLDER]
)
ASSETS_DC = AssetsDC(
    LOADING_ANIMATION_PATH = connect_pathes(ASSETS_FOLDER, "loader.gif"),
    LOGO_PATH = connect_pathes(ASSETS_FOLDER, "mef logo.png"),
    MAN_PP = connect_pathes(ASSETS_FOLDER, "man.png"),
    WOMAN_PP = connect_pathes(ASSETS_FOLDER, "woman.png")
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
    OLEXER_PROFILE_SELECTION_XPATH = "/html/body/div[2]/div/div[3]/ul/li",
    OLEXER_DROP_DOWN_MENU_XPATH = "/html/body/div[2]/div/div[3]/ul/li/ul",
    OLEXER_ID_SELECTION_XPATH = "//*[@id=\"yetkiDegistir\"]/div/ul",
    OLEXER_TRANSCRIPT_URL = "https://sis.mef.edu.tr/ogrenciler/belge/transkript"
)
PACKAGES_DC = PackagesDC(
    CHROME_DRIVER_DOWNLOAD_URL = "https://chromedriver.chromium.org/downloads",
    CONNECTION_TEST_URL = "https://www.google.com",
    CHROME_DRIVER_DOWNLOAD_PARTITION = {"base":"https://chromedriver.storage.googleapis.com", "args":"chromedriver_win32.zip"}
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