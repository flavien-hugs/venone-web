from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

from flask_minify import Minify
from flask_moment import Moment
from flask_flatpages import FlatPages

moment = Moment()
pages = FlatPages()
minify = Minify(html=True, js=True, cssless=True, bypass=["main.*"])


def init_plugin(app: "Flask") -> None:
    pages.init_app(app)
    moment.init_app(app)
    minify.init_app(app)
