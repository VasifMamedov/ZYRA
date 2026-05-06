from os import path

class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = 'AWDWQDASDSAFHSFJWIasjdalskfjqwoijf@1234098'

    BASE_DIRECTORY = path.abspath(path.dirname(__file__))
    UPLOAD_PATH = path.join(BASE_DIRECTORY, 'static', 'upload')

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_SUPPORTED_LOCALES = ['en', 'tr', 'ka']
    LANGUAGES = {
        'en': 'English',
        'tr': 'Türkçe',
        'ka': 'ქართული'
    }