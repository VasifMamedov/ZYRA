import pytest
import tempfile
import os
from src import create_app
from src import admin
from src.commands import init_db, populate_db


@pytest.fixture
def app():
    db_path, db_file = tempfile.mkstemp()
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'DEBUG': False,
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{db_file}.sqlite"
    })

    admin._views = []

    with app.app_context():
        init_db()
        populate_db()

    yield app
    os.close(db_path)
    os.unlink(db_file)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def server(app):
    return app.test_cli_runner()