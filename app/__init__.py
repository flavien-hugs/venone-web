import logging
import os
from logging.handlers import RotatingFileHandler

from config import config
from flask import Flask
from flask import render_template
from flask_flatpages import FlatPages
from flask_mail import Mail
from flask_migrate import Migrate
from flask_minify import Minify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


mail = Mail()
db = SQLAlchemy()
moment = Moment()
migrate = Migrate()
pages = FlatPages()
minify = Minify(html=True, js=True, cssless=True, bypass=["main.*"])


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    pages.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    minify.init_app(app)

    app.url_map.strict_slashes = False
    app.jinja_env.globals.update(zip=zip)

    with app.app_context():
        from .main import main as main_blueprint

        app.register_blueprint(main_blueprint)

        @app.errorhandler(404)
        def pageNotFound(error):
            page_title = f"{error.code} - page non trouvé"
            return (
                render_template("page/error.html", page_title=page_title, error=error),
                404,
            )

        @app.errorhandler(500)
        def internalServerError(error):
            page_title = f"{error.code} - quelques choses à mal tourné"
            app.logger.warning(
                "Une exception non gérée est affichée à l'utilisateur final.",
                exc_info=error,
            )
            return (
                render_template("page/error.html", page_title=page_title, error=error),
                500,
            )

        @app.errorhandler(400)
        def keyError(error):
            page_title = f"{error.code} - une demande invalide a entraîné une KeyError."
            app.logger.warning("Invalid request resulted in KeyError", exc_info=error)
            return (
                render_template("page/error.html", page_title=page_title, error=error),
                400,
            )

        @app.before_request
        def log_entry():
            app.logger.debug("Demande de traitement")

        @app.teardown_request
        def log_exit(exc):
            app.logger.debug("Traitement de la demande terminé", exc_info=exc)

        if not app.debug and not app.testing:
            if not os.path.exists("logs"):
                os.mkdir("logs")

            file_handler = RotatingFileHandler(
                "logs/logging.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)

            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info("running app")

        return app
