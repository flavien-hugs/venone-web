from flask_mail import Mail
from flask_minify import Minify
from flask_moment import Moment
from flask_migrate import Migrate
from flask_flatpages import FlatPages
from flask_sqlalchemy import SQLAlchemy


mail = Mail()
db = SQLAlchemy()
moment = Moment()
migrate = Migrate()
pages = FlatPages()
minify = Minify(html=True, js=True, cssless=True, bypass=["main.*"])
