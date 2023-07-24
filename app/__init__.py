import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import render_template

from app import exts
from config import config

from dotenv import dotenv_values
env = dotenv_values(".flaskenv")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    exts.mail.init_app(app)
    exts.pages.init_app(app)
    exts.moment.init_app(app)
    exts.db.init_app(app)
    exts.migrate.init_app(app, exts.db)
    exts.minify.init_app(app)

    app.config.from_object(env)
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
            app.logger.info("running venone app")

        return app
