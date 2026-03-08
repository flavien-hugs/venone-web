import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SITE_NAME = os.environ.get("SITE_NAME")
    COMPANY_NAME = os.environ.get("COMPANY_NAME")
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_ADDRESS_CONTACT = os.environ.get("EMAIL_ADDRESS_CONTACT")
    PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
    PHONE_NUMBER_TWO = os.environ.get("PHONE_NUMBER_TWO")
    PHONE_NUMBER_THREE = os.environ.get("PHONE_NUMBER_THREE")
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER")

    FLATPAGES_EXTENSION = ".md"
    FLATPAGES_ROOT = "pages/"
    FLATPAGES_MARKDOWN_EXTENSIONS = ["codehilite"]
    FLATPAGES_AUTO_RELOAD = True
    FLATPAGES_EXTENSION_CONFIG = {"codehilite": {"css_class": "highlight"}}

    WEBSITE_BUILDER = os.environ.get("WEBSITE_BUILDER")

    API_URL = os.environ.get("API_URL")
    CRM_BUILDER = os.environ.get("CRM_BUILDER")

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {"prod": ProductionConfig, "dev": DevelopmentConfig, "test": TestingConfig}
