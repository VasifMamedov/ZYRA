from os import path
import os

class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'secret'

    BASE_DIRECTORY = path.abspath(path.dirname(__file__))
    UPLOAD_PATH = path.join(BASE_DIRECTORY, 'static', 'upload')

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_SUPPORTED_LOCALES = ['en', 'tr', 'ka']
    LANGUAGES = {
        'en': 'English',
        'tr': 'Türkçe',
        'ka': 'ქართული'
    }