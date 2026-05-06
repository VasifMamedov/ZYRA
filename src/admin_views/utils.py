from uuid import uuid4
from os import path

def generate_filename(object, file):
    name, extension = path.splitext(file.filename)
    return f"{uuid4()}{extension}"