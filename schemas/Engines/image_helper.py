import os
import re

from typing import Union
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet,IMAGES

IMAGE_SET = UploadSet(name='images',extensions=IMAGES)

def save_image(image:FileStorage,folder:str = None,name:str = None)->str:
    return IMAGE_SET.save(storage=image,folder=folder,name=name)

def get_path(folder:str = None,name:str = None)->str:
    return IMAGE_SET.path(folder=folder,filename=name)

def find_image_any_format(folder:str = None,name:str = None)->str:
    for _format in IMAGES:
        image = f"{name}.{_format}"
        image_path = IMAGE_SET.path(filename=image,folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None

def _retrieve_filename(file:Union[FileStorage,str])->str:
    if isinstance(file,FileStorage):
        return file.name
    return file

def is_filename_safe(file:Union[FileStorage,str])->bool:
    filename = _retrieve_filename(file)
    allowed_format = '|'.join(IMAGES)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None

def get_basename(file:Union[FileStorage,str]):
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension(file:Union[FileStorage,str])->str:
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]