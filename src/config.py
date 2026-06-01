import os
from os import path


class Config(object):
    BASE_DIRECTORY = path.abspath(path.dirname(__file__))


    DATABASE_URL = os.environ.get('DATABASE_URL')

    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{path.join(BASE_DIRECTORY, 'database.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')

    UPLOAD_PATH = path.join(BASE_DIRECTORY, 'static', 'upload')


    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_SUPPORTED_LOCALES = ['en', 'tr', 'ka']
    LANGUAGES = {
        'en': 'English',
        'tr': 'Türkçe',
        'ka': 'ქართული'
    }