from PIL import Image
import PIL
import os
import requests
import time
import pytesseract
import config

def clean_up(dir):
    for file in os.listdir(dir):
        fpath = os.path.join(dir, file)
        os.remove(fpath)
        print("Cleanup:", file, "removed")

def create_dir(dir) -> str:
    parentPath = '.'
    # path = os.path.join(parentPath, dir)
    path = dir
    try:
        os.mkdir(path)
    except FileExistsError:
        clean_up(path)
    except FileNotFoundError:
        print(FileNotFoundError)
    finally:
        return path


def get_string(img_object) -> str:

    pytesseract.pytesseract.tesseract_cmd = config.TESS_DRIVER
    result = pytesseract.image_to_string(img_object)
        
    return result

def captcha_decode(captcha_url : str, dirpath : str = ".\\temp") -> str:
    while True:
        url = captcha_url
        r = requests.get(url)

        filename = 'captchaImage' + str(int(time.time())) + '.jpg'
        fpath = os.path.join(dirpath, filename)

        with open(fpath, 'wb') as out_file:
            out_file.write(r.content)

        try:
            img = Image.open(fpath)
            break
        except PIL.UnidentifiedImageError:
            continue
    return ''.join( get_string(img).split() ).upper()[:5]
