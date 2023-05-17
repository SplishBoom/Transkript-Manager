from PIL import Image
import requests

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

    logUrl = "https://sis.mef.edu.tr/auth/login/ln/tr"
    secUrl = "https://sis.mef.edu.tr/"

    payload = {"kullanici_adi": username, "kullanici_sifre": password}
    
    with requests.Session() as s:
        s.post(logUrl, data=payload)
        r = s.get(secUrl)

        if r.url == secUrl:
            return True

    return False

def validate_transcript(pdf) :
    return True

def get_gender(name) :
    return None