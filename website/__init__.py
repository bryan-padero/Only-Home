from flask import Flask
from os import path
from website.extensions import *


DB_NAME = "app_database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "12aSCszcb245"

    # DB Config
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    migrate.init_app(app, db, render_as_batch=True)
    db.init_app(app)

    from website.routes.account import account
    from website.routes.auth import auth
    from website.routes.api import api
    from website.routes.page import page

    app.register_blueprint(account, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')
    app.register_blueprint(page, url_prefix='/')

    from .models.user import User
    create_database(app)

    # Flask Bootstrap
    bootstrap.init_app(app)

    # Flask CKEditor
    ckeditor.init_app(app)

    # Flask Login Manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database Created")
