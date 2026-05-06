from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from src.admin_views.base import SecureIndexView
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel

babel = Babel()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
admin = Admin(name="Python Panel", index_view=SecureIndexView())
