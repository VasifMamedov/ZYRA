from flask import Flask, render_template, session

from src.views import auth_blueprint, main_blueprint, product_blueprint
from src.ext import db, migrate, login_manager, admin, csrf, babel
from src.config import Config
from src.commands import init_db_command, populate_db_command
from src.models import User, Product, Favorite
from src.admin_views.base import SecureModelView
from src.admin_views.product import ProductView
from src.admin_views.category import CategoryView
from src.models.category import Category

BLUEPRINTS = [auth_blueprint, main_blueprint, product_blueprint

              ]


COMMANDS = [
    init_db_command, populate_db_command
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_error_handlers(app)
    return app

    #ERRORS#


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500




def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def get_locale():
    return session.get('lang', 'en')


def register_extensions(app):

    #babel

    babel.init_app(app, locale_selector=get_locale)

    #Flask-SQLAlchemy

    db.init_app(app)

    #Flask-Migrate
    migrate.init_app(app, db)

    #Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    #Flask-Admin
    admin.init_app(app)
    admin.add_view(ProductView(Product, db.session))
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(CategoryView(Category, db.session))

    #CSRF
    csrf.init_app(app)

def register_commands(app):

    for command in COMMANDS:
        app.cli.add_command(command)
