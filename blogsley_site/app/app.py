import os
import sys

from loguru import logger

from flask import Flask, current_app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import jinja2
import arrow

import __blogsley__
from __blogsley__ import Config

from blogsley_flask.db import create_db

from blogsley_flask import BlogsleyFlask
class BlogsleyFlaskSite(BlogsleyFlask):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    @classmethod
    def create(self, config=None, environment=None):
        share_folder = __blogsley__.share_folder
        db_folder = __blogsley__.db_folder
        static_folder = __blogsley__.static_folder
        logger.info(f"static_folder: {static_folder}")

        static_url_path = ''

        __blogsley__.app = app = BlogsleyFlaskSite(self.__name__, static_url_path=static_url_path, static_folder=static_folder)
        app.config.from_object(Config)

        __blogsley__.db = db = SQLAlchemy(app)
        __blogsley__.migrate = migrate = Migrate(app, db)

        __blogsley__.login = login = LoginManager(app)
        login.login_view = 'auth.login'
        login.login_message = 'Please log in to access this page.'

        from flask_mail import Mail
        __blogsley__.mail = mail = Mail(app)

        from blogsley_flask.iam import IAM
        __blogsley__.iam = iam = IAM(app)

        from flask_babel import Babel, lazy_gettext as _l
        __blogsley__.babel = babel = Babel(app)

        from flask_bootstrap import Bootstrap
        __blogsley__.bootstrap = Bootstrap(app)

        from blogsley_site.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from blogsley_site.root import bp as root_bp
        app.register_blueprint(root_bp)

        from blogsley_site.dashboard import bp as dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

        from blogsley_site.events import bp as events_bp
        app.register_blueprint(events_bp, url_prefix='/events')

        from blogsley_flask.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        from blogsley_flask.image import bp as image_bp
        app.register_blueprint(image_bp, url_prefix='/images')

        from blogsley_flask.graphql import bp as graphql_bp
        app.register_blueprint(graphql_bp)

        app.app_protocol = lambda environ_path_info: 'graphql-ws'
        from blogsley_flask.sockets import Sockets
        sockets = Sockets(app)
        from blogsley_flask.graphql.subscription import bp as ws
        sockets.register_blueprint(ws, url_prefix=r'/')

        return app

def create_app(config=None, environment=None):
    logger.info(f"config : {config}")
    logger.info(f"environment: {environment}")

    app = BlogsleyFlaskSite.create(config, environment)

    #Configure Jinja2
    my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader(['blogsley_flask/templates', 'blogsley_site/templates']),
        ])
    app.jinja_loader = my_loader

    #Configure Login
    from blogsley_flask.user import User
    @__blogsley__.login.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    @app.template_filter('humanize')
    def humanize(d):
        return arrow.get(d).humanize()

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post}

    return app
    