import os

from dotenv import dotenv_values

env = dotenv_values(".flaskenv")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    DEBUG = False
    DEVELOPMENT = False

    SECRET_KEY = env.get("SECRET_KEY")
    SITE_NAME = "Venone"
    EMAIL_ADDRESS = "support@venone.app"
    EMAIL_ADDRESS_CONTACT = "contact@venone.app"
    PHONE_NUMBER = "(+225) 01 0137 6322"
    PHONE_NUMBER_TWO = "(225) 07 5795 0079"
    PHONE_NUMBER_THREE = "(225) 01 7121 0836"
    WHATSAPP_NUMBER = "+2250757950079"

    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "pages/"
    FLATPAGES_MARKDOWN_EXTENSIONS = ["codehilite"]

    SLOW_DB_QUERY_TIME = 0.5
    WEBSITE_BUILDER = env.get("WEBSITE_URL")

    API_URL = env.get("API_URL")
    CRM_BUILDER = env.get("CRM_BASE_URL")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(BASE_DIR, "dev.sqlite3")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URL") or "sqlite:///" + os.path.join(
        BASE_DIR, "prod.sqlite3"
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "prod": ProductionConfig,
    "dev": DevelopmentConfig,
}
