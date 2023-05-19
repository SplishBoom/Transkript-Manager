from PIL import Image
import requests
from Environment import UTILITIES_DC, PACKAGES_DC, connect_urls, SELENIUM_DC
import socket
import subprocess
import os
import platform
import re
from    bs4         import BeautifulSoup
import  io
from win32com.client import Dispatch


import  zipfile


def get_gif_frame_count(gif_file_path:str) -> int:
    """
    Method, that returns the number of frames in a gif file.
    @Params
        gif_file_path : str - (Required) The path to the gif file.
    @Returns
        number_of_frames : int - The number of frames in the gif file.
    """

    with Image.open(gif_file_path) as gif_file:
        number_of_frames = 0
        while True:
            try:
                gif_file.seek(number_of_frames)
                number_of_frames += 1
            except EOFError:
                break

    return number_of_frames

def authenticate(username, password) :

    payload = UTILITIES_DC.AUTH_PAYLOAD
    payload.update(kullanici_adi=username, kullanici_sifre=password)

    with requests.Session() as s:
        s.post(UTILITIES_DC.AUTH_LOG_URL, data=payload)
        r = s.get(UTILITIES_DC.AUTH_SEC_URL)

        if r.url == UTILITIES_DC.AUTH_SEC_URL:
            return True

    return False

def check_internet_connection() :
    try :
        requests.get(PACKAGES_DC.CONNECTION_TEST_URL)
        return True
    except :
        return False
    
def get_connection_details() :
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    port = socket.getservbyname("http", "tcp")
    try :
        ssid = subprocess.check_output('netsh wlan show interfaces | findstr SSID', shell=True).decode('utf-8').split(':')[1].strip()
        ssid = ssid[ssid.find(":")+1:ssid.find("\n")-1]
    except :
        ssid = "~Ethernet"

    return (hostname, address, port, ssid)

def download_chrome_driver() -> tuple:

    def get_chrome_version() -> str:

        parser = Dispatch("Scripting.FileSystemObject")

        try :
            version = parser.GetFileVersion(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        except :
            try :
                version = parser.GetFileVersion(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            except :
                return None

        version_base = version.split(".")[0]

        return version_base

    version_base = get_chrome_version()

    if version_base is None :
        return (False, "Couldn't find acceptable chrome version, please check your chrome installation.")

    version_base = version_base.split(".")[0]

    download_page_response = requests.get(PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_URL)

    parsed_page = BeautifulSoup(download_page_response.text, "html.parser")

    all_versions = parsed_page.find_all("a", class_="XqQF9c")

    for current_version in all_versions :

        if current_version.text.split(" ")[1].startswith(version_base) :
            official_version = current_version.text.split(" ")[1]
            break       

    file_download_url = connect_urls(PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_PARTITION["base"], official_version, PACKAGES_DC.CHROME_DRIVER_DOWNLOAD_PARTITION["args"])

    download_response = requests.get(file_download_url)
    zipFile = zipfile.ZipFile(io.BytesIO(download_response.content))
    zipFile.extractall(PACKAGES_DC.EXTRACTION_SITE)

    return True, SELENIUM_DC.CHROME_DRIVER_PATH

def validate_transcript(pdf) :
    return True

def get_gender(name) :
    return None